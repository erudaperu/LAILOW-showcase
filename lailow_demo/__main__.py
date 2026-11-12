"""Run: python -m lailow_demo [--csv PATH] [--json] [--write-sample PATH]."""

import argparse
import json

from .analytics import load_csv, opportunities, summarize, write_csv
from .sample import make_sample


def main() -> None:
    parser = argparse.ArgumentParser(description="LAILOW synthetic campaign analytics demo")
    parser.add_argument("--csv", help="Read records from a CSV with the documented demo schema")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    parser.add_argument("--write-sample", metavar="PATH", help="Write the fictional fixture to CSV")
    args = parser.parse_args()

    records = load_csv(args.csv) if args.csv else make_sample()
    if args.write_sample:
        write_csv(make_sample(), args.write_sample)
    summary, findings = summarize(records), opportunities(records)
    if args.json:
        print(json.dumps({"data_source": "user CSV" if args.csv else "synthetic sample",
                          "records": len(records), "campaigns": summary, "opportunities": findings}, indent=2))
        return
    print(f"LAILOW / SYNTHETIC SIGNAL REPORT   •   {len(records)} records")
    print("CAMPAIGN                 SPEND      SALES      ACOS     ROAS")
    for item in summary:
        acos = f"{item['acos']:.1%}" if item["acos"] is not None else "—"
        roas = f"{item['roas']:.2f}x" if item["roas"] is not None else "—"
        print(f"{item['campaign']:<24} ${item['spend']:>7.2f}   ${item['sales']:>7.2f}   {acos:>7}   {roas:>5}")
    print("\nREVIEW SIGNALS")
    for item in findings:
        print(f"• {item['campaign']}: {item['signal'].replace('_', ' ')}")
    if not findings:
        print("• No campaigns crossed the illustrative thresholds")
    print("\nFictional data and illustrative rules. No real business data.")


if __name__ == "__main__":
    main()
