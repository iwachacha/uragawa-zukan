#!/usr/bin/env python3
"""Warn about motif terms that are risky for the current audience strategy."""

from __future__ import annotations

import argparse
from pathlib import Path


BLOCK_TERMS = ["蜘蛛", "蛾", "ゴキブリ", "ハエ", "蚊", "ムカデ", "毛虫"]
CAUTION_TERMS = ["アリ", "幼虫", "芋虫", "虫", "寄生", "卵", "群がり", "複眼"]
ALLOW_TERMS = ["蝶", "カタツムリ", "ダンゴムシ", "てんとう虫"]


def check_text(text: str) -> tuple[list[str], list[str]]:
    blocked = [term for term in BLOCK_TERMS if term in text]
    cautions = [term for term in CAUTION_TERMS if term in text and term not in ALLOW_TERMS]
    return blocked, cautions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    had_block = False
    for raw_path in args.paths:
        path = Path(raw_path)
        text = path.read_text(encoding="utf-8")
        blocked, cautions = check_text(text)
        if blocked or cautions:
            print(f"{path}: motif safety warnings")
            if blocked:
                had_block = True
                print("- 控える主役候補: " + ", ".join(blocked))
            if cautions:
                print("- 注意語: " + ", ".join(cautions))
        else:
            print(f"{path}: ok")

    if args.strict and had_block:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
