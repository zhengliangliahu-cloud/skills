# 元启发式与 Matheuristic

## 目录

- 适用问题信号
- 建模套路与常见反模式
- 从初级到高级的算法谱系
- 参数调优清单
- 优缺点与失效模式
- 切换与升级信号

## 适用问题信号

- 精确法在业务时限内难以给出足够好的解。
- 目标函数包含黑箱仿真、复杂经验规则或不可微评价。
- 需要秒级到分钟级连续重求，且问题规模大、约束复杂。
- 可以接受近似解，但必须稳定地产出高质量方案。

## 建模套路与常见反模式

优先套路：

- 先定义解编码、可行性检查、修复器和快速增量评估。
- 先做 problem-specific neighborhoods，再考虑通用种群法。
- 先让启发式能稳定造出可行解，再追求更好目标值。
- 优先设计 matheuristic：用精确法处理关键子问题，用启发式做全局搜索。

常见反模式：

- 没有 baseline，就直接调 GA、SA、TS 参数。
- 评价函数太慢，导致任何元启发式都跑不起来。
- 没有可行性修复器，算法在不可行空间浪费大量时间。
- 用通用元启发式硬套强结构问题，忽略图算法和 MIP 子问题。

## 从初级到高级的算法谱系

- 贪心、局部搜索、repair heuristic。
- SA、TS、GRASP、ILS、VNS。
- GA、PSO、ACO 等种群法。
- LNS、ALNS、ruin-and-recreate。
- matheuristic：fix-and-optimize、relax-and-fix、MIP neighborhood、CP guided LNS。

## 参数调优清单

- 邻域设计：先围绕瓶颈资源、关键路径、关键客户、关键班次做局部扰动。
- SA：温度初值按接受率校准；冷却不要过快；设 reheating 机制。
- TS：禁忌期限与问题规模同量级；必要时加 aspiration criterion。
- GA：种群规模与评估预算匹配；优先 problem-aware crossover；保留精英解。
- ALNS：维护算子得分；定期淘汰低贡献邻域；区分 intensification 与 diversification。
- 终止条件：用时间预算、无改进轮数、稳定 KPI，而不是固定迭代数。

## 优缺点与失效模式

优点：

- 对大规模、强非线性、强业务规则问题很灵活。
- 容易结合历史方案、局部修复器和仿真。
- 能与 MIP/CP 子问题组合形成强实战框架。

失效模式：

- 参数多，迁移性差。
- 缺乏最优性证明，质量评估依赖基准和下界。
- 如果评价函数慢或修复器弱，算法很容易失控。

## 切换与升级信号

- 若需要强界、可解释性或最优性证明，回到 `linear-integer-and-convex.md`。
- 若主要困难其实是逻辑排程，联动 `constraint-programming-and-cp-sat.md`。
- 若路径和网络结构是核心，联动 `network-flow-routing-and-graph.md` 做 problem-specific moves。
- 若元启发式只能靠大规模搜索硬撑，考虑 `decomposition-column-generation-and-lagrangian.md` 的结构化拆分。
