#!/usr/bin/env python3
"""Measure a rendered video against the quality bar in config/format.json → production.

    python3 scripts/check_video.py episodes/<ep>/renders/<file>.mp4            # full check (after narration)
    python3 scripts/check_video.py <file>.mp4 --visual-only                    # before narration: skip audio checks
    python3 scripts/check_video.py <reference_clip>.mp4 --measure              # just print metrics (to calibrate the bar)

Measures with ffprobe/ffmpeg: resolution, fps, bitrate, integrated loudness and true peak (ebur128),
scene changes per minute (scene score > 0.25), longest static stretch (freezedetect), black stretches
(blackdetect) and narration silences (silencedetect). Exit code 1 if any FAIL.
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import FMT, Report  # noqa: E402

P = FMT["production"]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                         capture_output=True, text=True).stdout
    return json.loads(out)


def measure(path, audio=True):
    info = probe(path)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    num, den = (v["avg_frame_rate"].split("/") + ["1"])[:2] if v else ("0", "1")
    m = {"duration_sec": round(dur, 1), "width": v and v["width"], "height": v and v["height"],
         "fps": round(int(num) / max(int(den), 1), 2) if v else None, "codec": v and v["codec_name"],
         "bitrate_mbps": round(int(info["format"].get("bit_rate", 0)) / 1e6, 2), "has_audio": a is not None}
    sc = run(["ffmpeg", "-hide_banner", "-i", path, "-vf", "select='gt(scene,0.25)',showinfo", "-an", "-f", "null", "-"])
    cuts = len(re.findall(r"pts_time:", sc))
    m["scene_changes"] = cuts
    times = [float(x) for x in re.findall(r"pts_time:([\d.]+)", sc)]
    ow = min(P["pacing"].get("opening_sec", 120), dur)
    m["opening_scene_changes_per_min"] = round(sum(t < ow for t in times) / (ow / 60), 1) if ow else 0
    body = dur - ow
    m["body_scene_changes_per_min"] = round(sum(t >= ow for t in times) / (body / 60), 1) if body > 30 else None
    m["scene_changes_per_min"] = round(cuts / (dur / 60), 1) if dur else 0
    fz = run(["ffmpeg", "-hide_banner", "-i", path, "-vf", f"freezedetect=n=0.003:d={P['pacing']['max_static_sec']}",
              "-an", "-f", "null", "-"])
    freezes = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", fz)]
    m["static_over_limit"] = len(freezes)
    m["longest_static_sec"] = round(max(freezes), 1) if freezes else 0
    bk = run(["ffmpeg", "-hide_banner", "-i", path, "-vf", "blackdetect=d=0.3:pic_th=0.98", "-an", "-f", "null", "-"])
    spans = [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:[\d.]+ black_duration:([\d.]+)", bk)]
    card = P["pacing"].get("opening_black_card_max_sec", 0)
    # a date card on black at the very start (reference cold open) is allowed up to opening_black_card_max_sec
    m["opening_black_sec"] = round(next((d for s0, d in spans if s0 < 0.5), 0), 1)
    rest = [d for s0, d in spans if not (s0 < 0.5 and d <= card)]
    m["longest_black_sec"] = round(max(rest), 1) if rest else 0
    if audio and a is not None:
        eb = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
        il = re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)
        tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)
        m["integrated_lufs"] = float(il[-1]) if il else None
        m["true_peak_dbtp"] = float(tp[-1]) if tp else None
        sl = run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=n=-45dB:d={P['audio']['max_silence_sec']}",
                  "-vn", "-f", "null", "-"])
        m["silences_over_limit"] = len(re.findall(r"silence_end", sl))
        m["sample_rate"] = int(a.get("sample_rate", 0))
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--visual-only", action="store_true", help="내레이션 전: 음향 항목 생략")
    ap.add_argument("--measure", action="store_true", help="기준 비교 없이 수치만 출력 (레퍼런스 클립 측정용)")
    ap.add_argument("--expect-min", type=float, help="대본에서 계산한 예상 길이(분)")
    a = ap.parse_args()
    m = measure(a.video, audio=not a.visual_only)
    if a.measure:
        print(json.dumps(m, ensure_ascii=False, indent=1))
        return
    vq, au, pc = P["video"], P["audio"], P["pacing"]
    r = Report(f"영상 품질: {a.video} ({m['duration_sec'] / 60:.1f}분)")
    r.ok(m["width"] >= vq["width"] and m["height"] >= vq["height"], "해상도", f"{m['width']}×{m['height']} (최소 {vq['width']}×{vq['height']})")
    r.ok(vq["fps"][0] <= (m["fps"] or 0) <= vq["fps"][1] + 0.1, "프레임레이트", f"{m['fps']} fps")
    r.ok(m["bitrate_mbps"] >= vq["min_bitrate_mbps"], "비트레이트", f"{m['bitrate_mbps']} Mbps (최소 {vq['min_bitrate_mbps']})", fail="WARN")
    tag = " (잠정 기준)" if pc.get("status") == "provisional" else ""
    lo, hi = pc["scene_changes_per_min"]
    if m["body_scene_changes_per_min"] is None:
        r.add("WARN", "본문 화면 전환 빈도", "도입부보다 짧은 영상이라 본문 기준은 판정 안 함")
    else:
        r.ok(lo <= m["body_scene_changes_per_min"] <= hi, "본문 화면 전환 빈도 (잠정)",
             f"분당 {m['body_scene_changes_per_min']}회 (기준 {lo}~{hi}, 도입 {pc.get('opening_sec', 120)}초 이후)")
    omin = pc.get("opening_scene_changes_per_min_min")
    if omin:
        r.ok(m["opening_scene_changes_per_min"] >= omin, f"도입부({pc.get('opening_sec', 120)}초) 화면 전환 (레퍼런스 실측)",
             f"분당 {m['opening_scene_changes_per_min']}회 (최소 {omin}). 연속 패럴랙스 구간이면 video-qa 가 눈으로 판정", fail="WARN")
    r.ok(m["static_over_limit"] == 0, f"{pc['max_static_sec']:.0f}초 넘는 정지 화면 없음" + tag,
         f"{m['static_over_limit']}곳, 최장 {m['longest_static_sec']}초")
    r.ok(m["longest_black_sec"] <= pc["max_black_sec"], "암전 길이", f"최장 {m['longest_black_sec']}초 (최대 {pc['max_black_sec']}, 도입부 날짜 카드 {m['opening_black_sec']}초는 {pc.get('opening_black_card_max_sec', 0)}초까지 허용)")
    if a.expect_min:
        r.ok(abs(m["duration_sec"] / 60 - a.expect_min) <= 1.0, "길이가 대본 예상과 맞음", f"{m['duration_sec'] / 60:.1f}분 vs 예상 {a.expect_min:.1f}분", fail="WARN")
    if not a.visual_only:
        if not m["has_audio"]:
            r.add("FAIL", "오디오 트랙", "없음")
        else:
            il, tp = m.get("integrated_lufs"), m.get("true_peak_dbtp")
            r.ok(il is not None and abs(il - au["integrated_lufs"]) <= au["lufs_tolerance"], "음량",
                 f"{il} LUFS (목표 {au['integrated_lufs']}±{au['lufs_tolerance']})")
            r.ok(tp is not None and tp <= au["true_peak_max_dbtp"], "트루 피크", f"{tp} dBTP (최대 {au['true_peak_max_dbtp']})")
            r.ok(m["silences_over_limit"] == 0, f"{au['max_silence_sec']}초 넘는 무음 없음", f"{m['silences_over_limit']}곳", fail="WARN")
            r.ok(m["sample_rate"] >= au["sample_rate"], "샘플레이트", f"{m['sample_rate']} Hz", fail="WARN")
    else:
        r.add("WARN", "음향 검사 생략", "내레이션 전 단계 (--visual-only). 최종 렌더에서 다시 검사")
    r.print()
    print("  ※ 숫자로 못 보는 것(그래픽 완성도, 자막·카드 가독성, 레퍼런스와 나란히 본 인상)은 video-qa 가 프레임을 직접 보고 판정한다")
    sys.exit(1 if r.failed else 0)


if __name__ == "__main__":
    main()
