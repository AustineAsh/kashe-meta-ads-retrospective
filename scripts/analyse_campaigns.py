"""Compute reproducible descriptive KPIs from the sanitised campaign dataset."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import statistics

from .campaign_data import (
    PROJECT_ROOT,
    PUBLIC_CSV,
    link_click_rows,
    load_rows,
    recognized_rows,
    row_link_kpis,
    summarize,
)


def with_link_kpis(summary: dict[str, object]) -> dict[str, object]:
    summary = dict(summary)
    summary["weighted_cpc_ngn"] = summary["weighted_cost_per_result_ngn"]
    summary["derived_link_ctr_pct"] = summary["derived_result_rate_pct"]
    return summary


def share(part: float, whole: float) -> float:
    return part / whole * 100 if whole else 0.0


def result_type_summary(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    result_types = sorted({str(row["result_type"]) for row in rows})
    return {
        result_type: summarize(
            [row for row in rows if row["result_type"] == result_type]
        )
        for result_type in result_types
    }


def write_result_type_table(by_type: dict[str, dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "result_type",
        "rows",
        "results",
        "spend_ngn",
        "impressions",
        "sum_campaign_reach_not_unique",
        "weighted_cost_per_result_ngn",
        "derived_result_rate_pct",
        "derived_cpm_ngn",
        "impressions_per_summed_reach",
    ]
    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        for result_type, summary in by_type.items():
            writer.writerow({"result_type": result_type, **summary})


def write_top_link_table(
    link_rows: list[dict[str, object]], path: Path, limit: int = 20
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "campaign_row_id",
        "campaign_name",
        "results",
        "amount_spent_ngn",
        "impressions",
        "reach",
        "cost_per_result_ngn",
        "derived_ctr_pct",
        "derived_cpm_ngn",
        "derived_frequency",
    ]
    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        ranked = sorted(
            link_rows, key=lambda item: float(item["results"]), reverse=True
        )[:limit]
        for row in ranked:
            enriched = {**row, **row_link_kpis(row)}
            writer.writerow({field: enriched[field] for field in fields})


def write_bunda_subset(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "campaign_row_id",
        "campaign_name",
        "result_type",
        "results",
        "impressions",
        "reach",
        "amount_spent_ngn",
        "cost_per_result_ngn",
    ]
    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in rows)


def analyse(rows: list[dict[str, object]]) -> dict[str, object]:
    recognized = recognized_rows(rows)
    flagged = [row for row in rows if row["data_quality_flag"]]

    overall = summarize(rows)
    # Results from unlike objectives have no sensible pooled interpretation.
    overall["results"] = None
    overall["weighted_cost_per_result_ngn"] = None
    overall["derived_result_rate_pct"] = None

    by_type = result_type_summary(recognized)
    link = link_click_rows(rows)
    link_summary = with_link_kpis(summarize(link))

    cpc = [float(row["cost_per_result_ngn"]) for row in link]
    ctr = [row_link_kpis(row)["derived_ctr_pct"] for row in link]
    cpm = [row_link_kpis(row)["derived_cpm_ngn"] for row in link]
    frequency = [row_link_kpis(row)["derived_frequency"] for row in link]
    quartiles = statistics.quantiles(cpc, n=4, method="exclusive")
    link_summary.update(
        {
            "median_campaign_cpc_ngn": statistics.median(cpc),
            "sample_q1_campaign_cpc_ngn": quartiles[0],
            "sample_q3_campaign_cpc_ngn": quartiles[2],
            "min_campaign_cpc_ngn": min(cpc),
            "max_campaign_cpc_ngn": max(cpc),
            "median_campaign_ctr_pct": statistics.median(ctr),
            "median_campaign_cpm_ngn": statistics.median(cpm),
            "median_campaign_frequency": statistics.median(frequency),
        }
    )

    bunda_traffic = [
        row
        for row in link
        if row["campaign_name"] in {"Bunda Youtube – official", "Bunda Youtube"}
    ]
    bunda_traffic_summary = with_link_kpis(summarize(bunda_traffic))
    bunda_traffic_summary.update(
        {
            "share_of_link_clicks_pct": share(
                float(bunda_traffic_summary["results"]), float(link_summary["results"])
            ),
            "share_of_link_spend_pct": share(
                float(bunda_traffic_summary["spend_ngn"]), float(link_summary["spend_ngn"])
            ),
            "share_of_total_export_spend_pct": share(
                float(bunda_traffic_summary["spend_ngn"]), float(overall["spend_ngn"])
            ),
            "share_of_link_impressions_pct": share(
                float(bunda_traffic_summary["impressions"]),
                float(link_summary["impressions"]),
            ),
        }
    )

    non_bunda = [row for row in link if row not in bunda_traffic]
    non_bunda_summary = with_link_kpis(summarize(non_bunda))

    pressure = [
        row
        for row in link
        if "Feel the beats, feel the 'Pressure.' Now" in str(row["campaign_name"])
    ]
    remaining = [row for row in non_bunda if row not in pressure]
    remaining_summary = with_link_kpis(summarize(remaining))

    top3 = sorted(link, key=lambda row: float(row["results"]), reverse=True)[:3]
    top3_summary = with_link_kpis(summarize(top3))
    top3_summary.update(
        {
            "share_of_link_clicks_pct": share(
                float(top3_summary["results"]), float(link_summary["results"])
            ),
            "share_of_link_spend_pct": share(
                float(top3_summary["spend_ngn"]), float(link_summary["spend_ngn"])
            ),
            "share_of_link_impressions_pct": share(
                float(top3_summary["impressions"]), float(link_summary["impressions"])
            ),
        }
    )

    # A deliberately conservative lower bound: only rows whose surviving name
    # explicitly contains 'Bunda' are included. Generic/truncated names may
    # omit other Bunda-related activity.
    bunda_named = [
        row for row in recognized if "bunda" in str(row["campaign_name"]).lower()
    ]
    bunda_named_summary = summarize(bunda_named)
    bunda_named_link = [row for row in bunda_named if row["result_type"] == "Link clicks"]
    bunda_named_link_summary = with_link_kpis(summarize(bunda_named_link))
    bunda_named_thruplay = [row for row in bunda_named if row["result_type"] == "ThruPlay"]

    return {
        "scope_note": (
            "Result types are heterogeneous. Do not sum results across objectives or "
            "interpret summed campaign reach as unique people."
        ),
        "dataset": {
            "campaign_rows": len(rows),
            "recognized_rows": len(recognized),
            "flagged_rows": len(flagged),
            "missing_result_type_rows": sum(
                row["data_quality_flag"] == "missing_result_type" for row in flagged
            ),
            "distinct_campaign_name_strings": len({row["campaign_name"] for row in rows}),
            "overall": overall,
        },
        "by_result_type": by_type,
        "link_click_analysis": link_summary,
        "bunda_youtube_traffic_rows": bunda_traffic_summary,
        "link_clicks_excluding_bunda": non_bunda_summary,
        "link_clicks_excluding_bunda_and_pressure": remaining_summary,
        "top_3_link_click_rows_concentration": top3_summary,
        "bunda_name_lower_bound": {
            "note": (
                "Rows included only when the surviving campaign name explicitly contains "
                "'Bunda'; this is a lower bound, not the complete Bunda campaign budget."
            ),
            "all_named_rows": bunda_named_summary,
            "link_click_rows": bunda_named_link_summary,
            "thruplay_rows": summarize(bunda_named_thruplay),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse the prepared Meta campaign CSV.")
    parser.add_argument("--input", type=Path, default=PUBLIC_CSV)
    parser.add_argument(
        "--summary",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "summary.json",
    )
    parser.add_argument(
        "--result-type-table",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "result_type_summary.csv",
    )
    parser.add_argument(
        "--top-link-table",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "top_link_click_rows.csv",
    )
    parser.add_argument(
        "--bunda-table",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "bunda_named_rows_lower_bound.csv",
    )
    args = parser.parse_args()

    rows = load_rows(args.input)
    output = analyse(rows)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    recognized = recognized_rows(rows)
    by_type = result_type_summary(recognized)
    link = link_click_rows(rows)
    bunda_named = [
        row for row in recognized if "bunda" in str(row["campaign_name"]).lower()
    ]
    write_result_type_table(by_type, args.result_type_table)
    write_top_link_table(link, args.top_link_table)
    write_bunda_subset(bunda_named, args.bunda_table)

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
