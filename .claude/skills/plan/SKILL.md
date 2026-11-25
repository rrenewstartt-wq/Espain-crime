---
name: plan
description: 선정된 사건으로 6막 기획서(plan.md)를 만든다. "기획해줘", "/plan <slug>", 소재를 고른 직후 사용.
---

# /plan <slug>

팀: `episode-planner` (+ 사실이 부족하면 `source-verifier`).

1. `python3 scripts/topics.py show <slug>` 로 후보 확인. 상태가 `선정` 이 아니면 사용자에게 확인.
2. `episode-planner` 에게 기획을 맡긴다 → `episodes/<slug>/plan.md` (+ `new_episode.py` 로 폴더 생성).
3. ⚠️ 사실이 3개 이상이면 `source-verifier` 로 보강.
4. 사용자에게 6막 표와 결정적 순간, 질문 3개, 엔딩 질문, 제목 방향을 보여 주고 확인받는다.
5. `python3 scripts/topics.py set <slug> 제작`
