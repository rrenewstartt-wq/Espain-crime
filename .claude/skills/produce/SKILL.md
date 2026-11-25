---
name: produce
description: 제작 팀을 돌려 확정 대본으로 장면표·소재를 만들고, 레퍼런스·경쟁 채널과 동급 품질의 화면(내레이션 없는 임시 타이밍)을 렌더·검수한다. "장면표", "영상 만들어", "/produce <ep>".
---

# /produce <ep>

팀: `scene-planner` → `video-editor` → `video-qa` (+ 소재 권리는 `risk-reviewer`). 기준: `docs/production-style.md`, `config/format.json → production`.
**내레이션은 이 단계에서 만들지 않는다.** 맨 마지막 `/voice` 에서 한다.

1. 대본 감사가 합격인지 확인(`/write`). 아니면 멈추고 알린다.
1-1. `data/benchmark/video_style.json` 과 `docs/visual-style.md` 가 있는지 확인. 없으면 레퍼런스 화면을 아직 측정하지 못한 것이므로 사용자에게 클립을 요청하고(`docs/production-style.md`), 받으면 `/benchmark` 의 화면 스타일 측정부터 한다.
2. **장면표·소재:** `scene-planner` → `shots.md`(행당 6초 이하, 필수 요소 10가지 체크리스트), `assets/` + `assets/LICENSES.md`.
3. **권리 검토:** `risk-reviewer` 가 `shots.md`·`LICENSES.md` 의 저작권·실존 인물 표시를 본다. 4등급 이상이면 멈추고 사용자에게.
4. **화면 제작:** `video-editor` → HyperFrames 프로젝트 `video/`, 렌더 `renders/<ep>-visual.mp4` (임시 타이밍, 음악·효과음 포함, 내레이션 없음).
5. **품질 검수:** `video-qa` → `check_video.py --visual-only` + 프레임 판정. 수정이면 4~5를 다시(최대 3회). 그래도 안 되면 막힌 항목을 사용자에게 보고.
6. 보고: 길이, 화면 전환 빈도, 최장 정지, 필수 요소 표, video-qa 판정, 대표 프레임 3장(SendUserFile).

검사 기준을 완화하지 않는다. 잠정 기준이면 잠정이라고 보고한다.
