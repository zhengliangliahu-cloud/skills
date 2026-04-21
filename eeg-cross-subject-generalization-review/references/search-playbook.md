# Search Playbook

Use these query templates as starting points. Narrow scope before broadening it.

## Global Rules

1. Always combine a task term with a generalization term.
2. Prefer English keywords for database search.
3. Use Google Scholar only after checking official venues and databases.
4. When the user asks for `latest`, search recent years first, then backfill older anchors.

## Core Generalization Keywords

Use one or more of:

- `cross-subject`
- `subject-independent`
- `leave-one-subject-out`
- `LOSO`
- `unseen-subject`
- `transfer-to-new-subject`
- `inter-subject`

## MI Queries

Start with:

- `"EEG" AND "motor imagery" AND "cross-subject"`
- `"EEG" AND "motor imagery" AND "subject-independent"`
- `"EEG" AND "motor imagery" AND "leave-one-subject-out"`
- `"MI EEG" AND "domain adaptation" AND "cross-subject"`
- `"MI EEG" AND "meta-learning" AND "subject-independent"`

Search targets:

- IEEE Xplore
- PubMed
- OpenReview
- arXiv

## P300 Queries

Start with:

- `"P300" AND "EEG" AND "cross-subject"`
- `"P300 BCI" AND "subject-independent"`
- `"P300" AND "unseen-subject" AND EEG`

Search targets:

- PubMed
- journal pages
- competition and dataset pages

## SSVEP Queries

Start with:

- `"SSVEP" AND "cross-subject"`
- `"SSVEP BCI" AND "subject-independent"`
- `"SSVEP EEG" AND "transfer learning"`

Search targets:

- IEEE Xplore
- PubMed
- arXiv

## Emotion / Affective EEG Queries

Start with:

- `"emotion EEG" AND "cross-subject"`
- `"affective EEG" AND "subject-independent"`
- `"emotion recognition EEG" AND "unseen-subject"`

Search targets:

- PubMed
- Springer / BMC
- arXiv

## Foundation-Model Queries

Start with:

- `"EEG foundation model" AND "cross-subject"`
- `"EEG pretraining" AND "unseen-subject"`
- `"EEG large model" AND "generalization"`
- `"cross-task to cross-subject EEG decoding"`

Search targets:

- OpenReview
- arXiv
- PubMed for reviews
- NeurIPS competition pages

## Domain-Adaptation Queries

Start with:

- `"EEG" AND "domain adaptation" AND "cross-subject"`
- `"subject-independent EEG" AND "domain adaptation"`
- `"EEG decoding" AND "adaptive feature representation" AND "cross-subject"`

Look for:

- feature alignment
- adversarial adaptation
- Euclidean or Riemannian alignment
- contrastive transfer

## Meta-Learning Queries

Start with:

- `"EEG" AND "meta-learning" AND "cross-subject"`
- `"subject-independent EEG" AND "few-shot"`
- `"EEG" AND "transfer to new subject" AND "meta-learning"`

Check whether the paper really targets unseen-subject transfer, rather than only low-data within-subject calibration.

## Benchmark / Tool Queries

Start with:

- `"MOABB" EEG benchmark`
- `"Braindecode" EEG deep learning`
- `"EEG foundation challenge" cross-subject`
- `"benchmark" AND "EEG" AND "cross-subject"`

Use these searches when the user asks:

- what is actually reproducible
- which methods are benchmark-consistent
- where to find comparable baselines

## Fast Query Variants For Scholar

When search quality is poor, use title-like queries:

- `"Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI"`
- `"EEGPT: Pretrained Transformer for Universal and Reliable Representation of EEG Signals"`
- `"CSBrain: A Cross-scale Spatiotemporal Brain Foundation Model for EEG Decoding"`
- `"Transfer Learning for Brain-Computer Interfaces: A Euclidean Space Data Alignment Approach"`

## Stop Conditions

Stop broad search and switch to synthesis when:

1. you already have representative papers from frontier, stable, and workhorse lines
2. you can explain the main methodological branches
3. you can name trustworthy benchmarks and tools
4. new search results are mostly duplicates or weaker variants
