# 샘플 실사 배치 제안: archivos-del-terror-1992 — 0:00~2:01

작성 2026-11-26 · scene-planner. **제안서다.** `shots.md` 와 `sample/video/` 는 고치지 않았다(video-editor 담당). 행 번호·시각은 `sample/shots.md`(168단어/분 임시 타이밍) 기준.
소재 라이선스는 `assets/LICENSES.md` §8. 파일은 `assets/photos/`.

## 왜 바꾸나
video-qa 판정: 실사 비중 약 9% → 레퍼런스(사진·실사 콜라주가 거의 전부)와 동급 아님.
지금 실사가 들어간 행은 7·18·19·32·33·34·62 의 7행(10.4초, **8.6%**)이다.

| 배치안 | 실사 들어가는 행 | 길이 | 비중 |
|---|---:|---:|---:|
| 현재 | 7행 | 10.4초 | 8.6% |
| **이 제안, 지금 받은 파일만** | 35행 | 63.4초 | **52.3%** |
| + Flickr 대기분(§8-2) + Commons 대기분(A2 알마다, A4 Museo, A5 카세트) | 42행 | 77.3초 | 63.7% |

나머지 행은 날짜 카드·연표·숫자 카드·도식이다. 숫자 카드 행(39~42)에도 사진을 흐린 배경으로 깔아 실사 비중에 넣었다. 레퍼런스가 거의 100% 인지는 ❓ **가설**이다(도입부 클립 5개 측정만 근거). 여기서 더 올리려면 날짜 카드·연표 행에도 사진 바탕을 깔아야 한다. 그 판단은 video-qa 의 접촉 시트 비교에 맡긴다.

## 공통 규칙
- **2.5D 콜라주 방법:** 사진 1장을 앞·중간·뒤 2~3겹으로 오려 패럴랙스. 거기에 직접 만든 실루엣·종이·라벨을 얹는다. 6초 넘게 멈춘 화면은 없다(모든 행 2.6초 이하).
- **라벨:** 사건과 무관한 실물·장소 사진은 `Imagen ilustrativa`. 그 위에 인물 실루엣·소품을 합성하면 `RECREACIÓN`. 1차 문서는 `DOCUMENTO REAL` + 출처. 장소 실사는 `IMAGEN REAL` + 연도.
- **색:** HABS/HAER·LOC 사진은 흑백 원본이다. 1992 장면은 차가운 저채도 톤에 맞추고, 1954 장면은 따뜻한 세피아로 맞춘다(❓ 가설, shots.md 와 같음). 청록 `#2EC4B6` 은 글자·선·강조 박스에만 쓴다.
- **잘라 낼 것:** HABS 필름 테두리, `HABS No.` 글자, 촬영 번호표. 영어 글씨(장부·상자 라벨)는 매크로·흐림으로 읽히지 않게 한다.
- **얼굴:** 피해자 사진은 없다. Harris & Ewing 두 장(1930·1932)에는 사건과 무관한 일반인 얼굴이 보인다 → **얼굴이 안 들어가게 자르거나 흐림 필수**. 공인 얼굴은 스트로에스네르(A1)뿐이다.
- **오해 방지:** 미국 건물 사진(HABS)을 람바레·아순시온 현장이라고 말하지 않는다. 특히 투손 "COMANDANCIA DE POLICÍA" 간판은 **잘라 내거나 흐린다.** 스페인어 간판이 보이면 파라과이 현장 사진으로 오해된다.

## 1. 우선 구간 A — 건물·인물 재연 (0:13.9–0:17.8, 0:45.5–0:58.2)

| # | 시각 | 현재 화면 | 제안 사진 (`photos/`) | 화면 구성 | 라벨 |
|---|---|---|---|---|---|
| 9 | 0:13.9 (1.7s) | 경찰 건물 벡터 실루엣 | **지금:** `habs_az0060_tucson_comandancia_policia_1937.jpg`. 간판을 빼고 아치 문·회벽·창만 크롭. **Flickr 받으면 교체 후보:** `flickr_comandancia_policia_nacional_ramalleira.jpg`(아순시온 경찰청 본부 실사) | 회벽 건물 3겹 패럴랙스(벽·문·하늘). 기관 자막 `DEPARTAMENTO DE PRODUCCIONES — Policía, Lambaré` 는 그대로 | `RECREACIÓN` (실제 람바레 건물 아님). Ramalleira 판이면 `Imagen ilustrativa · Comandancia de la Policía Nacional, Asunción (foto 2023)` |
| 10 | 0:15.6 (2.2s) | 문틀 실루엣 + 뒷모습 인물 | 9 번 행과 같은 사진의 **아치 문 클로즈업**. 다른 안: `haer_pa0995_abandoned_office.jpg` 의 열린 문 | 문 안쪽 어둠으로 push-in, 서류 든 뒷모습 실루엣(직접 제작)이 들어감 | `RECREACIÓN` |
| 25 | 0:45.5 (2.3s) | 빈 서랍 3D 소품 | `habs_pa2957_file_cabinets_record_vault_1994.jpg`(서랍 열린 나무 서류장) | 열린 서랍 하나로 push-in, 서랍 속을 어둡게 비우고 먼지 입자 | `RECREACIÓN` |
| 26 | 0:47.9 (1.6s) | 건물 실루엣 복귀 `VERSIÓN POLICIAL` | **9 번 행과 같은 판** | 같은 구도·느린 push-in(되돌아오기 규칙: 같은 건물 판을 다시 씀) | `RECREACIÓN` |
| 27 | 0:49.5 (1.6s) | 타이포 `NADA QUE BUSCAR` | `owi_1942_battle_scarred_typewriter_liberman.jpg` 자판 크롭 | 흐린 타자기 위로 타이포가 찍힘 | `Imagen ilustrativa` |
| 28 | 0:51.1 (2.5s) | 경비 경찰 실루엣 | 9 번 판의 아치 문 + 경비 실루엣(직접 제작) | 문 앞을 막는 손 | `RECREACIÓN` · 역할 자막 `OFICIAL DE GUARDIA` 유지 |
| 29 | 0:53.6 (2.5s) | 판사 실루엣 + 영장, 역광 | 같은 문, 반대 방향(역광) | 문 안 빛을 키워 역광, 영장 종이 재연(G6) | `RECREACIÓN` |
| 31 | 0:58.2 (1.2s) | 어두운 계단(직접 제작) | `habs_pa1976_basement_stairway.jpg`(돌벽 지하와 나무 계단) | 계단을 따라 tilt-up + 손전등 빛 원 | `RECREACIÓN` |
| 32 | 0:59.4 (1.2s) | 자물쇠 문(A7 대기 → A6 단독) | `habs_il0937_basement_stairs_door_2008.jpg`(낡은 나무 문) + A6 자물쇠 | 문 사진에 A6 자물쇠 합성. **A7(Commons 429) 대신 이 문을 쓰면 대기 없이 완성** | `RECREACIÓN` |

regreso("Es otra vez la mañana…")에서는 **9·26·28 번 행의 건물·문 판과 31·32 번 행의 계단·문 판을 그대로** 다시 쓴다(shots.md "도입 ↔ regreso 같은 소재" 3번 항목을 실사 판으로 바꾸는 것).

## 2. 우선 구간 B — 문서고 발견 (1:00.6–1:29.0)

| # | 시각 | 현재 화면 | 제안 사진 (`photos/`) | 화면 구성 | 라벨 |
|---|---|---|---|---|---|
| 33–34 | 1:00.6–1:02.9 | A6 자물쇠 매크로·파손 | (그대로 A6) | — | `RECREACIÓN` |
| 35 | 1:02.9 (1.0s) | 문 열림 빛 번짐 | `habs_ca2282_vault_forced_entry_1997.jpg`(벽이 깨진 금고실, 열린 문, 바닥 잔해) | 빛 번짐이 걷히면 부서진 방이 드러남(1프레임 플래시 뒤) | `RECREACIÓN` |
| 36 | 1:03.9 (1.2s) | 직접 만든 서류 산 | `habs_ma1170_record_storage_room_1982.jpg`(천장까지 쌓인 서류) | 서가 3겹 패럴랙스, 위쪽 전등 빛 | `Imagen ilustrativa` |
| 37 | 1:05.1 (1.2s) | 색인 카드 클로즈업 | `habs_ca2248_card_catalog_drawers_1996.jpg`(카드 서랍 벽) → 서랍 하나로 줌, 안에 직접 만든 빈 카드(G12) | 실사 서랍 + 재연 카드 | `RECREACIÓN` (카드 글씨 판독 불가 유지) |
| 38 | 1:06.3 (1.2s) | 장부·폴더 측면 팬 | `haer_ne0071_handwritten_ledger_1879.jpg` 매크로(글씨가 읽히지 않게 얕은 심도) | 측면 팬 | `Imagen ilustrativa` |
| 39 | 1:07.5 (2.2s) | `≈ 800.000 PÁGINAS` | 36 번 사진을 흐리게(어둡게 60%) 깔고 숫자 카운터 | 숫자 카드 + 사진 바탕 | 출처 라벨 유지 |
| 40 | 1:09.7 (1.7s) | 종이 탑 tilt-up | 36 번 사진 세로 tilt-up | 같은 판 연속 | `Imagen ilustrativa` |
| 41 | 1:11.4 (2.5s) | `≈ 200 METROS LINEALES` 줄자 선 | `hec_1932_filing_fingerprints_mugshots.jpg` 의 **끝없는 서류장 통로**(앞 직원 얼굴은 잘라 냄) | 청록 줄자 선이 통로 소실점까지 달림 | `Imagen ilustrativa` |
| 42 | 1:13.9 (2.1s) | `11.225 FICHAS` 카드 격자 | 37 번 카드 서랍 벽 + 서랍마다 숫자가 켜짐 | 숫자 카드 + 사진 바탕 | `Imagen ilustrativa` |
| 43 | 1:16.1 (1.6s) | `≈ 20.000 FOTOGRAFÍAS` 빈 인화지 격자 | (받은 것 중 맞는 사진 없음 — 그래픽 유지) | — | — |
| 44 | 1:17.7 (1.6s) | `543 CASETES` + A5(대기) | A5 대기. 대안 없음 | — | `Imagen ilustrativa` |
| 47 | 1:22.9 (2.0s) | `≈ 12 HORAS` 시계 | (그래픽 유지) | — | — |
| 48 | 1:24.9 (1.9s) | 상자 줄 실루엣 | Flickr 대기 `flickr_archive_boxes_jvl_1.jpg`(기록 상자) | 상자 행렬 + 손 실루엣 | `RECREACIÓN` |
| 49 | 1:26.8 (2.2s) | 눅눅한 종이 결 매크로 | `haer_ne0071_handwritten_ledger_1879.jpg` 종이 가장자리 매크로 + 습기 얼룩(직접 합성) | 질문 1 타격과 함께 | `RECREACIÓN` |

## 3. 그 밖의 행

| # | 시각 | 제안 사진 | 화면 구성 | 라벨 |
|---|---|---|---|---|
| 3 | 0:03.6 | `nasa_sts072-730-079_asuncion_1996.jpg`(우주에서 본 아순시온, 1996) | M1 휩 줌 끝에서 위성 사진으로 크로스페이드 → 4 번 OSM 지도로 이어짐 | `IMAGEN REAL · NASA, 1996` |
| 4 | 0:05.0 | 같은 NASA 사진 크롭(강 굽이) → M2 | 4 km 원은 OSM 지도에서만(OSM 표기 유지) | `MAPA` + `© OpenStreetMap contributors` |
| 14 | 0:23.9 | `owi_1942_battle_scarred_typewriter_liberman.jpg` | 사건 표지가 타자기 롤러에 물린 채 글자가 찍힘 | `RECREACIÓN` |
| 23 | 0:40.7 | 같은 타자기, 다른 크롭 | 메모 `RESPUESTA OFICIAL` 이 타자기에서 올라옴(귀속 라벨 유지) | `RECREACIÓN` |
| 51–52 | 1:31.1–1:34.7 | `map_loc_1856_basin_la_plata_page_usn.jpg`(1856 라플라타 유역 지도, 미 해군) | 지도 **질감 바탕**에 Natural Earth 국경을 얹어 3국 점등·청록 선. 1856년 국경은 오늘과 달라 그대로 쓰지 않는다 | `Mapa de 1856 (Library of Congress)` 작게 |
| 53 | 1:34.7 | (선택) `doc_cia_1976-07-21_condor_cable_p2.png` 를 국적 도장 카드 뒤에 흐리게 | 1차 문서 질감. facts 연결 전에는 텍스트를 읽히게 하지 않는다 ⚠️ | `DOCUMENTO REAL · CIA, 1976` |
| 55 | 1:38.9 | `hec_1930_fingerprint_sheet_file_cabinet.jpg` 의 **지문 카드·서랍 부분만**(남성 얼굴 제외) | 재연 카드(G14) 옆에 실사 지문 용지 질감 | `Imagen ilustrativa` |
| 56 | 1:41.4 | 41 번 통로 사진 + 37 번 서랍 벽 | 카드 벽이 화면을 덮을 때 실사 서랍 벽으로 전환 | `Imagen ilustrativa` |
| 58 | 1:45.3 | A4(Museo de la Justicia, Commons 대기). 대체 실사 없음 | — | — |
| 60–61 | 1:48.1–1:52.1 | `loc_asuncion_palacio_lopez_1908-1919_npco.jpg`(아순시온 강변·Palacio de los López, 유리 원판) | 날짜 카드 `MAYO · 1954 — ASUNCIÓN` 뒤 세피아 바탕, 연표 축이 강변 수평선과 겹침 | `IMAGEN REAL · Asunción, c. 1910` (**1954년 사진 아님 — 연도 라벨 필수**) |
| 62 | 1:52.1 | A1 스트로에스네르 초상(그대로) | — | 기존대로 |
| 63 | 1:54.3 | `doc_cia_1954-05-07_paraguayan_political_crisis_p1.png` | 문서 push-in, 강조 막대가 `Paraguayan Political Crisis`·`7 May 1954` 와 `took over police headquarters` 줄을 훑음 → 연표 표지 `MAYO 1954 · GOLPE MILITAR` | `DOCUMENTO REAL · Informe CIA, 7 may. 1954 (desclasificado)` |
| 64–65 | 1:56.4–2:01.4 | Flickr 대기 `flickr_palacio_lopez_night_ciuffo.jpg` 또는 지금 있는 LOC 1908 판 재사용 | 35년 막대·7블록 뒤 흐린 바탕 | `Imagen ilustrativa` |

## 4. 사실 확인이 필요한 것 (fact-checker 에게)
- **63 행 CIA 1954-05-07 보고서:** 문서에 스트로에스네르 이름은 없다. 차베스 대통령 구금·사임서 제출, 40대대의 경찰 본부 점거, 사망 약 24명이 적혀 있다. 대본 L39("Ese mes, un golpe militar…")와 facts.md #26 에 이 문서를 각주로 붙일지 판단이 필요하다 ⚠️. 강조 줄은 각주가 붙은 문장만 쓴다.
- **53 행 CIA 1976-07-21 콘도르 전문:** facts.md #16 은 1976-07-28 전문을 인용한다. 이 07-21 전문을 화면에서 읽히게 하려면 각주를 추가해야 한다 ⚠️. 그 전에는 흐린 질감으로만 쓴다. 본편 escalada(콘도르 절, script L117~126)에 더 맞다.
- **9·26·28 행:** 실제 Departamento de Producciones 건물 사진은 여전히 없다(위치도 미확인, shots.md M2 메모). 그래서 실사 판이어도 `RECREACIÓN` 표시를 유지한다.

## 5. 못 구한 것 (이 샘플 범위)
- Archivo del Terror·CDyA 실물(문서·카드·상자) 사진: 라이선스가 확인되는 출처를 찾지 못했다. pj.gov.py 는 "© Derechos Reservados", Commons 는 429, UNESCO 신청서는 재사용 조건이 없다(LICENSES §8-4).
- 람바레 1990년대 거리: Flickr 흑백 필름 사진 1장(촬영 연도 미상, 대기)뿐이다.
- 스트로에스네르 시대(1954~89) 아순시온 거리·경찰·군 PD 사진: LOC·NASA·IA 에 없었다. Flickr 1986 Puerto Stroessner 1장(대기)만 있다. NARA 는 API 키가 필요해 검색하지 못했다.
- 마르틴 알마다 대체 사진: Commons 외 CC 출처를 찾지 못했다(A2 대기 유지).
- 카세트(44 행) 대체 사진: A5 대기 유지.
