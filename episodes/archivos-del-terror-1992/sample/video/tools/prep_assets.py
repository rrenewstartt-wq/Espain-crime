#!/usr/bin/env python3
"""Build every derived asset of the sample video into video/assets/ (gitignored).

    python3 episodes/archivos-del-terror-1992/sample/video/tools/prep_assets.py

Sources: episodes/<ep>/assets/ (licences in assets/LICENSES.md) and the repo fonts in assets/fonts/.
Everything here is either a graded copy of a licensed file or a texture/sound we make ourselves
(numpy noise, ffmpeg synthesis). Deterministic: fixed seeds.
"""
import json
import math
import os
import shutil
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.dirname(HERE)
EP = os.path.abspath(os.path.join(VIDEO, "..", ".."))
REPO = os.path.abspath(os.path.join(EP, "..", ".."))
SRC = os.path.join(EP, "assets")
OUT = os.path.join(VIDEO, "assets")
for d in ("img", "tex", "fonts", "audio", "map", "fig"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)


def out(*p):
    return os.path.join(OUT, *p)


def noise(w, h, scale, seed, octaves=4):
    """Fractal value noise in [0,1], shape (h,w)."""
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        gw, gh = max(2, int(w / scale * 2 ** o)), max(2, int(h / scale * 2 ** o))
        g = (rng.random((gh, gw)) * 255).astype(np.uint8)
        up = np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC), np.float32) / 255
        acc += up * amp
        tot += amp
        amp *= 0.5
    acc /= tot
    acc = (acc - acc.min()) / (acc.max() - acc.min() + 1e-6)
    return acc


def save(arr, path, mode="RGB", q=90):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode)
    if path.endswith(".jpg"):
        im.save(path, quality=q)
    else:
        im.save(path, optimize=True)


# ---------------------------------------------------------------- fonts
FONTS = ["Caveat-Bold.woff2", "Anton-Regular.ttf", "CourierPrime-Regular.woff2", "CourierPrime-Bold.woff2", "BarlowCondensed-Bold.woff2",
         "BarlowCondensed-ExtraBold.woff2", "IBMPlexMono-Regular.ttf", "IBMPlexMono-Bold.ttf", "WorkSans-Regular.ttf",
         "WorkSans-Bold.ttf", "WorkSans-BoldItalic.ttf"]
for f in FONTS:
    shutil.copy(os.path.join(REPO, "assets", "fonts", f), out("fonts", f))

# ---------------------------------------------------------------- textures
W, H = 2400, 1600
# cream paper: fibres + blotches + edge darkening
n1 = noise(W, H, 400, 1)
n2 = noise(W, H, 40, 2, 3)
fib = np.asarray(Image.fromarray((np.random.default_rng(3).random((H, W)) * 255).astype(np.uint8))
                 .filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
yy, xx = np.mgrid[0:H, 0:W]
edge = np.clip(np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)), 0, 1.4)
base = np.array([238, 222, 186], np.float32)
shade = 1 - 0.10 * n1 - 0.05 * n2 - 0.035 * fib - 0.12 * edge ** 3
paper = base[None, None, :] * shade[..., None]
stain = noise(W, H, 260, 4)
paper[..., 2] -= 18 * np.clip(stain - 0.55, 0, 1) * 4
save(paper, out("tex", "paper_cream.jpg"))
# grey card stock (index cards / folders), cooler
base2 = np.array([206, 208, 200], np.float32)
save(base2[None, None, :] * (1 - 0.08 * n1 - 0.05 * n2 - 0.04 * fib)[..., None], out("tex", "paper_grey.jpg"))
# dark desk / backdrop: blue-slate with soft mottling
dk = np.array([30, 46, 58], np.float32)
save(dk[None, None, :] * (0.75 + 0.45 * noise(1920, 1080, 500, 5))[..., None]
     * (1 - 0.35 * np.clip(np.hypot((np.mgrid[0:1080, 0:1920][1] - 960) / 960, (np.mgrid[0:1080, 0:1920][0] - 540) / 540), 0, 1.4) ** 2)[..., None],
     out("tex", "desk_dark.jpg"))
# film grain tile (grey, used with overlay blend)
g = np.random.default_rng(7).normal(128, 38, (512, 512))
save(np.repeat(g[..., None], 3, 2), out("tex", "grain.png"))
# smoke layers (white, alpha from fractal noise)
for i in range(3):
    a = noise(1920, 1080, 700, 20 + i, 5)
    a = np.clip((a - 0.42) * 2.2, 0, 1) ** 1.6
    rgba = np.zeros((1080, 1920, 4), np.float32)
    rgba[..., :3] = 235
    rgba[..., 3] = a * 255
    save(rgba, out("tex", f"smoke{i}.png"), "RGBA")
# sky for 1992 exteriors: hazy morning, pale blue to warm-white horizon (no amber)
sky = np.zeros((1080, 1920, 3), np.float32)
t = np.linspace(0, 1, 1080)[:, None]
top, hor = np.array([84, 134, 178]), np.array([238, 230, 210])
sky[:] = (top * (1 - t[..., None] ** 0.8) + hor * t[..., None] ** 0.8)
sky *= (0.94 + 0.08 * noise(1920, 1080, 600, 9))[..., None]
save(sky, out("tex", "sky_morning.jpg"))

# fingerprint pattern (generated, not a real print)
S = 700
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
cx, cy = S / 2, S * 0.55
warp = noise(S, S, 220, 11) * 26
r = np.hypot((xx - cx) * 1.0, (yy - cy) * 1.25) + warp
ang = np.arctan2(yy - cy, xx - cx)
ridges = 0.5 + 0.5 * np.sin(r / 5.2 + 0.9 * np.sin(ang * 2))
mask = np.clip(1 - (np.hypot((xx - cx) / (S * 0.36), (yy - cy) / (S * 0.46))) ** 6, 0, 1)
ink = (ridges > 0.55).astype(np.float32) * mask * (0.65 + 0.35 * noise(S, S, 60, 12))
rgba = np.zeros((S, S, 4), np.float32)
rgba[..., :3] = [34, 40, 48]
rgba[..., 3] = ink * 230
save(rgba, out("tex", "fingerprint.png"), "RGBA")

# scribble sheet for index cards (illegible handwriting-like strokes, no real names)
rng = np.random.default_rng(21)
for k in range(3):
    im = Image.new("RGBA", (900, 560), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for line in range(7):
        y = 70 + line * 66 + rng.integers(-4, 5)
        x = 40 + rng.integers(0, 30)
        end = 860 - rng.integers(0, 380)
        pts = []
        while x < end:
            for _ in range(rng.integers(3, 8)):
                pts.append((x, y + rng.normal(0, 7)))
                x += rng.integers(6, 14)
            if len(pts) > 1:
                d.line(pts, fill=(40, 52, 78, 200), width=3, joint="curve")
            pts = []
            x += rng.integers(14, 30)
    im = im.filter(ImageFilter.GaussianBlur(0.7))
    im.save(out("tex", f"scribble{k}.png"))

# ---------------------------------------------------------------- photos (licensed, see LICENSES.md)
def grade(src, dst, kind, maxw=2200):
    im = Image.open(src).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255
    lum = a @ np.array([0.299, 0.587, 0.114])
    if kind == "sepia":          # 1954: warm brown-cream, soft contrast
        lo, hi = np.array([0.22, 0.12, 0.05]), np.array([0.97, 0.86, 0.62])
        l2 = np.clip((lum - 0.04) / 0.94, 0, 1) ** 1.05
        o = lo * (1 - l2[..., None]) + hi * l2[..., None]
    elif kind == "cool":         # 1992 recreations: desaturated, slate shadows
        sat = 0.85
        o = lum[..., None] * (1 - sat) + a * sat
        o = o * np.array([0.92, 0.98, 1.04]) * 0.92 + np.array([0.0, 0.01, 0.02])
    elif kind == "doc":          # scanned documents: paper warmed slightly
        o = a * np.array([0.97, 0.95, 0.88]) + np.array([0.0, 0.0, 0.0])
    else:
        o = a
    save(o * 255, dst, q=92)


grade(os.path.join(SRC, "commons", "stroessner_1954_resck.jpg"), out("img", "stroessner_sepia.jpg"), "sepia")
grade(os.path.join(SRC, "commons", "padlocks_old_door_frame_varlan.jpg"), out("img", "padlocks_cool.jpg"), "cool")
for f in ("const1992_p01_portada.png", "const1992_p42_art135_habeas_data.png"):
    grade(os.path.join(SRC, "docs", f), out("img", f.replace(".png", ".jpg")), "doc", maxw=2400)
# pending Commons photos: graded only if fetch_pending_assets.sh got them
for f, kind in (("martin_almada_2008.jpg", "cool"), ("museo_justicia_archivo_terror_2019.jpg", "cool"),
                ("heap_of_tapes.jpg", "cool"), ("old_door_locked.jpg", "cool")):
    p = os.path.join(SRC, "commons", f)
    if os.path.exists(p) and os.path.getsize(p) > 10000:
        grade(p, out("img", f.replace(".jpg", "_g.jpg")), kind)

# archive photos delivered later (assets/photos/): copied only when LICENSES.md records them
_lic = open(os.path.join(SRC, "LICENSES.md")).read()
for f in sorted(os.listdir(os.path.join(SRC, "photos"))) if os.path.isdir(os.path.join(SRC, "photos")) else []:
    if f in _lic:
        grade(os.path.join(SRC, "photos", f), out("img", f), "sepia" if f.startswith("loc_") else "doc", maxw=2400)

# OSM city map (already dark-processed by scene-planner); copy as is
shutil.copy(os.path.join(SRC, "map_asuncion_lambare_osm_dark.png"), out("map", "asuncion_lambare_osm_dark.png"))

# ---------------------------------------------------------------- vector map of South America (Natural Earth, PD)
NE = os.path.join(SRC, "data", "naturalearth")
LON0, LON1, LAT0, LAT1 = -86.0, -30.0, -57.0, 8.0
K = 72.0                 # px per degree latitude
COS = math.cos(math.radians(25))
MW, MH = int((LON1 - LON0) * K * COS), int((LAT1 - LAT0) * K)


def proj(lon, lat):
    return (lon - LON0) * K * COS, (LAT1 - lat) * K


def ring_path(ring, tol=2.0):
    pts, last = [], None
    for lon, lat in ring:
        x, y = proj(lon, lat)
        if last is None or abs(x - last[0]) + abs(y - last[1]) >= tol:
            pts.append((x, y))
            last = (x, y)
    if len(pts) < 3:
        return ""
    return "M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + "Z"


def geom_path(g, tol=2.0):
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return "".join(ring_path(r, tol) for poly in polys for r in poly[:1])


countries = {}
for ft in json.load(open(os.path.join(NE, "ne_10m_admin_0_south_america.geojson")))["features"]:
    name = ft["properties"].get("NAME")
    countries[name] = geom_path(ft["geometry"])
rivers = []
for ft in json.load(open(os.path.join(NE, "ne_10m_rivers_south_america.geojson")))["features"]:
    p = ft["properties"]
    if (p.get("scalerank") or 9) > 5:
        continue
    g = ft["geometry"]
    lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
    for ln in lines:
        pts = [proj(*c[:2]) for c in ln]
        rivers.append("M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in pts[::2] + pts[-1:]))
places = {"Asunción": (-57.635, -25.300), "Lambaré": (-57.647, -25.346), "Buenos Aires": (-58.40, -34.61),
          "Montevideo": (-56.17, -34.88), "Santiago": (-70.65, -33.45)}
mapdata = {"w": MW, "h": MH, "countries": countries, "rivers": rivers,
           "places": {k: proj(*v) for k, v in places.items()},
           "labels": {n: proj(*c) for n, c in {"ARGENTINA": (-65.5, -36.5), "URUGUAY": (-56.0, -32.7),
                                                "CHILE": (-71.6, -29.0), "PARAGUAY": (-58.6, -22.6),
                                                "BRASIL": (-51.0, -12.0), "BOLIVIA": (-64.5, -17.0)}.items()}}
json.dump(mapdata, open(out("map", "southamerica.json"), "w"))

exec(open(os.path.join(HERE, "prep_textures_v2.py")).read())
exec(open(os.path.join(HERE, "prep_photos.py")).read())
import sys
if "--no-audio" in sys.argv:
    print("ok (no audio) →", OUT)
    sys.exit(0)

# ---------------------------------------------------------------- audio (all 48 kHz stereo)
SFX = os.path.join(SRC, "sfx")


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def norm(src, dst, lufs, extra=""):
    af = (extra + "," if extra else "") + f"loudnorm=I={lufs}:TP=-2:LRA=11,aresample=48000"
    ff("-i", src, "-af", af, "-ac", "2", "-ar", "48000", dst)


# bed: the synthesized drone (low) + a quiet high pad (own synthesis) so the bed survives small speakers
ff("-f", "lavfi", "-i", "sine=f=220:d=122", "-f", "lavfi", "-i", "sine=f=261.63:d=122", "-f", "lavfi", "-i", "sine=f=329.63:d=122",
   "-f", "lavfi", "-i", "anoisesrc=d=122:c=pink:a=0.05:seed=3",
   "-filter_complex",
   "[0][1][2]amix=inputs=3,volume=0.5,tremolo=f=0.13:d=0.6,lowpass=f=900[ch];"
   "[3]bandpass=f=1800:w=1200,tremolo=f=0.11:d=0.8,volume=0.6[air];"
   "[ch][air]amix=inputs=2,aecho=0.8:0.7:180|420:0.35|0.25,afade=t=in:d=3[o]",
   "-map", "[o]", "-ac", "2", "-ar", "48000", out("audio", "pad_high.wav"))
ff("-i", os.path.join(SFX, "drone_ambient_120s.wav"), "-i", out("audio", "pad_high.wav"),
   "-filter_complex", "[0]volume=1.0[d];[1]volume=0.22[p];[d][p]amix=inputs=2:duration=first:normalize=0[o]",
   "-map", "[o]", out("audio", "bed_raw.wav"))
norm(out("audio", "bed_raw.wav"), out("audio", "bed.wav"), -19)
# licensed tracks of assets/music/wav48k (48 kHz conversions, LICENSES.md §7): copied as they are (levels set in build.py)
os.makedirs(out("music"), exist_ok=True)
_wav = os.path.join(SRC, "music", "wav48k")
_licm = open(os.path.join(SRC, "LICENSES.md")).read()
for f in sorted(os.listdir(_wav)) if os.path.isdir(_wav) else []:
    if os.path.splitext(f)[0] in _licm and f.split("_")[0] in ("M01", "M02", "M03", "M05"):
        if not os.path.exists(out("music", f)):
            shutil.copy(os.path.join(_wav, f), out("music", f))

os.remove(out("audio", "bed_raw.wav"))
os.remove(out("audio", "pad_high.wav"))
norm(os.path.join(SFX, "impact_low_2s.wav"), out("audio", "impact.wav"), -11, "highpass=f=30,acompressor=threshold=-20dB:ratio=6:attack=5:release=250:makeup=4,alimiter=limit=0.6")
norm(os.path.join(SFX, "whoosh_1s.wav"), out("audio", "whoosh.wav"), -17)
ff("-i", os.path.join(SFX, "whoosh_1s.wav"), "-af", "asetrate=48000*1.25,aresample=48000,loudnorm=I=-18:TP=-2", "-ac", "2",
   out("audio", "whoosh_b.wav"))
ff("-i", os.path.join(SFX, "lock_break_metal.wav"), "-af", "volume=-6dB,alimiter=limit=0.7", "-ar", "48000", out("audio", "lock.wav"))
norm(os.path.join(SFX, "riser_3s.wav"), out("audio", "riser.wav"), -18)
ff("-i", os.path.join(SFX, "type_key_synth.wav"), "-af", "volume=-10dB", "-ar", "48000", out("audio", "tick.wav"))
# typewriter (CC BY 4.0, Work With Sounds / Konrad Gutkowski): normalized copy, cut by data-media-start in the scenes
ff("-i", os.path.join(SFX, "wws_typewriter_erika5.ogg"), "-af", "highpass=f=120,loudnorm=I=-20:TP=-2,aresample=48000", "-ac", "2",
   out("audio", "typewriter.wav"))
print("ok →", OUT)
