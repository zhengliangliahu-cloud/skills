# 跨领域应用 Playbook

## 目录

1. CV / 视频
2. NLP / LLM
3. 时间序列与生物信号
4. 多模态
5. 图学习与推荐
6. 通用决策表

## CV / 视频

### 任务特征

- 图像局部纹理强，视频还有时序和长程依赖。

### 适合的架构

- 图像小中数据：CNN、ConvNeXt、hybrid CNN-Transformer。
- 大规模视觉预训练：ViT、Swin、hierarchical Transformer。
- 视频：2D CNN + temporal module、3D CNN、TimeSformer、Video Swin、hybrid long-context routes。

### 常见选择逻辑

- 样本不大且局部纹理强：先用 CNN 或 hybrid。
- 预训练资源丰富、需要大规模迁移：再用 ViT 路线。

## NLP / LLM

### 任务特征

- 序列长、语义层级深、预训练生态成熟。

### 适合的架构

- 通用文本理解与生成：Transformer 仍是主线。
- 长上下文和效率压力大：efficient Transformer、retrieval、SSM/hybrid。
- 结构化推理或知识图谱增强：Transformer + graph / retrieval。

### 关键提醒

- 大模型场景下，数据和训练配方往往比微小架构差异更重要。
- 若是小样本专用任务，直接用巨大 backbone 并不总是最好。

## 时间序列与生物信号

### 任务特征

- 局部模式、周期性、趋势、长依赖和噪声共存。

### 适合的架构

- 小样本/噪声强：CNN、TCN、轻量 RNN。
- 长程依赖明确：Transformer、SSM、hybrid。
- 需要跨通道关系：GNN 或 channel attention。
- EEG/ECG/EMG：优先考虑预处理与协议，再定 backbone。

### 关键提醒

- 先用时间尺度定义感受野需求。
- 不要因为“序列”就默认 Transformer 最优。

## 多模态

### 任务特征

- 关键在对齐、互补和缺失模态鲁棒性。

### 适合的架构

- late fusion：baseline 首选，稳。
- cross-attention：模态交互强时使用。
- graph + multimodal：实体关系和模态关系都重要时使用。

### 关键提醒

- 模态时间对齐、采样率不一致和缺失值处理是首要问题。

## 图学习与推荐

### 任务特征

- 关系结构是主信息，规模和动态图常是难点。

### 适合的架构

- 大规模推荐：GraphSAGE、sampling GNN、序列推荐混合结构。
- 分子图：MPNN、GIN、Graph Transformer。
- 异构图：R-GCN、heterogeneous GNN、heterogeneous graph transformer。

### 关键提醒

- 图构造、邻居采样和负采样策略往往决定上限。
- 如果长距离依赖和复杂结构编码重要，再升级到 Graph Transformer。

## 通用决策表

- 数据少且噪声大：优先强先验、小模型、稳定协议。
- 数据大且预训练充分：优先 Transformer / hybrid / foundation 路线。
- 结构关系强：优先 GNN / Graph Transformer。
- 长序列吞吐关键：优先 TCN、efficient Transformer、SSM/hybrid。
- 需要部署和低延迟：优先轻量 CNN / TCN / distilled models。
