# Seed Papers and Tools

Use this file as a curated starting pool, not as a complete bibliography.
Status and links were checked against official or near-official sources on 2026-04-07.

## Frontier Anchors

- `EEG Foundation Challenge: From Cross-Task to Cross-Subject EEG Decoding`
  Venue/Year/Status: `NeurIPS 2025 Competition + arXiv 2025 | competition + preprint`
  Paradigm/Setting: large-scale EEG challenge; cross-task and cross-subject decoding on unseen subjects
  Method: not a single method paper; it defines a benchmark and challenge for zero-shot or transfer-style generalized EEG decoding
  Result: important because it shifts attention from single-dataset subject-independent papers toward broader, challenge-style generalization evaluation
  Why seed: use it when the user asks for the newest benchmark direction or the frontier of EEG generalization at scale
  Link: [NeurIPS competition page](https://nips.cc/virtual/2025/competition/127719), [arXiv 2506.19141](https://arxiv.org/abs/2506.19141)

- `CSBrain: A Cross-scale Spatiotemporal Brain Foundation Model for EEG Decoding`
  Venue/Year/Status: `arXiv 2025 | preprint`
  Paradigm/Setting: generalized EEG decoding across 11 tasks and 16 datasets
  Method: uses Cross-scale Spatiotemporal Tokenization and Structured Sparse Attention to model EEG structure across spatial and temporal scales
  Result: reports consistent gains over task-specific and foundation-model baselines across many tasks; exact numbers should be cited per downstream table, not collapsed into one headline
  Why seed: representative of the 2025 frontier shift from generic transformer scaling to structure-aware EEG foundation modeling
  Link: [arXiv 2506.23075](https://arxiv.org/abs/2506.23075)

- `Foundation Models on Wearable EEG using Self-Supervised Learning`
  Venue/Year/Status: `EMBC 2025 | published`
  Paradigm/Setting: wearable EEG pretraining and downstream transfer
  Method: adapts self-supervised pretraining to wearable EEG and evaluates transfer utility
  Result: useful as a neighboring frontier anchor when the user wants broad EEG foundation-model coverage beyond classical BCI datasets
  Why seed: shows how cross-subject generalization conversations are moving into real-world and wearable EEG settings
  Link: [PubMed 41038107](https://pubmed.ncbi.nlm.nih.gov/41038107/)

## High-Quality Core Papers

- `Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI`
  Venue/Year/Status: `ICLR 2024 Spotlight | published`
  Paradigm/Setting: multi-dataset EEG foundation model for downstream transfer across tasks
  Method: learns discrete neural tokens and performs masked code prediction over channel-wise EEG patches
  Result: the paper reports strong transfer results across multiple downstream EEG tasks and established LaBraM as a central foundation-model reference line
  Why seed: one of the most important field-defining anchors for modern EEG foundation-model discussion
  Link: [OpenReview](https://openreview.net/forum?id=QzTpTRVtrP)

- `EEGPT: Pretrained Transformer for Universal and Reliable Representation of EEG Signals`
  Venue/Year/Status: `NeurIPS 2024 | published`
  Paradigm/Setting: universal EEG representation learning with broad downstream transfer
  Method: builds a pretrained EEG transformer with emphasis on universal and reliable representations for heterogeneous EEG tasks
  Result: widely cited as a strong generalist baseline in the post-LaBraM wave; inspect the official paper tables before quoting task-specific gains
  Why seed: use it whenever the user asks about top-tier EEG foundation models with stronger venue quality than frontier-only preprints
  Link: [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/216c5cd45a71ceca91b10d6fdfc8f24f-Abstract-Conference.html)

- `BIOT: Biosignal Transformer for Cross-data Learning in the Wild`
  Venue/Year/Status: `NeurIPS 2023 | published`
  Paradigm/Setting: cross-data biosignal learning with heterogeneous channels, lengths, and missing values
  Method: tokenizes biosignals into a unified sentence-like representation to enable cross-dataset pretraining and transfer
  Result: important evidence that generalized biosignal representation learning can work under realistic heterogeneity, including EEG
  Why seed: strong reference for cross-dataset robustness and for understanding how generalized EEG transfer differs from classic subject-specific pipelines
  Link: [NeurIPS poster page](https://neurips.cc/virtual/2023/poster/71117)

## Workhorse Papers And Strong Baselines

- `Transfer Learning for Brain-Computer Interfaces: A Euclidean Space Data Alignment Approach`
  Venue/Year/Status: `IEEE Transactions on Biomedical Engineering 2020 | published`
  Paradigm/Setting: subject-independent BCI transfer
  Method: uses Euclidean alignment to reduce inter-subject covariance mismatch before classification
  Result: a classic strong baseline because it is simple, cheap, and often surprisingly competitive for cross-subject EEG transfer
  Why seed: default baseline anchor when the user asks for methods that are actually easy to implement and reproduce
  Link: [PubMed 31034407](https://pubmed.ncbi.nlm.nih.gov/31034407/)

- `MIN2Net: End-to-End Multi-Task Learning for Subject-Independent Motor Imagery EEG Classification`
  Venue/Year/Status: `IEEE Transactions on Biomedical Engineering 2022 | published`
  Paradigm/Setting: subject-independent MI classification
  Method: combines end-to-end representation learning with multi-task objectives designed for MI EEG
  Result: reported improved subject-independent performance on common MI benchmarks such as SMR-BCI and OpenBMI
  Why seed: useful when the user wants a deep model that is still focused on subject-independent MI rather than giant foundation-model pretraining
  Link: [PubMed 34932469](https://pubmed.ncbi.nlm.nih.gov/34932469/)

- `Adaptive Deep Feature Representation Learning for Cross-Subject EEG Decoding`
  Venue/Year/Status: `BMC Bioinformatics 2024 | published`
  Paradigm/Setting: cross-subject EEG decoding
  Method: combines adaptive feature learning and alignment-style objectives to learn shared but discriminative cross-subject representations
  Result: reports improved decoding accuracy on BCI Competition datasets under cross-subject settings; cite exact dataset-specific numbers from the paper tables
  Why seed: a useful bridge paper between classical domain adaptation and newer representation-learning styles
  Link: [BMC article](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-024-06024-w)

- `Deep Learning Based Inter-Subject Continuous Decoding of Movement From Scalp Electroencephalography`
  Venue/Year/Status: `Journal of Neural Engineering 2023 | published`
  Paradigm/Setting: inter-subject continuous movement decoding
  Method: applies deep learning to continuous EEG decoding rather than only trial-wise classification
  Result: important because it broadens the cross-subject discussion beyond discrete MI classification and into continuous decoding
  Why seed: use it when the user wants neighboring but still relevant evidence on generalized EEG decoding
  Link: [PubMed 36827555](https://pubmed.ncbi.nlm.nih.gov/36827555/)

## Reviews

- `Foundation Models for EEG Decoding: Current Progress and Prospective Research`
  Venue/Year/Status: `Journal of Neural Engineering 2025 | published review`
  Paradigm/Setting: EEG foundation-model landscape
  Method: review article, not a new model
  Result: synthesizes datasets, methods, opportunities, and bottlenecks for EEG foundation models
  Why seed: use it to position recent foundation models and to avoid writing a narrow MI-only story
  Link: [PubMed 41145005](https://pubmed.ncbi.nlm.nih.gov/41145005/)

- `Foundation Models for Neural Signal Decoding: EEG-Centered Perspectives Toward Unified Representations`
  Venue/Year/Status: `European Journal of Neuroscience 2026 | published review`
  Paradigm/Setting: broader neural-signal and EEG-centered foundation-model perspective
  Method: review article, not a new model
  Result: useful for framing unified representations, multimodal transfer, and the limits of current generalist EEG models
  Why seed: use it when the user wants a higher-level synthesis or future-directions section
  Link: [PubMed 41459740](https://pubmed.ncbi.nlm.nih.gov/41459740/)

- `EEG-Based Brain-Computer Interfaces and the Issue of Inter-Subject Variability: A Review`
  Venue/Year/Status: `Frontiers in Human Neuroscience 2013 | published review`
  Paradigm/Setting: foundational review of inter-subject variability in EEG-based BCI
  Method: review article, not a new model
  Result: old but still useful for framing why cross-subject transfer is hard and what kinds of variability matter
  Why seed: use it when the user needs historical grounding before the deep-learning or foundation-model era
  Link: [Referenced in newer official papers](https://openreview.net/attachment?id=MdgBATPjEu&name=pdf)

## Benchmark And Tool Anchors

- `MOABB: Trustworthy Algorithm Benchmarking for BCIs`
  Venue/Year/Status: `Journal of Neural Engineering 2018 | published`
  Paradigm/Setting: benchmark framework for BCI algorithms
  Method: standardizes datasets, pipelines, and evaluation procedures for more comparable BCI results
  Result: valuable because it improves benchmarking discipline rather than inventing a new model
  Why seed: essential when the user asks which results are actually comparable or reproducible
  Link: [paper summary with DOI](https://is.mpg.de/ei/publications/jaybar18), [MOABB docs](https://moabb.neurotechx.com/docs/index.html)

- `Braindecode`
  Venue/Year/Status: `Documentation / open-source tool | active`
  Paradigm/Setting: deep-learning toolbox for EEG, ECoG, and MEG decoding
  Method: provides preprocessing, model implementations, training helpers, and dataset integrations
  Result: not a paper result source by itself, but a crucial reality check for what models and pipelines are actually runnable
  Why seed: use it when the user asks which methods are easiest to reproduce, benchmark, or extend in practice
  Link: [Braindecode docs](https://braindecode.org/stable/index.html)
