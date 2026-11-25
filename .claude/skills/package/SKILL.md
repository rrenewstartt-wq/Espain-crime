---
name: package
description: 패키징 팀을 돌려 제목·썸네일을 만들고 한 묶음으로 검수한다. "제목이랑 썸네일", "/package <ep>".
---

# /package <ep>

팀: `title-writer` → `thumbnail-director` → `packaging-critic`.

1. `title-writer` → `titles.txt`, 상위 3개.
2. 사용자가 제목을 고르면(또는 "알아서"면 1순위) `meta.json → title` 과 `script.md` frontmatter `title` 에 넣는다.
3. `thumbnail-director` → `thumbnail/spec.json`, `out.png`, `out-168.png` (안 2개까지).
4. `packaging-critic` → 판정. 수정이면 2~3을 다시(최대 2회).
5. 사용자에게 `out.png` 를 보여 주고(SendUserFile) 제목과 함께 확인받는다.

강조색·채널명이 아직 정해지지 않았으면(`config/channel.json → own_channel`) 사용자에게 먼저 묻는다.
