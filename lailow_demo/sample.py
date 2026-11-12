"""Deterministic fictional records. No production fields or customer data."""

from datetime import date, timedelta

from .analytics import Record


def make_sample() -> list[Record]:
    scenarios = [
        ("ORBIT / Discovery", "Item A", 16.0, 27.0, 2),
        ("ORBIT / Exact", "Item B", 22.0, 39.0, 3),
        ("NOVA / Exploration", "Item C", 25.0, 0.0, 0),
    ]
    rows = []
    for index in range(14):
        for campaign, product, base_spend, unit_price, base_orders in scenarios:
            spend = round(base_spend + (index % 4) * 1.75, 2)
            orders = max(0, base_orders + (1 if index % 3 == 0 else 0) - (1 if index % 5 == 0 else 0))
            if unit_price == 0:
                orders = 0
            clicks = 18 + (index % 5) + base_orders * 2
            rows.append(Record(date(2026, 1, 1) + timedelta(days=index), campaign, product,
                               spend, round(orders * unit_price, 2), orders, clicks,
                               750 + index * 13 + base_orders * 40))
    return rows

