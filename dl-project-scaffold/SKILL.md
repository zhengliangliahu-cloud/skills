---
name: dl-project-scaffold
description: |
  深度学习实验项目的脚手架规范。当需要新建深度学习项目、组织项目目录结构、
  编写训练脚本、设计配置文件体系、或搭建数据加载 / 模型注册 / 结果管理流程时触发。
  提炼自 RiemannianCSP 项目的实战经验，适用于 PyTorch Lightning 生态。
---

# 深度学习实验项目脚手架

> 从 RiemannianCSP 项目提炼而来，面向**科研实验**场景的项目组织规范。
> 核心目标：**开箱即用、结构清晰、结果可追溯、新方法易扩展**。

---

## 1. 目录结构

```
<project_root>/
├── config/                     # 配置文件（唯一配置源）
│   ├── general.yaml            # 全局设置：种子、设备、当前方法/数据集选择
│   ├── data.yaml               # 所有数据集的参数定义（通道数、采样率、预处理等）
│   └── <method>.yaml           # 各算法独立的模型架构 + 训练超参 + 损失权重
│
├── datamodules/                # PyTorch Lightning DataModule（每个数据集一个文件）
│   ├── __init__.py             # 统一导出所有 DataModule 类
│   ├── load_<dataset_a>.py     # 数据集 A 的加载与预处理（含 LOSO / 单被试两种模式）
│   └── load_<dataset_b>.py
│
├── modeling/                   # 自研模型实现
│   └── <model_name>.py         # 继承 pl.LightningModule
│
├── baseline/                   # 对比方法（Baseline 模型）
│   ├── __init__.py             # 统一导出
│   ├── eegnet.py
│   └── deepconvnet.py
│
├── utils/                      # 工具函数（无业务逻辑耦合）
│   ├── data_cls.py             # DataModule 注册表 + 工厂函数
│   ├── model_cls.py            # 模型注册表 + 工厂函数
│   ├── metrics.py              # 通用指标回调 (UniversalMetricsCallback) + 结果摘要
│   ├── plotting.py             # 可视化（混淆矩阵、训练曲线）
│   ├── latency.py              # 推理延迟测量
│   ├── lr_scheduler.py         # 学习率调度器工厂
│   └── weight_initialization.py
│
├── visualization/              # 论文级可视化脚本（独立于训练流程）
│   └── generate_paper_figures.py
│
├── results/                    # 自动生成的实验结果（.gitignore）
│   └── <ExpName>_<Dataset>_seed-<Seed>_<Timestamp>/
│       ├── S01/                # 每个被试一个子目录
│       │   ├── config.yaml     # 该次运行的完整冻结配置
│       │   ├── results.txt     # 文本摘要
│       │   ├── checkpoints/    # 最佳 & 最后 checkpoint
│       │   ├── confmats/       # 混淆矩阵图
│       │   └── curves/         # 训练/验证曲线
│       └── results_<dataset>.xlsx  # 多被试汇总 Excel（三线表格式）
│
├── datasets/                   # 原始数据存放目录（.gitignore）
├── figs/                       # 论文图表输出（.gitignore）
│
├── train_<method>.py           # 主训练入口（每个方法一个，或通用一个）
├── train_batch.py              # 批量实验脚本（多方法 × 多数据集）
├── requirements.txt            # 依赖锁定
├── .gitignore
└── README.md
```

### 目录设计原则

| 原则 | 说明 |
|------|------|
| **配置与代码分离** | 所有可调参数集中在 `config/`，训练脚本不硬编码任何超参 |
| **数据加载独立** | 每个数据集一个 DataModule 文件，通过注册表按名索引 |
| **方法可插拔** | 自研模型放 `modeling/`，对比方法放 `baseline/`，通过注册表统一管理 |
| **结果自包含** | 每次实验的结果目录包含冻结配置快照，事后可完全复现 |
| **论文产出分离** | `visualization/` 只依赖已有结果或模型，不耦合训练逻辑 |

---

## 2. 配置文件设计

采用 **三文件分层**：`general.yaml` + `data.yaml` + `<method>.yaml`，通过 dict merge 组合。

### 2.1 general.yaml — 全局开关

```yaml
# === 全局配置 ===
exp_name: "MyExperiment"       # 实验名，用于结果目录命名
seed: 2025                     # 全局随机种子
accelerator: "gpu"             # "gpu" | "cpu" | "mps"
devices: [0]                   # GPU 设备列表

method: "my_model"             # 当前使用的方法名（对应 <method>.yaml 文件名）
dataset: "2a"                  # 当前使用的数据集名（对应 data.yaml 中的顶级 key）
```

> **设计要点**：`method` 和 `dataset` 作为全局选择器，同时决定加载哪个算法配置和哪段数据配置。
> 切换实验只需改这两个字段，不需要改训练脚本。

### 2.2 data.yaml — 数据集参数

```yaml
# 每个数据集是一个顶级 key
2a:
  n_channels: 22
  n_timepoints: 1000
  n_classes: 4
  n_subjects: 9
  test_subject: all           # all | 单个整数 | 整数列表
  loso: false                 # true=跨被试 LOSO, false=单被试 train/test split
  batch_size: 64
  num_workers: 0

  preprocessing:
    sfreq: 250
    low_cut: 4
    high_cut: 45
    # ... 数据集特有的预处理参数

openbmi:
  n_channels: 62
  # ...
```

> **设计要点**：
> - `test_subject: all` 时自动遍历所有被试。
> - 每个数据集可以有完全独立的预处理参数。
> - 数据路径可以内联（`data_path: "D:/datasets/..."` ），也可以走默认查找逻辑。

### 2.3 \<method\>.yaml — 算法配置

```yaml
# 模型架构
model:
  backbone: "EEGNet"
  dropout: 0.5
  d_model: 128
  # ... 模型特有参数

# 训练超参
train:
  max_epochs: 200
  learning_rate: 0.001
  weight_decay: 0.01
  scheduler:
    T_max: 200
    eta_min: 1.0e-6

# 损失函数权重
loss_weights:
  lambda_task: 3.0
  lambda_adv: 2.0
```

> **设计要点**：
> - `model` / `train` / `loss_weights` 三个顶级 key 各司其职。
> - 新方法只需新建一个 yaml 文件，general.yaml 里切换 `method` 即可。

### 2.4 配置合并逻辑

```python
def load_config(config_dir: Path) -> dict:
    """三文件合并为统一 config dict"""
    with open(config_dir / 'general.yaml', 'r', encoding='utf-8') as f:
        general = yaml.safe_load(f)

    with open(config_dir / 'data.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    method = general.get('method', 'default')
    with open(config_dir / f'{method}.yaml', 'r', encoding='utf-8') as f:
        algo = yaml.safe_load(f)

    # general + algo 平铺合并, data 作为独立子 key
    return {**general, **algo, 'data': data}
```

合并后的 config dict 结构：

```
config
├── exp_name, seed, accelerator, devices, method, dataset  (from general)
├── model: {...}                                            (from <method>.yaml)
├── train: {...}                                            (from <method>.yaml)
├── loss_weights: {...}                                     (from <method>.yaml)
└── data:                                                    (from data.yaml)
    ├── 2a: {...}
    ├── openbmi: {...}
    └── ...
```

---

## 3. 注册表模式（Model / DataModule）

用简单的字典映射 + 工厂函数，代替复杂的 auto-discovery。

### 3.1 模型注册表 — `utils/model_cls.py`

```python
from modeling.my_model import MyModel
from baseline import EEGNet, DeepConvNet

MODEL_REGISTRY = {
    'my_model': MyModel,
    'eegnet': EEGNet,
    'deepconvnet': DeepConvNet,
}

def get_model_cls(model_name: str):
    if model_name not in MODEL_REGISTRY:
        raise NotImplementedError(
            f"Unknown model: '{model_name}'. "
            f"Available: {list(MODEL_REGISTRY.keys())}"
        )
    return MODEL_REGISTRY[model_name]
```

### 3.2 DataModule 注册表 — `utils/data_cls.py`

```python
from datamodules import Dataset2aLOSO, Dataset2aSingle, ...

# 每个数据集提供 (LOSO版, 单被试版) 两个 DataModule
DATASET_MAP = {
    '2a': (Dataset2aLOSO, Dataset2aSingle),
    'openbmi': (OpenBMILOSO, OpenBMISingle),
}

def get_datamodule_cls(dataset_name: str, loso: bool = True):
    if dataset_name not in DATASET_MAP:
        raise NotImplementedError(f"Unknown dataset: '{dataset_name}'")
    loso_cls, single_cls = DATASET_MAP[dataset_name]
    return loso_cls if loso else single_cls
```

### 扩展流程

添加新数据集 / 新模型只需 3 步：
1. 在 `datamodules/` 或 `modeling/` 下新建文件
2. 在对应的 `__init__.py` 中导出
3. 在注册表中添加一行映射

---

## 4. 训练脚本结构

### 4.1 通用单被试训练流程

```python
def run_single_subject(config, subject_id, dataset_name, parent_output_dir=None):
    """单被试完整训练 + 评估流程"""

    # 1. 深拷贝配置，设置当前被试
    config = copy.deepcopy(config)
    config['data'][dataset_name]['test_subject'] = subject_id

    # 2. 创建结果目录
    result_dir = setup_result_dir(config, subject_id, parent_output_dir)
    for sub in ["checkpoints", "confmats", "curves"]:
        (result_dir / sub).mkdir(parents=True, exist_ok=True)

    # 3. 冻结配置快照
    with open(result_dir / "config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    # 4. 种子 & 数据
    pl.seed_everything(config['seed'], workers=True)
    dm = get_datamodule_cls(dataset_name, loso=...)(config['data'][dataset_name])

    # 5. 模型初始化
    model = get_model_cls(config['method'])(config, dataset_name)

    # 6. 回调
    metrics_cb = UniversalMetricsCallback()
    ckpt_cb = ModelCheckpoint(
        dirpath=str(result_dir / "checkpoints"),
        filename='best-{epoch:02d}-{val_acc:.4f}',
        monitor='val_acc', mode='max', save_top_k=1, save_last=True
    )

    # 7. Trainer fit
    trainer = pl.Trainer(
        max_epochs=config['train']['max_epochs'],
        accelerator=config['accelerator'],
        devices=config['devices'],
        callbacks=[ckpt_cb, LearningRateMonitor(), metrics_cb],
        gradient_clip_val=1.0,
        default_root_dir=str(result_dir),
    )
    trainer.fit(model, datamodule=dm)

    # 8. 评估最佳 checkpoint
    eval_trainer = pl.Trainer(
        accelerator=config['accelerator'], devices=config['devices'],
        logger=False, enable_checkpointing=False,
    )
    test_results = eval_trainer.test(model, datamodule=dm, ckpt_path=ckpt_cb.best_model_path)

    # 9. 后处理：混淆矩阵、训练曲线、延迟测量、结果摘要
    post_process(model, metrics_cb, result_dir, ...)

    return result_dict
```

### 4.2 主入口 `main()`

```python
def main(args):
    config = load_config(Path(args.config_dir))
    dataset_name = config['dataset']
    target_subjects = resolve_subjects(config, dataset_name)

    # 多被试 → 统一父目录
    root_dir = create_experiment_root(config, dataset_name) if len(target_subjects) > 1 else None

    results = []
    for sub_id in target_subjects:
        result = run_single_subject(config, sub_id, dataset_name, parent_output_dir=root_dir)
        results.append(result)

    # 汇总 Excel
    if root_dir and results:
        save_results_to_excel(results, dataset_name, root_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-dir', type=str, default='config')
    args = parser.parse_args()
    main(args)
```

### 4.3 批量实验脚本 `train_batch.py`

支持 **多方法 × 多数据集** 的笛卡尔积实验：

```python
def run_batch_experiments(algorithms, datasets, config_dir, output_dir):
    """
    algorithms: [{'name': 'baseline', ...overrides}, ...]
    """
    for algo in algorithms:
        for dataset in datasets:
            config = apply_overrides(base_config, algo, dataset)
            for sub_id in target_subjects:
                run_single_subject(config, sub_id, dataset, parent_output_dir=...)

    # 保存汇总: all_results.xlsx + summary.xlsx (按方法 × 数据集分组统计)
```

### 4.4 关键设计模式

| 模式 | 说明 |
|------|------|
| **深拷贝隔离** | 每个被试的 config 独立 `copy.deepcopy`，避免跨循环污染 |
| **冻结快照** | 每次运行将 config dump 到结果目录，事后溯源 |
| **评估独立 Trainer** | 测试阶段新建 Trainer，避免 fit 阶段残留状态干扰 |
| **目录自动命名** | `{exp_name}_{dataset}_seed-{seed}_{YYYYMMDD_HHMM}` |
| **被试子目录** | 多被试模式下 `S01/`, `S02/`...，结构一致便于遍历 |

---

## 5. DataModule 编写规范

### 5.1 基类模式

```python
class BaseDataModule(pl.LightningDataModule):
    def __init__(self, config: dict):
        super().__init__()
        self.cfg = config
        self.batch_size = config['batch_size']
        self.preprocessing = config['preprocessing']
        self.train_dataset = None
        self.test_dataset = None

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size,
                          shuffle=True, pin_memory=True, num_workers=0)

    def val_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size,
                          shuffle=False, pin_memory=True, num_workers=0)

    def test_dataloader(self):
        return self.val_dataloader()  # 通常 val=test (LOSO场景)
```

### 5.2 每个数据集的两种模式

| 模式 | 类名范式 | 说明 |
|------|---------|------|
| **LOSO** | `Dataset2aDataModule` | Leave-One-Subject-Out: 其余被试训练，目标被试测试 |
| **Single** | `Dataset2aSingleSubjectDataModule` | 单被试内部 80/20 分层划分 |

两种模式共享同一配置结构，通过 `loso: true/false` 切换。

### 5.3 预处理管线（在 `setup()` 中）

```
原始数据 → CAR → Euclidean/Riemannian Alignment → Z-Score → TensorDataset
```

每一步都由配置开关控制，支持按需组合。

---

## 6. LightningModule 编写规范

```python
class MyModel(pl.LightningModule):
    def __init__(self, config: dict, dataset_name: str):
        super().__init__()
        # 从 config 中读取所有参数
        self.save_hyperparameters()

        # config 路径约定
        data_cfg = config['data'][dataset_name]
        model_cfg = config['model']
        train_cfg = config['train']
        loss_cfg = config.get('loss_weights', {})

        # 构建网络...

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.train_cfg['learning_rate'],
            weight_decay=self.train_cfg['weight_decay']
        )
        scheduler = CosineAnnealingLR(
            optimizer,
            T_max=self.train_cfg['scheduler']['T_max'],
            eta_min=self.train_cfg['scheduler']['eta_min']
        )
        return [optimizer], [scheduler]

    def training_step(self, batch, batch_idx):
        x, y, s = batch  # 统一三元组: 数据, 标签, 被试ID
        # ...
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        # ...
        self.log('val_loss', loss)
        self.log('val_acc', acc)

    def test_step(self, batch, batch_idx):
        # ...
        self.log('test_acc', acc)
        self.log('test_kappa', kappa)
        self.log('test_loss', loss)
```

### 模型层面的约定

| 约定 | 说明 |
|------|------|
| **构造签名** | `__init__(self, config, dataset_name)` — 统一接口 |
| **batch 格式** | `(x, y, s)` 三元组，`s` 是被试 ID（domain 标签） |
| **日志 key** | `train_loss`, `val_acc`, `test_kappa` 等前缀统一 |
| **save_hyperparameters** | 确保 checkpoint 可恢复 |

---

## 7. 结果管理

### 7.1 目录结构

```
results/
└── MyModel_2a_seed-2025_20260419_1530/
    ├── S01/
    │   ├── config.yaml          # 冻结配置
    │   ├── results.txt          # 文本摘要
    │   ├── checkpoints/
    │   │   ├── best-epoch=42-val_acc=0.8500.ckpt
    │   │   └── last.ckpt
    │   ├── confmats/
    │   │   └── confusion_matrix.png
    │   └── curves/
    │       ├── acc.png
    │       └── total_loss.png
    ├── S02/
    │   └── ...
    └── results_2a.xlsx          # 汇总表
```

### 7.2 UniversalMetricsCallback

自动按 epoch 收集所有 `self.log()` 的标量指标，用于事后绘制训练曲线：

```python
class UniversalMetricsCallback(Callback):
    """自动收集 epoch 级 train/val 指标"""
    def __init__(self):
        self.history = {}       # {'train_loss': [...], 'val_acc': [...]}
        self._last_epoch = {}   # 去重同一 epoch 的重复记录

    def on_train_epoch_end(self, trainer, pl_module):
        self._record(trainer, filter=lambda k: not k.startswith("val_"))

    def on_validation_epoch_end(self, trainer, pl_module):
        self._record(trainer, filter=lambda k: k.startswith("val_"))
```

### 7.3 汇总 Excel

```python
def save_results_to_excel(results, dataset_name, save_dir):
    """保存为三线表格式的 xlsx，末行自动计算 Mean ± Std"""
    rows = [{'Subject': f"S{r['subject_id']}", 'Accuracy (%)': ..., "Cohen's Kappa": ...}
            for r in results]
    rows.append({'Subject': 'Average', 'Accuracy (%)': f"{mean:.2f} ± {std:.2f}", ...})
    # 用 openpyxl 设置三线表边框 + 表头加粗 + 居中对齐
```

---

## 8. 工具函数清单

| 文件 | 职责 | 关键函数 |
|------|------|---------|
| `utils/data_cls.py` | DataModule 工厂 | `get_datamodule_cls(name, loso)` |
| `utils/model_cls.py` | 模型工厂 | `get_model_cls(name)` |
| `utils/metrics.py` | 指标回调 + 结果摘要 | `UniversalMetricsCallback`, `write_summary()` |
| `utils/plotting.py` | 混淆矩阵 + 训练曲线 | `plot_confusion_matrix()`, `plot_curve()` |
| `utils/latency.py` | 推理延迟 | `measure_latency(model, input_shape)` |
| `utils/lr_scheduler.py` | LR 调度器 | `linear_warmup_cosine_decay()` |

---

## 9. .gitignore 模板

```gitignore
# 数据与结果（体积大，不入版本控制）
datasets/
results/
batch_results/
figs/

# Python 编译产物
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## 10. 新项目初始化 Checklist

当需要创建新的深度学习实验项目时，按以下顺序执行：

- [ ] 创建项目根目录和基础子目录 (`config/`, `datamodules/`, `modeling/`, `baseline/`, `utils/`, `visualization/`)
- [ ] 编写 `config/general.yaml` — 设置 `exp_name`, `seed`, `method`, `dataset`
- [ ] 编写 `config/data.yaml` — 定义目标数据集的参数
- [ ] 编写 `config/<method>.yaml` — 定义模型架构 + 训练超参 + 损失权重
- [ ] 实现 `datamodules/load_<dataset>.py` — LOSO 和 Single 两种模式
- [ ] 实现 `datamodules/__init__.py` — 统一导出
- [ ] 实现 `utils/data_cls.py` — 注册 DataModule
- [ ] 实现 `modeling/<model>.py` — 继承 `pl.LightningModule`
- [ ] 实现 `utils/model_cls.py` — 注册模型
- [ ] 复制 `utils/metrics.py`, `utils/plotting.py`, `utils/latency.py` — 通用工具可直接复用
- [ ] 编写 `train_<method>.py` — 主训练脚本
- [ ] 编写 `.gitignore` 和 `requirements.txt`
- [ ] 小规模验证：单被试 + 少 epoch 跑通全流程
- [ ] 全量实验：`test_subject: all` 运行所有被试

---

## 11. 运行命令速查

```bash
# 单方法训练（使用默认 config 目录）
python train_<method>.py

# 指定配置目录
python train_<method>.py --config-dir config

# 批量实验
python train_batch.py --algorithms my_model baseline --datasets 2a openbmi

# 生成论文图表
python visualization/generate_paper_figures.py --fig 0   # 0=全部
```

---

## Execution Rules

1. **新项目必须先跑通最小闭环**：1 个被试 + 10 个 epoch，确认数据流、模型、日志、checkpoint 全部正常。
2. **配置文件不允许在代码中硬编码覆盖**：所有超参必须可通过 yaml 文件控制。
3. **结果目录必须包含 config 快照**：`config.yaml` 和 `results.txt` 缺一不可。
4. **模型和数据集通过注册表管理**：不允许在训练脚本中 `if-else` 选择模型/数据集。
5. **评估阶段使用独立 Trainer**：避免训练状态污染测试结果。
6. **Windows 注意**：先 `import torch` 再导入 numpy/pandas/matplotlib，避免 DLL 冲突 (WinError 1114)。
