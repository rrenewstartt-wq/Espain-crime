#!/usr/bin/env python3
"""Build the upload package: description, tags and the next free upload slot (docs/packaging.md).

    python3 scripts/make_description.py episodes/<ep>
Reads meta.json (hook_line, context, comment_question, tags_subject, tags_field), facts.md (sources),
shots.md (credits) and writes release/description.txt, release/tags.txt, release/release.json.
Nothing is uploaded: a person uploads (CLAUDE.md).
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE, CHANNEL, FMT, Report, fold  # noqa: E402

WD = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def next_slot(taken):
    sc = FMT["schedule"]
    tz = ZoneInfo(sc["timezone"])
    h, m = map(int, sc["time"].split(":"))
    t = datetime.now(tz).replace(hour=h, minute=m, second=0, microsecond=0)
    while WD[t.weekday()] != sc["weekday"] or t <= datetime.now(tz) or t.isoformat() in taken:
        t = (t + timedelta(days=1)).replace(hour=h, minute=m)
    return t


def table_col(path, col):
    out = []
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) > col and cells[0] not in ("#", "---", "") and not set(cells[0]) <= set("-"):
            if cells[col] and not set(cells[col]) <= set("-"):
                out.append(cells[col])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    a = ap.parse_args()
    ep = a.episode.rstrip("/")
    meta = json.load(open(f"{ep}/meta.json", encoding="utf-8"))
    own = CHANNEL["own_channel"]
    r = Report(f"출고 패키지: {ep}")
    for k in ("hook_line", "context", "comment_question", "subject", "title"):
        r.ok(bool(meta.get(k)), f"meta.json {k}")
    sub = own.get("subscribe_line")
    r.ok(bool(sub), "채널 고유 구독 문구", "" if sub else "config/channel.json → own_channel.subscribe_line 을 사람이 정해야 함")
    if sub:
        r.ok(not re.search(r"m[aá]s historias como esta", fold(sub)), "레퍼런스 구독 문구와 다름")
    q = meta.get("comment_question", "")
    r.ok(q.startswith("¿") and q.endswith("?"), "💬 질문 형식", q)

    sources = [c for c in table_col(f"{ep}/facts.md", 2)]
    sources = sorted(set(s for s in sources if s and not s.startswith("출처")))
    credits = sorted(set(c for c in table_col(f"{ep}/shots.md", 6) if c and not c.startswith("출처")))
    r.ok(bool(sources), "Fuentes (facts.md 출처)", f"{len(sources)}개")
    r.ok(bool(credits), "Créditos (shots.md 출처·라이선스)", f"{len(credits)}개", fail="WARN")

    parts = [meta.get("hook_line", ""), meta.get("context", ""), f"Esta es la historia de {meta.get('subject', '')}.",
             f"🔔 {sub or '[구독 문구]'}\n💬 {q}"]
    if sources:
        parts.append("Fuentes:\n" + "\n".join(f"- {s}" for s in sources))
    if credits:
        parts.append("Créditos:\n" + "\n".join(f"- {c}" for c in credits))
    desc = "\n\n".join(p for p in parts if p)
    lo, hi = FMT["description"]["length_chars"]
    r.ok(lo <= len(desc) <= hi + 1500, "설명란 길이", f"{len(desc)}자", fail="WARN")
    r.ok("#" not in desc, "해시태그 없음 (레퍼런스 0)", fail="WARN")

    names = own.get("name_variants") or ([own["name"]] if own.get("name") else [])
    tags = list(dict.fromkeys([t.lower() for t in meta.get("tags_subject", [])] + [t.lower() for t in meta.get("tags_field", [])]
                              + ["misterio", "casos reales"] + [n.lower() for n in names]))
    tlo, thi = FMT["tags"]["count"]
    r.ok(tlo <= len(tags) <= thi, "태그 수", f"{len(tags)}개 (권장 {tlo}~{thi})", fail="WARN")
    r.ok(not any("enigma" in fold(t) for t in tags), "레퍼런스 채널명 태그 없음")

    taken = set()
    for p in glob.glob(f"{BASE}/episodes/*/release/release.json"):
        if os.path.dirname(os.path.dirname(p)) != os.path.abspath(ep):
            taken.add(json.load(open(p, encoding="utf-8")).get("slot"))
    slot = next_slot(taken)
    os.makedirs(f"{ep}/release", exist_ok=True)
    open(f"{ep}/release/description.txt", "w", encoding="utf-8").write(desc + "\n")
    open(f"{ep}/release/tags.txt", "w", encoding="utf-8").write(", ".join(tags) + "\n")
    json.dump({"title": meta.get("title"), "slot": slot.isoformat(), "slot_local": slot.strftime("%Y-%m-%d (%a) %H:%M ") + FMT["schedule"]["timezone"],
               "tags": tags, "description_file": "release/description.txt", "uploaded": False},
              open(f"{ep}/release/release.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r.add("PASS", "공개 예정 슬롯", slot.strftime("%Y-%m-%d %H:%M ") + FMT["schedule"]["timezone"])
    r.print()
    sys.exit(1 if r.failed else 0)


if __name__ == "__main__":
    main()
