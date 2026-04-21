# Publication Figure Standards

Use this file before final export or when the user asks for journal-ready figures.

Standards are based on common guidance from Elsevier, PLOS, Springer Nature, Matplotlib, ColorBrewer, Okabe-Ito/CUD, and general scientific-figure design literature such as "Ten Simple Rules for Better Figures".

## File Format

- Prefer `PDF`, `SVG`, or `EPS` for plots, charts, diagrams, and line art.
- Export `PNG` only as a preview or when the target workflow requires raster images.
- Use `TIFF` for journal submission only when requested.
- For raster output, use 300-600 DPI for general color/halftone figures; use higher resolution only when the journal specifically requires line-art TIFF.
- Keep original data and plotting code with the figure so the graphic can be regenerated instead of upsampled.

## Size And Typography

- Decide final printed size before plotting.
- Use about 3.35 in for single-column figures and about 6.9 in for double-column figures unless the journal template differs.
- Keep final figure text readable: usually 7-9 pt for tick labels and 8-10 pt for axis labels in compact paper figures.
- Use consistent font family and sizes across all panels.
- Prefer Arial, Helvetica, DejaVu Sans, or journal-approved fonts; use CJK-capable fallbacks for Chinese labels.
- Do not include a large in-figure title when the manuscript caption already provides the title.

## Lines, Markers, And Panels

- Keep important plot lines near 1 pt or thicker at final size.
- Use markers only when they encode observations or help identify sparse series.
- Use panel labels such as `a`, `b`, `c` consistently, placed outside or at the upper-left of each panel.
- Align axes, labels, and panel spacing in multi-panel figures.
- Use shared axes only when scales are truly comparable.

## Color And Accessibility

- Use color to encode data, highlight, or guide attention; avoid color as decoration.
- Categorical palettes: prefer Okabe-Ito or other colorblind-safe palettes.
- Sequential data: prefer perceptually uniform colormaps such as `viridis` or `cividis`.
- Diverging data: use diverging palettes only with a meaningful center such as zero, baseline, or chance.
- Avoid rainbow/jet for ordered data.
- Do not encode meaning only by color; add direct labels, line styles, markers, hatches, or facets.
- Check grayscale readability for print and color-vision-deficiency robustness for review.

## Axes And Labels

- Label every axis with variable name and unit.
- Use concise tick labels; rotate only when unavoidable.
- Use zero baseline for magnitude bars; for deviation bars, show the reference line clearly.
- State transformations such as log scale, normalization, percent change, z-score, or min-max scaling.
- Keep grid lines light and only where they support value reading.
- Remove top/right spines unless they are needed for boxed scientific axes.

## Uncertainty And Statistics

- Always define error bars: SD, SE, CI, bootstrap interval, min-max, or IQR.
- For repeated experiments, show sample size or number of seeds where relevant.
- Prefer confidence intervals or raw data overlays when making inferential claims.
- Use significance brackets sparingly; report exact p-values or methods in caption/text.
- Do not hide non-significant or failed results if they affect the claim.

## Common Figure Types

- Bar charts: use for aggregated category magnitudes; add error bars or raw points when needed.
- Line charts: use for trends; show uncertainty bands for repeated runs or forecasts.
- Heatmaps: choose a colorbar with units; keep annotation readable or omit it.
- Scatter plots: manage overplotting with alpha, small points, hexbin, contours, or sampling.
- Radar charts: normalize metrics and keep metrics/series few.
- Maps: use rates for choropleths and counts for proportional symbols.

## Final Checklist

- [ ] The chart type matches the primary data relationship.
- [ ] Data transformations and aggregations are explicit.
- [ ] Axes, units, legend, and colorbar are labeled.
- [ ] Text is readable at final size.
- [ ] Colors remain interpretable for colorblind and grayscale readers.
- [ ] Error bars or uncertainty intervals are defined.
- [ ] No visual encoding misleads magnitude, area, or baseline perception.
- [ ] Export includes vector format plus a high-resolution raster preview if useful.
- [ ] Figure can be regenerated from source data and code.

## Source Links

- Matplotlib plot types: https://matplotlib.org/stable/plot_types/
- Matplotlib style and rcParams: https://matplotlib.org/stable/users/explain/customizing.html
- Matplotlib savefig: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
- Matplotlib colormaps: https://matplotlib.org/stable/users/explain/colors/colormaps.html
- Seaborn API: https://seaborn.pydata.org/api.html
- Altair gallery: https://altair-viz.github.io/gallery/index.html
- Plotly Python: https://plotly.com/python/
- Bokeh user guide: https://docs.bokeh.org/en/latest/docs/user_guide/basic.html
- pandas plotting: https://pandas.pydata.org/docs/dev/reference/api/pandas.DataFrame.plot.html
- ONS chart choice: https://service-manual.ons.gov.uk/data-visualisation/chart-types/choosing-a-chart-type
- Financial Times Visual Vocabulary: https://github.com/ft-interactive/visual-vocabulary
- Elsevier artwork overview: https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-overview
- PLOS figure guidance: https://journals.plos.org/digitalhealth/s/figures
- Ten Simple Rules for Better Figures: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833
- Springer Nature manuscript guidelines: https://www.springernature.com/gp/authors/publish-a-book/manuscript-guidelines
- ColorBrewer: https://colorbrewer2.org/
- Okabe-Ito/CUD color guidance: https://jfly.uni-koeln.de/color/
