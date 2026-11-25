#!/usr/bin/env python3
"""Topic backlog (docs/topic-criteria.md).

    python3 scripts/topics.py add data/topics/inbox-YYYYMMDD-scout.json   # merge candidates, rescore
    python3 scripts/topics.py list [--top 10] [--all]
    python3 scripts/topics.py check "<case or keyword>"                   # duplicate / reference-overlap check
    python3 scripts/topics.py show <slug>
    python3 scripts/topics.py set <slug> <status> [--note "..."]          # 후보 → 검증됨 → 선정 → 제작 → 공개 / 보류 / 제외
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE, RAW, fold  # noqa: E402

BACKLOG = f"{BASE}/data/topics/backlog.json"
WEIGHTS = {"moment": 20, "demand": 20, "sources": 20, "question": 15, "latam": 10, "novelty": 15}
STATUSES = ["후보", "검증됨", "선정", "제작", "공개", "보류", "제외"]


def load():
    return json.load(open(BACKLOG, encoding="utf-8")) if os.path.exists(BACKLOG) else {"topics": []}


def save(d):
    os.makedirs(os.path.dirname(BACKLOG), exist_ok=True)
    json.dump(d, open(BACKLOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def score(c):
    s = c.get("scores", {})
    return sum(min(max(int(s.get(k, 0)), 0), w) for k, w in WEIGHTS.items())


def reference_hits(term):
    p = f"{RAW}/catalog.json"
    if not os.path.exists(p):
        return []
    t = fold(term)
    keys = [w for w in t.split() if len(w) > 3] or [t]
    return [v["title"] for v in json.load(open(p, encoding="utf-8"))["videos"]
            if all(k in fold(v["title"] + " " + " ".join(v.get("tags", []))) for k in keys)]


def cmd_check(term):
    d = load()
    t = fold(term)
    own = [x for x in d["topics"] if t in fold(x["slug"] + " " + x["case"])]
    ref = reference_hits(term)
    print(f"백로그: {len(own)}건" + "".join(f"\n  - {x['slug']} [{x.get('status')}] {x['case']}" for x in own))
    print(f"레퍼런스가 다룬 영상: {len(ref)}건" + "".join(f"\n  ⚠️ {r}" for r in ref))
    if ref:
        print("  → 다룰 수는 있지만 다른 관점이 필요하고 차별성 점수 0 (docs/originality.md 규칙 1)")
    return bool(own or ref)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["add", "list", "check", "show", "set", "rescore"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("status", nargs="?")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--note")
    a = ap.parse_args()
    d = load()
    by = {x["slug"]: x for x in d["topics"]}

    if a.cmd == "add":
        new = json.load(open(a.arg, encoding="utf-8"))["candidates"]
        added = 0
        for c in new:
            if c["slug"] in by:
                continue
            ref = reference_hits(c["case"])
            if ref:
                c.setdefault("scores", {})["novelty"] = 0
                c["reference_overlap"] = ref
            c["score"], c["status"] = score(c), "후보"
            d["topics"].append(c)
            added += 1
        save(d)
        print(f"{added}건 추가 (중복 {len(new) - added}건 건너뜀)")
    elif a.cmd == "rescore":
        for x in d["topics"]:
            x["score"] = score(x)
        save(d)
    elif a.cmd == "list":
        rows = [x for x in d["topics"] if a.all or x.get("status") not in ("제외", "공개")]
        rows.sort(key=lambda x: -x.get("score", 0))
        print(f"{'점수':>4} | {'상태':4} | slug | 사건 | 카테고리 | 한 줄")
        for x in rows[:None if a.all else a.top]:
            flag = " ⚠️레퍼런스" if x.get("reference_overlap") else ""
            print(f"{x.get('score', 0):>4} | {x.get('status', ''):4} | {x['slug']} | {x['case']} | {x.get('category', '')} | {x.get('one_line', '')}{flag}")
    elif a.cmd == "check":
        sys.exit(1 if cmd_check(a.arg) else 0)
    elif a.cmd == "show":
        print(json.dumps(by[a.arg], ensure_ascii=False, indent=1))
    elif a.cmd == "set":
        if a.status not in STATUSES:
            sys.exit(f"상태는 {STATUSES} 중 하나")
        by[a.arg]["status"] = a.status
        if a.note:
            by[a.arg].setdefault("notes", []).append(a.note)
        save(d)
        print(f"{a.arg} → {a.status}")


if __name__ == "__main__":
    main()
