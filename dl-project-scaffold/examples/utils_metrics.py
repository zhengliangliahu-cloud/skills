"""
通用指标回调 + 结果摘要

- UniversalMetricsCallback: 自动按 epoch 收集所有 self.log() 的标量指标
- write_summary: 将结果写入 results.txt 文本文件
"""

from pytorch_lightning import Callback
import numpy as np


class UniversalMetricsCallback(Callback):
    """自动收集 epoch 级 train/val 指标，供事后绘图使用。

    用法:
        cb = UniversalMetricsCallback()
        trainer = pl.Trainer(callbacks=[cb, ...])
        trainer.fit(model, dm)
        # 训练结束后:
        cb.history  # {'train_loss': [...], 'val_acc': [...], ...}
    """

    def __init__(self):
        super().__init__()
        self.history = {}       # key -> list of scalars
        self._last_epoch = {}   # key -> last recorded epoch (去重)

    @staticmethod
    def _to_scalar(v):
        if isinstance(v, (int, float)):
            return float(v)
        if hasattr(v, "item") and hasattr(v, "numel") and v.numel() == 1:
            return float(v.item())
        return None

    def _record_metrics(self, trainer, key_filter=None):
        epoch = trainer.current_epoch
        for k, v in trainer.callback_metrics.items():
            if key_filter is not None and not key_filter(k):
                continue
            value = self._to_scalar(v)
            if value is None:
                continue
            if self._last_epoch.get(k) == epoch:
                continue  # 同一 epoch 不重复记录
            self.history.setdefault(k, []).append(value)
            self._last_epoch[k] = epoch

    def on_train_epoch_end(self, trainer, pl_module):
        self._record_metrics(trainer,
                             key_filter=lambda k: not (k.startswith("val_") or k.startswith("test_")))

    def on_validation_epoch_end(self, trainer, pl_module):
        self._record_metrics(trainer,
                             key_filter=lambda k: k.startswith("val_"))


def write_summary(result_dir, model_name, dataset_name, subject_ids,
                  param_count, test_accs, test_losses, test_kappas,
                  train_times, test_times, response_times):
    """将实验结果写入 results.txt"""
    avg_acc = float(np.mean(test_accs))
    std_acc = float(np.std(test_accs))
    avg_kappa = float(np.mean(test_kappas))
    std_kappa = float(np.std(test_kappas))
    avg_loss = float(np.mean(test_losses))
    std_loss = float(np.std(test_losses))
    total_train = float(np.sum(train_times))
    avg_latency = float(np.mean(response_times))

    with open(result_dir / "results.txt", "w", encoding="utf-8") as f:
        f.write(f"Results for model: {model_name}\n")
        f.write(f"#Params: {param_count}\n")
        f.write(f"Dataset: {dataset_name}\n")
        f.write(f"Subject IDs: {subject_ids}\n\n")
        f.write("Per-subject results:\n")

        for i, sid in enumerate(subject_ids):
            f.write(
                f"Subject {sid} => "
                f"Train: {train_times[i]:.2f}m, "
                f"Test: {test_times[i]:.2f}s, "
                f"Acc: {test_accs[i]:.4f}, "
                f"Loss: {test_losses[i]:.4f}, "
                f"Kappa: {test_kappas[i]:.4f}\n"
            )

        f.write("\n--- Summary ---\n")
        f.write(f"Accuracy: {avg_acc * 100:.2f} ± {std_acc * 100:.2f}\n")
        f.write(f"Kappa:    {avg_kappa:.3f} ± {std_kappa:.3f}\n")
        f.write(f"Loss:     {avg_loss:.3f} ± {std_loss:.3f}\n")
        f.write(f"Total Training Time: {total_train:.2f} min\n")
        f.write(f"Avg Latency: {avg_latency:.2f} ms\n")

    print(f"\n=== Summary ===")
    print(f"Accuracy: {avg_acc * 100:.2f} ± {std_acc * 100:.2f}")
    print(f"Kappa:    {avg_kappa:.3f} ± {std_kappa:.3f}")
    print(f"Total Training Time: {total_train:.2f} min")
