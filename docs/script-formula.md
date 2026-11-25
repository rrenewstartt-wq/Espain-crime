# 대본 공식

수치는 `config/format.json` 이 기준이고, `scripts/check_script.py` 가 검사한다. 근거는 레퍼런스 현재 포맷 자막 18편(`docs/benchmark-report.md`).

## 파일 형식 (`episodes/<ep>/script.md`)

```markdown
---
title: "La Ciudad que Explotó desde sus Alcantarillas | Guadalajara 1992"
subject: "Explosiones de Guadalajara"          # 연결 문장에 들어갈 고유명사
---

## apertura
22 de abril de 1992. Son las diez y cinco de la mañana en el barrio de Analco, en Guadalajara.
…

## origen
…
```

- `## <막 id>` 6개를 순서대로: `apertura` `origen` `escalada` `regreso` `consecuencias` `hoy`.
- 본문은 **내레이션 문장만** 쓴다. 화면 지시는 `> ` 로 시작하는 줄(검사·낭독에서 빠짐), 출처 번호는 문장 끝 `[^3]` 각주로(`facts.md` 와 연결).
- 시간은 **분당 168단어**로 계산한다(`config/format.json → narration.wpm`). 1분 ≈ 168단어, 26분 ≈ 4,400단어.

## 1. 도입 (`apertura`, 0~2분)

| 시점 | 할 일 | 검사 |
|---|---|---|
| 첫 문장 | **날짜·시각으로 시작하는 장면.** 현재형 | 첫 문장에 연도·날짜·시각 |
| 0~20초 | 평범한 상황. 구체적 숫자 1~2개(승객 수, 거리, 금액) | |
| 15~60초 | **전환 문장.** 평범함을 깨는 한 문장. 기능만 가져오고 문장은 새로: "Todo encaja. Hasta que, a las diez y seis…", "Nadie sospecha nada. Pero esa mañana…" 레퍼런스 문형("o al menos eso es lo que parece", "lo que todavía no sabe es que")은 금지 | `turn_markers` 중 하나, `reference_catchphrases` 없음 |
| 전환 뒤 | 규모를 키우는 숫자 나열 (피해·범위·기간) | |
| 연결 문장 직전 40초 | **질문 2~4개**, 마지막은 "Y sobre todo, ¿…?" | 질문 수, 마지막 질문 |
| 45~130초 | **연결 문장** "Esta es la historia de [subject]." 또는 "Este es el misterio de [subject]." | `bridge_markers` + subject |
| 연결 직후 | 되감기: "Para entender …, hay que volver a [연도]." 또는 인물 출생부터 | |

**금지:** 인사, 채널 소개, 구독·좋아요 요청, "이 영상에서는…" 식의 목차 안내. 레퍼런스 현재 포맷 18편 중 0편.

## 2. 본문 6막

| 막 | 분량 | 할 일 |
|---|---|---|
| `apertura` | 4~8% | 위 표 |
| `origen` | 15~25% | 인물·조직·장소의 배경. 기술·제도 개념은 "Funciona así. Si tú …" 처럼 2인칭 예시로 한 번에 설명 |
| `escalada` | 20~30% | 수법·규모가 커지는 과정. 단계마다 숫자 하나 |
| `regreso` | 10~15% | **도입의 그 순간으로 돌아온다.** 영상의 35~65% 지점. 같은 날짜·시각을 다시 말한다 |
| `consecuencias` | 15~25% | 수사·재판·폭로. **진위가 의심되는 소재는 여기서 해체**: 기술적 모순 → 기록 부재 → 최초 출처 순서로 증거를 쌓는다 |
| `hoy` | 5~10% | 지금 그 사람·장소·기술은 어떤가 → 개인이 아니라 **제도·구조의 교훈** → 마지막 질문 |

- 질문은 분당 0.1~0.6개. 막을 넘길 때만 쓴다.
- 한 문장 평균 20단어 이하. 한 문장에 사실 하나.
- **현재형 유지:** "Son las…", "Ahora mismo…", "A esta hora…". ("En este preciso momento" 는 레퍼런스 말버릇이라 금지) 회상 장면도 현재형, 결과를 말할 때만 과거·미래형.

## 3. 엔딩 (`hoy`)
- 현재 상황 표지어(hoy, a día de hoy, años después, todavía, sigue) 하나 이상.
- 교훈은 개인 비난보다 **제도·시스템**: 레퍼런스 댓글에서 '제도 비판' 댓글이 좋아요 합계 1위(3.1만)였다.
- **마지막 문장은 질문**이고, 시청자가 판단하게 만든다. 형태는 매번 새로 쓴다. 레퍼런스의 "la pregunta de verdad no es si…" 문형은 금지(`banned.reference_catchphrases`).
- 엔딩에도 구독 요청은 없다. 구독 줄은 설명란에만.

## 4. 스페인어
- 중립 라틴아메리카 스페인어. `tú`, `ustedes`. **vosotros 금지**, 지역 속어 금지.
- 숫자는 낭독하기 쉽게: 큰 수는 "4.000 millones", 연도는 숫자.
- 확인 안 된 최상급("el más grande de la historia") 금지. 근거가 있으면 출처와 함께.
- 사인·범인·동기가 확정되지 않았으면 단정하지 않는다.

## 5. 예시 도입 (형식 시연용, 새로 쓴 문장)

```
22 de abril de 1992. Son las diez y cinco de la mañana en el barrio de Analco, en Guadalajara.
Los vecinos llevan tres días quejándose de un olor a gasolina que sale de las alcantarillas.
Los bomberos han venido, han medido y se han ido. Todo está bajo control.
Todo encaja. Hasta que, a las diez y seis, la calle Gante se levanta del suelo.
En menos de una hora, ocho kilómetros de calles explotan desde abajo.
¿Cómo puede explotar una ciudad entera desde sus alcantarillas?
¿Quién sabía lo que estaba pasando?
Y sobre todo, ¿por qué nadie hizo nada?
Esta es la historia de las explosiones de Guadalajara.
Para entender lo que pasó esa mañana, hay que volver a los años setenta…
```
*사실관계는 `facts.md` 로 검증하기 전의 시연 문장이다.*
