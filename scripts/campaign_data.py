"""Shared helpers for the prepared campaign-level dataset.

The project deliberately keeps these helpers small.  They provide one
canonical implementation for loading numeric fields and calculating repeated
descriptive summaries so that analysis and visualisation do not drift apart.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CSV = PROJECT_ROOT / "data" / "meta_campaign_export_sanitized.csv"

NUMERIC_FIELDS = (
    "results",
    "reach",
    "impressions",
    "cost_per_result_ngn",
    "amount_spent_ngn",
)

KNOWN_RESULT_TYPES = {
    "3-second video plays",
    "Facebook likes",
    "Leads (form)",
    "Link clicks",
    "Messaging conversations started",
    "Post engagements",
    "ThruPlay",
}


def load_rows(path: Path = PUBLIC_CSV) -> list[dict[str, object]]:
    """Load the public CSV, converting only the fields used numerically."""
    rows: list[dict[str, object]] = []
    with path.open(encoding="utf-8", newline="") as source:
        for raw in csv.DictReader(source):
            row: dict[str, object] = dict(raw)
            row["campaign_row_id"] = int(raw["campaign_row_id"])
            row["source_excel_row"] = int(raw["source_excel_row"])
            for field in NUMERIC_FIELDS:
                row[field] = float(raw[field]) if raw[field] != "" else None
            rows.append(row)
    return rows


def recognized_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Rows with a known result type and no preparation quality flag."""
    return [
        row
        for row in rows
        if not row["data_quality_flag"] and row["result_type"] in KNOWN_RESULT_TYPES
    ]


def link_click_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Recognised rows reported by Meta under the Link clicks result type."""
    return [row for row in recognized_rows(rows) if row["result_type"] == "Link clicks"]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Calculate grouped descriptive totals without mixing result types implicitly."""
    spend = round(math.fsum(float(row["amount_spent_ngn"] or 0) for row in rows), 2)
    impressions = math.fsum(float(row["impressions"] or 0) for row in rows)
    reach = math.fsum(float(row["reach"] or 0) for row in rows)
    results = math.fsum(float(row["results"] or 0) for row in rows)
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


def row_link_kpis(row: dict[str, object]) -> dict[str, float]:
    """Derive CTR, CPM and an impressions/reach ratio for one link-click row."""
    impressions = float(row["impressions"])
    reach = float(row["reach"])
    spend = float(row["amount_spent_ngn"])
    results = float(row["results"])
    return {
        "derived_ctr_pct": results / impressions * 100,
        "derived_cpm_ngn": spend / impressions * 1000,
        "derived_frequency": impressions / reach if reach else 0.0,
    }
