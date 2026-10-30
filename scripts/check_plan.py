#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""路书机械检查（Markdown 版）。

用法：
    python check_plan.py 路书.md [--days 3] [--drive]

检查项：
  A 每日标题数量与 --days 一致（给了才查）
  B 每天有早/午/晚三餐线索
  C 时间轴行带 HH:MM
  D 价格带查询时戳，或标了【未核实】/【估算】
  E 自驾模式：每天有停车条 🅿️ / 停车
  F 必备板块：预约、应急/备选、费用/预算
  G 无残留占位符（TODO、__X__、【待填】）

退出码 0 = 无 FAIL；1 = 有 FAIL。WARN 不影响退出码。
"""

import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DAY_RE = re.compile(r"^#{2,4}\s*(?:Day|D|第)\s*(\d+)\s*(?:天)?", re.I)
MEAL = {"早": r"早餐|早饭|含早", "午": r"午餐|午饭|中饭", "晚": r"晚餐|晚饭|夜宵"}
PRICE_RE = re.compile(r"¥\s*\d")
STAMP_RE = re.compile(r"（[^）]*(?:查|核实|时价)[^）]*）|【未核实】|【估算】")
TIME_RE = re.compile(r"\b([01]?\d|2[0-3]):[0-5]\d\b")


def split_days(text):
    lines = text.splitlines()
    days, cur, head = [], None, None
    for ln in lines:
        m = DAY_RE.match(ln.strip())
        if m:
            if cur is not None:
                days.append((head, cur))
            cur, head = [], ln.strip()
        elif cur is not None:
            cur.append(ln)
    if cur is not None:
        days.append((head, cur))
    return days


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--days", type=int)
    ap.add_argument("--drive", action="store_true")
    a = ap.parse_args()

    text = open(a.file, encoding="utf-8").read()
    fails, warns = [], []

    days = split_days(text)
    if a.days is not None:
        if len(days) != a.days:
            fails.append(f"A 天数：找到 {len(days)} 天，声明 {a.days} 天")
    elif not days:
        warns.append("A 没找到 Day/第N天 标题，无法按天检查")

    for head, body in days:
        blob = "\n".join(body)
        name = head[:40]
        for label, pat in MEAL.items():
            if not re.search(pat, blob):
                fails.append(f"B {name} 缺{label}餐")
        if a.drive and not re.search(r"🅿️|停车", blob):
            fails.append(f"E {name} 缺停车条")

    for i, ln in enumerate(text.splitlines(), 1):
        if PRICE_RE.search(ln) and not STAMP_RE.search(ln):
            warns.append(f"D 第{i}行价格无时戳：{ln.strip()[:60]}")

    axis_rows = [l for l in text.splitlines() if l.strip().startswith("|") and PRICE_RE.search(l)]
    if axis_rows and not any(TIME_RE.search(r) for r in axis_rows):
        fails.append("C 有排程表但没有 HH:MM 时间")

    for label, pat in {"F 预约": r"预约|放票|抢票", "F 应急": r"应急|备用|备选|Plan ?B", "F 费用": r"费用|预算|花费"}.items():
        if not re.search(pat, text, re.I):
            fails.append(f"{label} 板块缺失")

    for bad in ("TODO", "【待填】", "__CITY__"):
        if bad in text:
            fails.append(f"G 残留占位符：{bad}")

    unverified = text.count("【未核实】")
    print(f"天数 {len(days)}｜未核实 {unverified} 处｜FAIL {len(fails)}｜WARN {len(warns)}")
    for f in fails:
        print("FAIL", f)
    for w in warns:
        print("WARN", w)
    if not fails:
        print("PASS 可交付（未核实项需在正文明确列出）")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
