"""Reusable helpers for publication-ready scientific plots.

The module intentionally depends only on Matplotlib and the local JSON/style
assets so it can be imported in most Python data-analysis environments.
"""

from __future__ import annotations

import json
from itertools import cycle, islice
from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt


WIDTHS_INCH = {
    "single": 3.35,
    "one_half": 5.2,
    "double": 6.9,
    "full": 7.2,
}


def skill_root() -> Path:
    """Return the root folder of this skill."""

    return Path(__file__).resolve().parents[1]


def _asset_path(*parts: str) -> Path:
    return skill_root().joinpath("assets", *parts)


def load_palettes() -> dict:
    """Load bundled color, marker, line, and hatch definitions."""

    with _asset_path("palettes.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def set_paper_style(
    width: str | float = "single",
    height: float | None = None,
    dpi: int = 600,
    font_family: str | None = None,
) -> tuple[float, float]:
    """Apply the bundled Matplotlib style and return the figure size.

    Parameters
    ----------
    width:
        Named width (`single`, `one_half`, `double`, `full`) or numeric inches.
    height:
        Figure height in inches. Defaults to a compact golden-ratio-like height.
    dpi:
        Export DPI for raster formats.
    font_family:
        Optional first-choice font family. The style keeps common fallbacks.
    """

    style_path = _asset_path("mplstyles", "research-paper.mplstyle")
    plt.style.use(str(style_path))

    if isinstance(width, str):
        width_in = WIDTHS_INCH.get(width, WIDTHS_INCH["single"])
    else:
        width_in = float(width)
    height_in = float(height) if height is not None else width_in * 0.62

    mpl.rcParams["figure.figsize"] = (width_in, height_in)
    mpl.rcParams["savefig.dpi"] = dpi
    mpl.rcParams["figure.dpi"] = min(dpi, 150)
    if font_family:
        current = list(mpl.rcParams.get("font.sans-serif", []))
        mpl.rcParams["font.sans-serif"] = [font_family] + [
            font for font in current if font != font_family
        ]
        mpl.rcParams["font.family"] = "sans-serif"
    return width_in, height_in


def _find_palette(name: str):
    palettes = load_palettes()
    for section in ("categorical", "sequential", "diverging"):
        values = palettes.get(section, {})
        if name in values:
            return section, values[name]
    raise KeyError(f"Unknown palette '{name}'. Available groups: {list(palettes)}")


def get_palette(name: str = "okabe_ito", n: int | None = None) -> list[str]:
    """Return a list of colors from a bundled or Matplotlib palette."""

    section, spec = _find_palette(name)
    if isinstance(spec, str) and spec.startswith("matplotlib:"):
        cmap_name = spec.split(":", 1)[1]
        count = n or 8
        cmap = mpl.colormaps[cmap_name]
        if count == 1:
            return [mpl.colors.to_hex(cmap(0.6))]
        return [mpl.colors.to_hex(cmap(i / (count - 1))) for i in range(count)]

    colors = list(spec)
    if n is None or n <= len(colors):
        return colors if n is None else colors[:n]

    if section == "categorical":
        return list(islice(cycle(colors), n))

    cmap = mpl.colors.LinearSegmentedColormap.from_list(name, colors)
    return [mpl.colors.to_hex(cmap(i / (n - 1))) for i in range(n)]


def get_style_sequence(kind: str = "line_styles", n: int | None = None) -> list[str]:
    """Return bundled line styles, markers, or hatches."""

    values = list(load_palettes().get(kind, []))
    if n is None or n <= len(values):
        return values if n is None else values[:n]
    return list(islice(cycle(values), n))


def apply_clean_axes(
    ax,
    grid: str | None = "y",
    legend: bool = True,
    despine: bool = True,
):
    """Apply light journal-style axis cleanup to an Axes object."""

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    if grid in {"x", "y", "both"}:
        ax.grid(True, axis=grid if grid != "both" else "both")
        ax.set_axisbelow(True)
    else:
        ax.grid(False)

    ax.tick_params(axis="both", which="both", direction="out")

    if legend:
        handles, labels = ax.get_legend_handles_labels()
        labels = [label for label in labels if label and not label.startswith("_")]
        if labels:
            ax.legend(frameon=False, handlelength=1.6, labelspacing=0.35)
    return ax


def add_panel_label(
    ax,
    label: str,
    x: float = -0.12,
    y: float = 1.05,
    fontsize: float = 9,
    weight: str = "bold",
):
    """Add a journal-style panel label such as 'a' or 'A'."""

    return ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=fontsize,
        fontweight=weight,
    )


def save_figure(
    fig,
    output: str | Path,
    formats: Iterable[str] | None = None,
    dpi: int = 600,
    transparent: bool = False,
    close: bool = False,
) -> list[Path]:
    """Save a figure with tight bounds and return written paths."""

    output_path = Path(output)
    if formats is None:
        if output_path.suffix:
            formats = [output_path.suffix.lstrip(".")]
            base = output_path.with_suffix("")
        else:
            formats = ["pdf", "png"]
            base = output_path
    else:
        base = output_path.with_suffix("") if output_path.suffix else output_path

    base.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        path = base.with_suffix(f".{fmt}")
        fig.savefig(
            path,
            format=fmt,
            dpi=dpi if fmt in {"png", "tif", "tiff", "jpg", "jpeg"} else None,
            bbox_inches="tight",
            pad_inches=0.03,
            transparent=transparent,
        )
        written.append(path)

    if close:
        plt.close(fig)
    return written
