# 소재 기준

`case-scout` 가 후보를 내고 `source-verifier`·`risk-reviewer` 가 검증한다. 백로그는 `data/topics/backlog.json`, 관리는 `scripts/topics.py`.

## 레퍼런스 형식에 맞는 사건
- **사건 하나**로 24~29분을 채울 수 있다: 결정적 순간(도입), 배경, 확대, 결과, 현재가 모두 있다.
- 도입에 쓸 **날짜·시각이 확인되는 결정적 순간**이 있다.
- 질문 3개가 자연스럽게 나온다(어떻게 / 누가·왜 / 그리고 무엇보다).
- 현재와 이어지는 교훈이 있다(제도·기술·권력).
- 카테고리: 미스터리 장소 · 재난 · 인터넷·해킹 · 미해결·정체 · 정부 비밀 · 고대·예술 미스터리 · (스캠은 피해 규모가 국가적일 때만)

## 점수 (합계 100)
| 항목 | 배점 | 기준 |
|---|---:|---|
| 결정적 순간 | 20 | 날짜·시각·장소가 1차 자료로 확인되는 장면이 있는가 |
| 수요 | 20 | 레퍼런스 고성과 카테고리 + 댓글 요청(`docs/benchmark-report.md` 5·6장) |
| 자료 | 20 | 1차 자료(판결문, 공식 보고서, 당시 보도) 3개 이상 |
| 질문·반전 | 15 | 열린 질문이나 진위 해체 구조가 가능한가 |
| 중남미 연결 | 10 | 사건 자체 또는 세계적 사건의 중남미 연결고리 |
| 차별성 | 15 | 스페인어 장편 다큐가 적다. **레퍼런스가 다룬 사건이면 0점 + 경고** |

## 제외
- 확정 판결 없이 특정인을 범인으로 만들어야 성립하는 사건
- 미성년 피해자가 중심인 성범죄, 생존 피해자의 사생활이 중심인 사건
- 마약 조직 인물을 미화하게 되는 각도(광고 부적합). 다룬다면 "어떻게 가능했나"의 구조·제도에 초점
- 1차 자료 없이 위키·블로그·다른 유튜브 영상에만 근거하는 사건

## 후보 형식 (`data/topics/inbox-YYYYMMDD-scout.json`)
```json
{"candidates": [{
  "slug": "guadalajara-1992", "case": "Explosiones de Guadalajara", "country": "MX", "year": 1992,
  "category": "재난·사고", "key_moment": "1992-04-22 10:05, Analco",
  "one_line": "가스 냄새 신고 사흘 뒤 하수도 8km가 연쇄 폭발",
  "questions": ["¿Cómo explota una ciudad desde abajo?", "¿Quién sabía?", "¿Por qué nadie evacuó?"],
  "latam_link": "멕시코 사건", "sources": ["https://…"], "scores": {"moment": 18, "demand": 15, "sources": 16, "question": 12, "latam": 10, "novelty": 13},
  "risk_notes": "", "open_questions": []
}]}
```
