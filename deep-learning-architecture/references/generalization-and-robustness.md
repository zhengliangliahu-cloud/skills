# 泛化与稳健性

## 目录

1. 问题分型
2. 先改什么
3. Domain Generalization
4. Domain Adaptation
5. Transfer / Self-Supervised Learning
6. OOD、校准与不确定性
7. 跨被试 / 跨数据集协议
8. 失败定位

## 问题分型

### Domain Generalization

- 只有源域训练数据，希望泛化到未见域。
- 关键词：cross-subject、cross-site、cross-device、cross-dataset。

### Domain Adaptation

- 能看到目标域无标注或少量标注数据。
- 关键词：test-time adaptation、unsupervised DA、few-shot adaptation。

### 广义泛化能力

- 更广地关注过拟合、稳健性、校准、对噪声和分布偏移的脆弱性。

## 先改什么

按这个顺序排查，而不是一上来换 backbone。

1. 协议与数据
   先查切分、泄漏、标签定义、采样偏差、预处理一致性。
2. 强 baseline
   先有简单而稳的 CNN / TCN / Transformer-small / GNN baseline。
3. 训练策略
   再看正则化、增强、重采样、损失函数、early stopping、校准。
4. 预训练与迁移
   样本少或域偏移强时，优先比较自监督和迁移。
5. DG / DA 方法
   最后再叠 invariant learning、meta-learning、alignment、test-time adaptation。

## Domain Generalization

### 适合的策略

- 数据增强和 style randomization。
- 域不变表征学习。
- meta-learning / episodic training。
- 风险分解、IRM / REx 风格方法。
- 多专家 / 集成 / domain-specific heads。

### 优点

- 当目标域完全不可见时仍然有意义。

### 缺点

- 很多方法对实现细节和域定义非常敏感。
- 若源域覆盖不足，DG 方法也难救。

### 何时优先

- 目标域拿不到。
- 场景要求 cold-start 泛化。

## Domain Adaptation

### 适合的策略

- feature alignment、adversarial adaptation、pseudo-labeling、test-time adaptation。

### 优点

- 能利用目标域数据时通常更直接。

### 缺点

- 容易出现负迁移。
- 测试时自适应要特别注意稳定性和隐私边界。

## Transfer / Self-Supervised Learning

### 适用场景

- 源任务多、无标注数据丰富、目标任务样本少。

### 常见路线

- contrastive learning、masked reconstruction、multi-view learning、cross-domain pretraining。

### 关键判断

- 有时候“合适的预训练 + 普通 backbone”优于“最前沿 backbone + 从零训练”。

## OOD、校准与不确定性

### 必查项

- 置信度是否可校准。
- 错误样本是否集中在某些子域、被试、设备或长度区间。
- 评估是否包含 AUROC、ECE、Brier、selective prediction 等稳健性指标。

### 技术路线

- temperature scaling、deep ensembles、MC dropout、energy-based OOD、selective prediction。

## 跨被试 / 跨数据集协议

- 明确 subject-level split。
- 明确 dataset-level leave-one-dataset-out。
- 报告 per-domain/per-subject 方差，而不是只报平均值。
- 区分“seen subjects unseen sessions”和“completely unseen subjects”。

## 失败定位

### 症状到动作

- 训练好、跨域差：先看 domain shift 和协议，再看 DG/DA。
- 训练都不好：先看特征表达、标签质量和基础 backbone。
- 新域置信度高但错很多：先做校准和 OOD 检测。
- 某些域显著差：检查域间数据质量、采样率、设备、预处理是否一致。

### Guardrails

- 不要把所有跨域问题都归咎于 backbone。
- 不要默认 invariant learning 一定有效；先确认域标签和 shift 类型。
- 不要只报平均精度，不报 worst-domain 或跨 subject 方差。
