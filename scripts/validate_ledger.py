#!/usr/bin/env python3
"""Validate the Uragawa Zukan ledger TSV."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


EXPECTED_HEADER = [
    "No",
    "存在名",
    "モチーフ",
    "現実との接続点",
    "架空の裏事情",
    "反応の方向",
    "ビジュアルの核",
    "商品向き",
    "関連",
    "状態",
    "作成日",
]

VALID_STATUSES = {
    "",
    "idea",
    "draft",
    "image_prompted",
    "image_reviewed",
    "sns_test",
    "adopted",
    "merch_candidate",
    "merch_ready",
    "retired",
}

NO_RE = re.compile(r"^No\.\d{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_ledger(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"file not found: {path}"]

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != EXPECTED_HEADER:
            errors.append("header mismatch")
            errors.append(f"expected: {EXPECTED_HEADER}")
            errors.append(f"actual: {reader.fieldnames}")
            return errors

        seen_numbers: set[str] = set()
        seen_names: set[str] = set()
        previous_number = 0

        for index, row in enumerate(reader, start=2):
            no = row["No"].strip()
            name = row["存在名"].strip()
            status = row["状態"].strip()
            created = row["作成日"].strip()

            if not any(value.strip() for value in row.values()):
                errors.append(f"line {index}: empty row")
                continue

            if no:
                if not NO_RE.match(no):
                    errors.append(f"line {index}: invalid No format: {no}")
                elif no in seen_numbers:
                    errors.append(f"line {index}: duplicate No: {no}")
                else:
                    seen_numbers.add(no)
                    numeric = int(no.split(".")[1])
                    if numeric <= previous_number:
                        errors.append(f"line {index}: No must increase monotonically")
                    previous_number = numeric

            if not name:
                errors.append(f"line {index}: missing 存在名")
            elif name in seen_names:
                errors.append(f"line {index}: duplicate 存在名: {name}")
            else:
                seen_names.add(name)

            if status not in VALID_STATUSES:
                errors.append(f"line {index}: invalid 状態: {status}")

            if no and status not in {"adopted", "merch_candidate", "merch_ready", "retired"}:
                errors.append(f"line {index}: numbered entries should be adopted or later")

            if created and not DATE_RE.match(created):
                errors.append(f"line {index}: 作成日 must be YYYY-MM-DD")

            if status in {"adopted", "merch_candidate", "merch_ready"}:
                for field in ["モチーフ", "現実との接続点", "架空の裏事情", "反応の方向", "ビジュアルの核"]:
                    if not row[field].strip():
                        errors.append(f"line {index}: adopted entries need {field}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="data/uragawa_ledger.tsv")
    args = parser.parse_args()

    errors = validate_ledger(Path(args.path))
    if errors:
        print(f"{args.path}: invalid")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"{args.path}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
