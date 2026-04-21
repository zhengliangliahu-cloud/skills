# Chart Selection Guide

Use this file to decide what to draw and what to avoid. Prefer a simple, familiar chart unless a more complex chart is clearly needed.

## Decision Rules

1. State the message first: comparison, trend, distribution, relationship, deviation, composition, spatial pattern, flow, hierarchy, or diagnostic.
2. Check the data shape: categorical, numeric, time, ordered category, matrix, geographic, network, or nested hierarchy.
3. Use one primary relationship per figure. If two relationships compete, use two simple panels instead of one overloaded chart.
4. Preserve honest perception: shared baselines for magnitude comparisons, consistent scales across facets, clear units, visible sample size or uncertainty.
5. Avoid chart types the reader must decode slowly unless the paper's field expects them.

## Common Choices

| Goal | Prefer | Use with caution | Avoid |
|---|---|---|---|
| Compare category values | Bar, horizontal bar, dot/lollipop | Grouped bar when groups are few | 3D bars, truncated bar axes |
| Rank categories | Ordered bar or dot | Bump chart for ranks over time | Alphabetical category order when value rank matters |
| Show time trend | Line for stock/continuous time | Column for interval flow; area for volume | Connected points for unordered categories |
| Show distribution | Histogram, ECDF, box, violin, strip | KDE if sample size and smoothing are appropriate | Mean-only bar chart for distributional claims |
| Show relationship | Scatter, regression, hexbin | Bubble if area encoding is explained | Pie, radar, or dual-axis as substitutes for correlation |
| Show deviation | Diverging bar, residual plot, forest plot | Waterfall for sequential contributions | Unsigned bars when direction matters |
| Show part-to-whole | 100% stacked bar, treemap | Pie/donut only for one whole and few categories | Many-slice pie charts |
| Show matrix | Heatmap, clustered heatmap | Annotated heatmap if values fit | Rainbow colormap without reason |
| Show many metrics | Small multiples, heatmap | Radar for few normalized metrics | Radar with many series or incompatible scales |
| Show flow | Sankey/alluvial | Chord for expert audiences | Network hairballs for volume comparison |

## Strengths And Weaknesses

### Bar, Column, And Horizontal Bar

- Use for discrete categories and magnitude comparison.
- Start quantitative bars at zero unless showing deviation with a clearly marked baseline.
- Prefer horizontal bars when labels are long or categories exceed 6-8.
- Grouped bars work for small subgroup counts; beyond that, use facets or dot plots.
- Stacked bars show totals well but make middle segments hard to compare.

### Line And Area

- Use line charts for ordered x-values and trends.
- Use markers only when the number of points is small or individual observations matter.
- Avoid connecting nominal categories with lines.
- Use area charts for cumulative volume or part-to-whole over time; they are weaker for precise series comparison.
- Avoid dual axes unless units are different, the relationship is explicitly explained, and axis colors/labels prevent confusion.

### Scatter, Bubble, And Density

- Use scatter plots for numeric relationships, correlations, clusters, and outliers.
- Add regression/LOESS only when a trend model is meaningful.
- Use alpha, small points, hexbin, or 2D histograms for dense data.
- Bubble area must encode value, not radius; add a size legend.
- Do not infer causality from a scatter plot without study design support.

### Distribution Plots

- Use histograms when bin counts are interpretable; show bin width or choose bins deliberately.
- Use ECDF for robust distribution comparison without arbitrary bins.
- Use box plots for compact group summaries; add raw points for small samples.
- Use violin plots only when distribution shape matters and sample size is sufficient.
- Avoid bar charts with only mean +/- error when the distribution is the claim.

### Heatmaps

- Use heatmaps for matrices, correlations, confusion matrices, grids, and model-performance tables.
- Use sequential colormaps for ordered non-negative values.
- Use diverging colormaps only when a meaningful center exists, such as zero or chance level.
- Keep cell labels only when they remain readable; otherwise move exact values to a table.
- Clustered heatmaps are exploratory unless clustering method is stated.

### Radar Charts

- Use only for 3-8 metrics, 1-3 entities, same direction, comparable scales, and normalized values.
- State normalization; otherwise readers may compare incompatible ranges.
- Prefer small multiples or heatmaps for many methods or many metrics.
- Radar charts are poor for precise quantitative comparison because angles and areas distort perception.

### Pie, Donut, Treemap, And Sunburst

- Pie/donut charts are acceptable only for one whole, few slices, and rough comparison.
- Use ordered labels and direct percentages when using pie/donut.
- Prefer 100% stacked bars when comparing composition across groups.
- Treemaps handle many hierarchical parts but make similar areas hard to compare.
- Sunbursts communicate hierarchy but are hard to read for exact values.

### Maps

- Use choropleths for rates/ratios, not raw counts.
- Use proportional symbols for raw counts at locations.
- Include projection, scale, region boundary context, and missing-data encoding.
- Do not use maps when spatial pattern is irrelevant; a ranked bar chart may be clearer.

### Flow And Network

- Use Sankey/alluvial diagrams for volume transfer across stages.
- Sort nodes and limit categories to reduce crossings.
- Use network graphs for topology, not exact magnitude comparison.
- For dense networks, aggregate, filter, or use adjacency matrices.

## Misleading Patterns To Reject

- 3D effects for non-3D data.
- Decorative gradients, shadows, heavy backgrounds, or pictorial elements that do not encode data.
- Rainbow/jet colormaps for ordered data.
- Truncated y-axis on bars without explicit deviation framing.
- Unlabeled error bars or ambiguous "standard error vs standard deviation vs confidence interval".
- Too many colors with a separate legend far from the data.
- Mixing raw values and percentages on the same axis.
- Sorting categories inconsistently across related panels.
