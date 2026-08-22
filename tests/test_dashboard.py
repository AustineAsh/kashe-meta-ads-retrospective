from __future__ import annotations

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from scripts.dashboard_data import compact_number, load_dashboard_model

ROOT = Path(__file__).resolve().parents[1]


class TestDashboardModel(unittest.TestCase):
    def test_headline_uses_published_analysis(self) -> None:
        model = load_dashboard_model()
        headline = model["headline"]
        self.assertEqual(headline["campaign_rows"], 126)
        self.assertEqual(headline["link_clicks"], 635_240)
        self.assertAlmostEqual(headline["spend_ngn"], 1_029_228.11, places=2)
        self.assertAlmostEqual(headline["top_three_click_share_pct"], 94.3230904855)

    def test_contribution_is_complete(self) -> None:
        model = load_dashboard_model()
        for item in model["contribution"]:
            self.assertAlmostEqual(
                float(item["top_three_pct"]) + float(item["remaining_pct"]),
                100.0,
            )

    def test_sensitivity_preserves_expected_order(self) -> None:
        model = load_dashboard_model()
        cpc = [float(item["weighted_cpc_ngn"]) for item in model["sensitivity"]]
        ctr = [float(item["derived_ctr_pct"]) for item in model["sensitivity"]]
        self.assertEqual(cpc, sorted(cpc))
        self.assertEqual(ctr, sorted(ctr, reverse=True))

    def test_campaign_detail_is_ranked(self) -> None:
        model = load_dashboard_model()
        clicks = [int(item["Link clicks"]) for item in model["campaign_detail"]]
        self.assertEqual(len(clicks), 106)
        self.assertEqual(clicks, sorted(clicks, reverse=True))

    def test_compact_number(self) -> None:
        self.assertEqual(compact_number(10_332_896), "10.33m")
        self.assertEqual(compact_number(635_240), "635.2k")
        self.assertEqual(compact_number(86), "86")

    def test_streamlit_app_renders_without_exceptions(self) -> None:
        app = AppTest.from_file(ROOT / "dashboard.py", default_timeout=20).run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(
            [tab.label for tab in app.tabs],
            ["Decision brief", "Campaign detail", "Evidence boundary"],
        )
        self.assertIn(
            "Future campaign measurement plan",
            [heading.value for heading in app.subheader],
        )
        action_markup = "\n".join(item.value for item in app.markdown)
        self.assertIn("Executive summary", action_markup)
        self.assertIn("Business implication", action_markup)
        self.assertIn("Recommended action", action_markup)
        self.assertIn("Evidence limit", action_markup)
        self.assertIn("01 / PLAN", action_markup)
        self.assertIn("02 / INSTRUMENT", action_markup)
        self.assertIn("03 / RUN &amp; LEARN", action_markup)
        self.assertEqual(len(app.dataframe), 1)


if __name__ == "__main__":
    unittest.main()
