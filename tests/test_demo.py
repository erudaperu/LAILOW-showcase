import tempfile
import unittest
from datetime import date
from pathlib import Path

from lailow_demo.analytics import Record, load_csv, opportunities, summarize, write_csv
from lailow_demo.sample import make_sample


def record(spend=10, sales=20, orders=1, clicks=2, impressions=100, campaign="A"):
    return Record(date(2026, 1, 1), campaign, "Fixture", spend, sales, orders, clicks, impressions)


class DemoTests(unittest.TestCase):
    def test_sample_is_deterministic(self):
        self.assertEqual(make_sample(), make_sample())

    def test_sample_has_42_fictional_rows(self):
        self.assertEqual(len(make_sample()), 42)

    def test_summary_aggregates_by_campaign(self):
        item = summarize([record(spend=10), record(spend=5)])[0]
        self.assertEqual((item["spend"], item["sales"], item["orders"]), (15, 40, 2))

    def test_summary_sorts_by_spend(self):
        self.assertEqual(summarize([record(spend=1), record(spend=4, campaign="B")])[0]["campaign"], "B")

    def test_zero_sales_has_undefined_acos(self):
        self.assertIsNone(summarize([record(sales=0, orders=0)])[0]["acos"])

    def test_zero_spend_has_undefined_roas(self):
        self.assertIsNone(summarize([record(spend=0)])[0]["roas"])

    def test_zero_impressions_has_undefined_ctr(self):
        self.assertIsNone(summarize([record(clicks=0, impressions=0, orders=0)])[0]["ctr"])

    def test_spend_without_sales_signal(self):
        result = opportunities([record(spend=25, sales=0, orders=0)])
        self.assertEqual(result[0]["signal"], "spend_without_sales")

    def test_high_acos_signal(self):
        self.assertEqual(opportunities([record(spend=10, sales=20)])[0]["signal"], "high_acos")

    def test_threshold_boundary_is_not_high_acos(self):
        self.assertEqual(opportunities([record(spend=35, sales=100)]), [])

    def test_invalid_metric_relationship_rejected(self):
        with self.assertRaises(ValueError):
            record(clicks=101, impressions=100)

    def test_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.csv"
            rows = make_sample()
            write_csv(rows, path)
            self.assertEqual(load_csv(path), rows)


if __name__ == "__main__":
    unittest.main()

