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

## 2차 수정 (video-qa 불합격 대응, 2026-11-26)
- 노출 교대(VG_DARK/VG_LIFT) 삭제. 내부 컷은 `/*cut*/` 표시가 있는 곳만, 모두 다른 소재·크롭·인서트. 계획 샷 103개(`shots.json`).
- 소스 분리: `tools/build_head.py`(타이밍·팔레트·공통 스타일), `tools/build_scenes_a.py`(1–30), `tools/build_scenes_b.py`(31–65), `lib/a3d.js`(three.js 소품), `tools/prep_textures_v2.py`(질감·실루엣).
- 팔레트: 1992 차가운 아침(cold), 문서고 텅스텐(tung), 1954 세피아(sepia). 그레이드(비네트·그레인)는 장면 안, 청록 그래픽은 그 위 `-fg` 층.
- 음향: config `production.audio` 새 기준(음악은 내레이션 -28 dB, 쉬는 2초+ 구간 -20 dB, 효과음은 음악 +6~10 dB). 내레이션 -16 LUFS 가정 → 음악 스템 -43.8 LUFS, 효과음 스템 -35.2 LUFS. 음악 교체: `assets/music/` 에 LICENSES 기록된 곡 → `prep_assets.py` 가 `assets/audio/music.wav` 로 만들고 `build.py → MUSIC` 이 자동 사용.

## 3차 반영 (2026-11-26 오후)
- 실사 사진(§8-1) 오버라이드: `tools/build_scenes_photo.py`, 사진 가공 `tools/prep_photos.py`(크롭·톤·간판/행인 흐림). 사진이 없으면 그래픽 판으로 자동 복귀. 실사 행 32개, 58.2초(47.9%).
- 음악(§7, music-plan.md 기본 조합): M01 0–56.1 / 드론만 56.1–63.9 / M03 63.9 / M02 86.8 (101.4 +3 dB) / 103.9 끊김(드론) / M05 108.1. 곡 파일은 prep 가 `assets/music/` 로 복사, 배치표는 `build.py → MUSIC_PLAN`.
- 음악 스템 -45.0 LUFS(내레이션 -16 가정 시 -29 dB), 드론 -40.2, 효과음 -35.2(음악 +9.8 dB). 쉬는 2초+ 구간은 임시 타이밍에 없음 → /voice 에서 `music_segments()` 로.

## 2차 검수 '수정' 반영 (2026-11-26 저녁)
- IMAGEN ILUSTRATIVA 라벨 추가(39·40·41A·42A·56B), 로페스 궁 라벨 첫 프레임부터.
- 경비·판사(28·29): 인물 대신 문 판자 위 그림자(사진 질감 multiply). 상자 행렬(48, three.js): 인물 제거, 갈색 판지.
- 확대 배율: 모든 실사 행에 check_mag(`MAGS`), 최대 1.50. 28행 펀치인 1.25(원본 대비 1.5), 19행 B 1.42~1.48, 16행 배경 1.5.
- 투손 간판: 흐림 대신 같은 벽의 회벽 질감으로 아치 테두리를 메움(`prep_photos.clean_sign`).
- 지도: 1856 지도를 한 장으로(이음매 없음), 바다도 한 장. 강조 국가는 밝은 바탕 + 청록 빗금. 라벨에 "base: mapa de 1856 (LOC)".
- 드론: -46 LUFS, 끊긴 뒤 약 1초 무음 후 페이드인(57.1, 104.7).

## 4차본 (자료 영상) 진행 중 — 2026-11-26
- [ ] 클립 가공(prep_footage.py) · [ ] 장면 교체 · [ ] 지도 수정 · [ ] 상자 장면 · [ ] 렌더 2판 · [ ] 검사
- [x] 클립 가공(prep_footage.py, 24키)
- [x] 장면 교체 코드(build_scenes_footage.py) · [x] 지도 라벨/선 · [x] 상자 밝기 (빌드 확인 전)
- 빌드 확인: 실사 42행 79.0초(65.1%), 움직이는 실사 25행 40.8초(33.6%), 샷 105, 확대 최대 1.5. 다음: 렌더 2판 → 검사.
- 깨끗한 판 렌더 완료(305초). 검토용 판 렌더 중.
- 채도 WARN(0.319) → 차가운 책상 질감 채도 낮춤, 움직이는 실사 계산을 구간 합집합으로 수정(38.5초). 두 판 재렌더 중.
- 4차본 두 판 렌더 완료, 검사 PASS(채도 0.301).
