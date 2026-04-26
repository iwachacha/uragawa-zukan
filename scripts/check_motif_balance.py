#!/usr/bin/env python3
"""Report motif category balance and suggest next categories."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


TARGETS_PATH = Path("data/motif_balance_targets.tsv")
MEMORY_PATH = Path("data/style_memory.tsv")


def read_targets(path: Path) -> dict[str, dict[str, float | str]]:
    targets: dict[str, dict[str, float | str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            targets[row["カテゴリ"]] = {
                "target": float(row["目標割合"]),
                "max": float(row["直近上限割合"]),
                "priority": row["優先度"],
            }
    return targets


def read_memory(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", default=str(MEMORY_PATH))
    parser.add_argument("--targets", default=str(TARGETS_PATH))
    parser.add_argument("--window", type=int, default=10)
    parser.add_argument("--strict", action="store_true", help="Exit 1 when any category exceeds its recent max ratio")
    args = parser.parse_args()

    targets = read_targets(Path(args.targets))
    rows = read_memory(Path(args.memory))
    recent = rows[-args.window :]
    total = len(recent)

    print(f"対象件数: {total} / window={args.window}")
    if total == 0:
        print("履歴が空です。優先: 生き物, 植物・菌類")
        return 0

    counts = Counter(row.get("カテゴリ", "") for row in recent)
    over: list[str] = []
    under: list[tuple[float, str]] = []

    for category, info in targets.items():
        count = counts.get(category, 0)
        ratio = count / total
        target = float(info["target"])
        max_ratio = float(info["max"])
        print(f"{category}: {count}件 ({ratio:.0%}) / target {target:.0%} / max {max_ratio:.0%}")
        if ratio > max_ratio:
            over.append(category)
        if ratio < target:
            under.append((target - ratio, category))

    if over:
        print("過多カテゴリ: " + ", ".join(over))
    else:
        print("過多カテゴリ: なし")

    under.sort(reverse=True)
    suggestions = [category for _, category in under[:3]]

    if "道具・日用品" in over:
        suggestions = [category for category in suggestions if category != "道具・日用品"]
        for preferred in ["生き物", "植物・菌類"]:
            if preferred not in suggestions:
                suggestions.insert(0, preferred)
        suggestions = suggestions[:3]

    print("推奨次カテゴリ: " + ", ".join(suggestions or ["生き物", "植物・菌類"]))

    if "道具・日用品" in over:
        print("注意: 道具・日用品が過多です。次回は主役級の生き物または植物・菌類を優先してください。")

    if args.strict and over:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
