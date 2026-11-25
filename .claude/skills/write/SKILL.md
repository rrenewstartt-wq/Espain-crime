---
name: write
description: 대본 팀을 돌려 plan.md 로 레퍼런스 형식의 스페인어 대본을 쓰고, 사실 확인·스페인어 편집·형식 감사까지 통과시킨다. "대본 써줘", "/write <ep>".
---

# /write <ep>

팀: `scriptwriter` → `fact-checker` → `spanish-editor` → `format-auditor`. 기준: `docs/script-formula.md`.

1. **집필:** `scriptwriter` → `episodes/<ep>/script.md` + `facts.md` 각주. 자체 검사(`check_script.py`, `check_originality.py`) FAIL 0 까지.
2. **사실 확인:** `fact-checker` → `facts.md` 표. ❌ 가 있으면 1로 돌아가 고친다(고칠 문장은 scriptwriter 가).
3. **스페인어 편집:** `spanish-editor` → 사실·구조 유지, 소리만 다듬음.
4. **감사:** `format-auditor` → 합격/수정/불합격. 수정이면 scriptwriter 가 고치고 3~4를 다시. **최대 3회**, 그래도 안 되면 사용자에게 막힌 이유를 보고.
5. 보고: 길이(분), 도입 타임라인(전환·연결 문장 초), FAIL/WARN, ⚠️ 사실 개수, 감사 판정.

검사 기준(`config/format.json`)을 통과시키려고 바꾸지 않는다.
