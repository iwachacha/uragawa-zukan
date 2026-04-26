#!/usr/bin/env python3
"""Validate a Uragawa Zukan observation markdown file.

This is a lightweight structural check. It does not judge creativity; it catches
missing sections before image generation or archiving.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path


REQUIRED_HEADINGS = [
    "## 構想メモ",
    "## ウラガワ図鑑",
    "## ビジュアル設計",
    "## 画像生成プロンプト",
    "## SNS投稿文",
    "## SUZURI商品化メモ",
    "## 存在台帳登録用",
]

REQUIRED_MEMO_LABELS = [
    "カテゴリ",
    "モチーフ",
    "現実との接続点",
    "架空の裏事情",
    "反応の方向",
    "ビジュアルの核",
]

REQUIRED_VISUAL_LABELS = [
    "絵だけで伝えるべき意外性",
    "現実との接続を見せる要素",
    "裏事情の表現方法",
    "視覚的な主役",
    "画面内で起きている行動",
    "誰に刺す魅力",
    "想定ターゲット",
    "少し尖らせるポイント",
    "主役題材としての適性",
    "推奨商品フォーマット",
    "画像戦略タイプ",
    "背景の扱い",
    "描き込み範囲",
    "主役と周辺物のスケール",
    "ステッカーにしたときの外形",
    "避ける弱い表現",
    "商品化で映えるポイント",
]

PROMPT_HINTS = [
    "[GOAL]",
    "[SUBJECT]",
    "[ACTION]",
    "[HIDDEN SIDE]",
    "[COMPOSITION]",
    "[STYLE]",
    "[ACCENT]",
    "[AVOID]",
    "primary format:",
    "secondary use:",
    "visual strategy:",
    "background:",
    "relative scale:",
    "target product:",
    "master canvas:",
]

LEDGER_RE = re.compile(r"^No\.(?:XXX|\d{3})｜[^｜]+｜[^｜]+｜[^｜]+｜[^｜]+$", re.MULTILINE)
TITLE_RE = re.compile(r"^# (?:登録候補|No\.(?:XXX|\d{3}))｜.+", re.MULTILINE)


def validate_text(text: str) -> list[str]:
    errors: list[str] = []

    if not TITLE_RE.search(text):
        errors.append("title must start with '# 登録候補｜...' or '# No.001｜...'")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    for label in REQUIRED_MEMO_LABELS:
        if label not in text:
            errors.append(f"missing concept memo label: {label}")

    for label in REQUIRED_VISUAL_LABELS:
        if label not in text:
            errors.append(f"missing visual design label: {label}")

    if not LEDGER_RE.search(text):
        errors.append("missing ledger line: No.XXX｜存在名｜モチーフ｜特徴｜小話")

    if "かわいい" in text and "ただのかわいい" not in text and "甘すぎ" not in text:
        errors.append("mentions 'かわいい' but does not show a guard against ending as only cute")

    if "## 画像生成プロンプト" in text:
        for hint in PROMPT_HINTS:
            if hint not in text:
                errors.append(f"image prompt should mention: {hint}")

    if "文字の有無" not in text:
        errors.append("missing merch judgment: 文字の有無")

    return errors


def run_self_test() -> int:
    sample = """# 登録候補｜ひなたたたみの猫

## 構想メモ
- モチーフ：猫
- カテゴリ：生き物
- 現実との接続点：猫は日なたを好む
- 架空の裏事情：日なたを畳む
- 反応の方向：かわいい、妙に納得。ただのかわいいで終わらない
- ビジュアルの核：床の日なたがめくれる

## ウラガワ図鑑
### 観測文
猫は日なたを畳む。
### 特徴
日なたをしまう。
### 習性
曇りの日に出す。
### 注意点
雑に置かない。

## ビジュアル設計
- 絵だけで伝えるべき意外性：光が布のようにめくれる
- 現実との接続を見せる要素：窓枠の影
- 裏事情の表現方法：めくれ
- 視覚的な主役：猫と日なた
- 画面内で起きている行動：日なたを畳んでいる
- 誰に刺す魅力：静かな日用品ファンタジーが好きな人
- 想定ターゲット：ゆるかわな動植物が好きな女性層
- 少し尖らせるポイント：日なたを所有物のように扱う
- 主役題材としての適性：猫と光は外形が強い
- 推奨商品フォーマット：square, one-point
- 画像戦略タイプ：Character Icon
- 背景の扱い：背景なし
- 描き込み範囲：猫と光だけ
- 主役と周辺物のスケール：猫を主役、光は猫の半分程度
- ステッカーにしたときの外形：丸い猫と四角い光
- 避ける弱い表現：寝ているだけ
- 商品化で映えるポイント：外形

## 画像生成プロンプト
### 構造化プロンプト
[GOAL]
商品化向けのステッカー。
[SUBJECT]
猫と日なた。
[ACTION]
日なたを畳んでいる。
[HIDDEN SIDE]
日なたをしまう。
[COMPOSITION]
primary format: square
secondary use: one-point
visual strategy: Character Icon
background: none
relative scale: 猫を主役、光は猫の半分程度
target product: Sticker, T-Shirt, Tote
master canvas: 3000 x 3000 transparent PNG
余白多め。
[STYLE]
ゆるい手描き線。主線は茶色。色数は少なめ。背景は白。
[ACCENT]
めくれた光。
[AVOID]
寝ているだけ。

## SNS投稿文
### 短文版
猫は日なたを畳む。
### 図鑑版
観測された。
### 商品紹介版
ステッカー向き。

## SUZURI商品化メモ
- Tシャツ：ワンポイント
- ステッカー：向く
- スマホケース：下部配置
- ワンポイント：向く
- 総柄：一部可
- 文字の有無：なしでも成立

## 存在台帳登録用
No.XXX｜ひなたたたみの猫｜猫｜日なたを畳む。｜雨の日に一枚分けてくれる。
"""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
        handle.write(sample)
        path = Path(handle.name)
    errors = validate_text(path.read_text(encoding="utf-8"))
    path.unlink(missing_ok=True)
    if errors:
        print("self-test failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="Markdown file to validate")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.path:
        parser.error("path is required unless --self-test is used")

    path = Path(args.path)
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    errors = validate_text(path.read_text(encoding="utf-8"))
    if errors:
        print(f"{path}: invalid")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"{path}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
