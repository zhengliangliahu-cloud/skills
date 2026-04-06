# 网络流、路径与图优化

## 目录

- 适用问题信号
- 建模套路与常见反模式
- 从初级到高级的算法谱系
- 参数调优清单
- 优缺点与失效模式
- 切换与升级信号

## 适用问题信号

- 业务对象天然是点、边、路径、连通、流量、匹配、树结构。
- 典型问题包括最短路、最大流、最小费用流、二分匹配、网络设计、TSP、VRP。
- 约束先来自图结构，后来自容量、时间窗、班次、服务规则。

## 建模套路与常见反模式

优先套路：

- 先判断能否用纯图算法解掉大部分结构，再决定是否升到 MIP/CP。
- 对配送和网络设计先建立节点弧模型，必要时再考虑集合分割或路径变量。
- 对时间窗和服务时长用 time-expanded network 或 route feasibility checker。
- 对多商品流先确认是否真的需要完整 multi-commodity formulation。

常见反模式：

- 纯最短路问题直接上通用 MILP。
- 图太密却不做边筛选、聚类或候选弧预生成。
- VRP 早期就把所有业务细节全部加进主模型，没有先做基线。
- 子回路消除约束设计过弱，导致 LP 松弛没有判别力。

## 从初级到高级的算法谱系

- 最短路：Dijkstra、A*、Bellman-Ford、label correcting。
- 流与匹配：max-flow/min-cut、min-cost flow、assignment、matching。
- 树与连通：minimum spanning tree、Steiner tree 近似。
- 路径优化：TSP/VRP 的 branch-and-cut、set partitioning、column generation。
- 启发式：savings、insertion、2-opt、3-opt、or-opt、LNS、ALNS。

## 参数调优清单

- 做图预处理：删 dominated arcs、收缩必经节点、限制候选邻居。
- 对最小费用流和 shortest path 优先使用专用算法，不要滥用通用求解器。
- 对 VRP 优先准备可行初解，再加 cuts 或 set partitioning 强化。
- 对路径问题调邻域时，先测 `2-opt`、relocate、exchange，再上更贵的复合 moves。
- 对时间窗问题控制时间离散粒度，避免 time-expanded network 爆炸。

## 优缺点与失效模式

优点：

- 结构清晰时，专用算法速度极快且稳定。
- 容易提供高质量初解和下界。
- 适合与 MIP、CP、启发式组合。

失效模式：

- 侧约束一多，纯图结构优势迅速下降。
- 多商品、多层级、时空耦合会让模型膨胀。
- VRP 若不做强 cuts 或列生成，很容易出现松弛过弱。

## 切换与升级信号

- 图结构上叠加大量逻辑和排程规则时，切到 `constraint-programming-and-cp-sat.md`。
- 固定费用、设施开关、库存联动明显时，切到 `linear-integer-and-convex.md`。
- 路径变量数量巨大时，切到 `decomposition-column-generation-and-lagrangian.md`。
- 精确路径法无法在时限内给出高质量解时，切到 `metaheuristics-and-matheuristics.md`。
