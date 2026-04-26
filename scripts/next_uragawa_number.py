#!/usr/bin/env python3
"""Print the next available adopted Uragawa Zukan number."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


NO_RE = re.compile(r"^No\.(\d{3})$")


def next_number(path: Path) -> str:
    if not path.exists():
        return "No.001"

    used: list[int] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            match = NO_RE.match((row.get("id") or row.get("No") or "").strip())
            if match:
                used.append(int(match.group(1)))

    if not used:
        return "No.001"
    return f"No.{max(used) + 1:03d}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        default="data/uragawa_ledger.tsv",
        help="Path to the ledger TSV",
    )
    args = parser.parse_args()
    print(next_number(Path(args.ledger)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
