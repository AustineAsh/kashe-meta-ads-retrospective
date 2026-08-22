"""Prepare stable, decision-oriented data for the executive dashboard.

The dashboard consumes the published analysis products rather than calculating
a second, potentially divergent version of the campaign findings.
"""
from __future__ import annotations

import json
from pathlib import Path

from .campaign_data import PROJECT_ROOT, PUBLIC_CSV, link_click_rows, load_rows, row_link_kpis

SUMMARY_JSON = PROJECT_ROOT / "analysis" / "summary.json"


def _required(mapping: dict[str, object], key: str) -> dict[str, object]:
    """Return a required nested mapping with a useful error on malformed inputs."""
    value = mapping.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"Dashboard input is missing the '{key}' section.")
    return value


def load_dashboard_model(
    summary_path: Path = SUMMARY_JSON,
    csv_path: Path = PUBLIC_CSV,
) -> dict[str, object]:
    """Load and validate the compact model used by the Streamlit dashboard."""
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    dataset = _required(summary, "dataset")
    overall = _required(dataset, "overall")
    link = _required(summary, "link_click_analysis")
    top_three = _required(summary, "top_3_link_click_rows_concentration")

    contribution = [
        {
            "metric": "Link clicks",
            "top_three_pct": float(top_three["share_of_link_clicks_pct"]),
        },
        {
            "metric": "Link spend",
            "top_three_pct": float(top_three["share_of_link_spend_pct"]),
        },
        {
            "metric": "Impressions",
            "top_three_pct": float(top_three["share_of_link_impressions_pct"]),
        },
    ]
    for item in contribution:
        share = float(item["top_three_pct"])
        if not 0 <= share <= 100:
            raise ValueError(f"Contribution share is outside 0-100%: {item}")
        item["remaining_pct"] = 100 - share

    scenario_keys = [
        ("All link rows", "link_click_analysis"),
        ("Excluding Bunda", "link_clicks_excluding_bunda"),
        ("Excluding top three", "link_clicks_excluding_bunda_and_pressure"),
    ]
    sensitivity: list[dict[str, object]] = []
    for label, key in scenario_keys:
        scenario = _required(summary, key)
        sensitivity.append(
            {
                "scenario": label,
                "weighted_cpc_ngn": float(scenario["weighted_cpc_ngn"]),
                "derived_ctr_pct": float(scenario["derived_link_ctr_pct"]),
            }
        )

    rows = load_rows(csv_path)
    campaign_detail: list[dict[str, object]] = []
    for row in sorted(
        link_click_rows(rows),
        key=lambda item: float(item["results"] or 0),
        reverse=True,
    ):
        campaign_detail.append(
            {
                "Campaign": str(row["campaign_name"]),
                "Link clicks": int(float(row["results"])),
                "Spend (NGN)": round(float(row["amount_spent_ngn"]), 2),
                "Impressions": int(float(row["impressions"])),
                "CPC (NGN)": round(float(row["cost_per_result_ngn"]), 2),
                "CTR (%)": round(row_link_kpis(row)["derived_ctr_pct"], 2),
            }
        )

    return {
        "headline": {
            "campaign_rows": int(dataset["campaign_rows"]),
            "spend_ngn": float(overall["spend_ngn"]),
            "impressions": int(overall["impressions"]),
            "link_clicks": int(float(link["results"])),
            "weighted_cpc_ngn": float(link["weighted_cpc_ngn"]),
            "derived_ctr_pct": float(link["derived_link_ctr_pct"]),
            "top_three_click_share_pct": float(top_three["share_of_link_clicks_pct"]),
        },
        "contribution": contribution,
        "sensitivity": sensitivity,
        "campaign_detail": campaign_detail,
    }


def compact_number(value: float | int) -> str:
    """Format large counts for executive KPI cards without false precision."""
    absolute = abs(float(value))
    if absolute >= 1_000_000:
        return f"{value / 1_000_000:.2f}m"
    if absolute >= 1_000:
        return f"{value / 1_000:.1f}k"
    return f"{value:,.0f}"
