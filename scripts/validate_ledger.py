#!/usr/bin/env python3
"""Validate the Uragawa Zukan ledger TSV."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


EXPECTED_HEADER = [
    "id",
    "title",
    "category",
    "motif",
    "visual_strategy",
    "target_products",
    "status",
    "score",
    "continuity_links",
    "created_at",
    "notes",
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

VALID_CATEGORIES = {
    "",
    "生き物",
    "植物・菌類",
    "食べ物",
    "道具・日用品",
    "自然・場所",
    "質感・概念",
    "その他",
}

VALID_STRATEGIES = {
    "",
    "Character Icon",
    "World Object",
    "Relationship Pair",
    "Scene Emblem",
    "Pattern Seed",
}

ID_RE = re.compile(r"^No\.\d{3}$")
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

        seen_ids: set[str] = set()
        seen_titles: set[str] = set()
        previous_number = 0

        for index, row in enumerate(reader, start=2):
            if not any(value.strip() for value in row.values()):
                errors.append(f"line {index}: empty row")
                continue

            entry_id = row["id"].strip()
            title = row["title"].strip()
            category = row["category"].strip()
            strategy = row["visual_strategy"].strip()
            status = row["status"].strip()
            created = row["created_at"].strip()
            score = row["score"].strip()

            if entry_id:
                if not ID_RE.match(entry_id):
                    errors.append(f"line {index}: invalid id format: {entry_id}")
                elif entry_id in seen_ids:
                    errors.append(f"line {index}: duplicate id: {entry_id}")
                else:
                    seen_ids.add(entry_id)
                    numeric = int(entry_id.split(".")[1])
                    if numeric <= previous_number:
                        errors.append(f"line {index}: id must increase monotonically")
                    previous_number = numeric

            if not title:
                errors.append(f"line {index}: missing title")
            elif title in seen_titles:
                errors.append(f"line {index}: duplicate title: {title}")
            else:
                seen_titles.add(title)

            if category not in VALID_CATEGORIES:
                errors.append(f"line {index}: invalid category: {category}")

            if strategy not in VALID_STRATEGIES:
                errors.append(f"line {index}: invalid visual_strategy: {strategy}")

            if status not in VALID_STATUSES:
                errors.append(f"line {index}: invalid status: {status}")

            if entry_id and status not in {"adopted", "merch_candidate", "merch_ready", "retired"}:
                errors.append(f"line {index}: numbered entries should be adopted or later")

            if created and not DATE_RE.match(created):
                errors.append(f"line {index}: created_at must be YYYY-MM-DD")

            if score:
                try:
                    numeric_score = int(score)
                except ValueError:
                    errors.append(f"line {index}: score must be an integer")
                else:
                    if not 0 <= numeric_score <= 22:
                        errors.append(f"line {index}: score must be 0-22")

            if status in {"adopted", "merch_candidate", "merch_ready"}:
                for field in ["motif", "category", "visual_strategy", "target_products"]:
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
