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
{LEAKS}.forEach(([t, s]) => {{
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
AUD = [
    ("bed1", "assets/audio/bed.wav", 0.0, 56.1, 0.0, 0.62),            # drone stops on «Por ahora, nada contradice esa versión.»
    ("bed2", "assets/audio/bed.wav", 62.9, round(END - 62.9, 2), 8.0, 0.62),
    ("tw1", TW, 0.30, 1.85, 0.4, 0.9), ("tw2", TW, 2.42, 1.0, 5.2, 0.9),
    ("tw3", TW, 20.05, 0.85, 9.0, 0.6), ("tw4", TW, 23.98, 1.55, 12.0, 0.85),
    ("tw5", TW, 49.52, 0.85, 15.3, 0.85), ("tw6", TW, 89.03, 0.55, 2.0, 0.8),
    ("tw7", TW, 109.1, 1.4, 6.6, 0.85),
    ("wh1", "assets/audio/whoosh.wav", 3.5, 1.2, 0.0, 0.8), ("wh2", "assets/audio/whoosh_b.wav", 31.5, 0.9, 0.0, 0.6),
    ("wh3", "assets/audio/whoosh_b.wav", 62.82, 0.9, 0.0, 0.9), ("wh4", "assets/audio/whoosh.wav", 107.55, 1.2, 0.0, 0.9),
    ("wh5", "assets/audio/whoosh_b.wav", 66.2, 0.9, 0.0, 0.45),
    ("st1", IMP, 22.45, 1.6, 0.0, 0.5), ("st2", IMP, 44.05, 1.6, 0.0, 0.45),
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
        AUD.append((f"{name}_{i}", "assets/audio/tick.wav", round(t, 3), 0.06, 0.0, 0.7))
        t += step * (1 + i * 0.06)
        i += 1
# mix gains (offline ffmpeg sum of these cues: about -15 LUFS, peaks under -1 dBFS; hits 6–10 dB over the bed)
GAIN = {"bed": 2.4, "impact": 0.5, "lock": 0.55, "riser": 0.8, "whoosh": 1.0, "typewriter": 0.45, "tick": 1.0}


def gain(f):
    return next((g for k, g in GAIN.items() if k in f), 1.0)


def LANE(a):
    for pre, ln in (("bed", 3), ("tw", 4), ("wh", 5), ("st", 6), ("pz", 6), ("q", 6), ("tt", 6), ("lki", 6), ("lk", 7), ("rs", 8), ("k", 9)):
        if a.startswith(pre):
            return ln
    return 10


AUD = [(a, f, s_, du, ms, round(v * gain(f), 3)) for a, f, s_, du, ms, v in AUD]
audio = "\n".join(f'<audio id="a-{a}" class="clip" src="{f}" data-start="{s}" data-duration="{du}" data-media-start="{ms}" data-volume="{v}" data-track-index="{LANE(a)}"></audio>'
                  for a, f, s, du, ms, v in AUD)
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
print("built", len(SC), "scenes;", len(shots), "shots;", "photo slots missing:", [k for k, v in HAVE.items() if not v])
