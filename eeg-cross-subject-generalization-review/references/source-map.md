# Source Map

Use this file to decide where to search first and how much to trust each source.

## Priority Order

1. Official publication pages
   - OpenReview
   - conference proceedings
   - journal landing pages
   - DOI landing pages
   - PubMed
2. Official preprint or competition pages
   - arXiv
   - OpenReview submission pages
   - NeurIPS competition pages
3. Official benchmark and tool documentation
   - MOABB docs
   - Braindecode docs
   - dataset/project pages
4. Official code repositories
   - GitHub repositories linked from the paper or venue page
5. Scholar-style aggregators
   - Google Scholar only for discovery
   - do not rely on summaries or AI-generated review sites as final evidence

## What To Use Each Source For

### OpenReview / Conference Pages

Use for:

- venue confirmation
- paper status
- author list
- acceptance track or spotlight/poster label
- revision history

Best for:

- ICLR
- NeurIPS
- ICML
- workshop or frontier foundation-model papers

### Journal Pages / DOI / PubMed

Use for:

- final publication status
- journal, volume, issue, pages
- official abstract
- PMID / DOI

Best for:

- IEEE TBME / JBHI
- Journal of Neural Engineering
- Physiological Measurement
- BMC Bioinformatics
- Frontiers reviews
- European Journal of Neuroscience

### arXiv

Use for:

- latest preprint frontier work
- submission date
- abstract
- arXiv DOI

Use with care:

- never call it published unless a venue page confirms that

### Competition Pages

Use for:

- benchmark design
- challenge objective
- official leaderboard or task framing

Important:

- a competition page is not the same thing as a regular conference paper
- label as `competition` unless a separate paper page confirms `published` or `accepted`

### MOABB / Braindecode / Project Pages

Use for:

- benchmark protocols
- available datasets
- model zoo or baseline implementations
- reproducibility and code-path reality

These sources are especially useful when the user asks:

- which methods are benchmark-consistent
- which baselines are easiest to reproduce
- where to find comparable evaluations

## Recommended Search Destinations

### For frontier work

- OpenReview
- arXiv
- NeurIPS competition pages
- official project pages

### For high-quality and stable work

- PubMed
- DOI pages
- IEEE Xplore
- journal landing pages
- Springer / BMC / Frontiers pages

### For reproducibility and benchmark context

- MOABB docs: [https://moabb.neurotechx.com/docs/index.html](https://moabb.neurotechx.com/docs/index.html)
- Braindecode docs: [https://braindecode.org/stable/index.html](https://braindecode.org/stable/index.html)

## What Not To Trust As Final Ground Truth

- AI-generated literature-summary sites
- blog posts without official links
- secondary citation databases without paper landing pages
- tables copied from review slides without source traceability

## Extraction Checklist

For every candidate paper, try to extract:

1. full title
2. venue
3. year
4. status: `published`, `accepted`, `competition`, or `preprint`
5. task paradigm
6. cross-subject setting
7. method core idea
8. key result with metric and dataset
9. whether code or data is available
10. whether the result is directly comparable to other papers
