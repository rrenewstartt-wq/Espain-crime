# 샘플 영상 진행 상태 (video-editor)

## 다시 만들기
```bash
python3 episodes/archivos-del-terror-1992/sample/video/tools/prep_assets.py   # video/assets/ (gitignore) 재생성
python3 episodes/archivos-del-terror-1992/sample/video/tools/build.py         # index.html + compositions/s01..s65 + fx
bash scripts/render.sh episodes/archivos-del-terror-1992/sample/video episodes/archivos-del-terror-1992/renders/sample-visual.mp4
bash scripts/render.sh episodes/archivos-del-terror-1992/sample/video episodes/archivos-del-terror-1992/renders/sample-review.mp4 --variables '{"review":true}'
```
- 생성된 HTML 은 손으로 고치지 않는다. `tools/build.py` 를 고치고 다시 만든다.
- 장면 길이: `build.py → STARTS`(shots.md 시작 시각). /voice 에서 음성 시각으로 바꾸면 전체가 재타이밍된다(오디오 큐 시각은 `AUD` 표, 검토용 대본 줄은 `LINES`).
- 깨끗한 판/검토용 판: `index.html` 변수 `review`(boolean). 기본 false.

## 상태
- 2026-11-25: 65장면 + fx(그레인·비네트·빛 번짐) + 오디오 큐 작성, lint 0 error. 사진 4장(A2·A4·A5·A7) 429 → 대체 그래픽.
- render.sh: 절대 경로 출력이 `$OLDPWD/$OUT` 로 붙어 깨지던 문제 수정(cd 전에 절대 경로로 바꿈).
- 2026-11-26: 컷 감지 보강(샷마다 노출 그레이드 교대: 밝은 장면은 비네트, 어두운 장면은 안개 리프트), 색 온기 보강, 믹스 게인 조정(`GAIN`, 오프라인 합산으로 -15.1 LUFS · 피크 -1.7 dBFS 확인).
  최종: `renders/sample-visual.mp4`(347초 렌더), `renders/sample-review.mp4`(397초), 대표 프레임 `renders/sample-frames/`.
  check_video --visual-only: FAIL 0 (WARN 2: 본문 기준 미적용, 음향 생략). benchmark_frames --compare: FAIL 0 (WARN 1: 단색 톤 0.94 vs 0.65).
