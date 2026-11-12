"""Small, auditable campaign analytics for the public synthetic demo."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Record:
    day: date
    campaign: str
    product: str
    spend: float
    sales: float
    orders: int
    clicks: int
    impressions: int

    def __post_init__(self) -> None:
        if not self.campaign or not self.product:
            raise ValueError("campaign and product must be present")
        if min(self.spend, self.sales, self.orders, self.clicks, self.impressions) < 0:
            raise ValueError("metrics cannot be negative")
        if self.clicks > self.impressions:
            raise ValueError("clicks cannot exceed impressions")
        if self.orders > self.clicks:
            raise ValueError("orders cannot exceed clicks")


def load_csv(path: str | Path) -> list[Record]:
    with open(path, newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        required = {"day", "campaign", "product", "spend", "sales", "orders", "clicks", "impressions"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain: {', '.join(sorted(required))}")
        return [Record(date.fromisoformat(row["day"]), row["campaign"], row["product"],
                       float(row["spend"]), float(row["sales"]), int(row["orders"]),
                       int(row["clicks"]), int(row["impressions"])) for row in reader]


def write_csv(records: list[Record], path: str | Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for record in records:
            writer.writerow({**asdict(record), "day": record.day.isoformat()})


def summarize(records: list[Record]) -> list[dict]:
    groups: dict[str, dict] = {}
    for record in records:
        item = groups.setdefault(record.campaign, {"campaign": record.campaign, "spend": 0.0,
                                                   "sales": 0.0, "orders": 0, "clicks": 0,
                                                   "impressions": 0})
        for key in ("spend", "sales", "orders", "clicks", "impressions"):
            item[key] += getattr(record, key)
    result = []
    for item in groups.values():
        item["spend"] = round(item["spend"], 2)
        item["sales"] = round(item["sales"], 2)
        item["acos"] = round(item["spend"] / item["sales"], 4) if item["sales"] else None
        item["roas"] = round(item["sales"] / item["spend"], 4) if item["spend"] else None
        item["ctr"] = round(item["clicks"] / item["impressions"], 4) if item["impressions"] else None
        result.append(item)
    return sorted(result, key=lambda item: (-item["spend"], item["campaign"]))


def opportunities(records: list[Record], *, min_spend: float = 20.0,
                  max_acos: float = 0.35) -> list[dict]:
    """Illustrative rules for this demo, not LAILOW's private rules engine."""
    if min_spend < 0 or max_acos < 0:
        raise ValueError("thresholds must be nonnegative")
    findings = []
    for item in summarize(records):
        if item["spend"] >= min_spend and item["sales"] == 0:
            findings.append({"campaign": item["campaign"], "signal": "spend_without_sales",
                             "spend": item["spend"], "acos": None})
        elif item["acos"] is not None and item["acos"] > max_acos:
            findings.append({"campaign": item["campaign"], "signal": "high_acos",
                             "spend": item["spend"], "acos": item["acos"]})
    return sorted(findings, key=lambda item: (-item["spend"], item["campaign"]))

