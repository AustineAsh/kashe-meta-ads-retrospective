"""Write a deterministic manifest linking source metadata, code and outputs."""
from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import struct
import sys
import zlib

from .campaign_data import PROJECT_ROOT
from .io_utils import write_text_lf

SCRIPT_PATHS = [
    ".github/workflows/quality.yml",
    "scripts/__init__.py",
    "scripts/xlsx_reader.py",
    "scripts/campaign_data.py",
    "scripts/prepare_data.py",
    "scripts/canonicalize_public_csv.py",
    "scripts/validate_data.py",
    "scripts/analyse_campaigns.py",
    "scripts/visualise_results.py",
    "scripts/dashboard_data.py",
    "scripts/build_manifest.py",
    "scripts/run_pipeline.py",
    "scripts/io_utils.py",
    "tests/test_pipeline.py",
    "tests/test_dashboard.py",
    "dashboard.py",
    ".streamlit/config.toml",
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

EVIDENCE_PATHS = [
    "evidence/meta_account_spend_screenshot.png",
]


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hashes(paths: list[str]) -> dict[str, str]:
    missing = [relative for relative in paths if not (PROJECT_ROOT / relative).is_file()]
    if missing:
        raise FileNotFoundError(
            "Cannot build a complete manifest; expected files are missing: "
            + ", ".join(missing)
        )
    return {relative: file_sha256(PROJECT_ROOT / relative) for relative in paths}


def validate_png_structure(path: Path) -> None:
    """Reject truncated or structurally corrupt PNG evidence before hashing it."""
    content = path.read_bytes()
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Evidence file is not a PNG: {path}")

    position = 8
    chunk_types: list[bytes] = []
    while position < len(content):
        if position + 12 > len(content):
            raise ValueError(f"Truncated PNG chunk header: {path}")
        length = struct.unpack(">I", content[position : position + 4])[0]
        chunk_end = position + 12 + length
        if chunk_end > len(content):
            raise ValueError(f"Truncated PNG chunk data: {path}")

        chunk_type = content[position + 4 : position + 8]
        chunk_data = content[position + 8 : position + 8 + length]
        stored_crc = struct.unpack(">I", content[position + 8 + length : chunk_end])[0]
        calculated_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if stored_crc != calculated_crc:
            raise ValueError(f"PNG chunk checksum failed: {path}")

        chunk_types.append(chunk_type)
        position = chunk_end

    if position != len(content) or not chunk_types or chunk_types[0] != b"IHDR":
        raise ValueError(f"Invalid PNG chunk structure: {path}")
    if chunk_types[-1] != b"IEND":
        raise ValueError(f"PNG has no terminal IEND chunk: {path}")


def build_manifest() -> dict[str, object]:
    preparation_path = PROJECT_ROOT / "analysis" / "data_preparation_summary.json"
    preparation = json.loads(preparation_path.read_text(encoding="utf-8"))
    for relative in EVIDENCE_PATHS:
        validate_png_structure(PROJECT_ROOT / relative)
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
        "evidence_sha256": hashes(EVIDENCE_PATHS),
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
    write_text_lf(args.output, json.dumps(manifest, indent=2))
    print(f"Wrote reproducibility manifest -> {args.output}")


if __name__ == "__main__":
    main()
