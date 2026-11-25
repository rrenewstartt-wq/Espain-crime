#!/usr/bin/env python3
"""Check a title against the reference title formula (docs/title-formula.md).

    python3 scripts/check_title.py "El Pueblo Más Silencioso de México | La Zona del Silencio"
    python3 scripts/check_title.py --file episodes/<ep>/titles.txt     # one candidate per line
Exit code 1 if any candidate FAILs.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import FMT, RAW, Report, fold  # noqa: E402

T = FMT["title"]
TWIST = re.compile(r"pag[oó]|muri[oó]|perdi[oó]|salv[oó]|desapareci[oó]|cay[oó]|traicion|vida|nunca|jam[aá]s", re.I)
SMALL = {"de", "del", "la", "las", "el", "los", "y", "o", "en", "a", "con", "que", "por", "un", "una", "al", "se", "su", "lo", "es"}


def reference_titles():
    p = f"{RAW}/catalog.json"
    return [v["title"] for v in json.load(open(p, encoding="utf-8"))["videos"]] if os.path.exists(p) else []


def check(title, refs):
    r = Report(f"제목: {title}")
    parts = title.split("|")
    if not r.ok(len(parts) == 2, "파이프 구조 [훅] | [고유명사]", f"'|' {len(parts) - 1}개"):
        return r
    left, right = parts[0].strip(), parts[1].strip()
    n = len(title)
    lo, hi = T["length"]
    if n > T["length_max"]:
        r.add("FAIL", "길이", f"{n}자 > 최대 {T['length_max']}자")
    else:
        r.ok(lo <= n <= hi, "길이", f"{n}자 (권장 {lo}~{hi})", fail="WARN")
    lw = len(left.split())
    r.ok(T["left_words"][0] <= lw <= T["left_words"][1], "왼쪽 단어 수", f"{lw}단어 (권장 {T['left_words'][0]}~{T['left_words'][1]})", fail="WARN")

    r.add("PASS" if not re.search(r"\b(19|20)\d\d\b", left) else "WARN", "왼쪽에 연도 없음",
          "연도는 오른쪽이나 썸네일로" if re.search(r"\b(19|20)\d\d\b", left) else "")

    hooks = {k: bool(re.search(h["pattern"], fold(left) if k != "question" else title, re.I)) for k, h in T["hooks"].items()}
    r.ok(hooks["danger_fear"] or hooks["question"], "1순위 훅(위험·공포 또는 질문)",
         ", ".join(k for k, v in hooks.items() if v) or "훅 없음", fail="WARN")
    sup = len(re.findall(T["hooks"]["superlative"]["pattern"], fold(left)))
    r.ok(sup <= 1, "최상급 한 번 이하", f"{sup}번", fail="WARN")
    r.ok(not re.search(r"\d", left), "왼쪽에 숫자 없음 (레퍼런스 0.45×)", fail="WARN")
    if hooks["person_subject"]:
        r.ok(bool(TWIST.search(left)), "사람 주어는 반전·대가와 함께 (0.52×)", "반전 단어 없음" if not TWIST.search(left) else "", fail="WARN")
    r.ok(not re.search(r"[\U0001F300-\U0001FAFF☀-➿]", title), "이모지 없음")
    r.ok(not re.search(r"\b[A-ZÁÉÍÓÚÑ]{4,}\b", title), "전체 대문자 단어 없음", fail="WARN")
    lower_words = [w for w in left.split() if w[:1].islower() and fold(w) not in SMALL]
    r.ok(not lower_words, "Title Case", ("소문자 시작: " + ", ".join(lower_words)) if lower_words else "", fail="WARN")
    r.ok(len(right.split()) <= 6, "오른쪽은 고유명사 중심", f"{len(right.split())}단어", fail="WARN")

    # copy check: 5+ consecutive words shared with a reference title
    lt = fold(left).split()
    hit = None
    for ref in refs:
        rt = fold(ref.split("|")[0]).split()
        for i in range(len(lt) - 4):
            if " ".join(lt[i:i + 5]) in " ".join(rt):
                hit = ref
                break
        if hit:
            break
    r.ok(hit is None, "레퍼런스 제목과 5단어 이상 일치 없음", f"겹침: {hit}" if hit else "")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("titles", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    titles = list(a.titles)
    if a.file:
        titles += [l.strip() for l in open(a.file, encoding="utf-8") if l.strip() and not l.startswith("#")]
    if not titles:
        sys.exit("제목을 주세요")
    refs = reference_titles()
    failed = False
    for t in titles:
        rep = check(t, refs)
        rep.print(a.json)
        failed |= rep.failed
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
