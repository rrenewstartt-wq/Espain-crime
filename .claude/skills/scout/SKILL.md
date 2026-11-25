---
name: scout
description: 기획·소재 팀을 돌려 레퍼런스 형식에 맞는 다음 편 사건 후보를 찾고 검증·위험 검토·점수화한다. "소재 찾아줘", "다음 편 뭐 하지", 카테고리·국가를 주며 후보를 요청할 때 사용.
---

# /scout [카테고리·국가·개수]  예) /scout, /scout 멕시코 재난, /scout 해킹 8

팀: `case-scout` → `source-verifier` + `risk-reviewer`(동시에). 기준: `docs/topic-criteria.md`.

1. **발굴:** `case-scout` 에게 요청(조건 전달). 결과 파일을 백로그에 넣는다.
   ```bash
   python3 scripts/topics.py add data/topics/inbox-YYYYMMDD-scout.json
   python3 scripts/topics.py list --top 10
   ```
2. **검증 + 위험:** 상위 5~6개 slug 를 `source-verifier` 와 `risk-reviewer` 에게 나눠 준다. 결과로 점수를 고치고 `python3 scripts/topics.py rescore`, 통과한 것은 `set <slug> 검증됨`.
3. **보고:** 순위 | 사건 | 결정적 순간 | 카테고리(도달용/팬 결속용) | 한 줄 | 위험과 회피 | 제목 방향 1개. "사람 판단 필요" 위험은 따로.
4. 사용자가 고르면 `python3 scripts/topics.py set <slug> 선정` → `/plan <slug>`. "알아서"면 위험 2 이하 중 1위.
