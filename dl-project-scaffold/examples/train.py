"""
通用训练脚本模板

用法:
    python train.py                          # 使用默认 config/ 目录
    python train.py --config-dir config      # 指定配置目录

结构:
    1. load_config()         — 三文件合并
    2. run_single_subject()  — 单被试完整流程
    3. main()                — 入口，处理被试遍历 + 结果汇总
"""

import torch  # Windows: 必须先于 numpy/pandas 导入，避免 DLL 冲突 (WinError 1114)
import time
import argparse
import yaml
import copy
import sys
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, LearningRateMonitor, EarlyStopping

from utils.metrics import UniversalMetricsCallback, write_summary
from utils.plotting import plot_confusion_matrix, plot_curve
from utils.latency import measure_latency
from utils.data_cls import get_datamodule_cls
from utils.model_cls import get_model_cls


# ──────────────────────────────────────────────
# 配置加载
# ──────────────────────────────────────────────

def load_config(config_dir: Path) -> dict:
    """三文件合并为统一 config dict"""
    with open(config_dir / 'general.yaml', 'r', encoding='utf-8') as f:
        general = yaml.safe_load(f)
    with open(config_dir / 'data.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    method = general.get('method', 'default')
    with open(config_dir / f'{method}.yaml', 'r', encoding='utf-8') as f:
        algo = yaml.safe_load(f)

    return {**general, **algo, 'data': data}


# ──────────────────────────────────────────────
# 单被试实验
# ──────────────────────────────────────────────

def run_single_subject(base_config, subject_id, dataset_name, parent_output_dir=None):
    """执行单个被试的完整训练 + 评估流程"""

    config = copy.deepcopy(base_config)
    config['data'][dataset_name]['test_subject'] = subject_id

    exp_name = config.get('exp_name', 'Experiment')
    seed = config['seed']
    method = config.get('method', 'model')

    # ── 结果目录 ──
    if parent_output_dir:
        result_dir = parent_output_dir / f"S{subject_id:02d}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        dir_name = f"{exp_name}_{dataset_name}_S{subject_id:02d}_seed-{seed}_{timestamp}"
        result_dir = Path(__file__).resolve().parent / f"results/{dir_name}"

    for sub in ["checkpoints", "confmats", "curves"]:
        (result_dir / sub).mkdir(parents=True, exist_ok=True)

    # 冻结配置快照
    with open(result_dir / "config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    print(f"\n{'=' * 60}")
    print(f"🚀 Running {method} for Test Subject: {subject_id}")
    print(f"📂 Result Directory: {result_dir}")
    print(f"{'=' * 60}\n")

    pl.seed_everything(seed, workers=True)

    # ── 数据 ──
    loso = config['data'][dataset_name].get('loso', True)
    dm_cls = get_datamodule_cls(dataset_name, loso=loso)
    dm = dm_cls(config['data'][dataset_name])

    class_names = getattr(dm, 'class_names',
                          [str(i) for i in range(config['data'][dataset_name]['n_classes'])])

    # ── 模型 ──
    model_cls = get_model_cls(method)
    model = model_cls(config, dataset_name)
    param_count = sum(p.numel() for p in model.parameters())
    print(f"Model: {method}, Parameters: {param_count:,}")

    # ── 回调 ──
    metrics_cb = UniversalMetricsCallback()
    ckpt_cb = ModelCheckpoint(
        dirpath=str(result_dir / "checkpoints"),
        filename='best-{epoch:02d}-{val_acc:.4f}',
        monitor='val_acc', mode='max', save_top_k=1, save_last=True, verbose=True,
    )
    early_stop = EarlyStopping(monitor='val_acc', patience=80, mode='max', min_delta=0.01)

    # ── 训练 ──
    trainer = pl.Trainer(
        max_epochs=config['train']['max_epochs'],
        accelerator=config['accelerator'],
        devices=config['devices'],
        logger=True,
        default_root_dir=str(result_dir),
        callbacks=[ckpt_cb, LearningRateMonitor(logging_interval='epoch'),
                   metrics_cb, early_stop],
        check_val_every_n_epoch=1,
        log_every_n_steps=10,
        gradient_clip_val=1.0,
    )

    st_train = time.time()
    trainer.fit(model, datamodule=dm)
    train_time = (time.time() - st_train) / 60

    # ── 评估最佳 checkpoint ──
    best_ckpt = ckpt_cb.best_model_path or ckpt_cb.last_model_path
    if not best_ckpt:
        raise RuntimeError("No checkpoint available for evaluation.")

    eval_trainer = pl.Trainer(
        accelerator=config['accelerator'], devices=config['devices'],
        logger=False, enable_checkpointing=False,
    )
    model = model_cls.load_from_checkpoint(best_ckpt, config=config, dataset_name=dataset_name)

    st_test = time.time()
    test_results = eval_trainer.test(model, datamodule=dm, verbose=False)
    test_duration = time.time() - st_test

    res = test_results[0] if test_results else {}
    test_acc = res.get("test_acc", 0.0)
    test_loss = res.get("test_loss", 0.0)
    test_kappa = res.get("test_kappa", 0.0)

    print(f"Test Accuracy: {test_acc:.4f}, Kappa: {test_kappa:.4f}")

    # ── 后处理 ──
    # 延迟测量
    lat_ms = 0.0
    try:
        if hasattr(dm, 'test_dataset') and len(dm.test_dataset) > 0:
            sample_x = dm.test_dataset[0][0]
            lat_ms = measure_latency(model, (1, *sample_x.shape), device="cpu")
    except Exception as e:
        print(f"Warning: Latency measurement failed: {e}")

    # 混淆矩阵
    if hasattr(model, 'test_confmat'):
        try:
            cm = model.test_confmat
            if hasattr(cm, 'compute'):
                cm = cm.compute()
            plot_confusion_matrix(
                cm.cpu().numpy(),
                save_path=result_dir / "confmats/confusion_matrix.png",
                class_names=class_names,
                title=f"S{subject_id} (Acc: {test_acc:.2%})",
            )
        except Exception as e:
            print(f"Warning: Confusion matrix plot failed: {e}")

    # 训练曲线
    history = metrics_cb.history
    train_acc_vals = history.get('train_acc', [])
    val_acc_vals = history.get('val_acc', [])
    if train_acc_vals:
        plot_curve(train_acc_vals, val_acc_vals, "Accuracy", subject_id,
                   result_dir / "curves/acc.png")

    train_loss_vals = history.get('train_loss', [])
    val_loss_vals = history.get('val_loss', [])
    if train_loss_vals:
        plot_curve(train_loss_vals, val_loss_vals, "Loss", subject_id,
                   result_dir / "curves/loss.png")

    # 结果摘要
    write_summary(
        result_dir, exp_name, dataset_name, [str(subject_id)],
        param_count, [test_acc], [test_loss], [test_kappa],
        [train_time], [test_duration], [lat_ms],
    )

    print(f"✅ Subject {subject_id} finished. Results → {result_dir}")

    return {
        'subject_id': subject_id,
        'accuracy': test_acc * 100,
        'kappa': test_kappa,
        'loss': test_loss,
        'train_time': train_time,
        'latency': lat_ms,
    }


# ──────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────

def main(args):
    config = load_config(Path(args.config_dir))
    dataset_name = config['dataset']

    # 解析被试列表
    raw = config['data'][dataset_name].get('test_subject')
    if raw == 'all':
        subjects = list(range(1, config['data'][dataset_name].get('n_subjects', 9) + 1))
    elif isinstance(raw, list):
        subjects = raw
    elif isinstance(raw, int):
        subjects = [raw]
    else:
        print(f"Error: Unknown test_subject format: {raw}")
        sys.exit(1)

    print(f"📋 Subjects: {subjects}")

    # 多被试 → 统一父目录
    root = None
    if len(subjects) > 1:
        exp_name = config.get('exp_name', config.get('method', 'Exp'))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        dir_name = f"{exp_name}_{dataset_name}_seed-{config['seed']}_{timestamp}"
        root = Path(__file__).resolve().parent / f"results/{dir_name}"
        root.mkdir(parents=True, exist_ok=True)
        print(f"📁 Batch mode → {root}")

    # 逐被试执行
    results = []
    for sub_id in subjects:
        result = run_single_subject(config, sub_id, dataset_name, parent_output_dir=root)
        if result:
            results.append(result)

    # 汇总 Excel（需要 openpyxl + pandas）
    if root and results:
        try:
            import pandas as pd
            import numpy as np
            rows = [{'Subject': f"S{r['subject_id']}",
                     'Accuracy (%)': f"{r['accuracy']:.2f}",
                     "Cohen's Kappa": f"{r['kappa']:.4f}"}
                    for r in results]
            avg_acc = np.mean([r['accuracy'] for r in results])
            std_acc = np.std([r['accuracy'] for r in results])
            avg_kappa = np.mean([r['kappa'] for r in results])
            std_kappa = np.std([r['kappa'] for r in results])
            rows.append({
                'Subject': 'Average',
                'Accuracy (%)': f"{avg_acc:.2f} ± {std_acc:.2f}",
                "Cohen's Kappa": f"{avg_kappa:.4f} ± {std_kappa:.4f}",
            })
            df = pd.DataFrame(rows)
            df.to_excel(root / f"results_{dataset_name}.xlsx", index=False)
            print(f"📊 Summary saved → {root / f'results_{dataset_name}.xlsx'}")
        except ImportError:
            print("Warning: pandas/openpyxl not installed, skipping Excel export.")

    print("\n🎉 All experiments finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training Script')
    parser.add_argument('--config-dir', type=str, default='config',
                        help='Path to config directory')
    args = parser.parse_args()
    main(args)
