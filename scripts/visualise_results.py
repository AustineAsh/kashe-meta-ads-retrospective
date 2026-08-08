"""Generate deterministic descriptive SVG charts from the prepared dataset."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import statistics

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .campaign_data import PROJECT_ROOT, PUBLIC_CSV, link_click_rows, load_rows
from .io_utils import canonicalise_text_file

matplotlib.rcParams["svg.hashsalt"] = "kashe-meta-ads-retrospective"
matplotlib.rcParams["svg.fonttype"] = "none"


def clean_label(name: str, limit: int = 46) -> str:
    """Keep plot labels readable without depending on emoji/font availability."""
    label = re.sub(r"[^\x20-\x7E]", "", name)
    label = re.sub(r"\s+", " ", label).strip()
    return label if len(label) <= limit else label[: limit - 3] + "..."


def save_svg(fig: matplotlib.figure.Figure, path: Path) -> None:
    """Write stable SVG output without embedding a generation timestamp."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    canonicalise_text_file(path)


def cpc_distribution(link_rows_: list[dict[str, object]], output: Path) -> None:
    values = [float(row["cost_per_result_ngn"]) for row in link_rows_]
    minimum = min(values)
    maximum = max(values)
    # Log-spaced bins make the highly skewed positive CPC distribution visible
    # without removing the genuine high-cost rows.
    import math

    edges = [
        10 ** (math.log10(minimum) + i * (math.log10(maximum) - math.log10(minimum)) / 24)
        for i in range(25)
    ]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(values, bins=edges)
    ax.set_xscale("log")
    ax.axvline(
        statistics.median(values),
        linestyle="--",
        label="Median campaign-row CPC",
    )
    ax.set_xlabel("Campaign-row cost per link click (NGN, logarithmic scale)")
    ax.set_ylabel("Number of campaign rows")
    ax.set_title("Distribution of cost per link click")
    ax.legend()
    save_svg(fig, output)


def spend_vs_clicks(link_rows_: list[dict[str, object]], output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    x = [float(row["amount_spent_ngn"]) for row in link_rows_]
    y = [float(row["results"]) for row in link_rows_]
    ax.scatter(x, y, alpha=0.65)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Spend (NGN, logarithmic scale)")
    ax.set_ylabel("Recorded link clicks (logarithmic scale)")
    ax.set_title("Spend and link-click outcomes by campaign row")

    for row in link_rows_:
        name = str(row["campaign_name"])
        if name in {"Bunda Youtube – official", "Bunda Youtube"} or "Pressure.' Now" in name:
            ax.annotate(
                clean_label(name, 28),
                (float(row["amount_spent_ngn"]), float(row["results"])),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
            )
    save_svg(fig, output)


def top_link_rows(link_rows_: list[dict[str, object]], output: Path) -> None:
    ranked = sorted(link_rows_, key=lambda row: float(row["results"]), reverse=True)[:10]
    labels = [clean_label(str(row["campaign_name"])) for row in ranked]
    values = [float(row["results"]) for row in ranked]
    positions = list(range(len(ranked)))

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(positions, values)
    ax.set_yticks(positions, labels=labels)
    ax.invert_yaxis()
    ax.set_xlabel("Recorded link clicks")
    ax.set_title("Top 10 campaign rows by recorded link clicks")
    ax.margins(x=0.08)
    ax.bar_label(bars, fmt="{:,.0f}", padding=3, fontsize=8)
    save_svg(fig, output)


def sensitivity_charts(summary: dict[str, object], output_dir: Path) -> None:
    scenarios = [
        ("All link rows", summary["link_click_analysis"]),
        ("Excluding Bunda", summary["link_clicks_excluding_bunda"]),
        (
            "Excluding Bunda + Pressure",
            summary["link_clicks_excluding_bunda_and_pressure"],
        ),
    ]
    labels = [item[0] for item in scenarios]
    cpc = [float(item[1]["weighted_cpc_ngn"]) for item in scenarios]
    ctr = [float(item[1]["derived_link_ctr_pct"]) for item in scenarios]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, cpc)
    ax.set_ylabel("Weighted CPC (NGN)")
    ax.set_title("Sensitivity of weighted CPC to the largest response outliers")
    ax.tick_params(axis="x", labelrotation=15)
    ax.bar_label(bars, fmt="%.2f", padding=3)
    save_svg(fig, output_dir / "04_cpc_sensitivity.svg")

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, ctr)
    ax.set_ylabel("Derived link CTR (%)")
    ax.set_title("Sensitivity of aggregate link CTR to the largest response outliers")
    ax.tick_params(axis="x", labelrotation=15)
    ax.bar_label(bars, fmt="%.2f%%", padding=3)
    save_svg(fig, output_dir / "05_ctr_sensitivity.svg")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate descriptive campaign charts.")
    parser.add_argument("--input", type=Path, default=PUBLIC_CSV)
    parser.add_argument(
        "--summary",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "summary.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "assets",
    )
    args = parser.parse_args()

    rows = load_rows(args.input)
    links = link_click_rows(rows)
    summary = json.loads(args.summary.read_text(encoding="utf-8"))

    cpc_distribution(links, args.output_dir / "01_link_click_cost_distribution.svg")
    spend_vs_clicks(links, args.output_dir / "02_spend_vs_link_clicks.svg")
    top_link_rows(links, args.output_dir / "03_top_link_click_campaigns.svg")
    sensitivity_charts(summary, args.output_dir)
    print(f"Wrote 5 SVG charts to {args.output_dir}")


if __name__ == "__main__":
    main()
