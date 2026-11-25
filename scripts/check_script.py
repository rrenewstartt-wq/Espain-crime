#!/usr/bin/env python3
"""Check episodes/<ep>/script.md against the reference script formula (docs/script-formula.md).

    python3 scripts/check_script.py episodes/<ep>            # or a path to script.md
    python3 scripts/check_script.py episodes/<ep> --timeline # also print the opening timeline
Times are estimated at config/format.json → narration.wpm (168 words/min).
Exit code 1 if any FAIL.
"""
import argparse
import os
import re
import statistics as st
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from common import FMT, Report, fold, load_script, words  # noqa: E402

DATE = re.compile(r"\b(1[5-9]\d\d|20\d\d)\b|\b\d{1,2}:\d\d\b|\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|"
                  r"octubre|noviembre|diciembre)\b|\bson las\b|\bes la (una|medianoche)\b|\b(de la|por la) (mañana|tarde|noche|madrugada)\b", re.I)
PRESENT = re.compile(r"\b(son las|es la|ahora mismo|en este momento|a esta hora|est[aá] (pasando|ocurriendo)|está[n]?\b|llega[n]?\b|entra[n]?\b|sale[n]?\b)", re.I)
VOSOTROS = re.compile(r"\b(vosotr[oa]s|vuestr[oa]s?|os\b|hab[eé]is|sab[eé]is|ten[eé]is|quer[eé]is|pod[eé]is|est[aá]is|sois|\w+[aá]is\b|\w+[eé]is\b)", re.I)
VOS_OK = {"pais", "paises", "maiz", "raiz", "seis", "dieciseis", "veintiseis", "reis", "jersey"}
ACT_IDS = [a["id"] for a in FMT["body"]["acts"]]


def timeline(acts, wpm):
    """[(act, sentence, start_sec, end_sec)]"""
    out, t = [], 0.0
    for act, ss in acts:
        for s in ss:
            d = len(words(s)) / wpm * 60
            out.append((act, s, t, t + d))
            t += d
    return out


def any_re(patterns, text):
    return next((p for p in patterns if re.search(p, fold(text), re.I)), None)


def check(path, show_timeline=False):
    meta, acts = load_script(path)
    r = Report(f"대본: {path}")
    wpm = FMT["narration"]["wpm"]
    op, bo, en, ban = FMT["opening"], FMT["body"], FMT["ending"], FMT["banned"]
    tl = timeline(acts, wpm)
    if not tl:
        r.add("FAIL", "내레이션 없음")
        return r
    total = tl[-1][3]
    subject = meta.get("subject", "")
    r.ok(bool(subject), "frontmatter subject", subject or "subject: 가 없음 (연결 문장의 고유명사)")

    # acts
    ids = [a for a, _ in acts]
    r.ok(ids == ACT_IDS, "6막 순서", " → ".join(ids) if ids != ACT_IDS else "", fail="FAIL")
    lo, hi = FMT["runtime"]["allowed_min"]
    tlo, thi = FMT["runtime"]["target_min"]
    mins = total / 60
    nwords = sum(len(words(s)) for _, s, _, _ in tl)
    if not lo <= mins <= hi:
        r.add("FAIL", "길이", f"{mins:.1f}분 ({nwords}단어 ÷ {wpm}), 허용 {lo}~{hi}분")
    else:
        r.ok(tlo <= mins <= thi, "길이", f"{mins:.1f}분 ({nwords}단어), 권장 {tlo}~{thi}분", fail="WARN")
    for spec in bo["acts"]:
        secs = sum(e - s for a, _, s, e in tl if a == spec["id"])
        share = secs / total
        r.ok(spec["share"][0] <= share <= spec["share"][1], f"막 비율 {spec['id']}",
             f"{share:.0%} (권장 {spec['share'][0]:.0%}~{spec['share'][1]:.0%})", fail="WARN")

    # opening
    first = tl[0][1]
    r.ok(bool(DATE.search(first)), "첫 문장에 날짜·시각", first[:80])
    r.ok(bool(PRESENT.search(" ".join(s for a, s, _, _ in tl if a == "apertura"))), "도입이 현재형",
         "'Son las…', 'ahora mismo', 'está…' 같은 현재형 표지 없음" if not PRESENT.search(" ".join(s for a, s, _, _ in tl if a == "apertura")) else "", fail="WARN")
    turn = next(((s, t0) for a, s, t0, _ in tl if a == "apertura" and any_re(op["turn_markers"], s)), None)
    if turn is None:
        r.add("FAIL", "전환 문장", f"도입에 전환 표지({', '.join(op['turn_markers'][:3])}…) 없음")
    else:
        r.ok(op["turn_sec"][0] <= turn[1] <= op["turn_sec"][1], "전환 문장 시점",
             f"{turn[1]:.0f}초 (권장 {op['turn_sec'][0]}~{op['turn_sec'][1]}초): {turn[0][:60]}", fail="WARN")
    subj = fold(subject)
    bridge = next(((s, t0, i) for i, (a, s, t0, _) in enumerate(tl)
                   if any_re(op["bridge_markers"], s) and (not subj or subj.split()[0] in fold(s))), None)
    if bridge is None:
        r.add("FAIL", "연결 문장", f"'Esta es la historia de {subject or 'X'}.' 류 문장 없음")
    else:
        b_s, b_t, b_i = bridge
        r.ok(op["bridge_sec"][0] <= b_t <= op["bridge_sec"][1], "연결 문장 시점",
             f"{b_t:.0f}초 (권장 {op['bridge_sec'][0]}~{op['bridge_sec'][1]}초)", fail="WARN")
        r.ok(tl[b_i][0] == "apertura", "연결 문장이 도입(apertura) 끝에", tl[b_i][0], fail="WARN")
        qt = op["question_triplet"]
        qs = [s for _, s, t0, _ in tl[:b_i] if "?" in s and b_t - t0 <= qt["within_sec_before_bridge"]]
        r.ok(qt["min"] <= len(qs) <= qt["max"], "연결 직전 질문 묶음", f"{len(qs)}개 (권장 {qt['min']}~{qt['max']})")
        if qs:
            r.ok(fold(qs[-1]).startswith(fold(qt["last_starts_with"])), "마지막 질문은 'Y sobre todo, ¿…?'",
                 qs[-1][:60], fail="WARN")
        if b_i + 1 < len(tl):
            nxt = fold(tl[b_i + 1][1])
            r.ok(bool(re.search(r"para entender|hay que (volver|retroceder)|nace|naci[oó]|a principios|en los a[nñ]os|todo empieza", nxt)),
                 "연결 뒤 되감기", tl[b_i + 1][1][:60], fail="WARN")

    # banned everywhere
    full = " ".join(s for _, s, _, _ in tl)
    for key, label in (("cta_in_video", "영상 안 구독·좋아요 요청"), ("greeting", "인사"),
                       ("reference_catchphrases", "레퍼런스 말버릇")):
        hits = [p for p in ban[key] if re.search(p, fold(full), re.I)]
        r.ok(not hits, f"금지: {label}", ", ".join(hits))
    hits = [p for p in ban["unverifiable_superlatives"] if re.search(p, fold(full), re.I)]
    r.ok(not hits, "확인 안 된 최상급", ", ".join(hits) + " → 출처가 있으면 facts.md 에" if hits else "", fail="WARN")
    vos = sorted({w for w in re.findall(VOSOTROS, full) for w in ([w] if isinstance(w, str) else [w[0]])
                  if fold(w) not in VOS_OK})
    r.ok(not vos, "vosotros 없음 (중립 라틴아메리카 스페인어)", ", ".join(vos[:8]), fail="WARN")

    # loopback
    reg = [t0 for a, _, t0, _ in tl if a == "regreso"]
    if reg:
        sh = reg[0] / total
        lo_, hi_ = bo["loopback_share"]
        r.ok(lo_ <= sh <= hi_, "중반 되돌아오기 위치", f"{sh:.0%} 지점 (권장 {lo_:.0%}~{hi_:.0%})", fail="WARN")
        open_dates = set(m.group(0).lower() for s in (x for a, x, _, _ in tl if a == "apertura") for m in DATE.finditer(s))
        reg_text = " ".join(s for a, s, _, _ in tl if a == "regreso").lower()
        r.ok(any(d in reg_text for d in open_dates), "되돌아오기가 도입의 날짜·시각을 다시 말함",
             "도입 날짜 표지: " + ", ".join(sorted(open_dates)[:4]), fail="WARN")

    # questions density
    nq = full.count("?")
    qpm = nq / mins if mins else 0
    r.ok(bo["questions_per_min"][0] <= qpm <= bo["questions_per_min"][1], "질문 빈도",
         f"분당 {qpm:.2f}개 (권장 {bo['questions_per_min'][0]}~{bo['questions_per_min'][1]})", fail="WARN")

    # ending
    last = tl[-1][1]
    r.ok("?" in last, "마지막 문장은 질문", last[:80])
    hoy = " ".join(s for a, s, _, _ in tl if a == "hoy")
    r.ok(bool(any_re(en["present_day_markers"], hoy)), "엔딩에 현재 상황", fail="WARN")

    # style
    sl = [len(words(s)) for _, s, _, _ in tl]
    r.ok(st.median(sl) <= FMT["narration"]["sentence_words_median_max"], "문장 길이",
         f"중앙값 {st.median(sl):.0f}단어, 최장 {max(sl)}단어", fail="WARN")
    toks = words(full)
    grams = Counter(" ".join(toks[i:i + 4]) for i in range(len(toks) - 3))
    rep = [(g, n) for g, n in grams.most_common(5) if n > 3]
    r.ok(not rep, "같은 4단어 표현 4번 이상 반복 없음", "; ".join(f"'{g}'×{n}" for g, n in rep), fail="WARN")
    num_no_fn = 0
    raw = open(path, encoding="utf-8").read()
    for line in raw.splitlines():
        if line.startswith(("#", ">", "---")) or ":" in line[:20] and line.split(":")[0].isidentifier():
            continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            if re.search(r"\d", s) and "[^" not in s:
                num_no_fn += 1
    r.ok(num_no_fn == 0, "숫자 문장에 출처 각주 [^n]", f"각주 없는 숫자 문장 {num_no_fn}개 → facts.md 와 연결", fail="WARN")

    if show_timeline:
        print("\n도입 타임라인 (추정)")
        for a, s, t0, _ in tl:
            if t0 > 150:
                break
            print(f"  {int(t0 // 60)}:{int(t0 % 60):02d}  {s[:100]}")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--timeline", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    path = a.episode if a.episode.endswith(".md") else os.path.join(a.episode, "script.md")
    rep = check(path, a.timeline)
    rep.print(a.json)
    sys.exit(1 if rep.failed else 0)


if __name__ == "__main__":
    main()
