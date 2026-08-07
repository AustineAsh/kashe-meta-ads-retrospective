"""Reproduce descriptive metrics and charts for the historical Meta Ads export.

Exploratory/descriptive only. This script does not estimate causal creative effects.
"""
from pathlib import Path
import csv
import json
import re
import statistics

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "meta_campaign_export_sanitized.csv"
OUT = ROOT / "analysis" / "summary.json"
ASSETS = ROOT / "assets"

NUMERIC = {"results", "reach", "impressions", "cost_per_result_ngn", "amount_spent_ngn"}


def read_rows():
    rows = []
    with DATA.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            for key in NUMERIC:
                value = row.get(key, "")
                row[key] = float(value) if value not in ("", None) else None
            row["campaign_row_id"] = int(row["campaign_row_id"])
            rows.append(row)
    return rows


def summarize(rows):
    spend = sum(r["amount_spent_ngn"] or 0 for r in rows)
    impressions = sum(r["impressions"] or 0 for r in rows)
    reach = sum(r["reach"] or 0 for r in rows)
    results = sum(r["results"] or 0 for r in rows if isinstance(r["results"], (int, float)))
    return {
        "rows": len(rows),
        "spend_ngn": spend,
        "impressions": int(impressions),
        "sum_campaign_reach_not_unique": int(reach),
        "results": results,
        "weighted_cost_per_result_ngn": spend / results if results else None,
        "derived_result_rate_pct": results / impressions * 100 if impressions else None,
        "derived_cpm_ngn": spend / impressions * 1000 if impressions else None,
        "impressions_per_summed_reach": impressions / reach if reach else None,
    }


def clean_label(name, limit=45):
    name = re.sub(r"[^\x20-\x7E]", "", name)
    return name if len(name) <= limit else name[: limit - 3] + "..."


def create_charts(link):
    ASSETS.mkdir(exist_ok=True)

    cpc = [r["cost_per_result_ngn"] for r in link]
    plt.figure(figsize=(8, 5))
    plt.hist(cpc, bins=25)
    plt.xlabel("Campaign cost per link click (NGN)")
    plt.ylabel("Number of campaign rows")
    plt.title("Distribution of cost per link click")
    plt.tight_layout()
    plt.savefig(ASSETS / "01_link_click_cost_distribution.svg")
    plt.close()

    xs = [r["amount_spent_ngn"] for r in link if r["amount_spent_ngn"] and r["results"]]
    ys = [r["results"] for r in link if r["amount_spent_ngn"] and r["results"]]
    plt.figure(figsize=(8, 5.5))
    plt.scatter(xs, ys, alpha=0.65)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Spend (NGN, log scale)")
    plt.ylabel("Link clicks (log scale)")
    plt.title("Spend and link-click outcomes by campaign row")
    plt.tight_layout()
    plt.savefig(ASSETS / "02_spend_vs_link_clicks.svg")
    plt.close()

    ranked = sorted(link, key=lambda r: r["results"] or 0, reverse=True)[:10]
    labels = [clean_label(r["campaign_name"]) for r in ranked]
    values = [r["results"] for r in ranked]
    positions = list(range(len(ranked)))
    plt.figure(figsize=(9, 6))
    plt.barh(positions, values)
    plt.yticks(positions, labels)
    plt.gca().invert_yaxis()
    plt.xlabel("Link clicks")
    plt.title("Top 10 campaign rows by recorded link clicks")
    plt.tight_layout()
    plt.savefig(ASSETS / "03_top_link_click_campaigns.svg")
    plt.close()


def main():
    rows = read_rows()
    clean = [r for r in rows if not r["data_quality_flag"]]
    ambiguous = [r for r in rows if r["data_quality_flag"]]

    # Arithmetic validation: every recognized row should satisfy
    # exported cost per result ≈ spend / results.
    reconciled = 0
    max_abs_diff = 0.0
    for r in clean:
        if r["results"] and r["cost_per_result_ngn"] is not None:
            calculated = (r["amount_spent_ngn"] or 0) / r["results"]
            difference = abs(calculated - r["cost_per_result_ngn"])
            max_abs_diff = max(max_abs_diff, difference)
            if difference < 1e-6:
                reconciled += 1

    by_type = {}
    for result_type in sorted({r["result_type"] for r in clean}):
        by_type[result_type] = summarize([r for r in clean if r["result_type"] == result_type])

    link = [r for r in clean if r["result_type"] == "Link clicks"]
    link_summary = summarize(link)
    for r in link:
        r["derived_ctr_pct"] = r["results"] / r["impressions"] * 100 if r["impressions"] else None
        r["derived_frequency"] = r["impressions"] / r["reach"] if r["reach"] else None
        r["derived_cpm_ngn"] = r["amount_spent_ngn"] / r["impressions"] * 1000 if r["impressions"] else None

    cpc = [r["cost_per_result_ngn"] for r in link]
    ctr = [r["derived_ctr_pct"] for r in link]
    frequency = [r["derived_frequency"] for r in link]
    cpm = [r["derived_cpm_ngn"] for r in link]
    quartiles = statistics.quantiles(cpc, n=4, method="exclusive")
    link_summary.update({
        "derived_link_ctr_pct": link_summary["derived_result_rate_pct"],
        "weighted_cpc_ngn": link_summary["weighted_cost_per_result_ngn"],
        "median_campaign_cpc_ngn": statistics.median(cpc),
        "sample_q1_campaign_cpc_ngn": quartiles[0],
        "sample_q3_campaign_cpc_ngn": quartiles[2],
        "min_campaign_cpc_ngn": min(cpc),
        "max_campaign_cpc_ngn": max(cpc),
        "median_campaign_ctr_pct": statistics.median(ctr),
        "median_campaign_cpm_ngn": statistics.median(cpm),
        "median_campaign_frequency": statistics.median(frequency),
    })

    bunda = [r for r in link if r["campaign_name"] in ("Bunda Youtube – official", "Bunda Youtube")]
    bunda_summary = summarize(bunda)
    total_export_spend = sum(r["amount_spent_ngn"] or 0 for r in rows)
    bunda_summary.update({
        "derived_link_ctr_pct": bunda_summary["derived_result_rate_pct"],
        "weighted_cpc_ngn": bunda_summary["weighted_cost_per_result_ngn"],
        "share_of_link_clicks_pct": bunda_summary["results"] / link_summary["results"] * 100,
        "share_of_link_spend_pct": bunda_summary["spend_ngn"] / link_summary["spend_ngn"] * 100,
        "share_of_total_export_spend_pct": bunda_summary["spend_ngn"] / total_export_spend * 100,
        "share_of_link_impressions_pct": bunda_summary["impressions"] / link_summary["impressions"] * 100,
    })

    non_bunda = [r for r in link if r not in bunda]
    non_bunda_summary = summarize(non_bunda)
    non_bunda_summary.update({
        "derived_link_ctr_pct": non_bunda_summary["derived_result_rate_pct"],
        "weighted_cpc_ngn": non_bunda_summary["weighted_cost_per_result_ngn"],
    })

    pressure = [r for r in link if "Feel the beats, feel the 'Pressure.' Now" in r["campaign_name"]]
    remaining = [r for r in non_bunda if r not in pressure]
    remaining_summary = summarize(remaining)
    remaining_summary.update({
        "derived_link_ctr_pct": remaining_summary["derived_result_rate_pct"],
        "weighted_cpc_ngn": remaining_summary["weighted_cost_per_result_ngn"],
    })

    ranked = sorted(link, key=lambda r: r["results"], reverse=True)
    top3 = ranked[:3]
    top3_summary = summarize(top3)
    top3_summary.update({
        "share_of_link_clicks_pct": top3_summary["results"] / link_summary["results"] * 100,
        "share_of_link_spend_pct": top3_summary["spend_ngn"] / link_summary["spend_ngn"] * 100,
        "share_of_link_impressions_pct": top3_summary["impressions"] / link_summary["impressions"] * 100,
    })

    overall = summarize(rows)
    # Result types are heterogeneous, so an all-row result total/rate/CPR has no useful meaning.
    overall["results"] = None
    overall["weighted_cost_per_result_ngn"] = None
    overall["derived_result_rate_pct"] = None

    output = {
        "scope_note": "Result types are heterogeneous. Do not sum results across objectives or interpret summed reach as unique people.",
        "dataset": {
            "campaign_rows": len(rows),
            "recognized_rows": len(clean),
            "ambiguous_rows": len(ambiguous),
            "distinct_campaign_name_strings": len({r["campaign_name"] for r in rows}),
            "overall": overall,
        },
        "data_quality": {
            "recognized_rows_reconciling_spend_div_results_to_exported_cost_per_result": reconciled,
            "recognized_rows_checked": len(clean),
            "max_absolute_reconciliation_difference": max_abs_diff,
        },
        "by_result_type": by_type,
        "link_click_analysis": link_summary,
        "bunda_youtube_traffic_rows": bunda_summary,
        "link_clicks_excluding_bunda": non_bunda_summary,
        "link_clicks_excluding_bunda_and_pressure": remaining_summary,
        "top_3_link_click_rows_concentration": top3_summary,
    }

    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    create_charts(link)
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
