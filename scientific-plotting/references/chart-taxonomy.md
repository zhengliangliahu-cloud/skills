# Chart Taxonomy

Use this file when the task is broad ("make a chart", "choose a graph type", "visualize results"). Start from the data relationship, then choose the simplest chart that exposes that relationship.

Sources consulted include Matplotlib plot types, Seaborn API, Altair gallery and marks, Plotly Python docs, Bokeh user guide, pandas plotting docs, ONS chart-choice guidance, and the Financial Times Visual Vocabulary.

## Comparison And Magnitude

| Chart type | Best for |
|---|---|
| Column/bar chart | Compare category magnitudes from a shared zero baseline. |
| Horizontal bar chart | Long labels, many categories, ranked categories. |
| Grouped bar chart | Compare a small number of subgroups inside each category. |
| Stacked bar chart | Show total plus rough component contribution. |
| 100% stacked bar | Compare proportions across categories. |
| Lollipop/dot plot | Compare categories with less ink than bars. |
| Dumbbell/connected dot | Compare before/after or two related values per item. |
| Bullet chart | Compare actual value against target and qualitative bands. |
| Population pyramid | Compare mirrored distributions, usually age by sex/group. |
| Pictogram/isotype | Communicate counts to broad audiences; rarely primary for papers. |

## Ranking

| Chart type | Best for |
|---|---|
| Ordered bar/dot chart | Rank categories by value. |
| Bump chart | Show rank changes over time for limited series. |
| Slope chart | Compare two time points or two conditions. |
| Pareto chart | Rank contributors and cumulative share. |
| Heat table | Rank across two categorical dimensions. |

## Time And Ordered Change

| Chart type | Best for |
|---|---|
| Line chart | Stock data, continuous time, trends, multiple series. |
| Column chart | Flow data by interval, such as monthly counts. |
| Area chart | Cumulative or volume over time. |
| Stacked area/streamgraph | Part-to-whole over time when precision is secondary. |
| Step chart | Piecewise-constant values or policy/state changes. |
| Slope graph | Net change between two points. |
| Calendar heatmap | Daily/weekly periodic intensity. |
| Gantt/timeline | Durations, schedules, phases, events. |
| Fan chart/ribbon chart | Forecast uncertainty over time. |
| Control chart | Process metric over time with limits. |

## Distribution

| Chart type | Best for |
|---|---|
| Histogram | Frequency distribution for one numeric variable. |
| KDE/density plot | Smooth distribution shape, enough data, exploratory comparison. |
| ECDF | Full distribution comparison without bin choices. |
| Box plot | Median, IQR, outliers across groups. |
| Violin plot | Distribution shape plus summary across groups. |
| Boxen plot | Richer quantile detail for larger samples. |
| Strip/swarm/beeswarm plot | Raw observations for small to moderate sample sizes. |
| Ridgeline plot | Many distributions along a categorical/order axis. |
| Q-Q plot | Distributional assumption or model residual check. |
| Raincloud plot | Combined raw points, density, and summary. |

## Relationship And Correlation

| Chart type | Best for |
|---|---|
| Scatter plot | Relationship between two numeric variables. |
| Bubble plot | Scatter with a third magnitude variable encoded by area. |
| Regression/LOESS plot | Relationship plus fitted trend. |
| Hexbin/2D histogram | Dense scatter where overplotting hides density. |
| Contour/density contour | Continuous bivariate density. |
| Pair plot/scatter matrix | Many numeric variables during exploration. |
| Correlogram/correlation heatmap | Pairwise association matrix. |
| Connected scatter | Trajectory through two-variable space over time. |

## Deviation

| Chart type | Best for |
|---|---|
| Diverging bar chart | Positive/negative difference from baseline. |
| Waterfall chart | Sequential contributions to a net change. |
| Residual plot | Model error pattern and heteroscedasticity. |
| Bland-Altman plot | Agreement between two measurement methods. |
| Volcano plot | Effect size versus significance in omics-style results. |
| Forest plot | Effect sizes and confidence intervals across studies/subgroups. |

## Part-To-Whole And Composition

| Chart type | Best for |
|---|---|
| 100% stacked bar | Compare composition across groups. |
| Stacked area | Composition changes over ordered time. |
| Pie/donut chart | One whole with very few categories and rough shares only. |
| Treemap | Hierarchical part-to-whole with many categories. |
| Sunburst/icicle | Hierarchical composition across levels. |
| Mosaic/Marimekko | Two categorical dimensions and proportions. |
| Waffle/grid plot | Simple share counts; public-facing communication. |

## Spatial

| Chart type | Best for |
|---|---|
| Choropleth map | Rates/ratios over geographic regions. |
| Proportional symbol map | Counts or magnitudes at locations. |
| Dot-density map | Spatial distribution of many units. |
| Flow map | Movement between places. |
| Cartogram | Geography distorted by value; specialized use. |
| Contour/raster map | Continuous spatial fields. |

## Flow, Network, And Hierarchy

| Chart type | Best for |
|---|---|
| Sankey/alluvial | Flow volumes between stages/categories. |
| Chord diagram | Many-to-many flows; use only with careful labeling. |
| Network graph | Node-link relationships. |
| Tree/dendrogram | Hierarchy or clustering. |
| Arc diagram | Ordered network relations with less crossing than node-link. |
| Parallel sets | Categorical paths across stages. |

## Multivariate And High-Dimensional

| Chart type | Best for |
|---|---|
| Heatmap | Matrix values, model performance grids, correlations. |
| Clustered heatmap | Matrix plus row/column clustering. |
| Radar/spider chart | Few normalized metrics for few entities. |
| Parallel coordinates | Many numeric metrics, usually exploratory. |
| Ternary plot | Three-part composition constrained to sum to one. |
| Small multiples/facets | Same chart repeated across groups for comparison. |
| PCA/UMAP/t-SNE scatter | Low-dimensional embedding of high-dimensional data. |

## Scientific Diagnostics

| Chart type | Best for |
|---|---|
| Error-bar point plot | Mean/estimate with uncertainty interval. |
| Calibration curve | Predicted probability versus observed frequency. |
| ROC/PR curve | Classifier discrimination. |
| Confusion matrix | Classification errors by class. |
| Learning curve | Model metric versus data size or epoch. |
| Loss curve | Training dynamics over epochs/steps. |
| Ablation bar/dot chart | Component contribution to performance. |
| Critical difference diagram | Multiple-method statistical comparison. |
| Kaplan-Meier curve | Survival/time-to-event analysis. |

## Text And Tables

| Chart type | Best for |
|---|---|
| Table | Exact values that readers must look up. |
| Heat table | Exact values plus visual scanning. |
| Word cloud | Rough text frequency only; avoid for serious inference. |
| UpSet plot | Set intersections when Venn diagrams fail. |
