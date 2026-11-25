#!/usr/bin/env python3
"""Check a thumbnail against docs/thumbnail-formula.md.

    python3 scripts/check_thumbnail.py episodes/<ep>          # thumbnail/out.png + thumbnail/spec.json + meta.json
    python3 scripts/check_thumbnail.py path/to/image.png --text "69 DÍAS"
Measures: size, single-hue tone near the accent, no forbidden (reference red) hue, word count,
title/thumbnail word split, and perceptual distance from the 51 reference thumbnails.
"""
import argparse
import colorsys
import glob
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from common import FMT, RAW, Report, fold  # noqa: E402

TH = FMT["thumbnail"]


def hue_of(hexc):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)[0] * 360


def hue_dist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def dhash(im, n=8):
    g = im.convert("L").resize((n + 1, n), Image.LANCZOS)
    px = list(g.get_flattened_data())
    return sum(1 << i for i, (a, b) in enumerate((px[r * (n + 1) + c], px[r * (n + 1) + c + 1]) for r in range(n) for c in range(n)) if a > b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--text")
    a = ap.parse_args()
    if a.target.endswith((".png", ".jpg")):
        img_p, spec, meta = a.target, {"text": a.text or ""}, {}
    else:
        ep = a.target.rstrip("/")
        img_p = f"{ep}/thumbnail/out.png"
        spec = json.load(open(f"{ep}/thumbnail/spec.json", encoding="utf-8"))
        meta = json.load(open(f"{ep}/meta.json", encoding="utf-8"))
    im = Image.open(img_p).convert("RGB")
    r = Report(f"썸네일: {img_p}")
    r.ok(im.size == tuple(TH["size"]), "크기", f"{im.size[0]}×{im.size[1]}")

    accent = spec.get("accent") or TH["accent"]
    ah = hue_of(accent)
    small = im.resize((256, 144))
    sat = []
    for p in small.get_flattened_data():
        h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in p))
        if s > 0.35 and v > 0.2:
            sat.append(h * 360)
    near = sum(hue_dist(h, ah) <= 25 for h in sat) / len(sat) if sat else 0
    r.ok(near >= 0.85, "단색 톤 (강조색 ±25° 안의 채도 픽셀 비율)", f"{near:.0%}, 강조색 {accent}", fail="WARN")
    forb = [hue_of(f) for f in TH["forbidden_accents"]]
    red = sum(any(hue_dist(h, f) <= 12 for f in forb) for h in sat) / len(sat) if sat else 0
    if all(hue_dist(ah, f) > 12 for f in forb):
        r.ok(red < 0.03, "레퍼런스 빨강 없음", f"{red:.1%}")
    else:
        r.add("FAIL", "강조색이 레퍼런스 빨강", accent)

    text = spec.get("text", "")
    nw = len(text.split())
    r.ok(1 <= nw <= 4, "글자 1~4단어", f"'{text}'")
    r.ok(text == text.upper(), "대문자", fail="WARN")
    title = meta.get("title", "")
    if title and "|" in title:
        left = set(w for w in fold(title.split("|")[0]).split() if len(w) > 3)
        right = fold(title.split("|")[1])
        rep = [w for w in fold(text).split() if w in left]
        r.ok(not rep or all(w in right for w in rep), "썸네일 글자가 제목 왼쪽 훅을 반복하지 않음", ", ".join(rep), fail="WARN")

    refs = glob.glob(f"{RAW}/thumbs/*.jpg")
    if refs:
        mine = dhash(im)
        dist = min(bin(mine ^ dhash(Image.open(p))).count("1") for p in refs)
        r.ok(dist >= 10, "레퍼런스 썸네일과 구도 거리", f"최소 해밍 거리 {dist}/64 (10 미만이면 구도 복제 의심)")
    else:
        r.add("WARN", "레퍼런스 썸네일 없음", "python3 scripts/benchmark.py fetch 후 다시")
    r.print()
    print("  ※ 168px 미리보기(-168.png)를 열어 글자와 피사체가 한눈에 읽히는지 눈으로도 확인한다 (packaging-critic)")
    sys.exit(1 if r.failed else 0)


if __name__ == "__main__":
    main()
