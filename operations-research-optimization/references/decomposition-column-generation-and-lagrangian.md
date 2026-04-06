# 分解、列生成与拉格朗日松弛

## 目录

- 适用问题信号
- 建模套路与常见反模式
- 从初级到高级的算法谱系
- 参数调优清单
- 优缺点与失效模式
- 切换与升级信号

## 适用问题信号

- 模型规模巨大，但存在天然主从结构、块结构、场景结构或资源耦合约束。
- 路径、排班、切割库存等问题的可行模式数量极大，无法直接枚举。
- LP 松弛太弱，通用 branch-and-cut 很难收敛。

## 建模套路与常见反模式

优先套路：

- 明确“难的耦合约束”与“易分解子问题”。
- 对设施选址、场景规划、产销协同考虑 Benders 或 L-shaped。
- 对路径、排班、集合分割考虑 Dantzig-Wolfe / column generation。
- 对资源耦合强、局部子问题易解的模型考虑拉格朗日松弛。

常见反模式：

- 没有确认结构性收益就强上分解，反而增加系统复杂度。
- 主问题过弱，切和列虽然很多，但 bound 不改善。
- pricing 子问题本身就很难，导致列生成名义上成立、实践上失效。

## 从初级到高级的算法谱系

- Benders decomposition / L-shaped。
- Dantzig-Wolfe reformulation / column generation。
- branch-and-price / branch-cut-and-price。
- 拉格朗日松弛与 subgradient。
- Progressive hedging、ADMM 风格的工程化协调。

## 参数调优清单

- `stabilization`：对偶震荡明显时，用 trust region、penalty 或 box stabilization。
- `cut management`：保留高质量 cuts，定期清理弱 cuts。
- `column pool`：维护高价值列池，避免重复生成。
- `warm start`：主问题初始列、历史 cuts、旧场景解要复用。
- `pricing tolerance`：避免过早停止，也避免对子问题求太精。
- `convergence monitoring`：同时监控 primal、dual、bound gap 和每轮改进幅度。

## 优缺点与失效模式

优点：

- 能把工业大模型拆成可管理子问题。
- 更容易利用并行和结构化业务知识。
- 对路径、排班、场景规划常有数量级收益。

失效模式：

- 实现复杂度和维护成本显著高于单体模型。
- 数值稳定化不到位时，对偶振荡严重。
- 子问题不稳定或过慢时，整体框架难落地。

## 切换与升级信号

- 如果单体模型通过简单强化就够快，回到 `linear-integer-and-convex.md`。
- 如果只是需要高质量可行解而非强界，转到 `metaheuristics-and-matheuristics.md`。
- 若分解后的子问题本身是排程或路径问题，分别联动 `constraint-programming-and-cp-sat.md` 与 `network-flow-routing-and-graph.md`。
