#!/bin/bash
# Flickr 사진 다운로드 대기분 (assets/LICENSES.md §8-2). 라이선스는 2026-11-26 사진 페이지에서 확인함.
# 429/403 이 오면 멈춘다(우회하지 않는다). 받은 뒤 내용을 눈으로 확인할 것.
set -u
D="$(cd "$(dirname "$0")/.." && pwd)/assets/photos"; mkdir -p "$D"
UA="Mozilla/5.0 (compatible; archivo-oscuro-fetch/1.0)"
while read -r name url; do
  [ -z "$name" ] && continue
  [ -s "$D/$name" ] && [ "$(stat -c%s "$D/$name")" -gt 10000 ] && { echo "skip $name"; continue; }
  code=$(curl -s -A "$UA" --max-time 180 -o "$D/$name.part" -w "%{http_code}" "$url")
  if [ "$code" = "200" ]; then mv "$D/$name.part" "$D/$name"; echo "ok   $name"; else rm -f "$D/$name.part"; echo "FAIL $name HTTP $code — stop"; exit 1; fi
  sleep 6
done <<'LIST'
flickr_lambare_bw_film_coconutgroove.jpg https://live.staticflickr.com/5096/5516184865_f09e91fe99_o.jpg
flickr_comandancia_policia_nacional_ramalleira.jpg https://live.staticflickr.com/65535/53408803039_169c557406_k.jpg
flickr_comandancia_policia_nacional_chamorro.jpg https://live.staticflickr.com/2349/5728485597_4ef8fd4cef_b.jpg
flickr_palacio_lopez_night_ciuffo.jpg https://live.staticflickr.com/8458/8039941540_f49ae4aa81_3k.jpg
flickr_asuncion_rio_nubes_solop.jpg https://live.staticflickr.com/4225/34520523923_69bbf44ebe_o.jpg
flickr_asuncion_alturas_solop.jpg https://live.staticflickr.com/4251/35145466592_c91de58492_o.jpg
flickr_asuncion_fachada_dionisi_1.jpg https://live.staticflickr.com/2637/4294838700_1ef03962f4_o.jpg
flickr_asuncion_fachada_dionisi_2.jpg https://live.staticflickr.com/4056/4294096471_f835bdeae1_o.jpg
flickr_puerto_stroessner_1986_hamilton.jpg https://live.staticflickr.com/6172/6193581414_2041376255_b.jpg
flickr_typewriter_watkin.jpg https://live.staticflickr.com/6074/6073592478_3213ceedcd_3k.jpg
flickr_typewriter_freestocks.jpg https://live.staticflickr.com/7416/28066454506_d0b3a774cb_o.jpg
flickr_typewriter_katz.jpg https://live.staticflickr.com/593/22717806954_fbefd297de_4k.jpg
flickr_typewriter_taylor.jpg https://live.staticflickr.com/3257/4555309306_94d53aaf5b_k.jpg
flickr_typewriter_keys_rumpleteaser.jpg https://live.staticflickr.com/7021/6651911895_a7564a332f_o.jpg
flickr_filing_cabinets_mee.jpg https://live.staticflickr.com/3946/15724296035_1cdd9d5498_o.jpg
flickr_fichiers_papier_marlenedd_1.jpg https://live.staticflickr.com/7073/6890174394_05255ce25e_o.jpg
flickr_fichiers_papier_marlenedd_2.jpg https://live.staticflickr.com/7128/7036264955_11f485b821_o.jpg
flickr_card_catalog_marygrove.jpg https://live.staticflickr.com/7113/6869133600_c5fa4ee7e5_k.jpg
flickr_card_catalog_fulmer.jpg https://live.staticflickr.com/4049/4350629792_4dda1ab2cb_o.jpg
flickr_card_catalog_levine.jpg https://live.staticflickr.com/3607/3597095794_1180f3eef3_o.jpg
flickr_archive_boxes_jvl_1.jpg https://live.staticflickr.com/7340/13091907654_de4168a79e_k.jpg
flickr_archive_boxes_jvl_2.jpg https://live.staticflickr.com/3087/13091735873_559df3deaa_k.jpg
flickr_archive_boxes_jvl_3.jpg https://live.staticflickr.com/2041/13091907034_6ff2653700_k.jpg
flickr_shelves_documents_jones.jpg https://live.staticflickr.com/4436/37263585815_9889753c0c_o.jpg
LIST
