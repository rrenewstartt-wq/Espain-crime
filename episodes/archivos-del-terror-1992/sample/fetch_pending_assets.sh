#!/bin/bash
# Wikimedia 429 로 받지 못한 샘플 소재 4개를 다시 받는다. 라이선스는 assets/LICENSES.md 에 기록돼 있다.
# 사용: bash episodes/archivos-del-terror-1992/sample/fetch_pending_assets.sh
set -u
D="$(cd "$(dirname "$0")/../assets/commons" && pwd)"
UA="ResearchClient/1.0 (https://commons.wikimedia.org; non-commercial research)"
while read -r name url; do
  [ -s "$D/$name" ] && file "$D/$name" | grep -q JPEG && { echo "ok (이미 있음) $name"; continue; }
  for i in 1 2 3 4 5; do
    code=$(curl -s -A "$UA" -o "$D/$name.part" -w "%{http_code}" "$url")
    if [ "$code" = 200 ]; then mv "$D/$name.part" "$D/$name"; break; fi
    rm -f "$D/$name.part"; sleep $((i*20))
  done
  echo "$code $name"
done <<'L'
martin_almada_2008.jpg https://upload.wikimedia.org/wikipedia/commons/4/4f/MartinAlmada-2008.jpg
museo_justicia_archivo_terror_2019.jpg https://upload.wikimedia.org/wikipedia/commons/3/3f/Museo_de_la_Justicia_-_Asunci%C3%B3n_de_Paraguay.jpg
heap_of_tapes.jpg https://upload.wikimedia.org/wikipedia/commons/6/63/Heap_of_tapes.jpg
old_door_locked.jpg https://upload.wikimedia.org/wikipedia/commons/f/fd/Old_door_locked.jpg
L
