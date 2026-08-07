"""Write a deterministic manifest linking source metadata, code and outputs."""
from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import sys

from .campaign_data import PROJECT_ROOT

SCRIPT_PATHS = [
    "scripts/xlsx_reader.py",
    "scripts/campaign_data.py",
    "scripts/prepare_data.py",
    "scripts/validate_data.py",
    "scripts/analyse_campaigns.py",
    "scripts/visualise_results.py",
    "scripts/build_manifest.py",
    "scripts/run_pipeline.py",
    "tests/test_pipeline.py",
    ".github/workflows/quality.yml",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
]

PRODUCT_PATHS = [
    "data/meta_campaign_export_sanitized.csv",
    "analysis/data_preparation_summary.json",
    "analysis/validation_report.json",
    "analysis/summary.json",
    "analysis/result_type_summary.csv",
    "analysis/top_link_click_rows.csv",
    "analysis/bunda_named_rows_lower_bound.csv",
    "assets/01_link_click_cost_distribution.svg",
    "assets/02_spend_vs_link_clicks.svg",
    "assets/03_top_link_click_campaigns.svg",
    "assets/04_cpc_sensitivity.svg",
    "assets/05_ctr_sensitivity.svg",
]


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hashes(paths: list[str]) -> dict[str, str]:
    return {
        relative: file_sha256(PROJECT_ROOT / relative)
        for relative in paths
        if (PROJECT_ROOT / relative).exists()
    }


def build_manifest() -> dict[str, object]:
    preparation_path = PROJECT_ROOT / "analysis" / "data_preparation_summary.json"
    preparation = json.loads(preparation_path.read_text(encoding="utf-8"))
    return {
        "purpose": "Provenance manifest for the reproducible portfolio analysis pipeline.",
        "run_command_private_source": "python -m scripts.run_pipeline",
        "run_command_public_products": "python -m scripts.run_pipeline --from-public-csv",
        "source": {
            "filename": preparation["source_filename"],
            "sha256": preparation["source_sha256"],
            "publicly_committed": False,
            "reason_restricted": (
                "The original export contains a historical WhatsApp phone number; "
                "the public CSV is a redacted derivative."
            ),
        },
        "runtime": {
            "python_major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
            "matplotlib": importlib.metadata.version("matplotlib"),
        },
        "code_sha256": hashes(SCRIPT_PATHS),
        "product_sha256": hashes(PRODUCT_PATHS),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the reproducibility manifest.")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "analysis" / "run_manifest.json",
    )
    args = parser.parse_args()
    manifest = build_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote reproducibility manifest -> {args.output}")


if __name__ == "__main__":
    main()
