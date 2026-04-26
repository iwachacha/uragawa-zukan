#!/usr/bin/env python3
"""Validate idea bank and selection feedback TSV files."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


IDEA_HEADER = [
    "idea_id",
    "date",
    "status",
    "category",
    "motif",
    "real_connection",
    "hidden_circumstance",
    "visual_hook",
    "target_audience",
    "product_strategy",
    "risk_notes",
    "source_batch",
]

FEEDBACK_HEADER = [
    "idea_id",
    "date",
    "decision",
    "reason_tags",
    "comment",
    "promoted_to",
]

VALID_CATEGORIES = {
    "生き物",
    "植物・菌類",
    "食べ物",
    "道具・日用品",
    "自然・場所",
    "質感・概念",
    "その他",
}

VALID_IDEA_STATUSES = {"idea", "hold", "promoted", "rejected", "保留", "採用", "却下"}
VALID_DECISIONS = {"good", "bad", "interesting", "adopt", "hold", "reject", "良い", "悪い", "気になる", "採用", "保留", "却下"}
IDEA_ID_RE = re.compile(r"^I-\d{8}-\d{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def read_tsv(path: Path, expected_header: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    if not path.exists():
        return [], [f"file not found: {path}"]
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != expected_header:
            return [], [f"{path}: header mismatch: {reader.fieldnames}"]
        return list(reader), errors


def validate_ideas(path: Path) -> tuple[set[str], list[str]]:
    rows, errors = read_tsv(path, IDEA_HEADER)
    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        idea_id = row["idea_id"].strip()
        if not IDEA_ID_RE.match(idea_id):
            errors.append(f"{path}: line {index}: invalid idea_id: {idea_id}")
        if idea_id in seen:
            errors.append(f"{path}: line {index}: duplicate idea_id: {idea_id}")
        seen.add(idea_id)

        date = row["date"].strip()
        if date and not DATE_RE.match(date):
            errors.append(f"{path}: line {index}: date must be YYYY-MM-DD")

        status = row["status"].strip()
        if status and status not in VALID_IDEA_STATUSES:
            errors.append(f"{path}: line {index}: invalid status: {status}")

        category = row["category"].strip()
        if category and category not in VALID_CATEGORIES:
            errors.append(f"{path}: line {index}: invalid category: {category}")

        for field in ["motif", "real_connection", "hidden_circumstance", "visual_hook", "product_strategy"]:
            if status not in {"rejected", "却下"} and not row[field].strip():
                errors.append(f"{path}: line {index}: missing {field}")
    return seen, errors


def validate_feedback(path: Path, known_ids: set[str]) -> list[str]:
    rows, errors = read_tsv(path, FEEDBACK_HEADER)
    seen: set[tuple[str, str]] = set()
    for index, row in enumerate(rows, start=2):
        idea_id = row["idea_id"].strip()
        date = row["date"].strip()
        decision = row["decision"].strip()

        if not IDEA_ID_RE.match(idea_id):
            errors.append(f"{path}: line {index}: invalid idea_id: {idea_id}")
        elif known_ids and idea_id not in known_ids:
            errors.append(f"{path}: line {index}: idea_id not found in idea bank: {idea_id}")

        if date and not DATE_RE.match(date):
            errors.append(f"{path}: line {index}: date must be YYYY-MM-DD")

        if decision not in VALID_DECISIONS:
            errors.append(f"{path}: line {index}: invalid decision: {decision}")

        key = (idea_id, date)
        if key in seen:
            errors.append(f"{path}: line {index}: duplicate feedback for {idea_id} on {date}")
        seen.add(key)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ideas", default="data/idea_bank.tsv")
    parser.add_argument("--feedback", default="data/selection_feedback.tsv")
    args = parser.parse_args()

    known_ids, errors = validate_ideas(Path(args.ideas))
    errors.extend(validate_feedback(Path(args.feedback), known_ids))

    if errors:
        print("idea workflow data: invalid")
        for error in errors:
            print(f"- {error}")
        return 1

    print("idea workflow data: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

