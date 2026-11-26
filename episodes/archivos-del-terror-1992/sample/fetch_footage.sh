#!/usr/bin/env bash
# 자료 영상 구간만 잘라 받기 (archivos-del-terror-1992 샘플용, scene-planner 2026-11-26)
# 원본 전체를 받지 않고 HTTP 범위 탐색으로 필요한 구간만 읽는다. 결과는 assets/footage/ (커밋 안 함).
# 출처·라이선스 근거: assets/LICENSES.md §9 '자료 영상'.
# 처리: 소리 제거, 필름 텔레시네 되돌리기(fieldmatch+decimate → 23.976p), 정사각 픽셀 640x480(SD 원본, 업스케일 안 함),
#       x264 CRF 14. NASA 는 원본 해상도 그대로.
set -euo pipefail
OUT="$(cd "$(dirname "$0")/.." && pwd)/assets/footage"
mkdir -p "$OUT"
IA=https://archive.org/download
NASA=https://eol.jsc.nasa.gov/BeyondThePhotography/CrewEarthObservationsVideos/videos
IVTC="fieldmatch=order=auto:combmatch=full,yadif=deint=interlaced,decimate,scale=640:480:flags=lanczos,setsar=1"
ENC=(-an -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -movflags +faststart)

cut() { # name url start end filter
  local name=$1 url=$2 ss=$3 to=$4 vf=$5
  local f="$OUT/$name.mp4"
  [[ -s "$f" ]] && { echo "skip $name"; return; }
  local dur; dur=$(python3 -c "print(round($to-$ss,3))")
  ffmpeg -nostdin -v error -ss "$ss" -i "$url" -t "$dur" -vf "$vf" "${ENC[@]}" -y "$f"
  echo "ok  $name ($ss-$to)"
}

# --- FBI 'Document Examination' (1969, NARA 12093, 연방 저작물) ---
U=$IA/gov.archives.arc.12093/gov.archives.arc.12093.mpeg
cut fx01_fbi1969_fichero_oficina        "$U"  98.5 104.5 "$IVTC"
cut fx02_fbi1969_mano_saca_ficha        "$U" 112.3 117.8 "$IVTC"
cut fx03_fbi1969_mano_hojea_fichas      "$U" 118.0 124.0 "$IVTC"
cut fx04_fbi1969_manos_documento_mesa   "$U" 489.5 494.0 "$IVTC"
cut fx05_fbi1969_manos_hojean_archivo   "$U" 520.0 524.0 "$IVTC"
cut fx06_fbi1969_dedo_recorre_archivo   "$U" 528.0 532.7 "$IVTC"
cut fx07_fbi1969_mano_escribe_papeles   "$U" 555.0 561.0 "$IVTC"

# --- 'Basic Typing, Part I' (1944, US Navy MN-1512a, Prelinger PD) ---
U=$IA/basic_typing_1/basic_typing_1.mpeg
cut fx08_navy1944_tipos_golpean_papel   "$U" 143.0 149.0 "$IVTC"
cut fx09_navy1944_mano_teclas           "$U" 163.55 169.0 "$IVTC"
cut fx10_navy1944_silueta_mecanografa   "$U" 311.0 317.0 "$IVTC"
cut fx11_navy1944_dedo_tecla_macro      "$U" 681.0 685.7 "$IVTC"
cut fx12_navy1944_manos_escriben        "$U" 825.0 831.0 "$IVTC"

# --- 'I Want to Be a Secretary' (1941, Coronet, Prelinger PD) ---
U=$IA/IWanttoB1941/IWanttoB1941.mpeg
cut fx13_coronet1941_muro_ficheros      "$U" 416.0 422.0 "$IVTC"
cut fx14_coronet1941_manos_maquina      "$U" 485.0 490.5 "$IVTC"
cut fx15_coronet1941_lapiz_registro     "$U" 666.0 672.0 "$IVTC"

# --- 'Safeguarding Military Information' (1941, US Army / AMPAS, Prelinger PD) ---
U=$IA/Safeguar1941/Safeguar1941.mpeg
cut fx16_army1941_sombra_en_puerta      "$U"  19.0  23.6 "$IVTC"
cut fx17_army1941_abre_puerta_entra     "$U"  25.0  29.0 "$IVTC"
cut fx18_army1941_puerta_oscura_figura  "$U"  50.0  55.0 "$IVTC"
cut fx19_army1941_documento_sombra      "$U" 362.0 365.5 "$IVTC"

# --- 'Booked for Safekeeping' (1960, Louisiana Assn. for Mental Health, Prelinger PD) ---
U=$IA/Bookedfo1960/Bookedfo1960.mpeg
cut fx20_booked1960_calle_noche_pov     "$U" 328.0 334.0 "$IVTC"
cut fx21_booked1960_escalera_policia    "$U" 388.5 391.0 "$IVTC"
cut fx22_booked1960_linterna_oscuro     "$U" 672.0 677.0 "$IVTC"
cut fx23_booked1960_silueta_linterna    "$U" 687.0 693.0 "$IVTC"

# --- 'Your Police' (1953, Riviera Productions, Prelinger PD) ---
U=$IA/your_police/your_police.mpeg
cut fx24_police1953_mano_ventana        "$U" 142.0 145.0 "$IVTC"
cut fx25_police1953_mano_pomo_cerradura "$U" 145.0 147.2 "$IVTC"
cut fx27_police1953_agente_prueba_puerta "$U" 186.0 188.8 "$IVTC"

# --- 'Paraguay' (1945, Office of the Coordinator of Inter-American Affairs, NARA 47001) ---
U=$IA/gov.archives.arc.47001/gov.archives.arc.47001.mpeg
cut fx28_ociaa1945_asuncion_horizonte   "$U" 308.0 312.1 "$IVTC"
cut fx29_ociaa1945_asuncion_tejados     "$U" 313.0 316.0 "$IVTC"
cut fx29b_ociaa1945_asuncion_tejados2   "$U" 316.3 318.4 "$IVTC"
cut fx30_ociaa1945_asuncion_calle_cupula "$U" 345.0 347.2 "$IVTC"
cut fx31_ociaa1945_asuncion_tranvia     "$U" 350.0 356.0 "$IVTC"
cut fx32_ociaa1945_panteon_heroes       "$U" 372.95 375.1 "$IVTC"
cut fx33_ociaa1945_soldados_marchan     "$U" 383.4 386.9 "$IVTC"
cut fx34_ociaa1945_soldados_contrapicado "$U" 388.35 390.6 "$IVTC"
cut fx35_ociaa1945_vapor_rio            "$U" 470.0 474.1 "$IVTC"
cut fx36_ociaa1945_rio_paraguay         "$U" 475.0 481.0 "$IVTC"

# --- NASA JSC, ISS Expedition 28 (2011-08-19), 끝부분: 남미 서부(페루~볼리비아 라파스) 새벽 ---
U=$NASA/nsamerica_iss_20110819/nsamerica_iss_20110819HD.mp4
cut fx37_nasa2011_sudamerica_amanecer   "$U"  18.8  23.0 "setsar=1"
