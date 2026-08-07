"""Run the historical Meta Ads preparation-to-visualisation pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from .campaign_data import PROJECT_ROOT


def run_module(module: str, *arguments: str) -> None:
    command = [sys.executable, "-m", module, *arguments]
    print("+", " ".join(command))
    subprocess.run(command, check=True, cwd=PROJECT_ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run preparation, validation, analysis, charts and provenance checks."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=PROJECT_ROOT / "data" / "private" / "30-01-23.xlsx",
        help="Local path to the restricted original workbook.",
    )
    parser.add_argument(
        "--from-public-csv",
        action="store_true",
        help=(
            "Skip the private-source preparation stage and rebuild downstream products "
            "from the committed sanitised CSV. This is the mode used by public CI."
        ),
    )
    parser.add_argument(
        "--allow-source-hash-mismatch",
        action="store_true",
        help="Use only after manually reviewing a changed source workbook.",
    )
    args = parser.parse_args()

    if not args.from_public_csv:
        prepare_args = ["--source", str(args.source)]
        if args.allow_source_hash_mismatch:
            prepare_args.append("--allow-source-hash-mismatch")
        run_module("scripts.prepare_data", *prepare_args)
    else:
        run_module("scripts.canonicalize_public_csv")

    run_module("scripts.validate_data")
    run_module("scripts.analyse_campaigns")
    run_module("scripts.visualise_results")
    run_module("scripts.build_manifest")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
