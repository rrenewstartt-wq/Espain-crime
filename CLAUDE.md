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
[5 제작]     제작 팀     scene-planner (+ risk-reviewer)                    /produce     → shots.md
[6 검수]     독립 검수   format-auditor + risk-reviewer + packaging-critic  /audit
[7 출고]     메인 세션   make_description.py                                /release     → release/description.txt, tags.txt, release.json
```
한 편을 처음부터 끝까지: `/make-episode`. 에이전트 정의는 `.claude/agents/`, 스킬은 `.claude/skills/`.
검수 역할(`format-auditor`, `packaging-critic`, `risk-reviewer`)은 파일을 고치지 않는다. 만든 사람과 다른 눈으로 판정만 한다.

## 형식의 기준
- 모든 수치는 `config/format.json` 하나에 있고, 검사 스크립트가 이 파일을 읽는다. 근거는 `docs/benchmark-report.md`.
- 레퍼런스는 2025-11 이후 포맷이 바뀌었다(21~37분, 영상 안 요청 없음). 그 이후만 따른다(`config/channel.json → reference.current_format_since`).
- 사람이 읽는 명세: `docs/script-formula.md`(대본), `docs/title-formula.md`, `docs/thumbnail-formula.md`, `docs/packaging.md`(설명란·태그·일정), `docs/production-style.md`(화면·소리, 미확인 항목 표시), `docs/topic-criteria.md`.

## 반드시 지킬 것
1. **형식은 같게, 표현은 새로.** 대본 작성 중 레퍼런스 자막·영상을 보지 않는다. `check_originality.py` 불합격(8단어 이상 연속 일치, 5-gram 겹침 1% 초과)은 출고 불가.
   레퍼런스 말버릇(`banned.reference_catchphrases`), 빨간 강조색(`thumbnail.forbidden_accents`), 레퍼런스 채널명·구독 문구를 쓰지 않는다.
2. **레퍼런스 원자료는 커밋하지 않는다.** `data/benchmark/raw/`(자막·썸네일·설명란)는 `.gitignore`. 커밋하는 것은 측정값뿐.
3. **사실:** 대본의 사실 문장은 `[^n]` 각주로 `facts.md` 의 1차 자료와 연결한다. ⚠️ 는 공개 전에 1차 자료로 확인, ❌ 는 삭제.
   확정되지 않은 범인·사인·동기는 단정하지 않는다. 생존 피해자·미성년자·미확정 관련자는 실명 대신 이니셜·역할, 썸네일에서는 눈을 가린다.
4. **검사 기준을 낮추지 않는다.** FAIL 은 고치고, 남기는 WARN 은 이유를 보고한다. 기준을 바꾸는 것은 `/benchmark` 로 레퍼런스가 바뀌었을 때만, 사용자 승인 후.
5. **화면 소재는 라이선스가 확인된 것만.** 다른 유튜브·다큐 화면을 쓰지 않는다. 모든 소재는 `shots.md` 와 설명란 `Créditos:` 에.
6. **목소리는 본인 또는 허락받은 목소리만.** 타인 목소리를 복제하지 않는다.
7. **업로드는 사람이 한다.** 이 하네스는 출고 패키지까지만 만든다.
8. **채널명은 ARCHIVO OSCURO.** 사람이 정할 것: 구독 문구(`config/channel.json → own_channel.subscribe_line`), 썸네일 강조색(`config/format.json → thumbnail.accent`, 기본 앰버). 비어 있으면 묻는다.
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
python3 scripts/make_description.py episodes/<ep>                            # 설명란·태그·공개 슬롯
```
이 클라우드 환경에서는 Supadata 키가 네트워크 프록시로 들어가므로 `SUPADATA_API_KEY=proxy-injected` 로 실행한다.
