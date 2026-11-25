# 샘플 장면표: archivos-del-terror-1992 — 0:00~2:01 (apertura 전체 + origen 첫 3문장)

- 기준 대본: `script.md` 도입부 확정본(커밋 5caef74, 2026-11-25). 시간은 **분당 168단어 임시 타이밍**(목소리 녹음 후 재타이밍). `대본 첫 단어` 칸의 `L번호`는 script.md 줄 번호, 백틱 숫자는 시작 시각(초).
- 형식: `docs/production-style.md` 8칸 + 맨 끝 `메모` 칸(재연 표시·사실 주의). 한 행 = 한 화면 박자(컷 또는 카메라 움직임 전환), 모두 6초 이하.
- 화면 문법: `docs/visual-style.md` §3·§4 — 2.5D 사진·문서 콜라주 + 인포그래픽, 강조색 `#2EC4B6`(글자·선·강조 박스에만), 실사풍 생성 영상·스톡·유튜브/TV 화면 없음.
- 재연(직접 만든 실루엣·소품·서류 텍스처, 그리고 현장 사진이 아닌 일반 사진 합성)은 화면 구석에 `RECREACIÓN`, 사건과 무관한 실물 사진은 `Imagen ilustrativa`, 실제 자료에는 출처 라벨.

## 소재 목록

| 코드 | 파일 (`assets/` 기준) | 내용 | 출처·라이선스 |
|---|---|---|---|
| A1 | `commons/stroessner_1954_resck.jpg` (1206×1813) | 스트로에스네르 공식 초상, 1954-08-15 | Casa Fotográfica Resck, Wikimedia Commons, `{{PD-Paraguay}}` ⚠️ |
| A2 ⏳ | `commons/martin_almada_2008.jpg` (1191×2126) | 마르틴 알마다, 2008 | Maria Stella de Almada, Commons, CC BY-SA 4.0 |
| A4 ⏳ | `commons/museo_justicia_archivo_terror_2019.jpg` (960×1280) | 오늘의 Archivo del Terror(Museo de la Justicia), 2019 | Nojaedu, Commons, CC BY-SA 4.0 |
| A5 ⏳ | `commons/heap_of_tapes.jpg` (1638×2000) | 카세트 더미(사건 무관, 일러스트용) | Hmvh, Commons, 퍼블릭 도메인(PD-self) |
| A6 | `commons/padlocks_old_door_frame_varlan.jpg` (2000×1333) | 낡은 문틀의 자물쇠(사건 무관, 재연 합성용) | Horia Varlan, Commons, CC BY 2.0 |
| A7 ⏳ | `commons/old_door_locked.jpg` (4496×3000) | 잠긴 낡은 문(사건 무관, 재연 합성용) | Annatsach, Commons, CC BY-SA 4.0 |
| D1 | `docs/const1992_p01_portada.png` (1215×1733) | 1992 헌법 서명 원본 첫 장 | BACN, 공식 텍스트(저작권 보호 대상 아님, Ley 1.328/98 art. 8, 출처 표시) |
| D2 | `docs/const1992_p42_art135_habeas_data.png` (1227×1588) | 같은 원본 인쇄 40쪽: 제134조 끝, **제135조 Del Hábeas Data**, 제136조 | 위와 같음 |
| D3 | `docs/const1992_p123_firmas.png` (1227×1588) | 같은 원본 제헌의원 서명 페이지(예비) | 위와 같음 |
| M1 | `map_base_conosur_ne_4k.png` (3840×2160) | 남미 위치 지도 바탕(파라과이 청록, 아순시온 점) | 직접 제작, Natural Earth 데이터(퍼블릭 도메인) |
| M2 | `map_asuncion_lambare_osm_dark.png` (1536×1792), 원본 `map_base_asuncion_lambare_osm_z14.png` | 아순시온 도심~람바레 도시 지도(어두운 톤) | 직접 가공, 지도 © OpenStreetMap contributors (ODbL 1.0) |
| G1~G17 | (video-editor 가 HyperFrames 로 제작) | 아래 "직접 만드는 그래픽" | 직접 제작 |
| S* | `sfx/*.wav`, `sfx/wws_typewriter_erika5.ogg` | 배경 드론·효과음 | 직접 합성(ffmpeg) / Work With Sounds, Konrad Gutkowski, CC BY 4.0 |

⏳ = 라이선스는 확인했으나 Wikimedia 429 로 파일 다운로드 대기(`sample/fetch_pending_assets.sh`). 받지 못하면 대체안: A2 → 이름 자막 + 타자 카드, A4 → 제목을 검은 바탕 + 서류 텍스처 위에, A5 → 직접 그린 카세트 아이콘 격자, A7 → 직접 그린 문 일러스트.

M2 좌표 메모(1536×1792 픽셀, z14 타일 5566/9380 기준): 아순시온 도심(Plaza de los Héroes 부근) ≈ (746, 527). 지도의 `Lambaré` 지명 글자 ≈ (865, 1300). 4 km = 약 463 px(8.64 m/px). **Departamento de Producciones 건물 위치는 확인하지 못했다.** 핀은 찍지 않고 도심 기준 반경 4 km 원과 람바레 지명만 보여 준다(사법부 출판 "a 4 km del centro").

## 장면표

| # | 막 | 대본 첫 단어 | 길이(초) | 화면 유형 | 필수 요소 | 소재 | 출처·라이선스 | 메모 |
|---|---|---|---:|---|---|---|---|---|
| 1 | apertura | L9 «Es la mañana…» `000.0` | 2.4 | 날짜 카드 | 날짜 카드 · 효과음(타자기) | 검은 화면, 타자기 고정폭 글씨로 `22 · XII · 1992` 가 한 글자씩 찍힘(날짜 #2EC4B6). [G1] | Elaboración propia (ARCHIVO OSCURO) | regreso 에서 같은 카드 재사용 |
| 2 | apertura | ↳ `002.4` | 1.2 | 날짜 카드 | 날짜 카드 · 움직임 | 둘째 줄 `LAMBARÉ, PARAGUAY` 타이핑, 커서 깜박임, 카드가 살짝 밀려 들어옴(push-in). [G1] | Elaboración propia (ARCHIVO OSCURO) | 시각 표기 없음(facts #3 ⚠️) |
| 3 | apertura | ↳ `003.6` | 1.4 | 지도 | 지도 · 움직임 | 남미 위치 지도: 파라과이 청록 면, 아순시온 점으로 휩 줌. [M1] | Elaboración propia con datos Natural Earth (dominio público) |  |
| 4 | apertura | ↳ `005.0` | 1.4 | 지도 | 지도 · 출처 라벨 | 아순시온·람바레 도시 지도(어두운 톤): 도심 점에서 청록 반경 4 km 원이 퍼져 람바레 지명에 닿음. 라벨 `a 4 km del centro`·`Mapa: © OpenStreetMap contributors`. 건물 위치 핀은 찍지 않음. [M2] | Elaboración propia sobre mapa © OpenStreetMap contributors (ODbL 1.0) | 건물 정확 위치 미확인 → 반경만 |
| 5 | apertura | L10 «Faltan tres días…» `006.4` | 1.8 | 숫자 카드 | 숫자 카드 · 움직임 | 달력 띠 22→25 DIC 이 넘어가며 `FALTAN 3 DÍAS` 카운트다운. [G2] | Elaboración propia (ARCHIVO OSCURO) |  |
| 6 | apertura | ↳ `008.2` | 1.8 | 재연 이미지 | 재연 표시 · 움직임 | 1992년 탁상 달력 종이(직접 제작) 위로 아침 햇빛 광선이 쓸고 지나감, 열기 아지랑이. [G2] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 7 | apertura | L11 «Hace casi cuatro…» `010.0` | 1.6 | 자료 사진 | 이름 자막 · 출처 라벨 · 움직임 | 스트로에스네르 1954년 공식 초상, 탈색·느린 push-in. 이름 자막 `ALFREDO STROESSNER — gobernó Paraguay 1954–1989`, 라벨 `Retrato oficial, 1954`. [A1] | Casa Fotográfica Resck (1954), Wikimedia Commons, PD-Paraguay ⚠️ |  |
| 8 | apertura | ↳ `011.6` | 2.3 | 연표 | 연표 · 움직임 | 초상이 찢기듯 왼쪽으로 빠지고 미니 연표 `3 FEB 1989 ● ——— ● 22 DIC 1992`, 사이 구간 카운터 `CASI 4 AÑOS`. [G3] | Elaboración propia (ARCHIVO OSCURO) |  |
| 9 | apertura | L12 «Ante una dependencia…» `013.9` | 1.7 | 재연 이미지 | 재연 표시 · 이름 자막(기관) · 움직임 | 2층 경찰 건물 실루엣(벡터 일러스트, 실사 아님) 패럴랙스. 기관 자막 `DEPARTAMENTO DE PRODUCCIONES — Policía, Lambaré`. [G4] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 10 | apertura | ↳ `015.6` | 2.2 | 재연 이미지 | 재연 표시 · 움직임 | 입구 문틀 실루엣, 뒷모습 인물이 서류를 들고 안으로 걸어 들어감(실루엣). [G4] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 11 | apertura | ↳ `017.8` | 2.2 | 문서 확대 | 재연 표시 · 문서 확대 · 움직임 | 영장 종이 재연: 본문은 흐리게, 사건명 한 줄만 읽힘. 청록 밑줄. [G6] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN · 문구 창작 금지(사건명만) |
| 12 | apertura | L13 «Se llama José…» `020.0` | 2.1 | 문서 확대 | 이름 자막 · 움직임 | 타자 이름 카드 위 이름 자막 `JOSÉ AGUSTÍN FERNÁNDEZ — juez en lo criminal (1992)`. 사진 없음(라이선스 사진 미확보). [G5] | Elaboración propia (ARCHIVO OSCURO) |  |
| 13 | apertura | ↳ `022.1` | 1.8 | 문서 확대 | 움직임 | 직함 도장 `JUEZ EN LO CRIMINAL` 이 타자 카드에 찍힘. [G5] | Elaboración propia (ARCHIVO OSCURO) |  |
| 14 | apertura | L14 «El expediente que…» `023.9` | 2.0 | 문서 확대 | 재연 표시 · 효과음(타자기) | 사건 표지 재연에 타자기로 `MARTÍN ALMADA s/ HÁBEAS DATA` 가 찍힘. [G6] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 15 | apertura | ↳ `025.9` | 1.8 | 문서 확대 | 문서 확대 · 움직임 | `HÁBEAS DATA` 글자 매크로 줌, 청록 밑줄이 그어짐. [G6] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 16 | apertura | ↳ `027.7` | 1.9 | 도식 애니메이션 | 도식 · 움직임 | 용어 풀이 카드: `HÁBEAS DATA = derecho a ver los datos que el Estado guarda sobre ti`. [G7] | Elaboración propia (ARCHIVO OSCURO) | facts #38 |
| 17 | apertura | L15 «Almada es un…» `029.6` | 2.0 | 자료 사진 | 이름 자막 · 출처 라벨 · 움직임 | 마르틴 알마다 사진 패럴랙스(인물 오려 내기 + 배경 흐림). 자막 `MARTÍN ALMADA — educador`, 라벨 `Foto: 2008`. [A2] | Maria Stella de Almada (2008), Wikimedia Commons, CC BY-SA 4.0 | 1992년 사진 아님 → 연도 라벨 필수 |
| 18 | apertura | ↳ `031.6` | 1.3 | 문서 확대 | 문서 확대 · 출처 라벨 · 움직임 | 1992년 헌법 원본(서명본) 첫 장 push-in. 라벨 `Constitución Nacional 1992 · original firmado (BACN)`. [D1] | Constitución Nacional 1992, original firmado, BACN (bacn.gov.py); texto oficial sin protección de autor, Ley 1.328/98 art. 8, se cita la fuente |  |
| 19 | apertura | ↳ `032.9` | 1.8 | 문서 확대 | 문서 확대 · 출처 라벨 · 움직임 | 제135조 `Del Hábeas Data` 페이지 확대, 청록 강조 막대가 `Toda persona podrá acceder a la información y a los datos que sobre sí misma…` 줄을 훑음. [D2] | Constitución Nacional 1992, original firmado, BACN (bacn.gov.py); texto oficial sin protección de autor, Ley 1.328/98 art. 8, se cita la fuente |  |
| 20 | apertura | ↳ `034.8` | 2.0 | 도식 애니메이션 | 도식 · 움직임 | 도식: 사람 아이콘 → 청록 화살표 → 잠긴 서랍 `POLICÍA` + `?` (그가 자기 기록을 요구한다). [G7] | Elaboración propia (ARCHIVO OSCURO) |  |
| 21 | apertura | L16 «Han pasado 99…» `036.8` | 2.0 | 숫자 카드 | 숫자 카드 · 출처 라벨 | 카운터 0 → `99 DÍAS`, 아래 작은 글씨 `14 SEP 1992 → 22 DIC 1992`. [G8] | Elaboración propia (ARCHIVO OSCURO) | facts #39: 법원 접수 1992-09-14 → 12-22 = 99일 |
| 22 | apertura | ↳ `038.8` | 1.9 | 숫자 카드 | 숫자 카드 · 움직임 | 달력 낱장이 SEP → DIC 로 빠르게 넘어감. [G8] | Elaboración propia (ARCHIVO OSCURO) |  |
| 23 | apertura | L17 «Y la respuesta…» `040.7` | 2.4 | 재연 이미지 | 재연 표시 · 출처 라벨 | 타자 메모 재연 `RESPUESTA OFICIAL`: `los documentos desaparecieron` 한 줄만 선명. 귀속 라벨 `según recuerda el juez (ABC Color, 2019)`. [G9] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN · facts #40 ⚠️ 단독 회고 → 귀속 라벨 필수 |
| 24 | apertura | ↳ `043.1` | 2.4 | 연표 | 연표 · 움직임 | 연표가 `2–3 FEB 1989 · GOLPE` 로 되감기고, 서류 아이콘이 흩어져 사라짐. [G3] | Elaboración propia (ARCHIVO OSCURO) |  |
| 25 | apertura | ↳ `045.5` | 2.3 | 재연 이미지 | 재연 표시 · 움직임 | 빈 서류 서랍이 열리며 먼지만 떠오름(3D 소품 1개). [G10] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 26 | apertura | L18 «Según la Policía,…» `047.9` | 1.6 | 재연 이미지 | 재연 표시 · 움직임 | 건물 실루엣으로 복귀, 느린 push-in, 라벨 `VERSIÓN POLICIAL`. [G4] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 27 | apertura | ↳ `049.5` | 1.6 | 도식 애니메이션 | 도식 · 움직임 | 타이포 `NADA QUE BUSCAR` 이 타자기로 찍힘. [G10] | Elaboración propia (ARCHIVO OSCURO) |  |
| 28 | apertura | L19 «En la puerta,…» `051.1` | 2.5 | 재연 이미지 | 재연 표시 · 이름 자막(역할) · 움직임 | 문 앞 경비 경찰 실루엣이 손을 들어 막음. 역할 자막 `OFICIAL DE GUARDIA` (실명 없음). [G4] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 29 | apertura | ↳ `053.6` | 2.5 | 재연 이미지 | 재연 표시 · 움직임 | 판사 실루엣이 영장 종이를 들어 보이는 대치, 역광. [G4·G6] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 30 | apertura | L20 «Por ahora, nada…» `056.1` | 2.1 | 도식 애니메이션 | 도식 · 효과음(전환 문장: 배경음 끊김) | 사건 카드 3장(`GOLPE 1989` · `SIN DOCUMENTOS` · `NADA QUE BUSCAR`)이 퍼즐처럼 맞물리고 정지, 배경 드론이 뚝 끊김. [G10] | Elaboración propia (ARCHIVO OSCURO) | 전환 직전 문장(Por ahora…) |
| 31 | apertura | L21 «Hasta que, al…» `058.2` | 1.2 | 재연 이미지 | 재연 표시 · 움직임 | 어두운 계단을 카메라가 올라감(직접 만든 2.5D/3D 소품). [G11] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 32 | apertura | ↳ `059.4` | 1.2 | 재연 이미지 | 재연 표시 · 움직임 | 계단 끝 자물쇠 걸린 문(문 사진 + 자물쇠 사진 합성). [A7+A6] | Horia Varlan (2008), CC BY 2.0 + Annatsach (2019), CC BY-SA 4.0, Wikimedia Commons | RECREACIÓN · 실제 현장 사진 아님 |
| 33 | apertura | ↳ `060.6` | 1.1 | 재연 이미지 | 재연 표시 · 움직임 | 자물쇠 매크로, 손떨림 카메라, 공구 실루엣이 들어옴. [A6] | Horia Varlan (2008), Wikimedia Commons, CC BY 2.0 | RECREACIÓN |
| 34 | apertura | ↳ `061.7` | 1.2 | 재연 이미지 | 재연 표시 · 효과음(자물쇠 파손 + 저음 타격) | 자물쇠가 부서지는 순간 흰 플래시 1프레임 + 금속음. [A6] | Horia Varlan (2008), Wikimedia Commons, CC BY 2.0 | RECREACIÓN |
| 35 | apertura | ↳ `062.9` | 1.0 | 재연 이미지 | 재연 표시 · 효과음(휩) | 문이 열리며 빛이 쏟아짐(빛 번짐 전환). [G11] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 36 | apertura | L22 «Detrás aparece una…» `063.9` | 1.2 | 재연 이미지 | 재연 표시 · 움직임 | 서류 더미 산(직접 만든 종이·폴더 텍스처 적층, 3D 조명) 패럴랙스. [G12] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 37 | apertura | ↳ `065.1` | 1.2 | 재연 이미지 | 재연 표시 · 움직임 | 색인 카드가 흩어진 클로즈업(빈 칸·판독 불가 글씨, 실명 없음). [G12] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 38 | apertura | ↳ `066.3` | 1.2 | 재연 이미지 | 재연 표시 · 움직임 | 장부·폴더 등 측면 팬. [G12] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 39 | apertura | L26 «Con los años,…» `067.5` | 2.2 | 숫자 카드 | 숫자 카드 · 출처 라벨 · 효과음(카운터 틱) | 카운터 0 → `≈ 800.000 PÁGINAS`. 라벨 `Fuente: postulación UNESCO Memoria del Mundo (2008)`. [G13] | Elaboración propia (ARCHIVO OSCURO) | facts #7 |
| 40 | apertura | ↳ `069.7` | 1.7 | 숫자 카드 | 숫자 카드 · 움직임 | 숫자 아래로 종이 탑이 쌓여 올라감, 카메라 tilt-up. [G13] | Elaboración propia (ARCHIVO OSCURO) |  |
| 41 | apertura | L27 «Son unos doscientos…» `071.4` | 2.5 | 숫자 카드 | 숫자 카드 · 움직임 | `≈ 200 METROS LINEALES`: 청록 줄자 선이 선반을 따라 가로질러 그려짐. [G13] | Elaboración propia (ARCHIVO OSCURO) |  |
| 42 | apertura | L28 «Hay 11.225 fichas…» `073.9` | 2.1 | 숫자 카드 | 숫자 카드 · 움직임 | `11.225 FICHAS`: 작은 카드 격자가 빠르게 채워짐(실명 없음). [G13] | Elaboración propia (ARCHIVO OSCURO) |  |
| 43 | apertura | L29 «Hay unas 20.000…» `076.1` | 1.6 | 숫자 카드 | 숫자 카드 · 움직임 | `≈ 20.000 FOTOGRAFÍAS`: 빈 사진 틀 밀착 인화지 격자(얼굴 없음). [G13] | Elaboración propia (ARCHIVO OSCURO) |  |
| 44 | apertura | ↳ `077.7` | 1.6 | 숫자 카드 | 숫자 카드 · 재연 표시 · 움직임 | `543 CASETES` 카운터 + 카세트 더미 사진(현장 사진 아님) 느린 팬. [A5] | Hmvh (2009), Wikimedia Commons, dominio público (PD-self) | 라벨 `Imagen ilustrativa` |
| 45 | apertura | L30 «El inventario los…» `079.3` | 1.8 | 연표 | 연표 · 움직임 | 가로 연표 왼쪽 끝에 `1927` 도장이 찍힘. [G3] | Elaboración propia (ARCHIVO OSCURO) |  |
| 46 | apertura | ↳ `081.1` | 1.8 | 연표 | 연표 · 움직임 | 선이 오른쪽으로 달려 `FEB 1989` 도장, 구간 전체 청록. [G3] | Elaboración propia (ARCHIVO OSCURO) |  |
| 47 | apertura | L31 «Solo sacarlos de…» `082.9` | 2.0 | 숫자 카드 | 숫자 카드 · 움직임 | `≈ 12 HORAS` 시계 바늘 빠르게 회전. [G13] | Elaboración propia (ARCHIVO OSCURO) | facts #4 |
| 48 | apertura | ↳ `084.9` | 1.9 | 재연 이미지 | 재연 표시 · 움직임 | 문 밖으로 상자가 줄지어 나가는 실루엣(손에서 손으로 넘기는 사람 사슬은 regreso 에서 처음 보여 줌). [G12] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 49 | apertura | L32 «¿Cómo sobreviven casi…» `086.8` | 2.2 | 재연 이미지 | 재연 표시 · 효과음(질문 타격) | 눅눅한 종이 결 매크로(직접 만든 텍스처). [G12] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN · 질문 1 |
| 50 | apertura | ↳ `089.0` | 2.1 | 도식 애니메이션 | 도식 · 움직임 | `«PERDIDOS»` 타이핑 → 줄 그어 지워지고 `?` 가 남음. [G10] | Elaboración propia (ARCHIVO OSCURO) |  |
| 51 | apertura | L33 «¿Qué hacen en…» `091.1` | 2.0 | 지도 | 지도 · 효과음(질문 타격) | 남미 지도: 아르헨티나·우루과이·칠레가 차례로 청록으로 켜짐. [M1] | Elaboración propia con datos Natural Earth (dominio público) | 질문 2 |
| 52 | apertura | ↳ `093.1` | 1.7 | 지도 | 지도 · 움직임 | 세 나라에서 청록 선이 아순시온/람바레 점으로 모여듦. [M1] | Elaboración propia con datos Natural Earth (dominio público) |  |
| 53 | apertura | ↳ `094.7` | 1.7 | 재연 이미지 | 재연 표시 · 움직임 | 카드 재연 3장에 `ARGENTINA` `URUGUAY` `CHILE` 국적 도장(이름 칸은 비움). [G12] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN · facts #34 |
| 54 | apertura | L34 «Y sobre todo,…» `096.4` | 2.5 | 도식 애니메이션 | 도식 · 효과음(질문 타격) | 큰 타이포 `NEGABA HABERLOS DETENIDO` 가 도장처럼 찍힘. [G14] | Elaboración propia (ARCHIVO OSCURO) | 질문 3 · facts #46 |
| 55 | apertura | ↳ `098.9` | 2.5 | 재연 이미지 | 재연 표시 · 움직임 | 재연 카드 한 장: 사진 칸(빈 실루엣)·지문 칸(직접 만든 지문 패턴)이 차례로 채워짐, 글씨 판독 불가. [G14] | Elaboración propia (ARCHIVO OSCURO) | RECREACIÓN |
| 56 | apertura | ↳ `101.4` | 2.6 | 도식 애니메이션 | 도식 · 효과음(음악 상승) | `FICHADOS · CON FOTO · CON HUELLAS` 세 단어가 차례로 청록 강조, 카드가 벽처럼 쌓여 화면을 덮음. [G14] | Elaboración propia (ARCHIVO OSCURO) |  |
| 57 | apertura | L35 «Esta es la…» `103.9` | 1.4 | 도식 애니메이션 | 효과음(저음 타격) · 움직임 | 검은 바탕에 제목 `LOS ARCHIVOS DEL TERROR` 이 연기 속에서 드러남. [G15] | Elaboración propia (ARCHIVO OSCURO) |  |
| 58 | apertura | ↳ `105.3` | 1.8 | 자료 사진 | 출처 라벨 · 움직임 | 제목 뒤로 오늘의 기록 보관 장소 사진, 느린 push-in. 라벨 `Archivo del Terror · Museo de la Justicia, Asunción (foto 2019)`. [A4] | Nojaedu (2019), Wikimedia Commons, CC BY-SA 4.0 | 해상도 960px → 화면 60% 크기 액자 또는 흐린 배경으로만 |
| 59 | origen | L38 «Para entender por…» `107.1` | 1.0 | 도식 애니메이션 | 막 전환 · 효과음(라이저→휩) | 되감기 효과(테이프 되감기 줄무늬 + 0.4초 암전). [G16] | Elaboración propia (ARCHIVO OSCURO) | 막 전환 apertura→origen |
| 60 | origen | ↳ `108.1` | 2.2 | 날짜 카드 | 날짜 카드 · 효과음(타자기) | 같은 타자기 카드 계열: 연도 숫자가 1992 → 1954 로 거꾸로 굴러가고 `MAYO · 1954 — ASUNCIÓN` (날짜 #2EC4B6). [G1 변형] | Elaboración propia (ARCHIVO OSCURO) |  |
| 61 | origen | ↳ `110.3` | 1.8 | 연표 | 연표 · 움직임 | origen 연표가 열림: `1954 ●` 에서 오른쪽으로 축이 뻗음. [G17] | Elaboración propia (ARCHIVO OSCURO) |  |
| 62 | origen | L39 «Ese mes, un…» `112.1` | 2.2 | 자료 사진 | 출처 라벨 · 움직임 | 스트로에스네르 1954 초상 다른 크롭(제복 부분) 패럴랙스. 라벨 `Retrato oficial, agosto de 1954`. [A1] | Casa Fotográfica Resck (1954), Wikimedia Commons, PD-Paraguay ⚠️ | 사진은 쿠데타(5월)가 아니라 8월 취임 때 → 라벨로 구분 |
| 63 | origen | ↳ `114.3` | 2.1 | 연표 | 연표 · 움직임 | 연표에 `MAYO 1954 · GOLPE MILITAR` 표지가 청록 맥동으로 박힘. [G17] | Elaboración propia (ARCHIVO OSCURO) |  |
| 64 | origen | L40 «Va a gobernar…» `116.4` | 2.5 | 숫자 카드 | 숫자 카드 · 연표 | 카운터 `35 AÑOS`, 연표 막대가 1954 → 1989 로 채워짐. [G17] | Elaboración propia (ARCHIVO OSCURO) | facts #26 |
| 65 | origen | ↳ `118.9` | 2.5 | 숫자 카드 | 숫자 카드 · 움직임 | `= 7 PERÍODOS PRESIDENCIALES`: 블록 7개가 하나씩 채워짐. [G17] | Elaboración propia (ARCHIVO OSCURO) | facts #26 |

합계 **65행 · 121.4초**(apertura 0:00~1:47.1 = 58행, origen 1:47.1~2:01.4 = 7행). 평균 1.87초/행, 최장 2.6초. 예상 화면 전환 **분당 약 32회**(기준: 첫 2분 분당 25회 이상, 6초 넘는 정지 화면 없음).
기준 타이밍(168단어/분)으로는 연결 문장이 1:43.9, 되감기가 1:47.1이다. 대본 팀이 적은 1:45/1:48과 1~2초 차이가 나는데, 녹음 후 재타이밍에서 맞춘다.

## 직접 만드는 그래픽 (video-editor, HyperFrames)

| 코드 | 그래픽 | 규칙 |
|---|---|---|
| G1 | 날짜 카드: 검은 바탕, 타자기 고정폭 글씨, `22 · XII · 1992` 날짜는 #2EC4B6, 둘째 줄 `LAMBARÉ, PARAGUAY` 흰색. 한 글자씩 타이핑 + 타자기 효과음. 시각 표기 없음 | **regreso 에서 같은 디자인·같은 글자로 재사용**. 되감기 카드(`MAYO · 1954 — ASUNCIÓN`)는 같은 계열의 변형. 검은 카드 노출 5초 이하 |
| G2 | 달력 카운트다운 `FALTAN 3 DÍAS` + 1992 탁상 달력 종이(직접 그림) | 재연 종이에는 `RECREACIÓN` |
| G3 | 가로 연표(1927 / 2–3 FEB 1989 / 22 DIC 1992 도장) | 도장 글자 청록 |
| G4 | 2층 경찰 건물·인물 실루엣(벡터 일러스트, 실사풍 아님), 역할 자막 `OFICIAL DE GUARDIA` | 실제 건물 외관 사진이 없으므로 재연. 실명 없음 |
| G5 | 판사 이름 카드(타자 카드 + 도장 `JUEZ EN LO CRIMINAL`) | 생존 공직자. 라이선스 사진이 없어 얼굴 없이 이름 자막만 |
| G6 | 사건 표지·영장 재연: 사건명 `MARTÍN ALMADA s/ HÁBEAS DATA` 한 줄만 선명, 나머지는 흐림 | 원문 문구를 지어내지 않는다. `RECREACIÓN` |
| G7 | 도식: 사람 → 잠긴 서랍 `POLICÍA` / 용어 풀이 `HÁBEAS DATA = derecho a ver los datos que el Estado guarda sobre ti` | |
| G8 | 숫자 카운터 `99 DÍAS`, `14 SEP 1992 → 22 DIC 1992`, 달력 넘김 | facts #39(법원 접수 1992-09-14) |
| G9 | 타자 메모 재연 `RESPUESTA OFICIAL` + 귀속 라벨 `según recuerda el juez (ABC Color, 2019)` | facts #40 ⚠️ 단독 회고 → 라벨 필수 |
| G10 | 빈 서랍 3D 소품, 타이포 `NADA QUE BUSCAR`, 퍼즐 카드 3장, `«PERDIDOS»` → 줄 긋기 | |
| G11 | 계단 2.5D/3D 소품 + 문 열림 빛 번짐 | A6·A7 합성과 함께 `RECREACIÓN` |
| G12 | 서류 산·색인 카드·장부 텍스처(직접 만든 종이 결), 국적 도장 카드, 상자 행렬 실루엣 | 카드의 이름·글씨는 판독 불가 또는 빈 칸. 실존 피해자 카드 재현 금지 |
| G13 | 숫자 카드: `≈ 800.000 PÁGINAS` · `≈ 200 METROS LINEALES` · `11.225 FICHAS` · `≈ 20.000 FOTOGRAFÍAS` · `543 CASETES` · `≈ 12 HORAS` | 큰 굵은 숫자 + 단위, 카운터 애니메이션, 출처 라벨 `Fuente: postulación UNESCO Memoria del Mundo (2008)`(12시간은 `Fuente: Poder Judicial, 2008`) |
| G14 | 질문 3 타이포 `NEGABA HABERLOS DETENIDO` ↔ `FICHADOS · CON FOTO · CON HUELLAS`, 사진 칸·지문 칸 재연 카드 | 지문 패턴은 직접 생성(실제 지문 아님) |
| G15 | 제목 `LOS ARCHIVOS DEL TERROR`, 연기 속 등장 | 채널 서체 세트 |
| G16 | 되감기 전환(테이프 되감기 줄무늬 + 0.4초 암전) | 막 전환. 암전 1.5초 이하 |
| G17 | origen 연표 1954 → 1989, `35 AÑOS`, 블록 7개 `7 PERÍODOS PRESIDENCIALES` | origen 막 연표의 시작점 |

## 도입 ↔ regreso 같은 소재 (규칙 4)
regreso("Es otra vez la mañana del 22 de diciembre de 1992…")는 아래를 **그대로** 다시 쓴다. 시청자가 "그 순간"으로 돌아왔다고 느끼게 하려는 것이다.
1. G1 날짜 카드: 같은 디자인, 같은 글자, 같은 타자기 효과음
2. M2 람바레 지도: 같은 4 km 원 애니메이션
3. G4 건물 실루엣, G11 계단·자물쇠 문(A6+A7)

도입은 문이 열리는 빛(35번 행)에서 끊는다. regreso 에서 같은 문을 다시 열고 처음으로 안쪽을 보여 준다. 인간 사슬, 젖은 종이, 땅에 묻힌 신분증이 이때 나온다.
도입에서 빠진 군중 장면(구경꾼 실루엣·플래시·캠코더 뷰파인더, G4 변형)은 regreso 군중 문장에서 쓴다.

## 필수 화면 요소 체크리스트 (이 2분 구간)

| # | 요소 | 상태 | 행 |
|---|---|---|---|
| 1 | 날짜 카드(도입·되돌아오기 같은 디자인) | ✅ 도입 배치, regreso 재사용 지정 | 1–2, 되감기 변형 60 |
| 2 | 지도(장소 첫 등장마다) | ✅ 람바레·아순시온(3–4), 아르헨티나·우루과이·칠레(51–52). 1954 아순시온은 첫 등장이 아니라 생략 | 3, 4, 51, 52 |
| 3 | 숫자 카드(막마다 1개 이상) | ✅ apertura 11개, origen 2개(35 AÑOS, 7 PERÍODOS) | 5, 21–22, 39–44, 47, 64–65 |
| 4 | 문서 확대 + 강조 | ✅ 1992 헌법 서명 원본 제135조(1차 자료) 줄 강조 | 18, 19 (재연 문서 11, 14–15) |
| 5 | 이름 자막 | ✅ 스트로에스네르, 페르난데스 판사, 알마다, Departamento de Producciones(기관), 경비 경찰(역할) | 7, 9, 12, 17, 28 |
| 6 | 연표(origen) | ✅ origen 연표 시작(1954→1989). apertura 미니 연표도 있음 | 61, 63, 64 (+8, 24, 45–46) |
| 7 | 정지 이미지의 움직임 | ✅ 모든 사진·문서 행에 push-in·패닝·패럴랙스 지정, 6초 넘는 행 없음 | 전체 |
| 8 | 재연 표시 | ✅ 재연 23행에 `RECREACIÓN`, 사건 무관 실물 사진 1행(44)에 `Imagen ilustrativa` | 메모 칸 |
| 9 | 음악·효과음 | ✅ 배경 드론 + 전환 문장(30: 드론 끊김 → 31–35: 자물쇠 파손·타격·휩), 질문 묶음(49, 51, 54: 타격), 제목(57), 되감기(59: 라이저→휩). regreso 효과음은 이 구간 밖 | 필수 요소 칸 |
| 10 | 막 전환 효과 | ✅ apertura → origen 되감기 + 0.4초 암전 | 59 |
| (+) | 출처 라벨(config 11번째 항목) | ✅ 실제 자료 행 전부(지도·사진·헌법·숫자 출처) | 4, 7, 17, 18, 39, 58 … |

## 음악·효과음

라이선스가 있는 음악 라이브러리가 없다. 그래서 **배경음과 효과음은 ffmpeg 로 직접 합성**했다(저작권 문제 없음, `assets/sfx/`, 48 kHz 24-bit).

| 파일 | 길이 | 쓰는 곳 |
|---|---|---|
| `drone_ambient_120s.wav` | 120초 | 도입 전체 배경(55 Hz + 82.4 Hz 사인파 + 갈색 잡음, 느린 진폭 변화). 30번 행에서 끊었다가 35번 행부터 다시 |
| `whoosh_1s.wav` | 1.2초 | 휩 팬, 문 열림(35), 되감기 끝(59) |
| `impact_low_2s.wav` | 2초 | 자물쇠 파손(34), 질문 3개(49, 51, 54), 제목(57) |
| `lock_break_metal.wav` | 0.8초 | 자물쇠 파손(34) |
| `riser_3s.wav` | 3초 | 질문 3 → 제목 상승(56–57), 되감기(59) 직전 |
| `type_key_synth.wav` | 0.06초 | 타자기 대체용 키 소리(반복 배치) |
| `wws_typewriter_erika5.ogg` | — | 실제 타자기(Erika 5) 녹음. 날짜 카드·사건 표지·타이포 타이핑(1–2, 14, 27, 60). **CC BY 4.0, 크레딧 필수**: "Typewriter: Work With Sounds / Konrad Gutkowski, CC BY 4.0" |

- 셔터음·종이 넘김이 필요하면 같은 방식으로 합성한다. CC0 효과음 출처(Freesound CC0 등)는 이 환경에서 확인하지 못했다.
- 믹스 기준: 내레이션 아래 음악 -20 dB(`config/format.json → audio.music_under_narration_db`). 최종 -14 LUFS 는 `/voice` 단계에서 맞춘다.
- 합성 드론만으로 레퍼런스급 음악 품질이 되는지는 **❓ 가설**이다. video-qa 판정에 맡기고, 필요하면 사람이 라이선스 음악을 정한다.

## 화면 스타일 ❓ 항목 (가설, 확정 아님)
- 본편 색보정: 레퍼런스는 장면마다 자연색(세피아·청록-주황). 여기서는 1992 장면을 차가운 저채도, 1954 사진을 따뜻한 세피아로 가정했다. 도입부 클립 5개 측정만 근거라 **본문 톤은 미확인**이다.
- 재연 실루엣(벡터)이 레퍼런스의 시네마틱 재연 영상과 동급으로 읽히는지는 ❓. `benchmark_frames.py --compare` 와 video-qa 접촉 시트로 판정한다.
- 이름 자막 위치(하단 좌측, 굵은 이탤릭 대문자)는 도입 11초 클립 관찰만 근거다.
