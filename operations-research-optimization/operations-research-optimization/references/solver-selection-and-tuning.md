# 求解器选择与调参

## 目录

- 适用问题信号
- 建模套路与常见反模式
- 从初级到高级的算法谱系
- 参数调优清单
- 优缺点与失效模式
- 切换与升级信号

## 适用问题信号

- 需要在 `OR-Tools`、`Pyomo`、`SciPy`、`networkx`、`HiGHS`、`CBC`、`SCIP` 之间选主路线。
- 已有模型，但求解慢、无解、不可行、gap 降不动或数值不稳定。
- 需要明确何时该升到商业求解器。

## 建模套路与常见反模式

推荐路由：

- `OR-Tools CP-SAT`：排班、排程、复杂逻辑、布尔主导离散问题。
- `OR-Tools Routing`：标准 VRP/VRPTW 及其快速原型。
- `Pyomo + HiGHS`：LP、MIP、QP baseline，便于后续升级求解器。
- `Pyomo + CBC/SCIP`：整数问题增强版 baseline。
- `SciPy optimize`：平滑连续优化、参数校准、本地 NLP。
- `networkx`：纯图结构最短路、匹配、流问题的快速专用算法。

常见反模式：

- 因为工具熟悉就强行套，不看问题结构。
- 同一个问题同时堆多个建模层，导致调试困难。
- 求解慢时只调参数，不检查模型松弛、对称性和数据尺度。

## 从初级到高级的算法谱系

- 专用图算法与规则法 baseline。
- 开源 LP/MIP/CP/NLP 求解器。
- 开源 + 自定义 warm start / LNS / decomposition。
- 商业求解器与高级功能：callback、solution pool、advanced basis、automatic tuning。

## 参数调优清单

### OR-Tools CP-SAT

- `num_search_workers`
- `max_time_in_seconds`
- `relative_gap_limit`
- `random_seed`
- `search_branching`
- LNS neighborhood 设计与阶段式求解

### HiGHS / CBC / SCIP / 通用 MIP

- `presolve`
- `threads`
- `mip_gap`
- `time_limit`
- 启发式与 cuts 强度
- 分支优先级、对称性破坏、初始解输入

### SciPy / NLP

- 方法选择：`SLSQP`、`trust-constr`、`L-BFGS-B`
- 初值与 bounds
- 梯度 / Hessian 提供方式
- 收敛容差与最大迭代数

优先级顺序：

1. 先检查模型结构、界限、尺度、对称性。
2. 再喂 warm start 或 baseline 解。
3. 再调时间限制、gap、并行线程、启发式和 cuts。
4. 最后才考虑切求解器。

## 优缺点与失效模式

优点：

- 路由清晰时，开源栈足以覆盖大量工业问题。
- `Pyomo` 便于迁移求解器，`OR-Tools` 便于逻辑与路由建模。
- 专用图算法和启发式能大幅降低整体成本。

失效模式：

- 开源 MIP 在超大规模离散问题上性能波动大。
- `Routing` 模块遇到大量非标准约束时可扩展性有限。
- `SciPy` 更偏连续局部优化，不适合大规模离散组合问题。

## 切换与升级信号

- 先升级建模方式：图算法 -> MIP/CP，单体 -> 分解，精确 -> matheuristic。
- 若以下条件同时成立，再考虑商业求解器：
  - 已做变量域收紧、约束强化、warm start、合理调参。
  - 问题规模、稳定性要求或高级功能超出开源栈能力。
  - 商业求解器的许可成本低于业务收益。
- 商业升级优先级示意：
  - 强 MIP / MIQP / MIQCP：`Gurobi`、`CPLEX`、`Xpress`
  - 强锥优化：`Mosek`
  - 高级 NLP / MINLP：视模型类型选择 `IPOPT`、`KNITRO`、商业 MINLP 工具
