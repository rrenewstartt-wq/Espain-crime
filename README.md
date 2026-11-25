# espain-crime — ARCHIVO OSCURO

스페인어권(멕시코·중남미·스페인) 시청자를 위한 **단일 사건 다큐 롱폼 채널** 하네스.
레퍼런스 채널 [Detrás del Enigma](https://www.youtube.com/@detrasdelenimga)의 형식·공식·스타일을 실측 수치로 고정하고,
팀 단위 Claude 에이전트가 소재 → 기획 → 대본 → 패키징 → 장면표 → 검수 → 출고 패키지까지 만든다.

`cd espain-crime && claude` 로 실행하고 `/make-episode` 로 한 편을 만든다. 운영 지침은 [CLAUDE.md](CLAUDE.md).

## 레퍼런스에서 고정한 형식 (현재 포맷, 2025-11 이후 31편)

| 항목 | 값 | 검사 |
|---|---|---|
| 길이 | 24~29분 (레퍼런스 중앙값 26.3분) | `check_script.py` |
| 내레이션 | 분당 168단어, 현재형, 인사·구독 요청 없음 | `check_script.py` |
| 도입 | 날짜·시각 장면 → 전환(15~60초) → 질문 2~4개 → "Esta es la historia de X"(45~130초) | `check_script.py --timeline` |
| 본문 | 6막, 35~65% 지점에서 도입 장면으로 복귀 | `check_script.py` |
| 엔딩 | 현재 → 제도의 교훈 → 질문 | `check_script.py` |
| 제목 | `[훅] \| [고유명사]`, 50~70자, 위험·질문 훅 우선 | `check_title.py` |
| 썸네일 | 어두운 단색 톤 + 중앙 피사체 + 1~4단어 발광 대문자 + 문서 콜라주 | `thumbnail.py`, `check_thumbnail.py` |
| 설명란 | 장면 → 요지 → 연결 문장 → 🔔 → 💬 판단 질문 → 출처·크레디트 | `make_description.py` |
| 태그 | 8~11개 (고유명사 변형 + 분야 + 공통 2 + 채널명 2) | `make_description.py` |
| 일정 | 토요일 16:00 (멕시코시티), 주 1회 | `make_description.py` |

근거: [docs/benchmark-report.md](docs/benchmark-report.md) · 수치: [config/format.json](config/format.json)

## 팀

| 팀 | 에이전트 | 스킬 |
|---|---|---|
| 벤치마크 | format-analyst | `/benchmark` |
| 기획·소재 | case-scout, source-verifier, risk-reviewer, episode-planner | `/scout`, `/plan` |
| 대본 | scriptwriter, fact-checker, spanish-editor, format-auditor | `/write` |
| 패키징 | title-writer, thumbnail-director, packaging-critic | `/package` |
| 제작 | scene-planner | `/produce` |
| 검수·출고 | (독립 검수 3명) | `/audit`, `/release` |

## 같은 것과 다른 것
형식은 같게, 표현은 새로 만든다. 대본 문장, 썸네일 이미지, 채널명, 빨간 대표색, 말버릇은 가져오지 않는다.
대본은 1차 자료로 쓰고, `check_originality.py` 가 레퍼런스 자막 25편과의 문장 겹침을 막는다. 자세히는 [docs/originality.md](docs/originality.md).

## 사람이 정하고 하는 일
- 채널명: **ARCHIVO OSCURO** (결정됨) · 구독 문구: `config/channel.json → own_channel.subscribe_line`
- 썸네일 강조색: `config/format.json → thumbnail.accent` (기본 앰버 `#E0A526`)
- 내레이션 녹음(본인 목소리), 영상 편집·렌더, 업로드

## 설치
```bash
pip install -r requirements.txt
export YT_API_KEY=...          # YouTube Data API v3 (레퍼런스 재측정)
export SUPADATA_API_KEY=...    # 자막 API, 무료 월 100크레딧 (https://dash.supadata.ai)
python3 scripts/benchmark.py fetch   # 레퍼런스 원자료 → data/benchmark/raw/ (커밋 안 함)
```

글꼴: [Anton](assets/fonts/) (SIL Open Font License 1.1, `assets/fonts/OFL.txt`).
