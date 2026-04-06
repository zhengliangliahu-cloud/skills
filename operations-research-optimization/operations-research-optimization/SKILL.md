---
name: operations-research-optimization
description: |
  面向工业级运筹优化建模、算法选型、求解器路线设计、调参与排障的技能。用在需要把业务问题转成数学优化模型并选择合适求解路径的场景，包括 LP、MILP、QP、SOCP、NLP、CP/CP-SAT、网络流、路径规划、排班排产、选址、库存、资源分配、鲁棒/随机/多目标优化、分解算法、列生成、拉格朗日松弛、元启发式与 matheuristic。也用在模型无可行解、求解过慢、gap 长时间不收敛、规则约束复杂、需要 warm start、rolling horizon、fallback heuristic、以及判断何时从开源栈升级到商业求解器的场景。
---

# Operations Research Optimization

## Overview

用这个技能把业务目标、规则和数据约束转成可求解的运筹优化问题，并给出从建模到求解、从调参到工业落地的完整路线。默认优先使用 Python 开源栈：`OR-Tools`、`Pyomo`、`SciPy`、`networkx`，只有在升级条件明确时才建议 `Gurobi`、`CPLEX`、`Xpress` 或 `Mosek`。

## Core Workflow

1. 先把业务目标写成可比较的 KPI，并区分硬约束与软约束。
2. 先审计数据边界、粒度、时间尺度和历史波动，再决定是否值得上复杂模型。
3. 先识别结构，再选模型族：连续、离散、逻辑、图结构、不确定性、多目标、分解结构。
4. 先做最小可行基线，再做强化：变量收紧、约束强化、warm start、rolling horizon、分解、启发式兜底。
5. 先给出主路线，再给出 fallback 路线、失败模式和升级触发条件。

## Intake Checklist

先补齐以下输入，再开始给算法建议：

- 决策变量是什么，粒度是什么，是否可拆分为多个层级。
- 目标函数是什么，是否只有一个 KPI，还是成本、服务、稳定性、风险并存。
- 约束分为哪几类：容量、平衡、逻辑、时序、路径、班次、预算、服务水平。
- 数据是否完整：上下界、时间窗、需求分布、切换成本、资源日历、地理距离。
- 输出需要什么：最优值、可行解、近似解、规则解释、实时决策、滚动重求。
- 运行预算是什么：求解时间、硬件、可接受 gap、上线频率、是否需要可解释性。

## Route Problems To Model Families

按问题结构决定第一条路线，而不是按流行算法拍脑袋。

- 连续资源分配、成本最小化、配比、流量平衡优先看 LP、QP、SOCP、凸优化。
- 二元开关、固定费用、指派、选址、班次、背包、路径附加逻辑优先看 MILP/MINLP。
- 大量时序逻辑、互斥、日历、工序关系、no-overlap、复杂离散规则优先看 CP/CP-SAT。
- 纯图结构或弱耦合图结构优先看最短路、最大流、最小费用流、匹配、树、Routing。
- 不确定需求、波动运价、服务水平、风险约束优先看鲁棒、随机、在线、多阶段框架。
- 超大规模块结构、列空间巨大、场景可分、主从结构明确优先看分解、列生成、拉格朗日松弛。
- 精确法难以在预算内给出高质量解时，再看元启发式或 matheuristic，而不是反过来。

## Choose The Solver And Algorithm Path

- 用 `OR-Tools` 处理 `CP-SAT`、排班、离散逻辑和 Routing 类问题。
- 用 `Pyomo` 统一表达 LP、MILP、QP、NLP、鲁棒/随机扩展和分解原型。
- 用 `SciPy` 处理平滑连续优化、局部 NLP、校准类问题；需要高质量 NLP 时考虑 `IPOPT`。
- 用 `networkx` 或专用图算法做纯图结构 baseline，再决定是否升级到 MIP/CP。
- 用 `HiGHS` 做 LP/QP/MIP baseline；`CBC` 或 `SCIP` 作为离散补充；商业求解器只在开源路线被证明不足时升级。
- 用混合路线处理工业问题：图算法或启发式先造初解，MIP/CP 再强化；或主问题精确、子问题启发式。

## Industrialization Rules

- 先缩小变量域、收紧上下界、替换松的 `big-M`，再讨论调参。
- 先用简单可解释模型打通数据与业务闭环，再增加细约束、分层目标和风险项。
- 先定义停止条件和服务承诺：`time limit`、`relative gap`、最差可接受 KPI、兜底策略。
- 先准备 warm start、历史方案继承、规则修复器，再尝试复杂 heuristics。
- 先评估滚动窗口、分区求解、主从分解，再暴力堆机器。
- 先写清失败模式：无可行解、可行解太差、收敛太慢、求解器不稳定、数据漂移。

## Reference Map

- `references/problem-framing-and-modeling.md`
  业务问题拆解、变量与约束设计、数据审计、常见建模反模式。
- `references/linear-integer-and-convex.md`
  LP、MILP、QP、SOCP、凸优化、平滑 NLP、MINLP 的主路线和调参手册。
- `references/constraint-programming-and-cp-sat.md`
  逻辑约束、排程、离散搜索、`CP-SAT`、LNS 和传播建模。
- `references/network-flow-routing-and-graph.md`
  图结构、网络流、指派、匹配、TSP/VRP 和图上预处理。
- `references/scheduling-location-inventory-and-planning.md`
  排班排产、选址、库存、生产计划、供应链规划等工业高频问题。
- `references/stochastic-robust-online-and-multiobjective.md`
  不确定性、多目标、风险项、在线与滚动优化。
- `references/decomposition-column-generation-and-lagrangian.md`
  Benders、列生成、拉格朗日松弛、branch-and-price、稳定化。
- `references/metaheuristics-and-matheuristics.md`
  GA、SA、TS、GRASP、VNS/LNS/ALNS、混合精确法。
- `references/solver-selection-and-tuning.md`
  `OR-Tools`、`Pyomo`、`SciPy`、`networkx`、`HiGHS`、`CBC`、`SCIP` 的路线选择与调参。
- `references/industrial-playbooks-and-failure-modes.md`
  生产、配送、排班、选址、库存、资源配置的工业 playbook 与故障清单。

## Output Contract

触发这个技能时，默认输出以下内容，而不是只报算法名：

1. 问题抽象：变量、目标、约束、粒度、确定性假设。
2. 主路线：推荐模型族、推荐求解器、推荐建模库。
3. 候选路线：一个更保守的 baseline 和一个更强的升级路线。
4. 调参动作：先改模型什么，再改参数什么，顺序要明确。
5. 风险与失败模式：最可能卡住的位置，以及如何排障。
6. 升级触发条件：何时换算法、换建模方式、换求解器、换商业栈。

## Guardrails

- 不要在数据边界不清时直接推荐复杂随机优化。
- 不要在图结构明显时直接上笼统 MILP。
- 不要在逻辑和时序约束主导时强行线性化一切。
- 不要在没有 baseline 的情况下直接上元启发式。
- 不要在模型本身过松时把问题误判成“求解器太弱”。
- 不要在没有明确收益前默认建议商业求解器。
- 不要只给“试试调参数”式建议；要给具体参数、作用机制和优先级。

## Default Upgrade Triggers

- 开源 MIP 在合理建模强化后仍长期无可行解，或 gap 在可接受时间内无法下降。
- `CP-SAT` 能给出可行解但质量波动大，需要更强的线性松弛或更稳定的商业 MIP 支持。
- 需要工业级并行性能、稳定的高级 cuts、强 presolve、MIQP/MIQCP/NLP 支持。
- 需要成熟的 callback、solution pool、multi-objective、advanced basis、sensitivity、tuning tool。
- 需要面向生产 SLA 的稳定性能，而不是“偶尔能解出来”。

先读 `SKILL.md` 做路由，再只打开当前问题真正需要的 `references/` 文件，避免把整套知识库一次性塞进上下文。
