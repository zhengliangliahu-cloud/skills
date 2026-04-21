# Python Plotting Tools

Choose the smallest tool that can produce the required figure quality and file format.

## Default Stack

| Tool | Use for | Strengths | Limits |
|---|---|---|---|
| Matplotlib | Final static scientific figures | Full control, vector export, journal layouts, ecosystem base | Verbose for complex statistical defaults |
| Seaborn | Statistical plots from tidy DataFrames | Good defaults for distributions, categories, regression, facets | Still needs Matplotlib polishing |
| pandas.plot | Quick DataFrame checks | Fast exploratory plots, minimal code | Not enough control for final paper figures |
| NumPy/SciPy/statsmodels | Aggregation, uncertainty, regression, diagnostics | Correct statistics before plotting | Not plotting libraries by themselves |

Use Matplotlib for final layout and export even when Seaborn creates the initial Axes.

## Interactive And Declarative Tools

| Tool | Use for | Strengths | Limits |
|---|---|---|---|
| Plotly | Interactive exploration, HTML sharing, dashboards | Tooltips, zoom, many chart types, 3D/ternary/Sankey | Static journal export may need extra dependencies |
| Altair | Declarative grammar, clean quick charts, interactive notebooks | Compact grammar, transformations, linked views | Large data handling and static export need setup |
| Bokeh | Browser-based interactive apps | Linked interactions, widgets, server apps | More setup for static paper export |

For papers, use interactive tools for exploration unless the venue accepts interactive supplements.

## Specialized Libraries

| Need | Preferred tools |
|---|---|
| Geographic maps | geopandas, cartopy, contextily, pyproj |
| Networks | networkx, graphviz, pygraphviz/pydot |
| Sankey/alluvial | plotly, matplotlib.sankey for simple cases, holoviews for complex flows |
| Statistical models | scipy, statsmodels, scikit-learn metrics |
| Survival curves | lifelines, scikit-survival |
| Omics-style plots | bioinfokit or custom Matplotlib/Seaborn |
| Color maps | Matplotlib colormaps, colorcet if installed, ColorBrewer definitions |

## Tool Selection Rules

1. Use `matplotlib` + `seaborn` for final manuscript figures.
2. Use `plot_from_csv.py` when the user needs a quick standard chart from tidy CSV data.
3. Use direct Matplotlib code for multi-panel figures, custom annotations, journal sizing, or unusual axes.
4. Use Seaborn for `boxplot`, `violinplot`, `stripplot`, `swarmplot`, `histplot`, `kdeplot`, `ecdfplot`, `heatmap`, `regplot`, and faceted statistical plots.
5. Use Plotly/Altair/Bokeh only when interactivity is required or clearly useful for data exploration.
6. Do not add new dependencies unless the existing stack cannot reasonably make the chart.

## Data Preparation Pattern

Prefer tidy data:

```text
method, dataset, metric, value, seed
A, CIFAR10, accuracy, 0.91, 1
B, CIFAR10, accuracy, 0.93, 1
```

Then aggregate explicitly:

```python
summary = (
    df.groupby(["method", "dataset"], as_index=False)
      .agg(mean=("value", "mean"), sd=("value", "std"), n=("value", "size"))
)
summary["se"] = summary["sd"] / summary["n"].pow(0.5)
```

For heatmaps and matrices, pivot only after checking duplicates:

```python
matrix = df.pivot_table(index="method", columns="dataset", values="score", aggfunc="mean")
```

## Export Pattern

Use vector for line art:

```python
fig.savefig("figure.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig("figure.png", dpi=600, bbox_inches="tight", pad_inches=0.03)
```

Set embedded text-friendly font types for Illustrator/Inkscape editing:

```python
import matplotlib as mpl
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["svg.fonttype"] = "none"
```
