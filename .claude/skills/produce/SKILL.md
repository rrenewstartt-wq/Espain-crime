---
name: produce
description: 제작 팀을 돌려 확정 대본을 장면표(shots.md)로 바꾸고 화면 소재·라이선스를 모은다. "장면표", "/produce <ep>".
---

# /produce <ep>

팀: `scene-planner` (+ 소재 위험은 `risk-reviewer`).

1. 대본 감사가 합격인지 확인(`/write` 결과). 아니면 멈추고 알린다.
2. `scene-planner` → `episodes/<ep>/shots.md`.
3. `risk-reviewer` 에게 shots.md 의 저작권·실존 인물 표시를 검토받는다.
4. 보고: 장면 수, 화면 유형 비율, 라이선스 빈칸 수, 예상 길이, ❓ 가설로 둔 스타일 항목.

영상 렌더·음성 녹음은 이 하네스 밖에서 사람이 한다(`docs/production-style.md`). 목소리는 본인 또는 허락받은 목소리만.
