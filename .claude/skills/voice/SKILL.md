---
name: voice
description: 맨 마지막 단계. 내레이션을 만들고(본인 녹음 또는 본인·허락받은 목소리), 음성 길이로 화면을 재타이밍해 최종 렌더하고 최종 품질 검수까지 한다. "녹음", "내레이션", "최종 렌더", "/voice <ep>".
---

# /voice <ep>

팀: `voice-producer` → `video-editor` → `video-qa`. **파이프라인의 마지막 제작 단계다.**

1. **시작 조건:** `/audit` 합격, `renders/<ep>-visual.mp4` 가 `video-qa` 합격, `config/channel.json → voice.consent` 가 `own` 또는 `licensed`. 하나라도 아니면 멈추고 사용자에게 알린다(목소리 동의가 비어 있으면 묻는다).
2. **내레이션:** `voice-producer` → `audio/`(커밋 안 함), `data/voice.json`(줄별 길이). 본인 녹음이면 낭독 대본을 사용자에게 넘기고 파일을 받을 때까지 기다린다.
3. **재타이밍·믹스·최종 렌더:** `video-editor` → `renders/<ep>.mp4`, `release/<ep>.es.srt`.
4. **최종 품질 검수:** `video-qa` → `check_video.py` 전체(음량·트루 피크·무음 포함) + 프레임 판정. 수정이면 3~4를 다시.
5. 보고: 최종 길이, 음량, 화면 전환, video-qa 판정. 대표 프레임과 함께 최종 파일 경로를 알린다. 소리는 측정만 했다면 "들어보지 않았다"고 쓴다.
6. 다음: `/release <ep>`.
