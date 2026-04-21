---
name: scientific-plotting
description: Create publication-ready scientific figures with Python. Use when Codex needs to choose an appropriate chart type or generate, polish, debug, or export research-paper-quality plots including bar/column charts, line charts, horizontal bar charts, scatter plots, box plots, violin plots, histograms, KDE/ECDF plots, heatmaps, radar charts, error-bar charts, area/stacked charts, maps, Sankey/alluvial diagrams, network graphs, multi-panel figures, or journal-ready Matplotlib/Seaborn/Plotly/Altair/Bokeh visualizations.
---
# Scientific Plotting

## Core Workflow

1. 先写一个简短制图计划：数据关系、图表类型、编码方式、输出尺寸、目标格式和检查项。
2. 检查计划是否正确、完整、足够严格；若图表选择不确定，读取 `references/chart-selection-guide.md`。
3. 清洗并确认数据：列名、单位、样本量、缺失值、分组顺序、是否已汇总、误差线含义。
4. 优先用 `matplotlib` + `seaborn` 生成静态论文图；交互探索再选 `plotly`、`altair` 或 `bokeh`。
5. 使用 `scripts/sciplot_style.py` 的样式、调色板和保存函数，或调用 `scripts/plot_from_csv.py` 快速从 CSV 出图。
6. 输出前按 `references/publication-figure-standards.md` 检查：可读性、色盲友好、灰度可读、尺寸、DPI、矢量格式、图例、坐标轴、误导风险。

## Reference Loading

- 图表类型总览：读 `references/chart-taxonomy.md`。
- 选图、优缺点、误用警告：读 `references/chart-selection-guide.md`。
- Python 工具选型：读 `references/python-plotting-tools.md`。
- 论文插图规范和投稿检查：读 `references/publication-figure-standards.md`。

## Default Plotting Standards

- 静态论文图默认导出 `PDF` 或 `SVG`，同时保留 `PNG` 预览；PNG 默认 600 DPI。
- 单栏图宽约 3.35 in，双栏图宽约 6.9 in；多面板图先按投稿模板决定最终尺寸。
- 优先使用直接标签、短图例、明确单位、少量色彩、浅色网格、无多余边框。
- 分类配色优先 Okabe-Ito；连续热图优先 `viridis` 或 `cividis`；有零点/基线偏差时用发散色板。
- 不只依赖颜色；用线型、marker、hatch、直接标签或分面增强可读性。
- 避免 3D 柱图、装饰性背景、默认彩虹色、无基线柱图、无解释双轴图和过度拥挤雷达图。

## Reusable Scripts

Quick CSV plotting:

```bash
python scripts/plot_from_csv.py --input data.csv --chart line --x epoch --y accuracy --hue method --output fig.pdf
```

Reusable style helpers:

```python
from scripts.sciplot_style import set_paper_style, get_palette, apply_clean_axes, save_figure

set_paper_style(width="single")
colors = get_palette("okabe_ito", 4)
```

## Output Contract

When creating or revising a figure, return:

1. 选图理由：说明数据关系和为什么不用相近但更弱的图。
2. 生成或修改的文件路径。
3. 关键设计参数：尺寸、格式、DPI、字体、调色板、误差线含义。
4. 验证结果：至少说明是否检查了可读性、色盲/灰度、轴标签、图例遮挡和导出格式。
