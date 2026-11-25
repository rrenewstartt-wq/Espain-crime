---
name: benchmark
description: 레퍼런스 채널(@detrasdelenimga)을 다시 수집·측정해 형식 변화를 확인한다. "레퍼런스 다시 분석", "형식 바뀌었나", 한 달에 한 번, 레퍼런스가 새 영상을 올렸을 때 사용.
---

# /benchmark

팀: `format-analyst` (`.claude/agents/`). 근거 문서: `docs/benchmark-report.md`.

1. `format-analyst` 에게 수집·분석·비교를 맡긴다. 필요한 키: `YT_API_KEY`(환경 변수), `SUPADATA_API_KEY`(이 클라우드 환경은 프록시가 넣어 주므로 `SUPADATA_API_KEY=proxy-injected` 로 실행).
2. 결과 표(바뀐 값)를 사용자에게 보여 준다. `config/format.json` 수정안이 있으면 **사용자 승인 후** 반영하고 `docs/benchmark-report.md` 를 갱신한다.
3. `git diff data/benchmark/summary.json config/format.json docs/` 를 커밋한다. `data/benchmark/raw/` 는 커밋하지 않는다.

화면 스타일: 사람이 레퍼런스·경쟁 채널 클립을 `data/benchmark/raw/clips/<핸들>__<이름>.mp4` 로 넣어 주면 `format-analyst` 가 `benchmark_frames.py` 로 측정하고 `docs/visual-style.md` 를 쓴다(클립은 커밋하지 않음).

YouTube 가 막히면 우회하지 않는다. Supadata 크레딧(월 100)은 새 영상분만 쓴다.
