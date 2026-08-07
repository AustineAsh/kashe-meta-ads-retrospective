"""Reproduce the descriptive outputs in this repository.

This analysis is intentionally exploratory. It does not estimate causal effects.
"""
from pathlib import Path
import csv, statistics, re
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "meta_campaign_export_sanitized.csv"
ASSETS = ROOT / "assets"

NUMERIC = {
    "results", "reach", "impressions", "cost_per_result_ngn", "amount_spent_ngn",
    "impressions_per_reach", "results_per_1000_impressions", "cpm_ngn",
    "cpr_recalculation_abs_diff"
}

def read_rows():
    rows=[]
    with DATA.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            for key in NUMERIC:
                value=row.get(key, "")
                row[key]=float(value) if value not in ("", None) else None
            row["campaign_row_id"]=int(row["campaign_row_id"])
            rows.append(row)
    return rows


def grouped_weighted_cost(rows):
    results=sum(r["results"] or 0 for r in rows)
    spend=sum(r["amount_spent_ngn"] or 0 for r in rows)
    return spend/results if results else None


def main():
    rows=read_rows()
    link=[r for r in rows if r["result_type"]=="Link clicks" and not r["data_quality_flag"]]
    cpr=[r["cost_per_result_ngn"] for r in link if r["cost_per_result_ngn"] is not None]

    print(f"Campaign rows: {len(rows)}")
    print(f"Recognized link-click campaigns: {len(link)}")
    print(f"Link clicks: {int(sum(r['results'] or 0 for r in link)):,}")
    print(f"Weighted cost/link click: NGN {grouped_weighted_cost(link):,.2f}")
    print(f"Median campaign cost/link click: NGN {statistics.median(cpr):,.2f}")

    ASSETS.mkdir(exist_ok=True)

    plt.figure(figsize=(8,5))
    plt.hist(cpr, bins=25)
    plt.xlabel("Campaign cost per link click (NGN)")
    plt.ylabel("Number of campaigns")
    plt.title("Distribution of cost per link click across recognized campaigns")
    plt.tight_layout()
    plt.savefig(ASSETS/"01_link_click_cost_distribution.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8,5.5))
    xs=[r["amount_spent_ngn"] for r in link if r["amount_spent_ngn"] and r["results"]]
    ys=[r["results"] for r in link if r["amount_spent_ngn"] and r["results"]]
    plt.scatter(xs, ys, alpha=.65)
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("Spend (NGN, log scale)")
    plt.ylabel("Link clicks (log scale)")
    plt.title("Spend and link-click outcomes by campaign")
    plt.tight_layout()
    plt.savefig(ASSETS/"02_spend_vs_link_clicks.png", dpi=160)
    plt.close()

    ranked=sorted(link, key=lambda r:r["results"] or 0, reverse=True)[:10]
    labels=[]
    for r in ranked:
        name=re.sub(r"[^\x20-\x7E]", "", r["campaign_name"])
        labels.append(name if len(name)<=40 else name[:37]+"...")
    vals=[r["results"] for r in ranked]
    pos=list(range(len(ranked)))
    plt.figure(figsize=(9,6))
    plt.barh(pos, vals)
    plt.yticks(pos, labels)
    plt.gca().invert_yaxis()
    plt.xlabel("Link clicks")
    plt.title("Top 10 campaigns by recorded link clicks")
    plt.tight_layout()
    plt.savefig(ASSETS/"03_top_link_click_campaigns.png", dpi=160)
    plt.close()

if __name__ == "__main__":
    main()
