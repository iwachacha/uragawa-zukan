#!/usr/bin/env python3
"""Report motif category balance and suggest next categories."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


TARGETS_PATH = Path("data/motif_balance_targets.tsv")
TAXONOMY_PATH = Path("data/motif_taxonomy.tsv")
MEMORY_PATH = Path("data/style_memory.tsv")
IDEA_BANK_PATH = Path("data/idea_bank.tsv")


def read_targets(path: Path, taxonomy: Path) -> dict[str, dict[str, float | str]]:
    targets: dict[str, dict[str, float | str]] = {}

    if taxonomy.exists():
        with taxonomy.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                category = row.get("category", "").strip()
                if not category:
                    continue
                targets[category] = {
                    "target": float(row.get("target_ratio") or 0),
                    "max": float(row.get("max_recent_ratio") or 1),
                    "priority": row.get("priority", ""),
                    "role": row.get("role", ""),
                }
        if targets:
            return targets

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            category = row["カテゴリ"]
            targets[category] = {
                "target": float(row["目標割合"]),
                "max": float(row["直近上限割合"]),
                "priority": row["優先度"],
                "role": row.get("主役適性メモ", ""),
            }
    return targets


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def memory_categories(path: Path) -> list[str]:
    rows = read_rows(path)
    return [row.get("カテゴリ", "").strip() for row in rows if row.get("カテゴリ", "").strip()]


def idea_categories(path: Path) -> list[str]:
    rows = read_rows(path)
    ignored_statuses = {"reject", "rejected", "却下"}
    categories: list[str] = []
    for row in rows:
        status = row.get("status", "").strip()
        if status in ignored_statuses:
            continue
        category = row.get("category", "").strip()
        if category:
            categories.append(category)
    return categories


def suggest_categories(
    targets: dict[str, dict[str, float | str]],
    counts: Counter[str],
    total: int,
    over: list[str],
) -> list[str]:
    under: list[tuple[float, str]] = []
    for category, info in targets.items():
        ratio = counts.get(category, 0) / total if total else 0
        target = float(info["target"])
        if ratio < target:
            under.append((target - ratio, category))
    under.sort(reverse=True)
    suggestions = [category for _, category in under[:3]]

    if "道具・日用品" in over:
        suggestions = [category for category in suggestions if category != "道具・日用品"]
        for preferred in ["植物・菌類", "生き物"]:
            if preferred not in suggestions:
                suggestions.insert(0, preferred)
        suggestions = suggestions[:3]

    return suggestions or ["生き物", "植物・菌類"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", default=str(MEMORY_PATH))
    parser.add_argument("--ideas", default=str(IDEA_BANK_PATH))
    parser.add_argument("--targets", default=str(TARGETS_PATH))
    parser.add_argument("--taxonomy", default=str(TAXONOMY_PATH))
    parser.add_argument("--window", type=int, default=10)
    parser.add_argument("--include-ideas", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit 1 when any category exceeds its recent max ratio")
    args = parser.parse_args()

    targets = read_targets(Path(args.targets), Path(args.taxonomy))
    categories = memory_categories(Path(args.memory))
    source_note = "style_memory"
    if args.include_ideas:
        categories.extend(idea_categories(Path(args.ideas)))
        source_note += " + idea_bank"

    recent = categories[-args.window :]
    total = len(recent)

    print(f"対象件数: {total} / window={args.window} / source={source_note}")
    if total == 0:
        print("履歴が空です。優先: 生き物, 植物・菌類")
        return 0

    counts = Counter(recent)
    over: list[str] = []

    for category, info in targets.items():
        count = counts.get(category, 0)
        ratio = count / total
        target = float(info["target"])
        max_ratio = float(info["max"])
        priority = info.get("priority", "")
        role = info.get("role", "")
        print(f"{category}: {count}件 ({ratio:.0%}) / target {target:.0%} / max {max_ratio:.0%} / {priority} / {role}")
        if ratio > max_ratio:
            over.append(category)

    if over:
        print("過多カテゴリ: " + ", ".join(over))
    else:
        print("過多カテゴリ: なし")

    suggestions = suggest_categories(targets, counts, total, over)
    print("推奨次カテゴリ: " + ", ".join(suggestions))

    if "道具・日用品" in over:
        print("注意: 道具・日用品が過多です。次回は主役級の生き物または植物・菌類を優先してください。")

    if args.strict and over:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
