# espain-crime 하네스 — Claude 운영 지침

이 저장소는 **스페인어 단일 사건 다큐 롱폼 채널**을 만드는 하네스다. 레퍼런스 채널 **Detrás del Enigma(@detrasdelenimga)** 의
형식·공식·스타일을 **수치로 고정해 그대로 재현**하고, 표현(대본 문장·썸네일 이미지·채널명·대표색)은 직접 만든다(`docs/originality.md`).
대본과 화면 결과물은 스페인어, 문서와 보고는 한국어로 쓴다.

## 파이프라인과 팀

```
[0 벤치마크]  벤치마크 팀  format-analyst                                  /benchmark   → data/benchmark/summary.json, config/format.json
[1 소재]     기획·소재 팀 case-scout → source-verifier + risk-reviewer       /scout       → data/topics/backlog.json
[2 기획]     기획·소재 팀 episode-planner                                   /plan        → episodes/<ep>/plan.md
[3 대본]     대본 팀     scriptwriter → fact-checker → spanish-editor → format-auditor   /write → script.md, facts.md
[4 패키징]   패키징 팀   title-writer → thumbnail-director → packaging-critic           /package → titles.txt, thumbnail/out.png
[5 화면]     제작 팀     scene-planner → video-editor → video-qa (내레이션 없음)        /produce → shots.md, video/, renders/<ep>-visual.mp4
[6 검수]     독립 검수   format-auditor + risk-reviewer + packaging-critic + video-qa   /audit
[7 목소리]   제작 팀     voice-producer → video-editor → video-qa  ★맨 마지막            /voice   → renders/<ep>.mp4, release/<ep>.es.srt
[8 출고]     메인 세션   make_description.py                                /release     → release/description.txt, tags.txt, release.json
```
한 편을 처음부터 끝까지: `/make-episode`. HyperFrames 작업 전에는 `/hyperframes` 스킬을 먼저 읽는다. 에이전트 정의는 `.claude/agents/`, 스킬은 `.claude/skills/`.
검수 역할(`format-auditor`, `packaging-critic`, `risk-reviewer`, `video-qa`)은 파일을 고치지 않는다. 만든 사람과 다른 눈으로 판정만 한다.

## 형식의 기준
- 모든 수치는 `config/format.json` 하나에 있고, 검사 스크립트가 이 파일을 읽는다. 근거는 `docs/benchmark-report.md`.
- 레퍼런스는 2025-11 이후 포맷이 바뀌었다(21~37분, 영상 안 요청 없음). 그 이후만 따른다(`config/channel.json → reference.current_format_since`).
- 사람이 읽는 명세: `docs/script-formula.md`(대본), `docs/title-formula.md`, `docs/thumbnail-formula.md`, `docs/packaging.md`(설명란·태그·일정), `docs/production-style.md`(제작 순서·영상 품질 기준·필수 화면 요소), `docs/topic-criteria.md`.

## 반드시 지킬 것
0. **영상 품질은 레퍼런스·경쟁 4채널과 최소 동급.** `config/format.json → production` 기준(1080p, -14 LUFS, 6초 넘는 정지 화면 금지, 필수 화면 요소 10가지)과 `video-qa` 판정을 통과하지 못하면 출고하지 않는다. 잠정 기준도 완화하지 않는다. 화면 스타일·포맷·구성(컷 리듬·색·그래픽·막별 화면 흐름)도 동급이어야 하며, `benchmark_frames.py --compare` 와 `video-qa` 의 접촉 시트 비교로 판정한다. 레퍼런스 클립 측정 전에는 화면 스타일 동급을 확인할 수 없다.
00. **목소리 내레이션은 맨 마지막.** 화면 제작·모든 검수가 끝난 뒤 `/voice` 에서만 녹음한다. 녹음 후 음성 길이로 재타이밍해 최종 렌더한다.
1. **형식은 같게, 표현은 새로.** 대본 작성 중 레퍼런스 자막·영상을 보지 않는다. `check_originality.py` 불합격(8단어 이상 연속 일치, 5-gram 겹침 1% 초과)은 출고 불가.
   레퍼런스 말버릇(`banned.reference_catchphrases`), 빨간 강조색(`thumbnail.forbidden_accents`), 레퍼런스 채널명·구독 문구를 쓰지 않는다.
2. **레퍼런스 원자료는 커밋하지 않는다.** `data/benchmark/raw/`(자막·썸네일·설명란)는 `.gitignore`. 커밋하는 것은 측정값뿐.
3. **사실:** 대본의 사실 문장은 `[^n]` 각주로 `facts.md` 의 1차 자료와 연결한다. ⚠️ 는 공개 전에 1차 자료로 확인, ❌ 는 삭제.
   확정되지 않은 범인·사인·동기는 단정하지 않는다. 생존 피해자·미성년자·미확정 관련자는 실명 대신 이니셜·역할, 썸네일에서는 눈을 가린다.
4. **검사 기준을 낮추지 않는다.** FAIL 은 고치고, 남기는 WARN 은 이유를 보고한다. 기준을 바꾸는 것은 `/benchmark` 로 레퍼런스가 바뀌었을 때만, 사용자 승인 후.
5. **화면 소재는 라이선스가 확인된 것만.** 다른 유튜브·다큐 화면을 쓰지 않는다. 모든 소재는 `shots.md` 와 설명란 `Créditos:` 에.
6. **목소리는 본인 또는 서면 허락받은 목소리만**(`config/channel.json → voice.consent`, 비어 있으면 묻는다). 타인 목소리를 복제하지 않는다. 음성·렌더 파일은 커밋하지 않는다.
7. **업로드는 사람이 한다.** 이 하네스는 최종 영상과 출고 패키지까지 만든다.
8. **채널명은 ARCHIVO OSCURO.** 구독 문구는 'Suscríbete para no perderte el próximo expediente.'. 강조색은 청록 `#2EC4B6`(빨강=레퍼런스, 앰버=Anatomía 는 금지). 재연 장면은 2.5D 사진·문서 콜라주 + 인포그래픽(`docs/visual-style.md`).
9. YouTube 가 막히면(봇 확인, IP 차단) 우회하지 않는다. 자막은 Supadata API(`SUPADATA_API_KEY`, 월 100크레딧)로 받는다.

## 자주 쓰는 명령
```bash
pip install -r requirements.txt
python3 scripts/benchmark.py fetch && python3 scripts/benchmark.py analyze   # 레퍼런스 재측정 (YT_API_KEY, SUPADATA_API_KEY)
python3 scripts/topics.py list --top 10                                      # 소재 순위 (add / check / show / set / rescore)
python3 scripts/new_episode.py <slug> --subject "<고유명사>"                  # 에피소드 폴더
python3 scripts/check_script.py episodes/<ep> --timeline                     # 대본 형식 (도입 타임라인 포함)
python3 scripts/check_originality.py episodes/<ep>                           # 레퍼런스와의 문장 겹침
python3 scripts/check_title.py --file episodes/<ep>/titles.txt               # 제목 공식
python3 scripts/thumbnail.py episodes/<ep> && python3 scripts/check_thumbnail.py episodes/<ep>
bash scripts/render.sh episodes/<ep>/video episodes/<ep>/renders/<ep>-visual.mp4   # HyperFrames 렌더 (설정 고정)
python3 scripts/check_video.py episodes/<ep>/renders/<ep>-visual.mp4 --visual-only   # 화면 품질 (내레이션 전)
python3 scripts/check_video.py episodes/<ep>/renders/<ep>.mp4                 # 최종 품질 (음량 포함)
python3 scripts/make_description.py episodes/<ep>                            # 설명란·태그·공개 슬롯
```
이 클라우드 환경에서는 Supadata 키가 네트워크 프록시로 들어가므로 `SUPADATA_API_KEY=proxy-injected` 로 실행한다.
