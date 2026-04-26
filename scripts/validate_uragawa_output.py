#!/usr/bin/env python3
"""Validate a Uragawa Zukan observation markdown file.

Default mode checks structure and template completeness. Use --strict for
filled candidates before image generation or ledger registration.
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
    "[CORE SUBJECT]",
    "[HIDDEN-WORLD LOGIC]",
    "[VISUAL HOOK]",
    "[COMPOSITION]",
    "[PRODUCT USE]",
    "[STYLE]",
    "[MUST INCLUDE]",
    "[MUST AVOID]",
    "[NEGATIVE CONSTRAINTS]",
    "primary format:",
    "secondary crops:",
    "visual strategy:",
    "background:",
    "master canvas:",
    "target product:",
    "sticker cutout:",
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

VALID_STRATEGIES = {
    "Character Icon",
    "World Object",
    "Relationship Pair",
    "Scene Emblem",
    "Pattern Seed",
}

VALID_PRODUCTS = {
    "Sticker",
    "T-Shirt",
    "Tote",
    "Smartphone Case",
    "Acrylic Key Chain",
    "Acrylic Stand",
}

BLOCK_TERMS = ["蜘蛛", "蛾", "ゴキブリ", "ハエ", "蚊", "ムカデ", "毛虫"]

TITLE_RE = re.compile(r"^# (?:登録候補|No\.(?:XXX|\d{3}))｜.+", re.MULTILINE)
LEGACY_LEDGER_RE = re.compile(r"^No\.(?:XXX|\d{3})｜[^｜]+｜[^｜]+｜[^｜]+｜[^｜]+$", re.MULTILINE)
TSV_LEDGER_HEADER = "id\ttitle\tcategory\tmotif\tvisual_strategy\ttarget_products\tstatus\tscore\tcontinuity_links\tcreated_at\tnotes"
TSV_LEDGER_ROW_RE = re.compile(r"^No\.(?:XXX|\d{3})\t", re.MULTILINE)


def field_value(text: str, label: str) -> str:
    patterns = [
        rf"^-\s*{re.escape(label)}[：:]\s*(.*)$",
        rf"^{re.escape(label)}[：:]\s*(.*)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def prompt_value(text: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}:\s*(.*)$", text, flags=re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def contains_any(value: str, options: set[str]) -> bool:
    value_lower = value.lower()
    return any(option.lower() in value_lower for option in options)


def validate_text(text: str, strict: bool = False) -> list[str]:
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

    if not (LEGACY_LEDGER_RE.search(text) or (TSV_LEDGER_HEADER in text and TSV_LEDGER_ROW_RE.search(text))):
        errors.append("missing ledger entry block or legacy ledger line")

    if "## 画像生成プロンプト" in text:
        for hint in PROMPT_HINTS:
            if hint not in text:
                errors.append(f"image prompt should mention: {hint}")

    if "文字の有無" not in text:
        errors.append("missing merch judgment: 文字の有無")

    if strict:
        errors.extend(validate_strict(text))

    return errors


def validate_strict(text: str) -> list[str]:
    errors: list[str] = []

    category = field_value(text, "カテゴリ")
    if category not in VALID_CATEGORIES:
        errors.append(f"strict: invalid or empty category: {category or '(empty)'}")

    motif = field_value(text, "モチーフ")
    if not motif:
        errors.append("strict: motif is required")

    blocked = sorted({term for term in BLOCK_TERMS if term in motif or term in text})
    if blocked:
        errors.append("strict: blocked motif term found: " + ", ".join(blocked))

    strategy = field_value(text, "画像戦略タイプ") or prompt_value(text, "visual strategy")
    if strategy and strategy not in VALID_STRATEGIES:
        errors.append(f"strict: invalid visual strategy: {strategy}")
    if not strategy:
        errors.append("strict: visual strategy is required")

    primary_format = prompt_value(text, "primary format")
    if primary_format and "square" not in primary_format.lower():
        errors.append(f"strict: primary format should be square by default: {primary_format}")
    if not primary_format:
        errors.append("strict: primary format is required")

    target_product = prompt_value(text, "target product")
    if not target_product:
        errors.append("strict: target product is required")
    elif not contains_any(target_product, VALID_PRODUCTS):
        errors.append(f"strict: target product should name a supported product: {target_product}")

    master_canvas = prompt_value(text, "master canvas")
    if not master_canvas:
        errors.append("strict: master canvas is required")
    elif "3000" not in master_canvas or "transparent" not in master_canvas.lower():
        errors.append(f"strict: master canvas should usually be 3000 x 3000 transparent PNG: {master_canvas}")

    background = prompt_value(text, "background")
    if not background:
        errors.append("strict: background is required")

    visual_action = field_value(text, "画面内で起きている行動")
    if not visual_action:
        errors.append("strict: visible action is required")

    target = field_value(text, "想定ターゲット") or field_value(text, "誰に刺す魅力")
    if not target:
        errors.append("strict: target audience / appeal is required")

    if "かわいい" in text:
        guards = ["ただかわいい", "ただのかわいい", "甘すぎ", "not just cute", "only cute"]
        if not any(guard in text for guard in guards):
            errors.append("strict: mentions 'かわいい' but does not guard against only-cute weakness")

    return errors


def run_self_test() -> int:
    sample = """# 登録候補｜雨ためのカタツムリ

## 構想メモ
- カテゴリ：生き物
- モチーフ：カタツムリ
- 現実との接続点：雨の日に現れる、殻を持つ、濡れた葉にいる
- 架空の裏事情：殻に余った雨をためて、乾いた朝に少しずつ配る
- 反応の方向：かわいい、静かなエモさ。ただかわいいで終わらない
- ビジュアルの核：半透明の殻に小さな雨水が入っている

## ウラガワ図鑑
### 観測文
雨ためのカタツムリは、降りすぎた雨を殻にしまう。
### 特徴
殻の奥に小さな水面が見える。
### 習性
乾いた葉に一滴だけ分ける。
### 注意点
急がせるとこぼす。

## ビジュアル設計
- 絵だけで伝えるべき意外性：殻が小さな雨瓶になっている
- 現実との接続を見せる要素：濡れた葉と雨粒
- 裏事情の表現方法：半透明の殻の中の水面
- 視覚的な主役：カタツムリ
- 画面内で起きている行動：葉に一滴だけ雨を注いでいる
- 誰に刺す魅力：静かな植物・小動物モチーフが好きな女性層
- 想定ターゲット：ゆるかわ、エモ、おしゃれな小物が好きな女性層
- 少し尖らせるポイント：雨を所有している小さな役割感
- 主役題材としての適性：殻と体の外形が強く、雨との接続が明確
- 推奨商品フォーマット：square, one-point
- 画像戦略タイプ：World Object
- 背景の扱い：透明背景または白背景
- 描き込み範囲：カタツムリ、葉、雨粒だけ
- 主役と周辺物のスケール：カタツムリは葉より小さく、現実感を残す
- ステッカーにしたときの外形：丸い殻と葉先のしずく
- 避ける弱い表現：普通のカタツムリが乗っているだけ
- 商品化で映えるポイント：殻の青い水面と丸い外形

## 画像生成プロンプト
### 構造化プロンプト
[GOAL]
product-ready square sticker illustration for Sticker, T-Shirt, and Tote. The appeal is a quiet rain-keeper snail that is not just cute.
[CORE SUBJECT]
main subject: a small round snail with a translucent shell shaped like a tiny rain jar.
[HIDDEN-WORLD LOGIC]
real-world connection: snails appear after rain and carry spiral shells.
[VISUAL HOOK]
first-glance surprise: the shell is half-filled with pale blue rainwater.
[ACTION]
The snail pours one drop onto a dry leaf.
[COMPOSITION]
primary format: square
secondary crops: one-point and vertical phone crop
visual strategy: World Object
background: transparent or white
camera / angle: slight front view
spacing: generous whitespace
master canvas: 3000 x 3000 transparent PNG
[PRODUCT USE]
target product: Sticker, T-Shirt, Tote
sticker cutout: round shell plus leaf tip
t-shirt / tote placement: centered one-point
phone-case crop: lower third placement
acrylic concerns: avoid thin detached drops
[STYLE]
line: soft brown hand-drawn line, slightly thick.
[MUST INCLUDE]
- translucent rain shell
- small leaf
- one clear drop
[MUST AVOID]
- realistic slimy body
- many eggs
- horizontal-only composition
[NEGATIVE CONSTRAINTS]
no tiny explanatory text, no horizontal-only composition, no realistic unpleasant insect details, no weak still life, no white subject disappearing on white background

## SNS投稿文
### 短文版
降りすぎた雨は、たまに殻へしまわれる。
### 図鑑版
雨ためのカタツムリ。乾いた朝に一滴だけ配る。
### 商品紹介版
小さな雨を背負ったカタツムリのステッカー。

## SUZURI商品化メモ
- Tシャツ：胸元ワンポイント
- ステッカー：向く
- スマホケース：下部配置
- ワンポイント：向く
- 総柄：雨粒を使えば可
- 文字の有無：なしでも成立

## 存在台帳登録用
id\ttitle\tcategory\tmotif\tvisual_strategy\ttarget_products\tstatus\tscore\tcontinuity_links\tcreated_at\tnotes
No.XXX\t雨ためのカタツムリ\t生き物\tカタツムリ\tWorld Object\tSticker,T-Shirt,Tote\tdraft\t18\t-\t2026-04-26\tfixture
"""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
        handle.write(sample)
        path = Path(handle.name)
    errors = validate_text(path.read_text(encoding="utf-8"), strict=True)
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
    parser.add_argument("--strict", action="store_true")
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

    errors = validate_text(path.read_text(encoding="utf-8"), strict=args.strict)
    if errors:
        print(f"{path}: invalid")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"{path}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
