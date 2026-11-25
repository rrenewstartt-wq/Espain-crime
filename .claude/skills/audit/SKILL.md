---
name: audit
description: 에피소드 하나를 출고 전에 전부 검사한다(형식·독창성·사실·위험·패키징). "검수", "출고 전 확인", "/audit <ep>".
---

# /audit <ep>

검사기 전부 + 독립 검수 4명(`format-auditor`, `risk-reviewer`, `packaging-critic`, `video-qa`)을 **동시에** 돌린다. 내레이션 전 단계라 영상은 `renders/<ep>-visual.mp4` 를 본다.

```bash
python3 scripts/check_script.py episodes/<ep> --timeline
python3 scripts/check_originality.py episodes/<ep>
python3 scripts/check_title.py "$(python3 -c "import json;print(json.load(open('episodes/<ep>/meta.json'))['title'])")"
python3 scripts/check_thumbnail.py episodes/<ep>
python3 scripts/check_video.py episodes/<ep>/renders/<ep>-visual.mp4 --visual-only
```

판정표: 대본 형식 | 독창성 | 사실(⚠️·❌ 개수, facts.md) | 위험(4 이상) | 제목 | 썸네일 | 화면 품질(video-qa).
하나라도 불합격이면 "출고 불가"와 이유. 모두 합격이면 마지막 단계 `/voice <ep>` (내레이션 → 최종 렌더) → `/release <ep>`.
