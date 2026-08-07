"""Canonicalise the committed public CSV without changing analytical meaning.

This stage exists so the restricted-workbook preparation and the public-CI path
use the same text representation: stable field order, numeric serialisation,
Unicode normalisation, newline handling and LF record endings.
"""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import unicodedata

from .campaign_data import PROJECT_ROOT, PUBLIC_CSV
from .prepare_data import OUTPUT_FIELDS

NUMERIC_FIELDS = {
    "campaign_row_id",
    "source_excel_row",
    "results",
    "reach",
    "impressions",
    "cost_per_result_ngn",
    "amount_spent_ngn",
}


def canonical_text(value: str) -> str:
    return unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")


def canonical_number(value: str) -> int | float | str:
    if value == "":
        return ""
    number = float(value)
    return int(number) if number.is_integer() else number


def canonicalize(path: Path = PUBLIC_CSV) -> None:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    if fields != OUTPUT_FIELDS:
        raise ValueError(
            "Public CSV schema differs from the preparation schema; "
            "regenerate it from the verified source workbook."
        )

    canonical_rows = []
    for row in rows:
        canonical_rows.append(
            {
                field: (
                    canonical_number(row[field])
                    if field in NUMERIC_FIELDS
                    else canonical_text(row[field])
                )
                for field in OUTPUT_FIELDS
            }
        )

    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(
            destination, fieldnames=OUTPUT_FIELDS, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(canonical_rows)

    preparation_summary = PROJECT_ROOT / "analysis" / "data_preparation_summary.json"
    if preparation_summary.exists():
        summary = json.loads(preparation_summary.read_text(encoding="utf-8"))
        summary["output_csv_sha256"] = sha256(path.read_bytes()).hexdigest()
        preparation_summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Canonicalise the public campaign CSV.")
    parser.add_argument("--input", type=Path, default=PUBLIC_CSV)
    args = parser.parse_args()
    canonicalize(args.input)
    print(f"Canonicalised public CSV -> {args.input}")


if __name__ == "__main__":
    main()
