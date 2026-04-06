---
name: ml-experiment
description: |
  管理机器学习实验全流程：环境搭建、数据准备、训练运行、结果分析与可视化。
  当涉及 conda/venv 环境管理、训练脚本运行、实验结果对比、超参搜索、GPU 调度或模型评估时触发。
---
# ML 实验管理

## Overview

本技能覆盖机器学习实验从环境搭建到结果分析的完整生命周期。
优先保证实验可复现性、结果可追溯性和资源高效利用。

## Core Workflow

1. **环境检查**：确认 conda/venv 环境、CUDA 版本、关键依赖。
2. **数据准备**：检查数据路径、格式、预处理流程。
3. **实验配置**：确认超参数、随机种子、训练策略。
4. **训练执行**：运行训练脚本，监控 GPU 占用和损失曲线。
5. **结果收集**：汇总指标、生成对比表格、保存 checkpoint。
6. **分析可视化**：绘制关键指标图、统计显著性检验。

## 环境管理规范

### Conda 环境
1. 每个项目独立 conda 环境，命名规则：`<project-name>` 或 `<project-name>-py<version>`。
2. 使用 `environment.yml` 或 `requirements.txt` 锁定依赖版本。
3. 安装顺序：先 `conda install pytorch torchvision torchaudio pytorch-cuda=<version> -c pytorch -c nvidia`，再 `pip install -r requirements.txt`。
4. 使用前检查：`conda activate <env> && python -c "import torch; print(torch.cuda.is_available())"` 验证 GPU 可用。

### 依赖管理
- 核心框架（PyTorch/TensorFlow）通过 conda 安装以确保 CUDA 兼容。
- 其他依赖通过 pip 安装。
- 避免混用 conda 和 pip 安装同一包。

## 实验记录规范

### 必须记录的信息
- **超参数**：学习率、batch size、epochs、优化器、调度器参数。
- **随机种子**：`torch.manual_seed(seed)`, `np.random.seed(seed)`, `random.seed(seed)`。
- **硬件信息**：GPU 型号、CUDA 版本、内存占用。
- **数据集信息**：训练/验证/测试集大小、采样策略、数据增强方法。
- **Git commit hash**：代码版本追溯。

### 输出格式
- 结果以 CSV 或 JSON 格式输出，便于后续分析。
- 模型 checkpoint 命名：`<model>_<dataset>_<epoch>_<metric>.pth`。
- 训练日志保存为 `.log` 文件。

## 结果分析

### 汇总多次实验
```python
import pandas as pd

# 读取多次实验结果
results = pd.read_csv('results.csv')
# 按方法分组，计算均值±标准差
summary = results.groupby('method').agg(['mean', 'std'])
```

### 统计检验
- 使用 paired t-test 或 Wilcoxon signed-rank test 比较方法差异。
- 报告 p-value，标注显著性水平（*p<0.05, **p<0.01, ***p<0.001）。

### 可视化
- 使用 matplotlib/seaborn 绘制对比图。
- 图表风格：白色背景、清晰标签、合适字号（≥12pt）。
- 保存为 PDF/SVG 格式用于论文，PNG 格式用于报告。

## 常见问题排查

| 问题 | 排查步骤 |
|------|---------|
| CUDA out of memory | 1. 减小 batch size  2. 使用 gradient accumulation  3. 使用 mixed precision (AMP) |
| 训练 loss 不下降 | 1. 检查学习率  2. 检查数据加载是否正确  3. 检查 label 编码  4. 从小数据集 overfitting 测试 |
| 结果不可复现 | 1. 固定所有随机种子  2. 设置 `torch.backends.cudnn.deterministic = True`  3. 检查数据 shuffle |
| 训练速度慢 | 1. 检查 DataLoader `num_workers`  2. 检查数据是否在 GPU 上  3. 使用 `pin_memory=True` |

## Execution Rules

1. 在运行任何训练前，先确认环境和 GPU 可用性。
2. 对于长时间训练，使用后台运行并定期检查状态。
3. 保存中间 checkpoint，防止意外中断导致进度丢失。
4. 实验结果对比时，确保控制变量一致。
5. 任何涉及大量计算的操作，先在小数据集上验证正确性。
