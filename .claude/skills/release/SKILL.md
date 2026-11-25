---
name: release
description: 출고 패키지(설명란, 태그, 공개 예정 슬롯)를 만든다. 업로드는 사람이 한다. "설명란", "태그", "언제 올려", "/release <ep>".
---

# /release <ep>

1. `/audit` 합격인지 확인.
2. `meta.json` 의 hook_line(날짜·장소가 든 장면 한두 문장), context(요지 1~2문단), comment_question(제도의 선택을 묻는 💬 질문), tags_subject(고유명사 변형 3~5개), tags_field(1~2개)를 채운다. 문장은 대본과 같은 사실만.
3. `python3 scripts/make_description.py episodes/<ep>` → `release/description.txt`, `tags.txt`, `release.json`(다음 토요일 16:00 멕시코시티).
4. 사용자에게 제목·설명란·태그·썸네일·공개 시각을 한 번에 보여 준다.
5. **업로드하지 않는다.** 사람이 올리고 알려 주면 `topics.py set <slug> 공개`, `release.json → uploaded: true`.

채널 구독 문구(`config/channel.json → own_channel.subscribe_line`)가 비어 있으면 사용자에게 정해 달라고 한다.
