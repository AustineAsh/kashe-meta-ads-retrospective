"""Validate the prepared public campaign dataset before analysis."""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import re

from .campaign_data import KNOWN_RESULT_TYPES, NUMERIC_FIELDS, PROJECT_ROOT, PUBLIC_CSV
from .io_utils import write_text_lf

PHONE_RE = re.compile(r"(?i)(?:phone=|wa\.me/)\+?\d{7,15}")
EXPECTED_SEMANTIC_FINGERPRINT = (
    "e7bd7362a87011574993c559b52f9540a3330cbe6ffe8ddfa683892f69935544"
)
SEMANTIC_NUMERIC_FIELDS = {
    "campaign_row_id",
    "source_excel_row",
    "results",
    "reach",
    "impressions",
    "cost_per_result_ngn",
    "amount_spent_ngn",
}


def semantic_fingerprint(rows: list[dict[str, str]], fieldnames: list[str]) -> str:
    """Hash the prepared records independent of CSV newline/number formatting."""
    canonical_rows = []
    for row in rows:
        canonical = {}
        for field in fieldnames:
            value = row[field]
            if field in SEMANTIC_NUMERIC_FIELDS:
                if value == "":
                    canonical[field] = None
                else:
                    number = float(value)
                    canonical[field] = int(number) if number.is_integer() else number
            else:
                canonical[field] = value
        canonical_rows.append(canonical)
    payload = json.dumps(
        canonical_rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256(payload).hexdigest()


EXPECTED_FIELDS = {
    "campaign_row_id",
    "source_excel_row",
    "campaign_name",
    "result_type",
    "results",
    "reach",
    "impressions",
    "cost_per_result_ngn",
    "amount_spent_ngn",
    "data_quality_flag",
}


def load_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        return list(reader), list(reader.fieldnames or [])


def number(row: dict[str, str], field: str, *, allow_missing: bool = False) -> float | None:
    value = row.get(field, "")
    if value == "":
        if allow_missing:
            return None
        raise ValueError(f"Missing {field} on campaign_row_id={row.get('campaign_row_id')}")
    return float(value)


def validate(path: Path = PUBLIC_CSV) -> dict[str, object]:
    rows, fieldnames = load_rows(path)
    errors: list[str] = []
    warnings: list[str] = []

    missing_fields = sorted(EXPECTED_FIELDS - set(fieldnames))
    unexpected_fields = sorted(set(fieldnames) - EXPECTED_FIELDS)
    if missing_fields:
        errors.append("Missing expected columns: " + ", ".join(missing_fields))
    if unexpected_fields:
        warnings.append("Unexpected columns present: " + ", ".join(unexpected_fields))

    fingerprint = semantic_fingerprint(rows, fieldnames)
    if fingerprint != EXPECTED_SEMANTIC_FINGERPRINT:
        errors.append(
            "Prepared public records do not match the semantic fingerprint of the "
            "verified private-source preparation."
        )

    row_ids = [int(row["campaign_row_id"]) for row in rows]
    if row_ids != list(range(1, len(rows) + 1)):
        errors.append("campaign_row_id is not a complete 1..N sequence")

    source_rows = [int(row["source_excel_row"]) for row in rows]
    if len(source_rows) != len(set(source_rows)):
        errors.append("source_excel_row is not unique")

    if any(PHONE_RE.search(row["campaign_name"]) for row in rows):
        errors.append("A WhatsApp phone number remains in a published campaign name")

    recognized = 0
    flagged = 0
    missing_result_type = 0
    cpr_checked = 0
    cpr_reconciled = 0
    max_cpr_difference = 0.0
    reach_over_impressions: list[int] = []

    for row in rows:
        row_id = int(row["campaign_row_id"])
        result_type = row["result_type"]
        flag = row["data_quality_flag"]
        recognized_row = result_type in KNOWN_RESULT_TYPES
        values: dict[str, float | None] = {}

        for field in NUMERIC_FIELDS:
            allow_missing = not recognized_row and field in {"results", "cost_per_result_ngn"}
            try:
                values[field] = number(row, field, allow_missing=allow_missing)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if values[field] is not None and values[field] < 0:
                errors.append(f"Negative {field} on campaign_row_id={row_id}")

        if values.get("impressions", 0) <= 0:
            errors.append(f"Non-positive impressions on campaign_row_id={row_id}")
        if recognized_row and (values.get("results") is None or values.get("results", 0) <= 0):
            errors.append(f"Non-positive results on recognized campaign_row_id={row_id}")
        if values.get("reach", 0) > values.get("impressions", float("inf")):
            reach_over_impressions.append(row_id)

        if recognized_row:
            recognized += 1
            if flag:
                errors.append(
                    f"Recognized result type is unexpectedly flagged on campaign_row_id={row_id}"
                )
            if values.get("results"):
                calculated_cpr = values["amount_spent_ngn"] / values["results"]
                difference = abs(calculated_cpr - values["cost_per_result_ngn"])
                max_cpr_difference = max(max_cpr_difference, difference)
                cpr_checked += 1
                if difference < 1e-6:
                    cpr_reconciled += 1
                else:
                    errors.append(
                        f"Cost-per-result does not reconcile on campaign_row_id={row_id}: "
                        f"export={values['cost_per_result_ngn']}, calculated={calculated_cpr}"
                    )
        else:
            flagged += 1
            expected_flag = "missing_result_type" if not result_type else "unrecognized_result_type"
            if expected_flag == "missing_result_type":
                missing_result_type += 1
                if row["results"] != "" or row["cost_per_result_ngn"] != "":
                    errors.append(
                        "Missing result type should retain blank Results and Cost per result "
                        f"on campaign_row_id={row_id}"
                    )
            if flag != expected_flag:
                errors.append(
                    "Unknown/missing result type is not correctly flagged on "
                    f"campaign_row_id={row_id}"
                )

    if reach_over_impressions:
        warnings.append(
            "Reach exceeds impressions on campaign rows: "
            + ", ".join(map(str, reach_over_impressions))
        )

    report = {
        "status": "pass" if not errors else "fail",
        "rows": len(rows),
        "recognized_result_rows": recognized,
        "flagged_result_rows": flagged,
        "missing_result_type_rows": missing_result_type,
        "distinct_campaign_name_strings": len({row["campaign_name"] for row in rows}),
        "cost_per_result_rows_checked": cpr_checked,
        "cost_per_result_rows_reconciled": cpr_reconciled,
        "max_cost_per_result_absolute_difference": max_cpr_difference,
        "semantic_fingerprint_sha256": fingerprint,
        "expected_semantic_fingerprint_sha256": EXPECTED_SEMANTIC_FINGERPRINT,
        "errors": errors,
        "warnings": warnings,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the sanitised campaign CSV.")
    parser.add_argument("--input", type=Path, default=PUBLIC_CSV)
    parser.add_argument(
        "--report",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "validation_report.json",
    )
    args = parser.parse_args()

    report = validate(args.input)
    write_text_lf(args.report, json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
