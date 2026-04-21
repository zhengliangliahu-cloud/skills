---
name: eeg-cross-subject-generalization-review
description: 调研、筛选、比较并撰写 EEG 跨被试泛化相关文献综述。Use when Codex needs to find, verify, classify, summarize, compare, or write about EEG cross-subject, subject-independent, leave-one-subject-out, unseen-subject, or transfer-to-new-subject generalization papers, benchmarks, foundation models, domain adaptation, meta-learning, and evaluation protocols in BCI or adjacent EEG decoding tasks.
---

# EEG Cross-Subject Generalization Review

## Overview

Use this skill to produce rigorous literature reviews on EEG cross-subject generalization.
Default to Chinese prose, but preserve English paper titles, venue names, dataset names, benchmark names, and metric names.
Treat `motor imagery (MI)` as the main axis, while also covering `P300`, `SSVEP`, `emotion`, and adjacent EEG decoding settings when they genuinely study unseen-subject transfer.

## 1. 任务定义

先明确用户要的到底是哪一种“跨被试泛化”：

1. 明确任务范式：
   - `MI`
   - `P300`
   - `SSVEP`
   - `emotion`
   - 其他 EEG decoding / foundation-model transfer 任务
2. 明确泛化设定：
   - `cross-subject`
   - `subject-independent`
   - `leave-one-subject-out`
   - `unseen-subject`
   - `transfer-to-new-subject`
3. 明确用户关注点：
   - `最前沿工作`
   - `最高质量工作`
   - `最 work 的工作`
   - `综述文档`
   - `组会/汇报版总结`
4. 明确时间范围：
   - 如果用户没说，默认先看近 3 年，再补关键老工作。
5. 明确是否需要严格双轨：
   - `published / accepted`
   - `competition / preprint`

如果用户说“谁最好”，不要直接给单一冠军。先检查数据集、协议、指标、校准量、是否 LOSO、是否 cross-dataset、是否有 target-subject calibration，再决定能不能比较。

## 2. 来源优先级

按下面顺序找和核实信息。优先官方源，二级源只用来补线索，不用来定事实。

1. `官方 venue / journal 页面`
   - OpenReview
   - NeurIPS / ICLR / ICML / IEEE / Springer / BMC / Frontiers / PubMed / DOI landing page
2. `arXiv / OpenReview submission / competition page`
   - 用于最前沿工作和状态核实
3. `benchmark / tool 官方文档`
   - MOABB
   - Braindecode
   - dataset project pages
4. `官方代码仓库`
   - 用于确认代码可得、数据处理、训练设置、复现门槛
5. `Google Scholar`
   - 只用于补漏，不单独作为最终事实源

需要扩展来源清单时，优先读取：

- `references/source-map.md`
- `references/seed-papers.md`

## 3. 检索流程

按下面顺序执行，不要一上来就堆一长串论文名。

1. 先界定任务和边界。
   - 先写清用户要的是哪一类 EEG 任务、哪种跨被试设定、哪个时间段。
2. 先跑主题检索。
   - 用 `cross-subject`, `subject-independent`, `leave-one-subject-out`, `unseen-subject`, `transfer learning`, `domain adaptation`, `foundation model`, `meta-learning` 这些关键词组合。
3. 再跑范式检索。
   - 按 `MI / P300 / SSVEP / emotion / foundation model / benchmark` 分别检索。
4. 先核实论文状态，再摘方法和结果。
   - 先确认 `published / accepted / competition / preprint`，再写摘要。
5. 去重并清洗。
   - 同一篇论文如果同时出现在 arXiv 和正式发表页，优先保留正式发表页，保留 arXiv 作为补充链接。
6. 只保留真正解决跨被试问题的论文进入主榜单。
   - 如果只是一般 EEG 分类，但没有 unseen-subject 评测，不要放进主榜单。
7. 最后再做三类归档。
   - `最前沿`
   - `最高质量`
   - `最 work`

需要现成检索式时，读取 `references/search-playbook.md`。

## 4. 筛选标准

进入主榜单前，至少满足下面条件之一：

1. 论文明确写出：
   - `cross-subject`
   - `subject-independent`
   - `leave-one-subject-out`
   - `unseen-subject`
   - `transfer-to-new-subject`
2. 评测协议明确包含 target subject 未见数据。
3. 结果表确实报告了跨被试设定，而不是只报告 within-subject 或 cross-session。

默认排除或降级处理：

1. 只做单被试训练/测试的工作。
2. 只讲通用 EEG foundation model，但没有任何跨被试迁移证据的工作。
3. 只给 headline accuracy，没有说明协议、数据集、类别数、校准量、指标定义的工作。
4. 只在二级来源出现，找不到官方论文页、正式 DOI、PubMed、OpenReview、arXiv 或正式 competition 页面支撑的工作。

如果论文方法本身很重要，但跨被试证据不足：

- 可以收录到“背景/相关方法”；
- 不要收录到“最 work”主结论。

## 5. 三类工作归档规则

固定用三栏，不要把三栏混写。

### 最前沿工作

优先看：

1. 时间新不新。
2. 是否代表新范式。
   - foundation model
   - large-scale pretraining
   - cross-task to cross-subject transfer
   - competition benchmark
3. 是否提出新评测或新规模数据。

这类工作允许包含 `competition` 和 `preprint`，但必须显式标注状态。

### 最高质量工作

优先看：

1. venue / journal 质量。
2. 方法是否完整、设定是否清晰。
3. 实验是否覆盖多个任务、多个数据集或严格协议。
4. 论文是否足够适合做“领域代表作”。

这类工作默认优先 `published` 或 `accepted`。

### 最 work 的工作

优先看：

1. 泛化协议是否严格。
2. benchmark 设定是否规范。
3. 是否跨数据集或跨被试稳定。
4. 是否有公开代码或容易复现。
5. 是否能作为强基线或稳定方案复用。

“最 work” 不等于“数值最高”。如果一个方法只在单数据集、单协议下拿到最高 accuracy，但复现门槛高、协议不透明、没有稳定外部证据，不要把它放在第一梯队。

更细的判据写在 `references/ranking-rubric.md`。

## 6. 写作规范

写每篇论文时，固定交代下面 6 件事：

1. `发表位置 / 年份 / 状态`
2. `核心方法一句话`
3. `为何有效`
4. `关键结果`
5. `评测边界`
6. `是否可复现`

压缩写法优先，避免空话。每篇论文至少回答：

- 这篇论文到底解决了什么跨被试问题？
- 它的方法与前作相比新增了什么？
- 结果是在什么数据集、什么协议、什么指标下成立？
- 这个结果能不能与别的论文直接比较？

默认写作规则：

1. 先讲设定，再讲方法，再讲结果。
2. 不要把不同数据集、不同类别数、不同协议下的结果直接横比。
3. 如果必须对比，先加一句比较边界说明。
4. 把 `preprint`、`competition`、`published` 明确写出来。
5. 遇到 foundation model 论文，单独交代：
   - 预训练数据规模
   - 下游任务范围
   - 是否真正覆盖 unseen-subject transfer
6. 遇到 benchmark / tool，单独交代：
   - 它解决的是“评测可信度”还是“模型能力”

需要模板和警报语句时，读取 `references/writing-standard.md`。

## 7. 输出契约

默认输出分 4 段，除非用户明确要求更短格式。

1. `总览摘要`
   - 先交代这个领域当前主线是什么。
   - 明确“前沿线”和“稳健线”是否一致。
2. `三类代表工作清单`
   - 分成 `最前沿 / 最高质量 / 最 work`
   - 每篇论文都写 `Venue/Year/Status`
3. `结构化对比表`
   - 固定表头：
   - `Paper | Venue/Year/Status | Paradigm | Setting | Method | Key Result | Why It Matters | Code/Data`
4. `研究空白与下一步建议`
   - 指出评测不一致、数据规模不足、协议不统一、复现缺口等问题

如果用户只问某个子问题，也保持同样的证据纪律：

1. 先标状态。
2. 再写方法。
3. 再写结果。
4. 最后写可比性边界。

## On-Demand References

只在需要时读取下面文件，不要一次性全载入：

- 来源渠道与可信度：`references/source-map.md`
- 检索式模板：`references/search-playbook.md`
- 评分与归档规则：`references/ranking-rubric.md`
- 写作模板与警报：`references/writing-standard.md`
- 起始论文池：`references/seed-papers.md`
