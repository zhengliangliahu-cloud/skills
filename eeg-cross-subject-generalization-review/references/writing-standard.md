# Writing Standard

Use this file when turning papers into readable Chinese summaries.

## Default Output Shape

Unless the user asks for another format, return:

1. `总览摘要`
2. `三类代表工作清单`
3. `结构化对比表`
4. `研究空白与下一步建议`

## Per-Paper Mini Template

For each paper, cover these fields in compact prose:

`Venue/Year/Status` -> `核心方法` -> `为何有效` -> `关键结果` -> `评测边界` -> `可复现性`

Example sentence pattern:

`[Paper]` 发表于/提交于 `[Venue/Year/Status]`。它的核心做法是 `[one-sentence method]`，主要通过 `[why it works]` 改善 `[cross-subject difficulty]`。论文在 `[dataset/protocol/metric]` 下报告了 `[key result]`，但需要注意 `[comparison caveat]`。代码/数据 `[available or not available]`。

## Table Header

Use this exact header by default:

`Paper | Venue/Year/Status | Paradigm | Setting | Method | Key Result | Why It Matters | Code/Data`

## Comparison Rules

Before comparing numbers, check:

1. same task paradigm or not
2. same dataset or not
3. same class count or not
4. same evaluation split or not
5. same metric or not
6. same target-subject calibration budget or not

If any of these differ, add a caveat sentence before ranking.

## Ready-To-Use Caveat Sentences

- `这些结果来自不同数据集和协议，只能作趋势参考，不能直接横向排名。`
- `该工作使用了 target-subject calibration，因此不能与严格 zero-calibration 的 subject-independent 结果直接比较。`
- `该论文报告的是 cross-session 结果，不应替代 cross-subject 证据。`
- `该方法属于 preprint/competition 证据，方向很新，但稳定性判断应低于正式发表论文。`

## Common Writing Mistakes To Avoid

1. Do not call a preprint published.
2. Do not call a competition page a regular conference paper.
3. Do not mix `accuracy`, `kappa`, `F1`, and `AUROC` without saying so.
4. Do not compare 2-class MI and 4-class MI as if they were identical tasks.
5. Do not hide whether the method uses domain adaptation, calibration, or target-subject labels.
6. Do not write empty claims like `performance is greatly improved` without protocol and metric context.

## What Good Summaries Sound Like

Good summaries are:

- specific
- bounded
- method-aware
- protocol-aware
- honest about uncertainty

Bad summaries:

- only restate the abstract
- only report one headline metric
- ignore publication status
- ignore comparability
