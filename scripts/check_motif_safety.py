#!/usr/bin/env python3
"""Check motif safety terms in candidate files and TSV records.

By default this scans structured motif/category fields instead of full policy
documents, so docs that list blocked terms as rules do not fail the check.
Use --raw only when intentionally scanning arbitrary text.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


BLOCK_TERMS = ["蜘蛛", "蛾", "ゴキブリ", "ハエ", "蚊", "ムカデ", "毛虫"]
CAUTION_TERMS = ["アリ", "幼虫", "芋虫", "虫", "寄生", "卵", "群がり", "複眼"]
ALLOW_TERMS = ["蝶", "カタツムリ", "ダンゴムシ", "てんとう虫"]

STRUCTURED_LABELS = [
    "カテゴリ",
    "モチーフ",
    "主役題材としての適性",
    "避ける弱い表現",
    "メインビジュアル",
    "リスク",
]

TSV_FIELD_CANDIDATES = [
    "category",
    "カテゴリ",
    "motif",
    "モチーフ",
    "risk_notes",
    "リスク",
    "comment",
    "コメント",
]


def find_terms(text: str) -> tuple[list[str], list[str]]:
    blocked = sorted({term for term in BLOCK_TERMS if term in text})
    cautions = sorted(
        {
            term
            for term in CAUTION_TERMS
            if term in text and not any(allowed in text for allowed in ALLOW_TERMS)
        }
    )
    return blocked, cautions


def markdown_context(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        for label in STRUCTURED_LABELS:
            if stripped.startswith(f"- {label}：") or stripped.startswith(f"- {label}:"):
                lines.append(stripped)
    return "\n".join(lines)


def tsv_context(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames:
            return ""
        fields = [field for field in reader.fieldnames if field in TSV_FIELD_CANDIDATES]
        parts: list[str] = []
        for row in reader:
            parts.extend(row.get(field, "") for field in fields)
        return "\n".join(parts)


def structured_context(path: Path, raw: bool) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if raw:
        return text, "raw"
    if path.suffix.lower() == ".tsv":
        return tsv_context(path), "structured-tsv"
    if path.suffix.lower() in {".md", ".markdown"}:
        context = markdown_context(text)
        if context:
            return context, "structured-md"
    return "", "no-structured-fields"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--raw", action="store_true", help="scan the entire file text")
    args = parser.parse_args()

    had_block = False
    for raw_path in args.paths:
        path = Path(raw_path)
        context, mode = structured_context(path, args.raw)
        if not context.strip():
            print(f"{path}: skipped ({mode})")
            continue

        blocked, cautions = find_terms(context)
        if blocked or cautions:
            print(f"{path}: motif safety warnings ({mode})")
            if blocked:
                had_block = True
                print("- 控える主役候補: " + ", ".join(blocked))
            if cautions:
                print("- 注意語: " + ", ".join(cautions))
        else:
            print(f"{path}: ok ({mode})")

    if args.strict and had_block:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
