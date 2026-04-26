#!/usr/bin/env python3
"""Validate style memory TSV rows."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


EXPECTED_HEADER = ["日付", "存在名", "カテゴリ", "モチーフ", "反応方向", "視覚トリック", "色方向", "商品向き", "メモ"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_CATEGORIES = {
    "生き物",
    "植物・菌類",
    "食べ物",
    "道具・日用品",
    "自然・場所",
    "質感・概念",
    "その他",
}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"file not found: {path}"]

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != EXPECTED_HEADER:
            return [f"header mismatch: {reader.fieldnames}"]

        seen: set[tuple[str, str]] = set()
        for index, row in enumerate(reader, start=2):
            if not any(value.strip() for value in row.values()):
                errors.append(f"line {index}: empty row")
                continue

            date = row["日付"].strip()
            name = row["存在名"].strip()
            category = row["カテゴリ"].strip()
            motif = row["モチーフ"].strip()
            trick = row["視覚トリック"].strip()

            if not DATE_RE.match(date):
                errors.append(f"line {index}: 日付 must be YYYY-MM-DD")
            if not name:
                errors.append(f"line {index}: missing 存在名")
            if category not in VALID_CATEGORIES:
                errors.append(f"line {index}: invalid カテゴリ: {category}")
            if not motif:
                errors.append(f"line {index}: missing モチーフ")
            if not trick:
                errors.append(f"line {index}: missing 視覚トリック")

            key = (date, name)
            if key in seen:
                errors.append(f"line {index}: duplicate date/name pair: {date} {name}")
            seen.add(key)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="data/style_memory.tsv")
    args = parser.parse_args()
    errors = validate(Path(args.path))
    if errors:
        print(f"{args.path}: invalid")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{args.path}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
