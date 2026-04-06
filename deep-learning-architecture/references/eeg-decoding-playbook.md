# EEG 解码 Playbook

## 目录

1. 统一检查项
2. Motor Imagery
3. ERP / P300
4. SSVEP
5. 睡眠分期
6. 癫痫与临床分类
7. 情绪与认知状态
8. 预处理与架构联动
9. 常见泄漏点

## 统一检查项

### 任务特征

- EEG 通常小样本、高噪声、跨被试差异大、跨会话漂移明显。
- 通道拓扑、频带特征、时间动态和伪迹处理经常比 backbone 选择更影响结果。

### 默认比较路线

- CNN 路线：EEGNet、DeepConvNet、ShallowConvNet、TSception 类。
- TCN / temporal conv 路线：适合中长时窗和低延迟需求。
- Transformer / Conformer 路线：适合长时序交互、跨通道关系更复杂的场景，但更吃数据。
- 图路线：当通道关系、脑区连接或动态功能连接是研究重点时考虑 GCN/GAT/Graph Transformer。
- 混合路线：CNN + Transformer、CNN + GNN、TCN + attention。

### 必查协议

- intra-subject 还是 cross-subject。
- session split 是否独立。
- train/val/test 是否在被试层面切分。
- 窗口重叠是否跨 split。
- 预处理统计量是否只用训练集估计。

## Motor Imagery

### 任务特征

- 频带节律和空间模式重要，常聚焦 mu / beta 变化。
- 跨被试泛化通常难。

### 适合的架构

- CNN：EEGNet、Shallow/DeepConvNet 仍然是强 baseline。
- TCN：适合时序模式明显且预算有限。
- Conformer / Transformer：当窗口较长、跨通道全局依赖更重要时可比较。
- GNN：如果显式建通道图或脑区图，适合研究空间依赖。

### 优点与缺点

- CNN 稳定、样本效率高，但全局交互有限。
- Transformer 表达强，但对小样本和 protocol 非常敏感。
- GNN 对空间关系更自然，但图构造质量决定上限。

### 常用技巧

- 频带滤波、时频变换、Riemannian feature 或 CSP 作为对照。
- subject-wise normalization、通道 dropout、mixup、对比学习预训练。

### 何时不该用某路线

- 没有足够样本或预训练时，不要默认 Transformer 优于 CNN。
- 没有可信图先验时，不要为了“脑网络”硬上 GNN。

## ERP / P300

### 任务特征

- 事件锁定、短时间窗、时间定位更重要。
- 延迟和在线性能常是核心指标。

### 适合的架构

- 轻量 CNN、TCN、small attention 模型。
- 大型 Transformer 往往不是首选。

### 关键建议

- 强化时间对齐和刺激同步。
- 把 latency、ITR、在线稳定性纳入比较，不只看离线准确率。

## SSVEP

### 任务特征

- 频率识别与谐波结构重要。
- 窗口较短，实时性强。

### 适合的架构

- 频域感知 CNN、轻量时频模型、多分支模型。
- 如果使用 Transformer，通常需要明确证明其优于频谱先验模型。

### 常见坑

- 只比准确率，不比短窗性能和鲁棒性。
- 忽视刺激频率设计和谐波建模。

## 睡眠分期

### 任务特征

- 长时序上下文、阶段转移、跨 epoch 依赖显著。

### 适合的架构

- CNN + RNN、CNN + Transformer、TCN、长序列模型。
- SSM / efficient Transformer 在超长上下文设定下值得比较。

### 关键建议

- 先定义上下文窗口长度。
- 对类别不平衡和 stage transition 做专门评估。

## 癫痫与临床分类

### 任务特征

- 伪迹、病人差异、标签噪声和临床协议差异都很大。

### 适合的架构

- 稳健 CNN / TCN baseline 必须先有。
- 需要解释性时，优先考虑能回溯时频和通道贡献的结构。

### 关键建议

- patient-level split 是底线。
- 数据集差异大时，泛化策略常比 backbone 更重要。

## 情绪与认知状态

### 任务特征

- 标签本身主观，跨被试和跨实验条件偏移大。
- 跨脑区依赖可能重要。

### 适合的架构

- CNN / hybrid baseline。
- 图模型适合研究通道依赖与功能连接。
- Transformer 可用于长时窗或多模态融合，但需警惕小样本过拟合。

### 当前趋势

- 图建模在情绪 EEG 里很活跃，但“图怎么构”比“用不用 GNN”更关键。

## 预处理与架构联动

- 原始时域输入：更适合 CNN、TCN、Transformer。
- 时频图：更适合 2D CNN、CNN + attention。
- 通道关系图：更适合 GCN/GAT/Graph Transformer。
- 手工特征 + 深度模型：适合作为低样本对照。
- 多视角输入：时域 + 频域 + 图，可用多分支或 cross-attention。

## 常见泄漏点

- trial 切窗后随机分配到 train/test。
- 对全数据做 z-score、ICA、频带选择后再切分。
- 同一被试相邻窗口高度重叠但分到不同 split。
- 用测试域参与超参或模型选择。
- 报告 cross-subject 结果时混入 subject-specific calibration。
