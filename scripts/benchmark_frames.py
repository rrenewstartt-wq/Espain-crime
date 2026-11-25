#!/usr/bin/env python3
"""Measure the VISUAL style of videos (reference/competitor clips, or our own renders).

    python3 scripts/benchmark_frames.py data/benchmark/raw/clips/*.mp4          # → data/benchmark/video_style.json + contact sheets
    python3 scripts/benchmark_frames.py episodes/<ep>/renders/<ep>-visual.mp4 --compare   # ours vs reference style

YouTube blocks video downloads from this cloud, so reference clips must be supplied by a person
(any legally obtained copy or screen recording; a few minutes per channel is enough) and placed in
data/benchmark/raw/clips/<channel>__<anything>.mp4. Clips stay in raw/ and are never committed.

Per video it measures: shot lengths (scene cuts), brightness/saturation, hue distribution and how
monochrome the grade is, share of near-black frames, and it writes a contact sheet (one frame every
10 s) for visual review by video-qa / format-analyst. Only numbers go to video_style.json.
"""
import argparse
import colorsys
import glob
import json
import os
import re
import statistics as st
import subprocess
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE, RAW, Report  # noqa: E402

OUT = f"{BASE}/data/benchmark/video_style.json"


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout.strip())


def shots(path, dur):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vf", "select='gt(scene,0.25)',showinfo", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    cuts = [0.0] + [float(x) for x in re.findall(r"pts_time:([\d.]+)", err)] + [dur]
    return [round(b - a, 2) for a, b in zip(cuts, cuts[1:]) if b - a > 0.05]


def frames(path, every, tmp):
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps=1/{every},scale=320:-1", f"{tmp}/f%05d.jpg"], check=True)
    return sorted(glob.glob(f"{tmp}/f*.jpg"))


def color_stats(paths):
    bright, sat, hues, black = [], [], [0] * 12, 0
    for p in paths:
        im = Image.open(p).convert("RGB").resize((64, 36))
        px = list(im.get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.getdata())
        hsv = [colorsys.rgb_to_hsv(*(c / 255 for c in q)) for q in px]
        v = st.mean(x[2] for x in hsv)
        bright.append(v)
        sat.append(st.mean(x[1] for x in hsv))
        if v < 0.06:
            black += 1
        for h, s, vv in hsv:
            if s > 0.35 and vv > 0.2:
                hues[int(h * 12) % 12] += 1
    tot = sum(hues) or 1
    share = [round(h / tot, 3) for h in hues]
    top = max(range(12), key=lambda i: share[i])
    mono = share[top] + share[(top - 1) % 12] + share[(top + 1) % 12]
    return {"brightness_mean": round(st.mean(bright), 3), "saturation_mean": round(st.mean(sat), 3),
            "dominant_hue_deg": top * 30 + 15, "monochrome_share": round(mono, 3),
            "black_frame_share": round(black / len(paths), 3), "hue_share_30deg": share}


def contact_sheet(paths, out, cols=6):
    if not paths:
        return
    w, h = Image.open(paths[0]).size
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), "white")
    for i, p in enumerate(paths):
        sheet.paste(Image.open(p), ((i % cols) * w, (i // cols) * h))
    sheet.save(out, quality=82)


def measure(path, sheet_dir):
    dur = duration(path)
    sl = shots(path, dur)
    with tempfile.TemporaryDirectory() as tmp:
        fr = frames(path, 2, tmp)
        col = color_stats(fr)
        os.makedirs(sheet_dir, exist_ok=True)
        sheet = os.path.join(sheet_dir, os.path.splitext(os.path.basename(path))[0] + "-sheet.jpg")
        contact_sheet(fr[::5], sheet)  # every 10 s
    return {"file": os.path.basename(path), "duration_sec": round(dur, 1), "shots": len(sl),
            "shot_len_median": round(st.median(sl), 2) if sl else None,
            "shot_len_p90": round(sorted(sl)[int(0.9 * (len(sl) - 1))], 2) if sl else None,
            "cuts_per_min": round(len(sl) / (dur / 60), 1), **col, "contact_sheet": os.path.relpath(sheet, BASE)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--compare", action="store_true", help="우리 영상을 video_style.json 의 레퍼런스 값과 비교")
    a = ap.parse_args()
    if a.compare:
        if not os.path.exists(OUT):
            sys.exit("레퍼런스 화면 측정값이 없습니다. 클립을 data/benchmark/raw/clips/ 에 두고 먼저 측정하세요 (docs/production-style.md).")
        ref = json.load(open(OUT, encoding="utf-8"))["summary"]["reference"]
        for v in a.videos:
            m = measure(v, os.path.join(os.path.dirname(os.path.abspath(v)), "sheets"))
            r = Report(f"화면 스타일 비교: {v}")
            r.ok(abs(m["shot_len_median"] - ref["shot_len_median"]) <= 0.3 * ref["shot_len_median"], "컷 길이 중앙값",
                 f"{m['shot_len_median']}초 vs 레퍼런스 {ref['shot_len_median']}초 (±30%)")
            r.ok(abs(m["brightness_mean"] - ref["brightness_mean"]) <= 0.08, "평균 밝기", f"{m['brightness_mean']} vs {ref['brightness_mean']}", fail="WARN")
            r.ok(abs(m["monochrome_share"] - ref["monochrome_share"]) <= 0.2, "단색 톤 정도", f"{m['monochrome_share']} vs {ref['monochrome_share']}", fail="WARN")
            r.ok(abs(m["saturation_mean"] - ref["saturation_mean"]) <= 0.1, "평균 채도", f"{m['saturation_mean']} vs {ref['saturation_mean']}", fail="WARN")
            r.print()
            print(f"  접촉 시트: {m['contact_sheet']} ← 레퍼런스 시트와 나란히 놓고 video-qa 가 눈으로 판정")
        return
    rows = [measure(v, f"{RAW}/clips/sheets") for v in a.videos]
    by = {}
    for r in rows:
        by.setdefault(r["file"].split("__")[0], []).append(r)
    summ = {}
    for ch, rs in by.items():
        summ[ch] = {k: round(st.median(x[k] for x in rs if x[k] is not None), 3)
                    for k in ("shot_len_median", "shot_len_p90", "cuts_per_min", "brightness_mean", "saturation_mean", "monochrome_share", "black_frame_share")}
        summ[ch]["clips"] = len(rs)
    ref_key = next((k for k in summ if "enigma" in k.lower() or "detras" in k.lower()), None)
    out = {"note": "클립에서 측정한 화면 스타일 수치. 클립 자체와 접촉 시트는 raw/ 에만 있다", "per_clip": rows,
           "summary": {**summ, "reference": summ.get(ref_key) if ref_key else None}}
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for ch, s in summ.items():
        print(ch, s)
    print(f"→ {os.path.relpath(OUT, BASE)}. 다음: config/format.json → production.pacing 을 레퍼런스 값으로 갱신(사용자 승인), docs/visual-style.md 작성")


if __name__ == "__main__":
    main()
