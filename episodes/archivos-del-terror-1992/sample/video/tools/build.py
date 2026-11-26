#!/usr/bin/env python3
"""Build the sample video project (see build_head.py for the rules).

    python3 episodes/archivos-del-terror-1992/sample/video/tools/build.py

Sources: build_head.py (timing, palette, shared style), build_scenes_a.py (rows 1–30), build_scenes_b.py
(rows 31–65), ../lib/a3d.js (three.js props). Output: ../index.html, ../compositions/*.html.
"""
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
for _f in ("build_head.py", "build_scenes_a.py", "build_scenes_b.py"):
    exec(compile(open(os.path.join(_HERE, _f)).read(), _f, "exec"))
SC_PREV = dict(SC)              # graphic versions, kept as fallbacks and reused by the photo overrides
exec(compile(open(os.path.join(_HERE, "build_scenes_photo.py")).read(), "build_scenes_photo.py", "exec"))
REAL_ROWS |= {7, 8, 16, 18, 19, 33, 34, 62}     # rows built on real photographs/scans in the graphic files


# ------------------------------------------------------------------ write scene files
def write_scene(n):
    p = f"s{n:02d}"
    d = DUR[n - 1]
    CUR[0] = PALN[n]
    sc = SC[n](p, d)
    cuts = sorted({float(x) for x in re.findall(r"/\*cut:([\d.]+)\*/", sc["js"])})
    # grade layers (vignette + film grain), then graphics above them so the accent stays clean
    grain = "".join(f"tl.set(q('grain'), {{ backgroundPosition: '{(k * 137) % 512}px {(k * 211) % 512}px' }}, {k * 2 / FPS:.3f});"
                    for k in range(int(d * FPS / 2) + 1))
    canvas = f'<canvas id="{p}-c3" width="1920" height="1080" style="position:absolute;left:0;top:0;width:1920px;height:1080px"></canvas>' if sc["mod"] else ""
    fg = f'<div id="{p}-fg" class="ao-fg">{sc["fg"]}</div>' if sc["fg"] else ""
    body = f"""{canvas}{sc['html']}
<div id="{p}-vig" class="ao-vig"></div><div id="{p}-grain" class="ao-grain"></div>
{fg}"""
    end = f"tl.set({{}}, {{}}, {d - 0.001:.3f});\nwindow.__timelines[\"{p}\"] = tl;"
    if sc["mod"]:
        import json as _j
        script = f"""<script type="module">
import {{ mount }} from "./lib/a3d.js";
const P = "{p}";
{JSLIB}
const draw = await mount("{p}-c3", "{sc['mod']['kind']}", {_j.dumps(sc['mod']['opts'])});
const st = {{ t: 0 }};
tl.fromTo(st, {{ t: 0 }}, {{ t: {d}, duration: {d}, ease: "none", onUpdate: () => draw(st.t) }}, 0);
draw(0);
{sc['js']}
{grain}
{end}
</script>"""
    else:
        script = f"""<script>
(function () {{
const P = "{p}";
{JSLIB}
{sc['js']}
{grain}
{end}
}})();
</script>"""
    html = f"""<template>
<style>
{BASE_CSS}
#root{{background:{sc['bg']}}}
{sc['css']}
</style>
<div id="root" data-composition-id="{p}" data-width="1920" data-height="1080" data-duration="{d}">
{body}
</div>
{script}
</template>
"""
    open(os.path.join(COMP, f"{p}.html"), "w").write(html)
    return cuts


CUTS = {n: write_scene(n) for n in range(1, 66)}
# internal cuts per scene, also read from /*cut*/ markers next to shot() calls
for n in range(1, 66):
    js_src = open(os.path.join(COMP, f"s{n:02d}.html")).read()
    if "/*cut*/" in js_src:
        t = re.findall(r"/\*cut\*/\s*(?:shot\('[^']+', |tl\.set\(q\('[^']+'\), \{[^}]*\}, )([\d.]+)", js_src)
        CUTS[n] = sorted(set(CUTS[n]) | {float(x) for x in t})

# ------------------------------------------------------------------ fx: light blooms on chosen seams (no grain here: grain lives in each scene)
LEAKS = [(10.0, 0), (13.9, 1), (29.6, 0), (45.5, 1), (63.9, 0), (86.8, 1), (103.9, 1), (112.1, 0)]
FX = f"""<template>
<style>
#root{{position:absolute;inset:0;pointer-events:none}}
#fx-leak{{position:absolute;left:-400px;top:-200px;width:1500px;height:1500px;border-radius:50%;background:radial-gradient(circle,rgba(255,246,232,.75),rgba(255,236,210,.25) 40%,rgba(0,0,0,0) 70%);opacity:0}}
</style>
<div id="root" data-composition-id="fx" data-width="1920" data-height="1080" data-duration="{END}"><div id="fx-leak"></div></div>
<script>
(function () {{
const tl = gsap.timeline({{ paused: true }});
{json.dumps([list(x) for x in LEAKS])}.forEach(([t, s]) => {{
  tl.fromTo('#fx-leak', {{ opacity: 0, x: s ? 1300 : -200, y: s ? -100 : 200 }}, {{ opacity: 0.55, x: s ? 900 : 200, y: 0, duration: 0.2, ease: 'power2.out' }}, t - 0.1);
  tl.to('#fx-leak', {{ opacity: 0, duration: 0.4, ease: 'power2.in' }}, t + 0.1);
}});
tl.set({{}}, {{}}, {END - 0.001});
window.__timelines["fx"] = tl;
}})();
</script>
</template>
"""
open(os.path.join(COMP, "fx.html"), "w").write(FX)

# ------------------------------------------------------------------ root: scene hosts, audio, review overlay
hosts = [f'<div id="s{n:02d}" data-composition-id="s{n:02d}" data-composition-src="compositions/s{n:02d}.html" data-start="{STARTS[n - 1]}" '
         f'data-duration="{DUR[n - 1]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:1"></div>'
         for n in range(1, 66)]

TW = "assets/audio/typewriter.wav"
IMP = "assets/audio/impact.wav"
# music bed: a licensed track converted by prep_assets.py to assets/audio/music.wav replaces the synthesized drone
MUSIC = "assets/audio/music.wav" if os.path.exists(os.path.join(ASSETS, "audio", "music.wav")) else "assets/audio/bed.wav"
MUSIC_FILE_LUFS = -19.0           # both files are loudness-normalized to this in prep_assets.py
# config/format.json → production.audio (user, 2026-11-26): music ~28 dB under the narration, up to -20 dB only in pauses >= 2 s.
# No narration yet: preview with narration assumed at -16 LUFS → music -44 LUFS under lines, -36 LUFS in pauses.
NARRATION_LUFS = -16.0
MUSIC_UNDER_DB, MUSIC_PAUSE_DB, PAUSE_MIN = -28.0, -20.0, 2.0
SFX_MASTER = 0.123                  # all effects together; tuned so the effect stem sits 6–10 dB over the music stem


def vol(lufs):
    return round(10 ** ((lufs - MUSIC_FILE_LUFS) / 20), 4)


# narration windows: provisional = words at 168 wpm from each line start (replace with data/voice.json in /voice)
SPEECH = [(t0, t0 + len(txt.split()) / 168 * 60) for t0, txt in LINES]
MUSIC_OFF = [(56.1, 62.9)]        # the drone stops on «Por ahora, nada contradice esa versión.» and returns with the door


def music_segments():
    """(start, end, lufs) runs: under-narration level, pause level where the voice rests >= PAUSE_MIN."""
    marks = []
    for i, (a, b) in enumerate(SPEECH):
        nxt = SPEECH[i + 1][0] if i + 1 < len(SPEECH) else END
        b = min(b, nxt)
        if nxt - b >= PAUSE_MIN:
            marks.append((a, b, NARRATION_LUFS + MUSIC_UNDER_DB))
            marks.append((b, nxt, NARRATION_LUFS + MUSIC_PAUSE_DB))
        else:
            marks.append((a, nxt, NARRATION_LUFS + MUSIC_UNDER_DB))
    runs = []
    for a, b, l in marks:
        for oa, ob in MUSIC_OFF:              # cut the silences out
            if a < ob and b > oa:
                if a < oa:
                    runs.append((a, oa, l))
                a = max(a, ob)
        if b > a:
            if runs and runs[-1][2] == l and a <= runs[-1][1] + 1e-6:
                runs[-1] = (runs[-1][0], b, l)
            else:
                runs.append((a, b, l))
    return runs


# music placement: sample/music-plan.md (scene-planner, 2026-11-26), tracks in assets/LICENSES.md §7.
# volume = the plan's per-track "under narration" gain (narration assumed -16 LUFS → music about -44 LUFS).
# The provisional timing has no narration pause >= 2 s, so the pause level (-20 dB) is not used yet; in /voice
# music_segments() above gives the pause windows from the measured narration.
M = "assets/music/"
MUSIC_PLAN = [  # id, file, start, end, offset in the track, volume, fade in, fade out
    ("m01", M + "M01_ondrosik_be_careful.wav", 0.0, 56.1, 0.0, 0.051, 0.8, 0.05),           # cut on «Por ahora…»
    ("m03", M + "M03_isaiah658_unsolved_investigation.wav", 63.9, 87.8, 0.0, 0.071, 0.8, 1.0),  # the room; 1 s crossfade into M02
    ("m02", M + "M02_ondrosik_calm_before_the_storm.wav", 86.8, 101.4, 0.0, 0.044, 1.0, 0.0),
    ("m02r", M + "M02_ondrosik_calm_before_the_storm.wav", 101.4, 103.9, 14.6, 0.062, 0.0, 0.05),  # +3 dB rise into the title, cut
    ("m05", M + "M05_ondrosik_waves_of_longing.wav", 108.1, END, 0.0, 0.050, 1.5, 0.8),
]
# synthesized drone (own work) only as a support layer where there is no music, about -40 LUFS
DRONE = [("dr1", "assets/audio/bed.wav", 56.1, 65.0, 56.1, vol(-40.0), 0.05, 1.1),
         ("dr2", "assets/audio/bed.wav", 103.9, 107.6, 103.9, vol(-40.0), 0.3, 0.5)]
AUD = [(a, f, s_, round(e - s_, 3), ms, v, fi, fo) for a, f, s_, e, ms, v, fi, fo in MUSIC_PLAN + DRONE]
SFX = [
    ("tw1", TW, 0.30, 1.85, 0.4, 0.9), ("tw2", TW, 2.42, 1.0, 5.2, 0.9),
    ("tw3", TW, 20.05, 0.85, 9.0, 0.6), ("tw4", TW, 23.98, 1.55, 12.0, 0.85),
    ("tw5", TW, 49.52, 0.85, 15.3, 0.85), ("tw6", TW, 89.03, 0.55, 2.0, 0.8),
    ("tw7", TW, 109.1, 1.4, 6.6, 0.85),
    ("wh1", "assets/audio/whoosh.wav", 3.5, 1.2, 0.0, 0.8), ("wh2", "assets/audio/whoosh_b.wav", 31.5, 0.9, 0.0, 0.6),
    ("wh3", "assets/audio/whoosh_b.wav", 62.82, 0.9, 0.0, 0.9), ("wh4", "assets/audio/whoosh.wav", 107.55, 1.2, 0.0, 0.9),
    ("wh5", "assets/audio/whoosh_b.wav", 66.2, 0.9, 0.0, 0.45),
    ("st1", IMP, 22.45, 1.6, 0.0, 1.1), ("st2", IMP, 44.05, 1.6, 0.0, 1.0),
    ("pz", IMP, 57.4, 2.0, 0.0, 1.0),
    ("lk", "assets/audio/lock.wav", 61.95, 0.8, 0.0, 1.0), ("lki", IMP, 61.95, 2.0, 0.0, 1.6),
    ("q1", IMP, 86.85, 2.0, 0.0, 1.6), ("q2", IMP, 91.15, 2.0, 0.0, 1.6),
    ("q3", IMP, 96.45, 2.0, 0.0, 1.7), ("zq3b", IMP, 97.67, 2.0, 0.0, 1.1),
    ("rs1", "assets/audio/riser.wav", 100.95, 3.0, 0.0, 0.8), ("tt", IMP, 103.95, 2.0, 0.0, 1.8),
    ("rs2", "assets/audio/riser.wav", 106.1, 1.0, 2.0, 0.8),
    ("rs0", "assets/audio/riser.wav", 58.4, 3.0, 0.0, 0.35),
]
for name, t0, dur, step in (("k21", 36.85, 0.85, 0.09), ("k39", 67.55, 1.0, 0.09), ("k42", 73.95, 0.95, 0.08), ("k64", 116.45, 1.15, 0.1)):
    i, t = 0, t0
    while t < t0 + dur:
        SFX.append((f"{name}_{i}", "assets/audio/tick.wav", round(t, 3), 0.06, 0.0, 0.7))
        t += step * (1 + i * 0.06)
        i += 1
# balance between effects (relative); SFX_MASTER moves them together
GAIN = {"impact": 0.6, "lock": 0.6, "riser": 0.9, "whoosh": 1.6, "typewriter": 2.2, "tick": 2.0}


def gain(f):
    return next((g for k, g in GAIN.items() if k in f), 1.0) * SFX_MASTER


def LANE(a):
    if a in ("m03", "m02r"):
        return 2
    for pre, ln in (("m0", 3), ("dr", 12), ("tw", 4), ("wh", 5), ("st", 6), ("pz", 6), ("q", 6), ("tt", 6), ("lki", 6), ("lk", 7), ("rs", 8), ("k", 9)):
        if a.startswith(pre):
            return ln
    return 10


AUD += [(a, f, s_, du, ms, round(v * gain(f), 3), 0, 0) for a, f, s_, du, ms, v in SFX]
audio = "\n".join(f'<audio id="a-{a}" class="clip" src="{f}" data-start="{s}" data-duration="{du}" data-media-start="{ms}" data-volume="{v}"'
                  + (f' data-fade-in="{fi}"' if fi else "") + (f' data-fade-out="{fo}"' if fo else "") + f' data-track-index="{LANE(a)}"></audio>'
                  for a, f, s, du, ms, v, fi, fo in AUD)
caps = []
for i, (t0, txt) in enumerate(LINES):
    t1 = LINES[i + 1][0] if i + 1 < len(LINES) else END
    caps.append(f'<div id="cap{i}" class="clip cap" data-start="{t0}" data-duration="{round(t1 - t0, 3)}" data-track-index="11"><span>{esc(txt)}</span></div>')

INDEX = f"""<!doctype html>
<html lang="es" data-composition-variables='[{{"id":"review","type":"boolean","label":"Versión de revisión (texto del guion + BORRADOR)","default":false}}]'>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{FONTS}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
#review {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; z-index: 90; display: none; pointer-events: none; }}
#review .cap {{ position: absolute; left: 240px; width: 1440px; bottom: 34px; text-align: center; }}
#review .cap span {{ display: inline-block; font: 400 28px/1.35 "Work Sans", sans-serif; color: #fff; background: rgba(0,0,0,.66); padding: 6px 16px; }}
#review-flag {{ position: absolute; left: 110px; top: 70px; font: 700 22px/1 "IBM Plex Mono", monospace; letter-spacing: .14em; color: #fff;
  background: rgba(0,0,0,.7); padding: 10px 14px; border: 2px solid #fff; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080" data-fps="30">
{chr(10).join(hosts)}
<div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{END}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:80"></div>
{audio}
<div id="review" data-track-kind="captions" data-layout-allow-caption-zone>
<div id="review-flag">BORRADOR · SIN NARRACIÓN</div>
{chr(10).join(caps)}
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const v = (window.__hyperframes && window.__hyperframes.getVariables) ? window.__hyperframes.getVariables() : {{}};
if (v.review === true || v.review === "true") document.getElementById("review").style.display = "block";
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(os.path.join(VIDEO, "index.html"), "w").write(INDEX)
# shot list (scene starts + internal cuts) for measuring the real cut rate
shots = []
for n in range(1, 66):
    if n == 2:
        continue
    shots.append(STARTS[n - 1])
    shots += [round(STARTS[n - 1] + c, 3) for c in CUTS[n]]
json.dump({"shot_starts": sorted(shots), "end": END}, open(os.path.join(VIDEO, "shots.json"), "w"), indent=0)
real = sum(DUR[n - 1] for n in REAL_ROWS)
json.dump({"shot_starts": sorted(shots), "end": END, "real_rows": sorted(REAL_ROWS), "real_sec": round(real, 1)}, open(os.path.join(VIDEO, "shots.json"), "w"), indent=0)
print("real-photo rows:", len(REAL_ROWS), f"{real:.1f} s = {100 * real / END:.1f}%")
print("built", len(SC), "scenes;", len(shots), "shots;", "photo slots missing:", [k for k, v in HAVE.items() if not v])
