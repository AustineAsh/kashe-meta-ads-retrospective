"""Prepare a public, analysis-ready CSV from the original Meta Ads workbook.

This is targeted data preparation rather than an attempt to comprehensively
'clean' a historical advertising export.  The script preserves source rows,
removes only redundant/uninformative fields, converts the fields used in the
analysis to consistent values, flags rather than guesses at missing result fields,
and redacts the historical phone number embedded in one campaign name.
"""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Sequence

from .xlsx_reader import read_worksheet

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SOURCE_SHA256 = (
    "5facbe664cfd86bdc64822ed081c43668637a67dff59ce754dc97eb5397e5dc0"
)
SOURCE_SHEET = "Raw Data Report"
KNOWN_RESULT_TYPES = {
    "3-second video plays",
    "Facebook likes",
    "Leads (form)",
    "Link clicks",
    "Messaging conversations started",
    "Post engagements",
    "ThruPlay",
}

OUTPUT_FIELDS = [
    "campaign_row_id",
    "source_excel_row",
    "campaign_name",
    "delivery_status",
    "delivery_level",
    "attribution_setting",
    "result_type",
    "results",
    "reach",
    "impressions",
    "cost_per_result_ngn",
    "amount_spent_ngn",
    "reporting_starts",
    "reporting_ends",
    "data_quality_flag",
]

PHONE_QUERY_RE = re.compile(r"(?i)(phone=)\+?\d{7,15}")
WA_ME_RE = re.compile(r"(?i)(wa\.me/)\+?\d{7,15}")


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def redact_campaign_name(name: str) -> tuple[str, bool]:
    """Redact phone digits only when they appear in an obvious WhatsApp URL."""
    redacted = PHONE_QUERY_RE.sub(r"\1[REDACTED]", name)
    redacted = WA_ME_RE.sub(r"\1[REDACTED]", redacted)
    return redacted, redacted != name


def find_header_row(rows: Sequence[Sequence[object | None]]) -> int:
    """Locate the source header row by labels rather than a fixed row number."""
    for index, row in enumerate(rows):
        values = {str(value) for value in row if value is not None}
        if "Campaign name" in values and "Result type" in values:
            return index
    raise ValueError("Could not locate the Meta Ads header row")


def positions(headers: Sequence[object | None], label: str) -> list[int]:
    return [index for index, value in enumerate(headers) if value == label]


def require_position(headers: Sequence[object | None], label: str) -> int:
    matches = positions(headers, label)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {label!r} column, found {len(matches)}")
    return matches[0]


def numeric_value(
    value: object | None,
    label: str,
    source_row: int,
    *,
    allow_missing: bool = False,
) -> int | float | None:
    """Return a numeric source value without inventing missing values."""
    if value in (None, ""):
        if allow_missing:
            return None
        raise ValueError(f"Missing/non-numeric {label!r} in source row {source_row}")
    if isinstance(value, bool):
        raise ValueError(f"Non-numeric {label!r} in source row {source_row}")
    if isinstance(value, (int, float)):
        return value
    try:
        number = float(str(value))
    except ValueError as exc:
        raise ValueError(
            f"Could not parse {label!r}={value!r} in source row {source_row}"
        ) from exc
    return int(number) if number.is_integer() else number


def prepare_rows(source: Path) -> tuple[list[dict[str, object]], dict[str, object]]:
    worksheet = read_worksheet(source, SOURCE_SHEET)
    rows = worksheet.rows
    header_index = find_header_row(rows)
    headers = rows[header_index]

    campaign_name_columns = positions(headers, "Campaign name")
    if len(campaign_name_columns) != 2:
        raise ValueError(
            "The historical export is expected to contain two Campaign name columns"
        )

    column = {
        "delivery_status": require_position(headers, "Delivery status"),
        "delivery_level": require_position(headers, "Delivery level"),
        "attribution_setting": require_position(headers, "Attribution setting"),
        "result_type": require_position(headers, "Result type"),
        "results": require_position(headers, "Results"),
        "reach": require_position(headers, "Reach"),
        "impressions": require_position(headers, "Impressions"),
        "cost_per_result_ngn": require_position(headers, "Cost per result"),
        "amount_spent_ngn": require_position(headers, "Amount spent (NGN)"),
        "reporting_starts": require_position(headers, "Reporting starts"),
        "reporting_ends": require_position(headers, "Reporting ends"),
    }

    # The ranking fields contain '-' in every source row.  Verify that before
    # excluding them from the public analysis-ready table.
    ranking_labels = [
        "Quality ranking",
        "Engagement rate ranking",
        "Conversion rate ranking",
    ]
    ranking_columns = {
        label: require_position(headers, label) for label in ranking_labels
    }
    results_initial_column = require_position(headers, "Results (initial)")

    prepared: list[dict[str, object]] = []
    duplicate_name_mismatches: list[int] = []
    unexpected_ranking_values: list[tuple[int, str, object]] = []
    redaction_count = 0
    unexpected_initial_results: list[tuple[int, object]] = []

    for source_index, row in enumerate(rows[header_index + 1 :], start=header_index + 2):
        # source_index is one-based Excel row number because enumerate starts at
        # header_index + 2 while Python row indexes are zero based.
        if not any(value not in (None, "") for value in row):
            continue

        first_name = str(row[campaign_name_columns[0]] or "")
        second_name = str(row[campaign_name_columns[1]] or "")
        if first_name != second_name:
            duplicate_name_mismatches.append(source_index)

        for label, index in ranking_columns.items():
            value = row[index]
            if value not in (None, "", "-"):
                unexpected_ranking_values.append((source_index, label, value))

        initial_result = row[results_initial_column]
        if initial_result not in (None, ""):
            unexpected_initial_results.append((source_index, initial_result))

        campaign_name, was_redacted = redact_campaign_name(first_name)
        redaction_count += int(was_redacted)

        result_type = str(row[column["result_type"]] or "")
        if result_type in KNOWN_RESULT_TYPES:
            flag = ""
        elif not result_type:
            flag = "missing_result_type"
        else:
            flag = "unrecognized_result_type"

        allow_missing_result_fields = bool(flag)

        prepared.append(
            {
                "campaign_row_id": len(prepared) + 1,
                "source_excel_row": source_index,
                "campaign_name": campaign_name,
                "delivery_status": str(row[column["delivery_status"]] or ""),
                "delivery_level": str(row[column["delivery_level"]] or ""),
                "attribution_setting": str(row[column["attribution_setting"]] or ""),
                "result_type": result_type,
                "results": numeric_value(
                    row[column["results"]],
                    "Results",
                    source_index,
                    allow_missing=allow_missing_result_fields,
                ),
                "reach": numeric_value(row[column["reach"]], "Reach", source_index),
                "impressions": numeric_value(
                    row[column["impressions"]], "Impressions", source_index
                ),
                "cost_per_result_ngn": numeric_value(
                    row[column["cost_per_result_ngn"]],
                    "Cost per result",
                    source_index,
                    allow_missing=allow_missing_result_fields,
                ),
                "amount_spent_ngn": numeric_value(
                    row[column["amount_spent_ngn"]], "Amount spent", source_index
                ),
                "reporting_starts": str(row[column["reporting_starts"]] or ""),
                "reporting_ends": str(row[column["reporting_ends"]] or ""),
                "data_quality_flag": flag,
            }
        )

    if duplicate_name_mismatches:
        raise ValueError(
            "Duplicate Campaign name columns disagree on source rows: "
            + ", ".join(map(str, duplicate_name_mismatches))
        )
    if unexpected_ranking_values:
        raise ValueError(
            "Ranking columns contained unexpected data; review before dropping them: "
            + repr(unexpected_ranking_values[:5])
        )
    if unexpected_initial_results:
        raise ValueError(
            "Results (initial) contained data; review before dropping it: "
            + repr(unexpected_initial_results[:5])
        )

    summary = {
        "source_sheet": SOURCE_SHEET,
        "header_excel_row": header_index + 1,
        "campaign_rows_prepared": len(prepared),
        "duplicate_campaign_name_columns_checked": 2,
        "duplicate_campaign_name_mismatches": len(duplicate_name_mismatches),
        "ranking_columns_verified_uninformative": ranking_labels,
        "phone_redactions": redaction_count,
        "recognized_result_rows": sum(not row["data_quality_flag"] for row in prepared),
        "flagged_result_rows": sum(bool(row["data_quality_flag"]) for row in prepared),
        "missing_result_type_rows": sum(
            row["data_quality_flag"] == "missing_result_type" for row in prepared
        ),
        "unrecognized_result_type_rows": sum(
            row["data_quality_flag"] == "unrecognized_result_type" for row in prepared
        ),
        "distinct_campaign_name_strings": len({row["campaign_name"] for row in prepared}),
        "fields_retained": OUTPUT_FIELDS,
        "fields_intentionally_not_carried_forward": [
            "blank leading source column",
            "duplicate Campaign name column",
            "Quality ranking (all '-')",
            "Engagement rate ranking (all '-')",
            "Conversion rate ranking (all '-')",
            "Results (initial) (blank on all campaign rows)",
        ],
    }
    return prepared, summary


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare the sanitised Meta campaign CSV from the original workbook."
    )
    parser.add_argument("--source", type=Path, required=True, help="Path to 30-01-23.xlsx")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "meta_campaign_export_sanitized.csv",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "data_preparation_summary.json",
    )
    parser.add_argument(
        "--allow-source-hash-mismatch",
        action="store_true",
        help="Allow a workbook different from the verified historical source.",
    )
    args = parser.parse_args()

    source_hash = file_sha256(args.source)
    if source_hash != EXPECTED_SOURCE_SHA256 and not args.allow_source_hash_mismatch:
        raise SystemExit(
            "Source workbook SHA-256 does not match the verified historical file. "
            "Use --allow-source-hash-mismatch only after reviewing the new source."
        )

    rows, summary = prepare_rows(args.source)
    write_csv(rows, args.output)
    summary.update(
        {
            "source_filename": args.source.name,
            "source_sha256": source_hash,
            "expected_source_sha256": EXPECTED_SOURCE_SHA256,
            "output_csv": (
                str(args.output.relative_to(PROJECT_ROOT))
                if args.output.is_relative_to(PROJECT_ROOT)
                else args.output.name
            ),
            "output_csv_sha256": file_sha256(args.output),
        }
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(
        f"Prepared {len(rows)} campaign rows -> {args.output} "
        f"({summary['recognized_result_rows']} recognized, "
        f"{summary['flagged_result_rows']} flagged)."
    )


if __name__ == "__main__":
    main()
