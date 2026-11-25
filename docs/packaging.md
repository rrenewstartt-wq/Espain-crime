# 설명란 · 태그 · 업로드 일정

만들기: `python3 scripts/make_description.py episodes/<ep>` → `episodes/<ep>/release/description.txt`, `tags.txt`, `release.json`.
수치는 `config/format.json → description, tags, schedule`.

## 설명란 (레퍼런스 현재 포맷: 구독 줄 97%, 💬 질문 84%, 해시태그 0)

```
[장면 한두 문장: 날짜·장소·충격 사실]                    ← meta.json: hook_line

[사건 요지 1~2문단: 누가, 무엇을, 왜 아직 논란인지]         ← meta.json: context

Esta es la historia de [subject].                          ← 연결 문장 (대본과 같은 고유명사)

🔔 [채널 고유 구독 문구]                                    ← config/channel.json: own_channel.subscribe_line
💬 [판단을 묻는 질문 1개]                                   ← meta.json: comment_question

Fuentes:                                                   ← facts.md 의 1차 자료
- …
Créditos:                                                  ← 쓰인 영상·이미지의 출처와 라이선스
- …
```
- 💬 질문은 **제도의 선택을 묻는 판단 질문**을 우선한다("¿Tú lo habrías denunciado o callado?"). 레퍼런스 댓글에서 제도 비판 반응이 가장 컸다.
- 구독 문구는 레퍼런스의 "SUSCRÍBETE para más historias como esta" 를 쓰지 않는다. 채널 고유 문구는 사람이 정해 `config/channel.json` 에 넣는다.
- 출처·크레디트 줄은 레퍼런스에는 일부만 있지만, 우리는 **항상** 넣는다(사실 확인과 라이선스 근거).

## 태그 (영상당 8~11개, 레퍼런스 중앙값 9)
1. 주제 고유명사와 철자 변형 3~5개: 악센트 있음/없음, 약칭, 별명 (`explosiones de guadalajara`, `guadalajara 1992`, `22 de abril`)
2. 주제 분야 1~2개 (`hacking`, `fraude`, `desastres`)
3. 공통 2개: `misterio`, `casos reales`
4. 자기 채널명 2표기(악센트 있음/없음)

## 업로드 일정
- **매주 토요일 16:00 (멕시코시티)**. 레퍼런스는 토요일이 31편 중 9편으로 가장 많고 게시 시각 중앙값이 16시다.
- 레퍼런스 간격 중앙값은 10.5일이지만, 댓글의 업로드 재촉(36개, 좋아요 6,064)과 최근 48일 공백을 보면 **주 1회 고정**이 빈자리다.
- `make_description.py` 가 다음 빈 토요일을 `release.json` 에 적는다. **업로드는 사람이 한다.** 이 하네스에는 업로드 단계가 없다.
