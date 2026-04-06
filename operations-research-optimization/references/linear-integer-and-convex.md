# 线性、整数与凸优化

## 目录

- 适用问题信号
- 建模套路与常见反模式
- 从初级到高级的算法谱系
- 参数调优清单
- 优缺点与失效模式
- 切换与升级信号

## 适用问题信号

- 目标和约束主要由线性关系、二次项或凸约束构成。
- 存在固定费用、开关决策、选址、背包、指派、覆盖、产能扩展等离散决策。
- 需要较强下界、最优性证明或清晰的灵敏度解释。
- 问题可以写成 LP、MILP、QP、MIQP、SOCP、平滑 NLP、部分 MINLP。

## 建模套路与常见反模式

优先套路：

- 用 LP 松弛观察结构，再决定是否加整数变量。
- 用指示约束、cover constraints、flow balance、set partitioning 强化模型。
- 对固定费用和逻辑门槛优先尝试强形式，而不是宽松 `big-M`。
- 对凸问题保持凸性，避免不必要的线性化破坏问题结构。
- 对平滑 NLP 提供高质量初值、可微函数和稳定尺度。

常见反模式：

- 二元变量泛滥，但很多可以通过预处理或网络结构消掉。
- 用一个巨大 `big-M` 套住所有业务规则。
- 在 MIQP/MINLP 上没有任何界限收紧就直接求。
- 对 NLP 提供不可微或噪声很大的目标，导致局部求解器行为失真。

## 从初级到高级的算法谱系

- LP：单纯形、对偶单纯形、内点法。
- MILP：branch-and-bound、branch-and-cut、启发式可行解搜索。
- 凸 QP/SOCP：内点法、active-set、商业二阶锥求解器。
- 平滑 NLP：SQP、内点法、信赖域方法。
- MINLP：outer approximation、generalized Benders、spatial branch-and-bound。

工业上常见的升级路线：

- 先做 LP 或连续松弛 baseline。
- 再做 MILP 或 MIQP。
- 若线性化导致模型过大或过弱，再考虑 CP、分解或 matheuristic。

## 参数调优清单

### MIP / MILP

- `presolve`：默认开高；若诊断建模错误，可临时调低观察原模型。
- `cuts`：问题结构弱时增加 cuts；若 cuts 太多拖慢节点处理，再回调。
- `heuristics`：无可行解时提高启发式力度；已有好解但 bound 慢时降低。
- `branch priority`：对设施开关、主资源选择、主路径变量设置高优先级。
- `symmetry breaking`：对同质机器、同质车辆、同质仓库增加对称性破坏约束。
- `gap / time limit`：先定义业务可接受 `relative gap`，不要默认追求严格最优。
- `warm start`：喂历史方案、贪心方案、图算法方案，降低首个可行解时间。
- `relaxation strength`：增加 cover inequalities、flow-based 强化、有效上界。

### QP / SOCP / 凸优化

- 做 scaling，避免 Hessian 或约束矩阵病态。
- 检查变量边界是否可收紧，减少 ill-conditioning。
- 对 barrier / interior-point 调整容差时，先确认原问题尺度已规范。

### NLP / MINLP

- `initialization`：提供多个初值，尤其是非凸或多局部极小问题。
- `derivatives`：优先提供解析梯度和 Hessian，避免差分噪声。
- `regularization`：约束接近退化时增加稳定化项。
- `tolerance`：只有在确认业务可接受后才放宽收敛容差。

## 优缺点与失效模式

优点：

- 可给出强界和最优性证明。
- 目标与约束解释清晰，便于业务对齐。
- 与分解、列生成、启发式结合成熟。

失效模式：

- 松弛太弱，节点树爆炸。
- 大量对称结构拖慢搜索。
- `big-M` 过大导致数值问题与虚假可行性。
- NLP 局部解质量对初值极敏感。
- MINLP 在开源栈上很快触到性能天花板。

## 切换与升级信号

- 时序和逻辑主导时，切到 `constraint-programming-and-cp-sat.md`。
- 图结构主导时，切到 `network-flow-routing-and-graph.md`。
- 场景分解或列空间巨大时，切到 `decomposition-column-generation-and-lagrangian.md`。
- 连续优化不凸或目标是黑箱时，转到 `metaheuristics-and-matheuristics.md`。
- 在 `HiGHS`、`CBC`、`SCIP` 上已做模型强化仍无法满足时效或稳定性时，再升级到 `Gurobi`、`CPLEX`、`Xpress` 或 `Mosek`。
