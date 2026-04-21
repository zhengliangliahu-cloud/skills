"""Create common publication-ready plots from a CSV/TSV file."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sciplot_style import apply_clean_axes, get_palette, save_figure, set_paper_style


CHARTS = ("bar", "barh", "line", "scatter", "box", "violin", "hist", "kde", "heatmap", "radar")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV/TSV data file")
    parser.add_argument("--chart", required=True, choices=CHARTS, help="Chart type")
    parser.add_argument("--x", help="Column mapped to x/categories")
    parser.add_argument("--y", help="Column mapped to y/values")
    parser.add_argument("--hue", help="Grouping column; for heatmap, value column")
    parser.add_argument("--output", required=True, help="Output file path, e.g. fig.pdf")
    parser.add_argument("--width", default="single", help="single|one_half|double|full or inches")
    parser.add_argument("--height", type=float, help="Figure height in inches")
    parser.add_argument("--dpi", type=int, default=600, help="Raster export DPI")
    parser.add_argument("--palette", default="okabe_ito", help="Bundled palette name")
    parser.add_argument("--xlabel", help="Override x-axis label")
    parser.add_argument("--ylabel", help="Override y-axis label")
    parser.add_argument("--title", help="Optional title; usually omit for journal figures")
    return parser.parse_args()


def read_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    sep = "\t" if path.suffix.lower() in {".tsv", ".tab"} else ","
    return pd.read_csv(path, sep=sep)


def width_value(value: str) -> str | float:
    try:
        return float(value)
    except ValueError:
        return value


def require_columns(df: pd.DataFrame, *cols: str | None) -> None:
    missing = [col for col in cols if col and col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Available: {list(df.columns)}")


def hue_count(df: pd.DataFrame, hue: str | None) -> int:
    return int(df[hue].nunique()) if hue and hue in df.columns else 8


def label_axes(ax, args: argparse.Namespace) -> None:
    if args.chart == "barh":
        ax.set_xlabel(args.ylabel or args.y or "")
        ax.set_ylabel(args.xlabel or args.x or "")
        if args.title:
            ax.set_title(args.title)
        return

    if args.xlabel:
        ax.set_xlabel(args.xlabel)
    elif args.x:
        ax.set_xlabel(args.x)
    if args.ylabel:
        ax.set_ylabel(args.ylabel)
    elif args.y:
        ax.set_ylabel(args.y)
    if args.title:
        ax.set_title(args.title)


def make_standard_plot(df: pd.DataFrame, args: argparse.Namespace):
    width, height = set_paper_style(width_value(args.width), args.height, dpi=args.dpi)
    fig, ax = plt.subplots(figsize=(width, height))
    colors = get_palette(args.palette, hue_count(df, args.hue))

    if args.chart in {"bar", "barh", "line", "scatter", "box", "violin"}:
        require_columns(df, args.x, args.y, args.hue)

    if args.chart == "bar":
        sns.barplot(data=df, x=args.x, y=args.y, hue=args.hue, errorbar=None, palette=colors, ax=ax)
        apply_clean_axes(ax, grid="y")
    elif args.chart == "barh":
        sns.barplot(data=df, x=args.y, y=args.x, hue=args.hue, errorbar=None, palette=colors, ax=ax)
        apply_clean_axes(ax, grid="x")
    elif args.chart == "line":
        sns.lineplot(
            data=df,
            x=args.x,
            y=args.y,
            hue=args.hue,
            marker="o",
            errorbar=None,
            palette=colors,
            ax=ax,
        )
        apply_clean_axes(ax, grid="y")
    elif args.chart == "scatter":
        sns.scatterplot(data=df, x=args.x, y=args.y, hue=args.hue, palette=colors, ax=ax)
        apply_clean_axes(ax, grid="both")
    elif args.chart == "box":
        sns.boxplot(data=df, x=args.x, y=args.y, hue=args.hue, palette=colors, ax=ax)
        apply_clean_axes(ax, grid="y")
    elif args.chart == "violin":
        sns.violinplot(data=df, x=args.x, y=args.y, hue=args.hue, palette=colors, cut=0, inner="box", ax=ax)
        apply_clean_axes(ax, grid="y")
    elif args.chart == "hist":
        require_columns(df, args.x, args.y, args.hue)
        sns.histplot(data=df, x=args.x, y=args.y, hue=args.hue, palette=colors, ax=ax)
        apply_clean_axes(ax, grid="y")
    elif args.chart == "kde":
        require_columns(df, args.x, args.y, args.hue)
        sns.kdeplot(data=df, x=args.x, y=args.y, hue=args.hue, palette=colors, fill=args.y is None, ax=ax)
        apply_clean_axes(ax, grid="y")
    else:
        raise ValueError(f"Unsupported standard chart: {args.chart}")

    label_axes(ax, args)
    fig.tight_layout()
    return fig


def make_heatmap(df: pd.DataFrame, args: argparse.Namespace):
    width, height = set_paper_style(width_value(args.width), args.height, dpi=args.dpi)
    fig, ax = plt.subplots(figsize=(width, height))

    if args.x and args.y and args.hue:
        require_columns(df, args.x, args.y, args.hue)
        matrix = df.pivot_table(index=args.y, columns=args.x, values=args.hue, aggfunc="mean")
    elif args.x and args.y:
        require_columns(df, args.x, args.y)
        matrix = pd.crosstab(df[args.y], df[args.x])
    else:
        numeric = df.select_dtypes(include=[np.number])
        if numeric.empty:
            raise ValueError("Heatmap needs --x/--y columns or numeric columns for correlation.")
        matrix = numeric.corr()

    sns.heatmap(
        matrix,
        cmap="viridis",
        linewidths=0.25,
        linecolor="white",
        cbar_kws={"shrink": 0.85, "label": args.hue or "value"},
        ax=ax,
    )
    label_axes(ax, args)
    fig.tight_layout()
    return fig


def make_radar(df: pd.DataFrame, args: argparse.Namespace):
    require_columns(df, args.x, args.y, args.hue)
    width, height = set_paper_style(width_value(args.width), args.height, dpi=args.dpi)

    categories = list(pd.unique(df[args.x]))
    if len(categories) < 3:
        raise ValueError("Radar charts need at least three categories.")
    if len(categories) > 10:
        raise ValueError("Radar charts become hard to read with more than 10 categories.")

    if args.hue:
        table = df.pivot_table(index=args.hue, columns=args.x, values=args.y, aggfunc="mean")
    else:
        table = df.pivot_table(index=lambda _: "value", columns=args.x, values=args.y, aggfunc="mean")
    table = table.reindex(columns=categories)

    angles = np.linspace(0, 2 * math.pi, len(categories), endpoint=False).tolist()
    closed_angles = angles + angles[:1]
    colors = get_palette(args.palette, len(table))

    fig = plt.figure(figsize=(width, height))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(categories)

    max_value = float(np.nanmax(table.to_numpy()))
    ax.set_ylim(0, max_value * 1.08 if max_value > 0 else 1)
    ax.grid(True, linewidth=0.45, alpha=0.8)

    for color, (label, row) in zip(colors, table.iterrows()):
        values = row.astype(float).to_list()
        values = values + values[:1]
        ax.plot(closed_angles, values, color=color, linewidth=1.4, marker="o", label=str(label))
        ax.fill(closed_angles, values, color=color, alpha=0.12)

    if args.ylabel:
        ax.set_rlabel_position(90)
    if args.title:
        ax.set_title(args.title)
    if args.hue:
        ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1.18, 1.12))
    fig.tight_layout()
    return fig


def output_formats(path: str | Path) -> tuple[Path, list[str]]:
    output = Path(path)
    if not output.suffix:
        return output, ["pdf", "png"]
    fmt = output.suffix.lstrip(".").lower()
    if fmt == "png":
        return output.with_suffix(""), ["png", "pdf"]
    if fmt in {"pdf", "svg", "eps"}:
        return output.with_suffix(""), [fmt, "png"]
    return output.with_suffix(""), [fmt]


def main() -> None:
    args = parse_args()
    df = read_table(args.input)

    if args.chart == "heatmap":
        fig = make_heatmap(df, args)
    elif args.chart == "radar":
        fig = make_radar(df, args)
    else:
        fig = make_standard_plot(df, args)

    base, formats = output_formats(args.output)
    written = save_figure(fig, base, formats=formats, dpi=args.dpi, close=True)
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
