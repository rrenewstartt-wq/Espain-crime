#!/usr/bin/env python3
"""Make sure our script does not copy the reference channel's wording (docs/originality.md).

Compares episodes/<ep>/script.md (narration only) with every reference transcript in
data/benchmark/raw/transcripts/ (run `python3 scripts/benchmark.py fetch` first) and the reference
descriptions. Fails on any shared run of 8+ words or a 5-gram overlap above config/format.json.

    python3 scripts/check_originality.py episodes/<ep>
    python3 scripts/check_originality.py --calibrate     # reference vs reference baseline
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import FMT, RAW, Report, load_script, narration_text, ngrams, words  # noqa: E402

O = FMT["originality"]
RUN = O["max_shared_run_words"] + 1


def reference_docs():
    docs = {}
    for p in glob.glob(f"{RAW}/transcripts/*.json"):
        seg = json.load(open(p, encoding="utf-8"))["segments"]
        docs[os.path.basename(p)[:-5]] = words(" ".join(s["text"] for s in seg))
    cat = f"{RAW}/catalog.json"
    if os.path.exists(cat):
        for v in json.load(open(cat, encoding="utf-8"))["videos"]:
            docs[f"desc:{v['id']}"] = words(v["title"] + " " + v["description"])
    return docs


# phrases the formula itself requires (bridge line, last opening question) are not copying
FORMULA = [m.split() for m in FMT["opening"]["bridge_markers"]] + [["y", "sobre", "todo"]]


def formula_gram(g):
    s = " ".join(g)
    return any(" ".join(f) in s or s in " ".join(f) for f in FORMULA)


def compare(ours, docs):
    g5 = {g for g in ngrams(ours, 5) if not formula_gram(g)}
    gr = ngrams(ours, RUN)
    ref5, runs = set(), {}
    for name, toks in docs.items():
        ref5 |= ngrams(toks, 5)
        hit = gr & ngrams(toks, RUN)
        if hit:
            runs[name] = sorted(" ".join(h) for h in hit)
    overlap = len(g5 & ref5) / len(g5) if g5 else 0
    return overlap, runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    docs = reference_docs()
    if not docs:
        sys.exit("레퍼런스 자막이 없습니다: python3 scripts/benchmark.py fetch")
    if a.calibrate:
        tr = {k: v for k, v in docs.items() if not k.startswith("desc:")}
        res = []
        for k, toks in tr.items():
            ov, runs = compare(toks, {kk: vv for kk, vv in tr.items() if kk != k})
            res.append((ov, len(runs), k))
        res.sort()
        print("레퍼런스 자막끼리 비교 (같은 채널·같은 작가라 우리 기준보다 높게 나오는 게 정상)")
        for ov, nr, k in res:
            print(f"  {k}: 5-gram 겹침 {ov:.2%}, 8단어+ 일치 문서 {nr}개")
        return
    path = a.episode if a.episode.endswith(".md") else os.path.join(a.episode, "script.md")
    _, acts = load_script(path)
    ours = words(narration_text(acts))
    overlap, runs = compare(ours, docs)
    r = Report(f"독창성: {path} (레퍼런스 자막 {sum(not k.startswith('desc:') for k in docs)}편 + 설명란)")
    if len(ours) < 500:
        r.add("WARN", "5-gram 겹침", f"{overlap:.2%} — 원고가 {len(ours)}단어라 비율 판정은 보류 (500단어 이상에서 판정)")
    else:
        r.ok(overlap <= O["max_5gram_overlap"], "5-gram 겹침",
             f"{overlap:.2%} (한도 {O['max_5gram_overlap']:.0%}, 공식 표지 'Esta es la historia de'·'Y sobre todo' 제외)")
    detail = "; ".join(f"{k}: '{v[0]}'" + (f" 외 {len(v) - 1}" if len(v) > 1 else "") for k, v in list(runs.items())[:5])
    r.ok(not runs, f"{RUN}단어 이상 연속 일치 없음", detail)
    r.print(a.json)
    sys.exit(1 if r.failed else 0)


if __name__ == "__main__":
    main()
