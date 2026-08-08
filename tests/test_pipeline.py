from __future__ import annotations

import csv
from hashlib import sha256
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from scripts.analyse_campaigns import analyse
from scripts.build_manifest import (
    EVIDENCE_PATHS,
    PRODUCT_PATHS,
    SCRIPT_PATHS,
    build_manifest,
    validate_png_structure,
)
from scripts.campaign_data import load_rows
from scripts.canonicalize_public_csv import canonicalize
from scripts.prepare_data import prepare_rows, redact_campaign_name, write_csv
from scripts.validate_data import validate
from scripts.xlsx_reader import column_index

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CSV = ROOT / "data" / "meta_campaign_export_sanitized.csv"
PRIVATE_SOURCE = Path(
    os.environ.get(
        "KASHE_PRIVATE_SOURCE",
        ROOT / "data" / "private" / "30-01-23.xlsx",
    )
)


class TestPreparationHelpers(unittest.TestCase):
    def test_excel_column_index(self) -> None:
        self.assertEqual(column_index("A1"), 0)
        self.assertEqual(column_index("R129"), 17)
        self.assertEqual(column_index("AA4"), 26)

    def test_whatsapp_phone_redaction(self) -> None:
        source = "Promoting https://api.whatsapp.com/send?phone=0000000000000"
        cleaned, changed = redact_campaign_name(source)
        self.assertTrue(changed)
        self.assertEqual(
            cleaned,
            "Promoting https://api.whatsapp.com/send?phone=[REDACTED]",
        )


class TestPublishedDataset(unittest.TestCase):
    def test_public_csv_canonicalization_is_idempotent(self) -> None:
        before = PUBLIC_CSV.read_bytes()
        canonicalize(PUBLIC_CSV)
        self.assertEqual(PUBLIC_CSV.read_bytes(), before)

    def test_validation_passes(self) -> None:
        report = validate(PUBLIC_CSV)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["rows"], 126)
        self.assertEqual(report["recognized_result_rows"], 122)
        self.assertEqual(report["flagged_result_rows"], 4)
        self.assertEqual(report["missing_result_type_rows"], 4)
        self.assertEqual(report["cost_per_result_rows_reconciled"], 122)

    def test_missing_result_rows_are_preserved_and_flagged(self) -> None:
        with PUBLIC_CSV.open(encoding="utf-8", newline="") as source:
            rows = list(csv.DictReader(source))
        flagged = [row for row in rows if row["data_quality_flag"]]
        self.assertEqual(len(flagged), 4)
        self.assertTrue(
            all(row["data_quality_flag"] == "missing_result_type" for row in flagged)
        )
        self.assertTrue(all(row["result_type"] == "" for row in flagged))
        self.assertTrue(all(row["results"] == "" for row in flagged))
        self.assertTrue(all(row["cost_per_result_ngn"] == "" for row in flagged))

    def test_analysis_reproduces_published_headline_metrics(self) -> None:
        output = analyse(load_rows(PUBLIC_CSV))
        overall = output["dataset"]["overall"]
        link = output["link_click_analysis"]
        bunda = output["bunda_youtube_traffic_rows"]

        self.assertEqual(overall["impressions"], 10_332_896)
        self.assertAlmostEqual(overall["spend_ngn"], 1_029_228.11, places=2)
        self.assertEqual(link["results"], 635_240.0)
        self.assertAlmostEqual(link["weighted_cpc_ngn"], 1.4284510579, places=9)
        self.assertAlmostEqual(link["derived_link_ctr_pct"], 6.5318891282, places=9)
        self.assertEqual(bunda["results"], 565_764.0)
        self.assertAlmostEqual(bunda["weighted_cpc_ngn"], 0.6927157613, places=9)

        flagged = output["dataset"]["flagged_rows_delivery"]
        self.assertEqual(flagged["rows"], 4)
        self.assertAlmostEqual(flagged["spend_ngn"], 126.39, places=2)
        self.assertEqual(flagged["impressions"], 462)
        self.assertIsNone(flagged["results"])

        concentration = output["top_3_link_click_rows_concentration"]
        self.assertAlmostEqual(concentration["share_of_link_clicks_pct"], 94.3230904855, places=8)
        self.assertAlmostEqual(concentration["share_of_link_spend_pct"], 44.2731479760, places=8)
        self.assertAlmostEqual(concentration["share_of_link_impressions_pct"], 28.0043692625, places=8)

        without_bunda = output["link_clicks_excluding_bunda"]
        without_largest = output["link_clicks_excluding_bunda_and_pressure"]
        self.assertAlmostEqual(without_bunda["weighted_cpc_ngn"], 7.4197652427, places=8)
        self.assertAlmostEqual(without_bunda["derived_link_ctr_pct"], 0.9768921063, places=8)
        self.assertAlmostEqual(without_largest["weighted_cpc_ngn"], 14.0222563918, places=8)
        self.assertAlmostEqual(without_largest["derived_link_ctr_pct"], 0.5150443598, places=8)

    def test_bunda_name_subset_is_explicit_lower_bound(self) -> None:
        output = analyse(load_rows(PUBLIC_CSV))
        subset = output["bunda_name_lower_bound"]
        self.assertEqual(subset["all_named_rows"]["rows"], 18)
        self.assertAlmostEqual(subset["all_named_rows"]["spend_ngn"], 450_035.75, places=2)
        self.assertIsNone(subset["all_named_rows"]["results"])
        self.assertIsNone(subset["all_named_rows"]["weighted_cost_per_result_ngn"])
        self.assertEqual(subset["link_click_rows"]["results"], 568_819.0)

    def test_public_pipeline_runner_completes(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "scripts.run_pipeline", "--from-public-csv"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, msg=completed.stderr)

    def test_manifest_is_complete(self) -> None:
        manifest = build_manifest()
        self.assertEqual(set(manifest["code_sha256"]), set(SCRIPT_PATHS))
        self.assertEqual(set(manifest["evidence_sha256"]), set(EVIDENCE_PATHS))
        self.assertEqual(set(manifest["product_sha256"]), set(PRODUCT_PATHS))

    def test_public_png_evidence_is_structurally_valid(self) -> None:
        for relative in EVIDENCE_PATHS:
            with self.subTest(path=relative):
                validate_png_structure(ROOT / relative)

    def test_text_products_use_canonical_lf_line_endings(self) -> None:
        text_products = [
            ROOT / path
            for path in PRODUCT_PATHS
            if Path(path).suffix in {".json", ".svg"}
        ]
        self.assertEqual(len(text_products), 8)
        for path in text_products:
            with self.subTest(path=path.name):
                content = path.read_bytes()
                self.assertNotIn(b"\r\n", content)
                self.assertTrue(content.endswith(b"\n"))
                if path.suffix == ".svg":
                    self.assertIn(b"<svg", content)

    def test_public_products_are_stable_across_repeated_runs(self) -> None:
        def product_hashes() -> dict[str, str]:
            return {
                path: sha256((ROOT / path).read_bytes()).hexdigest()
                for path in PRODUCT_PATHS
            }

        subprocess.run(
            [sys.executable, "-m", "scripts.run_pipeline", "--from-public-csv"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        first = product_hashes()
        subprocess.run(
            [sys.executable, "-m", "scripts.run_pipeline", "--from-public-csv"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(product_hashes(), first)


@unittest.skipUnless(PRIVATE_SOURCE.exists(), "Private original workbook is not present")
class TestEndToEndPreparationWithPrivateSource(unittest.TestCase):
    def test_private_source_recreates_public_csv(self) -> None:
        rows, summary = prepare_rows(PRIVATE_SOURCE)
        self.assertEqual(summary["campaign_rows_prepared"], 126)
        self.assertEqual(summary["phone_redactions"], 1)
        self.assertEqual(summary["missing_result_type_rows"], 4)

        with tempfile.TemporaryDirectory() as tmp:
            regenerated = Path(tmp) / "regenerated.csv"
            write_csv(rows, regenerated)
            source_report = validate(regenerated)
            public_report = validate(PUBLIC_CSV)
            self.assertEqual(source_report["status"], "pass")
            self.assertEqual(
                source_report["semantic_fingerprint_sha256"],
                public_report["semantic_fingerprint_sha256"],
            )


if __name__ == "__main__":
    unittest.main()
