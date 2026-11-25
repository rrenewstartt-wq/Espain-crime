#!/usr/bin/env python3
"""Create episodes/<slug>/ with every file the teams fill in.

    python3 scripts/new_episode.py guadalajara-1992 --subject "las explosiones de Guadalajara"
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE, FMT  # noqa: E402

SCRIPT = """---
title: ""            # /package 에서 확정 (check_title.py)
subject: "{subject}"  # 연결 문장 'Esta es la historia de …' 에 들어갈 고유명사
---

> 형식: docs/script-formula.md · 검사: python3 scripts/check_script.py episodes/{slug} --timeline
> 분당 {wpm}단어 기준 목표 {lo}~{hi}분 = {wlo:,}~{whi:,}단어. 사실 문장 끝에 [^n] 각주(facts.md).

## apertura
> 날짜·시각 장면(현재형) → 평범함 + 숫자 → 전환 → 규모 숫자 → 질문 2~4개(마지막 'Y sobre todo, ¿…?') → 'Esta es la historia de {subject}.'

## origen
> 'Para entender …, hay que volver a …' 로 시작. 배경. 개념은 'Funciona así. Si tú …'

## escalada
> 수법·규모가 커지는 과정. 단계마다 숫자 하나

## regreso
> 도입의 그 날짜·시각으로 돌아온다 (영상 35~65% 지점)

## consecuencias
> 수사·재판·폭로. 진위 소재는 기술적 모순 → 기록 부재 → 최초 출처로 해체

## hoy
> 현재 상황 → 제도·구조의 교훈 → 마지막 문장은 질문
"""

FACTS = """# 사실 확인표: {slug}

대본의 각주 번호마다 한 줄. ✅ = 1차 자료로 확인, ⚠️ = 2차 자료뿐(공개 전 1차로 확인), ❌ = 틀림(대본에서 삭제).

| # | 대본 속 주장 | 출처 (1차 우선, URL·문서명·쪽) | 상태 |
|---|---|---|---|
| 1 | | | |

## 확정되지 않은 것 (대본에서 단정 금지)
-

## 실명 처리
- 확정 판결 없는 관련자·생존 피해자·미성년자: 이니셜 또는 역할로
"""

SHOTS = """# 장면표: {slug}

형식: docs/production-style.md. 출처·라이선스 칸이 비면 불합격.

| # | 막 | 대본 첫 단어 | 길이(초) | 화면 유형 | 필수 요소 | 소재 | 출처·라이선스 |
|---|---|---|---:|---|---|---|---|
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--subject", required=True)
    a = ap.parse_args()
    d = f"{BASE}/episodes/{a.slug}"
    if os.path.exists(d):
        sys.exit(f"이미 있습니다: {d}")
    os.makedirs(f"{d}/thumbnail", exist_ok=True)
    os.makedirs(f"{d}/release", exist_ok=True)
    wpm = FMT["narration"]["wpm"]
    lo, hi = FMT["runtime"]["target_min"]
    open(f"{d}/script.md", "w", encoding="utf-8").write(
        SCRIPT.format(subject=a.subject, slug=a.slug, wpm=wpm, lo=lo, hi=hi, wlo=lo * wpm, whi=hi * wpm))
    open(f"{d}/facts.md", "w", encoding="utf-8").write(FACTS.format(slug=a.slug))
    open(f"{d}/shots.md", "w", encoding="utf-8").write(SHOTS.format(slug=a.slug))
    json.dump({"slug": a.slug, "subject": a.subject, "title": "", "title_candidates": [],
               "hook_line": "", "context": "", "comment_question": "",
               "tags_subject": [], "tags_field": [],
               "thumbnail": {"type": "", "text": "", "subject_image": "", "collage": [], "eye_bar": []},
               "status": "기획"},
              open(f"{d}/meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"만들었습니다: episodes/{a.slug}/ (script.md, facts.md, shots.md, meta.json, thumbnail/, release/)")


if __name__ == "__main__":
    main()
