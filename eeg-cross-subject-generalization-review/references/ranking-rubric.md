# Ranking Rubric

Use this file to keep the three buckets consistent across tasks and time ranges.

## Evidence Tracks

Always separate papers into two evidence tracks before ranking them:

### Track A: Stable Evidence

Use for:

- `published`
- `accepted`

This track supports stronger claims such as:

- representative work
- higher-confidence summary
- stable field direction

### Track B: Frontier Evidence

Use for:

- `competition`
- `preprint`

This track supports weaker but timely claims such as:

- newest trend
- likely next direction
- early signal of benchmark shift

Never merge Track A and Track B into one single top list without explicit status labels.

## Bucket Definitions

### Most Frontier

Score highest on:

1. recency
2. novelty of formulation or scale
3. benchmark or competition impact
4. new pretraining or evaluation regime

Typical examples:

- new foundation models
- large-scale challenges
- cross-task to cross-subject transfer papers

### Highest Quality

Score highest on:

1. venue or journal quality
2. experimental completeness
3. clarity of protocol and reporting
4. representativeness for the field

Typical examples:

- ICLR / NeurIPS / ICML papers
- IEEE TBME / JBHI / JNE / strong review journals

### Most Workable

Score highest on:

1. strict cross-subject protocol
2. benchmark consistency
3. reproducibility
4. stable performance across datasets or tasks
5. low hidden dependence on special preprocessing or private code

This bucket is the default answer to "what should I actually try first?"

## Practical Scoring Guide

Score each candidate from 0 to 2 on each axis:

- protocol strictness
- benchmark comparability
- reproducibility
- method clarity
- practical usability
- novelty

Interpretation:

- `Most frontier`: novelty dominates, but status must be visible
- `Highest quality`: method clarity plus venue strength dominate
- `Most workable`: protocol strictness, benchmark comparability, and reproducibility dominate

## Hard Constraints

Do not rank a paper as `most workable` if:

1. the cross-subject protocol is vague
2. the target-subject calibration budget is unclear
3. the result is reported on a non-comparable custom split only
4. no code, no benchmark context, and no reproducibility details are available

Do not rank a paper as `highest quality` if:

1. it is only a preprint
2. key experiments are missing
3. the paper is important but method or evaluation details are too thin

## Tie-Break Rules

When several papers are close:

1. prefer stricter subject-disjoint evaluation
2. prefer multi-dataset evidence
3. prefer public code or benchmark integration
4. prefer clearer reporting over marginal metric gains

## Default Language For Judgments

Use phrases like:

- `更前沿，但证据仍偏早期`
- `发表质量更高，适合做代表作`
- `更适合作为复现与落地起点`
- `结果亮眼，但当前不可与 LOSO 设定直接横比`
