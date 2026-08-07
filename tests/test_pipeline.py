from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from scripts.analyse_campaigns import analyse
from scripts.campaign_data import load_rows
from scripts.canonicalize_public_csv import canonicalize
from scripts.prepare_data import prepare_rows, redact_campaign_name, write_csv
from scripts.validate_data import validate
from scripts.xlsx_reader import column_index

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CSV = ROOT / "data" / "meta_campaign_export_sanitized.csv"
PRIVATE_SOURCE = ROOT / "data" / "private" / "30-01-23.xlsx"


class TestPreparationHelpers(unittest.TestCase):
    def test_excel_column_index(self) -> None:
        self.assertEqual(column_index("A1"), 0)
        self.assertEqual(column_index("R129"), 17)
        self.assertEqual(column_index("AA4"), 26)

    def test_whatsapp_phone_redaction(self) -> None:
        source = "Promoting https://api.whatsapp.com/send?phone=2348142618972"
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

    def test_bunda_name_subset_is_explicit_lower_bound(self) -> None:
        output = analyse(load_rows(PUBLIC_CSV))
        subset = output["bunda_name_lower_bound"]
        self.assertEqual(subset["all_named_rows"]["rows"], 18)
        self.assertAlmostEqual(subset["all_named_rows"]["spend_ngn"], 450_035.75, places=2)
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
