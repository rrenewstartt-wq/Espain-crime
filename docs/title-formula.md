# 제목 공식

검사: `python3 scripts/check_title.py "<제목>"`. 수치는 `config/format.json → title`. 근거는 레퍼런스 현재 포맷 31편.

## 구조: `[훅] | [고유명사]` (31/31편)
- **왼쪽 훅 (5~10단어):** 이름을 숨긴 채 "이상한 사실"이나 질문을 던진다. 추천 피드에서 클릭을 부르는 부분.
- **오른쪽:** 고유명사(사건명·인물명·장소명). 검색과 "들어 본 사건"이라는 친숙함을 맡는다. 질문형 변형 허용: `¿Quién es X?`, `El Misterio de X`, `¿Qué Pasó en X?`
- 길이 50~70자(레퍼런스 중앙값 64자, 최대 81자). 왼쪽에는 고유명사를 넣지 않는다.
- 스페인어 Title Case(단어마다 첫 글자 대문자). 이모지·전체 대문자 단어 없음.

## 훅 우선순위 (레퍼런스 내 조회수 배수, 있음 ÷ 없음 중앙값)

| 훅 | 배수 | 쓰는 법 |
|---|---:|---|
| 위험·공포 (Peligroso, Temido, Oscuro, Siniestro) | 1.75× | 1순위 |
| 질문 (¿Quién? ¿Por qué? ¿Dónde?) | 1.5× | 1순위. 왼쪽 또는 오른쪽 |
| 최상급 (Más, Mayor, Único, Peor) | 0.9× | 한 번만. 최근 영상과 같은 최상급 반복 금지 |
| 사람 주어 (El Hombre/La Mujer/El Niño que…) | 0.52× | **반전·대가가 붙을 때만** ("…y Pagó con Su Vida") |
| 숫자 (왼쪽) | 0.45× | 왼쪽에는 피한다. 숫자는 썸네일 글자로 |

## 공식 3가지 (형태만, 예시는 새로 쓴 것)
1. `El/La [대상] Más [공포 형용사] de [범위] | [고유명사]` → *El Pueblo Más Silencioso de México | La Zona del Silencio*
2. `¿[Quién/Qué/Por qué] + 은폐·책임 질문? | El Misterio de [고유명사]` → *¿Quién Dejó que la Ciudad Explotara? | Guadalajara 1992*
3. `El/La [사물] que [불가능한 행위] | [고유명사]` → *El Túnel que Nadie Vio Construir | La Fuga del Altiplano*

## 체크리스트 (`check_title.py` 가 자동 판정)
- [ ] `|` 가 정확히 하나
- [ ] 50~70자 (81자 초과는 불합격)
- [ ] 왼쪽 5~10단어, 왼쪽에 고유명사 없음(문장 첫 단어 외 대문자 연속 이름 탐지)
- [ ] 위험·공포 또는 질문 훅 하나 이상
- [ ] 최상급 하나 이하, 왼쪽 숫자 없음
- [ ] 사람 주어로 시작하면 반전·대가 단어(pagó, murió, perdió, salvó, desapareció…)가 있음
- [ ] 이모지·전체 대문자 단어 없음
- [ ] 레퍼런스 제목과 왼쪽 훅이 같지 않음(5단어 이상 연속 일치 금지)
