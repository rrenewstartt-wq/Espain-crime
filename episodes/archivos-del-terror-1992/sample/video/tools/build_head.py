#!/usr/bin/env python3
"""Generate the HyperFrames sample (0:00–2:01) from the shot table — v2 after video-qa (2026-11-26).

    python3 episodes/archivos-del-terror-1992/sample/video/tools/build.py

Writes video/index.html and video/compositions/sNN.html (one file per row of sample/shots.md).
Timing = STARTS (shots.md, 168 wpm provisional). In /voice replace STARTS with narration times and rebuild.
Never edit the generated HTML by hand: change this file (and build_scenes.py) and rebuild.

Rules this file follows (docs/visual-style.md, video-qa 2026-11-26):
- an internal cut exists only where the content changes (other material, other crop, an insert); no grade tricks;
- palettes per period: PAL (1992 cold morning, archive tungsten, 1954 sepia); deep blacks, no haze lifts;
- teal #2EC4B6 only for type, lines and outline boxes, drawn in the graphics layer ABOVE the grade (vignette + grain);
- recreations: lit three.js props (lib/a3d.js) and backlit 2.5D layers, labelled RECREACIÓN.
Photos that are still missing (Commons 429) live in PHOTO: drop the file in assets/commons, run prep_assets.py,
and the scenes that have a photo branch switch automatically.

Clean vs review render: index.html declares the boolean variable `review` (default false).
  render --variables '{"review":true}'  → script lines at the bottom + "BORRADOR · SIN NARRACIÓN".
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.dirname(HERE)
COMP = os.path.join(VIDEO, "compositions")
os.makedirs(COMP, exist_ok=True)
ACC = "#2EC4B6"
FPS = 30

# ------------------------------------------------------------------ timing (shots.md, start seconds)
STARTS = [0.0, 2.4, 3.6, 5.0, 6.4, 8.2, 10.0, 11.6, 13.9, 15.6, 17.8, 20.0, 22.1, 23.9, 25.9, 27.7, 29.6, 31.6, 32.9,
          34.8, 36.8, 38.8, 40.7, 43.1, 45.5, 47.9, 49.5, 51.1, 53.6, 56.1, 58.2, 59.4, 60.6, 61.7, 62.9, 63.9, 65.1,
          66.3, 67.5, 69.7, 71.4, 73.9, 76.1, 77.7, 79.3, 81.1, 82.9, 84.9, 86.8, 89.0, 91.1, 93.1, 94.7, 96.4, 98.9,
          101.4, 103.9, 105.3, 107.1, 108.1, 110.3, 112.1, 114.3, 116.4, 118.9]
END = 121.4
assert len(STARTS) == 65
DUR = [round(b - a, 3) for a, b in zip(STARTS, STARTS[1:] + [END])]

# script lines for the review overlay (script.md line → start second)
LINES = [
    (0.0, "Es la mañana del 22 de diciembre de 1992 en Lambaré, a cuatro kilómetros del centro de Asunción."),
    (6.4, "Faltan tres días para Navidad y el día amanece caluroso."),
    (10.0, "Hace casi cuatro años que cayó la dictadura de Alfredo Stroessner."),
    (13.9, "Ante una dependencia policial de nombre administrativo, el Departamento de Producciones, llega un juez con una orden."),
    (20.0, "Se llama José Agustín Fernández y es juez en lo criminal."),
    (23.9, "El expediente que lo trae hasta aquí lleva un nombre corto: «Martín Almada sobre Hábeas Data»."),
    (29.6, "Almada es un educador que, amparado en la Constitución de junio, pide ver lo que la policía guarda sobre él."),
    (36.8, "Han pasado 99 días desde que el juzgado recibió su pedido."),
    (40.7, "Y la respuesta oficial, según recuerda el juez, es que esos documentos desaparecieron con el golpe de febrero de 1989."),
    (47.9, "Según la Policía, ya no queda nada que buscar."),
    (51.1, "En la puerta, el oficial de guardia no quiere dejarlo pasar sin su jefe."),
    (56.1, "Por ahora, nada contradice esa versión."),
    (58.2, "Hasta que, al final de una escalera, un cerrajero rompe el candado de una puerta cerrada."),
    (63.9, "Detrás aparece una montaña desordenada de libros, carpetas y fichas."),
    (67.5, "Con los años, el inventario hablará de cerca de 800.000 páginas."),
    (71.4, "Son unos doscientos metros lineales de papel."),
    (73.9, "Hay 11.225 fichas de personas detenidas."),
    (76.1, "Hay unas 20.000 fotografías y 543 casetes de audio."),
    (79.3, "El inventario los fecha entre 1927 y febrero de 1989."),
    (82.9, "Solo sacarlos de este lugar va a llevar unas doce horas."),
    (86.8, "¿Cómo sobreviven casi intactos los papeles que una policía decía haber perdido?"),
    (91.1, "¿Qué hacen en un depósito de Lambaré las fichas de detenidos argentinos, uruguayos y chilenos?"),
    (96.4, "Y sobre todo, ¿por qué un aparato que negaba haber detenido a ciertos desaparecidos los tenía fichados, con foto y huellas?"),
    (103.9, "Esta es la historia de los Archivos del Terror."),
    (107.1, "Para entender por qué existe esa habitación, hay que volver a mayo de 1954."),
    (112.1, "Ese mes, un golpe militar lleva al poder al general Alfredo Stroessner."),
    (116.4, "Va a gobernar treinta y cinco años seguidos, el equivalente a siete períodos presidenciales."),
]

ASSETS = os.path.join(VIDEO, "assets")
# photo slots (shots.md codes). Present → photo version of the scene; absent → graphic fallback.
PHOTO = {"A2": "martin_almada_2008_g.jpg", "A4": "museo_justicia_archivo_terror_2019_g.jpg",
         "A5": "heap_of_tapes_g.jpg", "A7": "old_door_locked_g.jpg"}
HAVE = {k: os.path.exists(os.path.join(ASSETS, "img", f)) for k, f in PHOTO.items()}
MAP = json.load(open(os.path.join(ASSETS, "map", "southamerica.json")))

# palette per scene: cold = 1992 morning, tung = archive discovery under tungsten, sepia = 1954
PALN = {}
for n in range(1, 66):
    PALN[n] = "cold" if n <= 30 else ("tung" if n <= 58 else "sepia")
for n in (51, 52):
    PALN[n] = "map"
CUR = ["cold"]


def DESK():
    pal = CUR[0] if CUR[0] in ("cold", "tung", "sepia") else "cold"
    return f"background:#000 url(assets/tex/desk_{pal}.jpg) center/cover"


def BIGPAPER():
    pal = CUR[0] if CUR[0] in ("cold", "tung", "sepia") else "cold"
    return (f'<div style="position:absolute;left:-1500px;top:-1500px;width:4920px;height:4080px;'
            f'background:url(assets/tex/paper_{pal}.jpg) 1500px 1500px/1920px 1080px"></div>')


def PAPER(pos="center", size="cover"):
    pal = CUR[0] if CUR[0] in ("cold", "tung", "sepia") else "cold"
    return f"background:url(assets/tex/paper_{pal}.jpg) {pos}/{size}"


FONTS = """
@font-face{font-family:"Anton";src:url("assets/fonts/Anton-Regular.ttf")}
@font-face{font-family:"Courier Prime";src:url("assets/fonts/CourierPrime-Regular.woff2");font-weight:400}
@font-face{font-family:"Courier Prime";src:url("assets/fonts/CourierPrime-Bold.woff2");font-weight:700}
@font-face{font-family:"Barlow Condensed";src:url("assets/fonts/BarlowCondensed-ExtraBold.woff2");font-weight:800}
@font-face{font-family:"Barlow Condensed";src:url("assets/fonts/BarlowCondensed-Bold.woff2");font-weight:700}
@font-face{font-family:"IBM Plex Mono";src:url("assets/fonts/IBMPlexMono-Regular.ttf");font-weight:400}
@font-face{font-family:"IBM Plex Mono";src:url("assets/fonts/IBMPlexMono-Bold.ttf");font-weight:700}
@font-face{font-family:"Work Sans";src:url("assets/fonts/WorkSans-Regular.ttf");font-weight:400}
@font-face{font-family:"Work Sans";src:url("assets/fonts/WorkSans-Bold.ttf");font-weight:700}
@font-face{font-family:"Work Sans";src:url("assets/fonts/WorkSans-BoldItalic.ttf");font-weight:700;font-style:italic}
@font-face{font-family:"Caveat";src:url("assets/fonts/Caveat-Bold.woff2");font-weight:700}
"""
BASE_CSS = FONTS + f"""
#root{{position:absolute;inset:0;overflow:hidden;background:#000;color:#f1f3f2;font-family:"Work Sans",sans-serif}}
.ao-full{{position:absolute;left:0;top:0;width:1920px;height:1080px}}
.ao-cam{{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:50% 50%}}
.ao-fg{{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:40;transform-origin:50% 50%}}
.ao-vig{{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:20;pointer-events:none;
  background:radial-gradient(ellipse at 50% 48%,rgba(0,0,0,0) 48%,rgba(0,0,0,.38) 78%,rgba(0,0,0,.72) 100%)}}
.ao-grain{{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:21;pointer-events:none;
  background:url(assets/tex/grain.png);mix-blend-mode:overlay;opacity:.26}}
.ao-tag{{position:absolute;top:70px;right:110px;font:700 22px/1 "IBM Plex Mono",monospace;letter-spacing:.16em;color:#f3f5f4;
  background:rgba(5,7,9,.72);padding:11px 16px 11px 14px;display:flex;align-items:center;gap:12px;text-transform:uppercase;z-index:60}}
.ao-tag i{{width:12px;height:12px;background:{ACC};display:block;flex:none}}
.ao-tag.src{{font-weight:400;font-size:19px;letter-spacing:.07em;text-transform:none}}
.ao-tag.src b{{font-weight:700;letter-spacing:.14em;text-transform:uppercase}}
.ao-lt{{position:absolute;left:176px;bottom:150px;z-index:55;padding:4px 30px 6px 0}}
.ao-lt .bar{{position:absolute;left:-26px;top:8px;width:10px;bottom:10px;background:{ACC}}}
.ao-lt .nm{{font:800 80px/0.95 "Barlow Condensed",sans-serif;text-transform:uppercase;color:#fff;display:inline-block;
  transform:skewX(-9deg);letter-spacing:.01em;text-shadow:0 4px 22px rgba(0,0,0,.8),0 0 2px rgba(0,0,0,.7)}}
.ao-lt .rl{{font:400 33px/1.2 "Work Sans",sans-serif;color:#eef2f0;margin-top:10px;text-shadow:0 2px 12px rgba(0,0,0,.95)}}
.ao-ch{{display:none}}
.ao-num{{font-family:"Anton",sans-serif;color:{ACC};line-height:.92;letter-spacing:.005em;font-variant-numeric:tabular-nums}}
.ao-unit{{font-family:"Anton",sans-serif;color:#f4f2ec;letter-spacing:.03em}}
.ao-shadow{{box-shadow:0 30px 60px rgba(0,0,0,.6),0 6px 14px rgba(0,0,0,.45)}}
.ao-stamp{{font-family:"Anton",sans-serif;color:#1f5f73;border:8px solid #1f5f73;padding:6px 26px 2px;letter-spacing:.06em;
  display:inline-block;mix-blend-mode:multiply;opacity:.9}}
.ao-stampT{{font-family:"Anton",sans-serif;color:{ACC};border:8px solid {ACC};padding:6px 26px 2px;letter-spacing:.06em;display:inline-block}}
.ao-blurline{{height:16px;background:#3c3a36;border-radius:3px;filter:blur(4px);opacity:.6;margin:0 0 26px}}
.ao-hand{{font-family:"Caveat",cursive;font-weight:700}}
"""

JSLIB = """
const tl = gsap.timeline({ paused: true });
const q = (s) => "#" + P + "-" + s;
function type(key, n, t0, dt) { for (let i = 0; i < n; i++) tl.set(q(key + i), { display: "inline" }, t0 + i * dt); }
function blink(key, t0, t1, per) { let on = true; for (let t = t0; t < t1 - 0.001; t += per) { tl.set(q(key), { opacity: on ? 1 : 0 }, t); on = !on; } }
function fmt(n) { return Math.round(n).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, "."); }
function count(key, a, b, t0, d, pre, suf) { const F = Math.max(1, Math.round(d * 30)); for (let f = 0; f <= F; f++) { const p = f / F, e = 1 - Math.pow(1 - p, 3); tl.set(q(key), { textContent: "\\u200B" + (pre || "") + fmt(a + (b - a) * e) + (suf || "") }, t0 + f / 30); } }
function shot(key, t0, t1, a, b, ease) { tl.set(q(key), { scale: a[0], x: a[1], y: a[2], rotation: a[3] || 0 }, t0); tl.to(q(key), { scale: b[0], x: b[1], y: b[2], rotation: b[3] || 0, duration: t1 - t0, ease: ease || "none" }, t0); }
function show(key, t0, t1) { tl.set(q(key), { opacity: 0 }, 0); tl.set(q(key), { opacity: 1 }, t0); if (t1 !== undefined) tl.set(q(key), { opacity: 0 }, t1); }
function lt(t0) { tl.fromTo(q("lt"), { clipPath: "inset(-20% 100% -20% -10%)", x: -40 }, { clipPath: "inset(-20% -5% -20% -10%)", x: 0, duration: 0.5, ease: "expo.out" }, t0); }
function tag(t0) { tl.fromTo(q("tag"), { opacity: 0, x: 20 }, { opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }, t0); }
function whipIn(key, t0, dx) { tl.fromTo(q(key), { x: dx, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }, t0); }
function stampIn(key, t0, rot) { tl.fromTo(q(key), { scale: 2.4, opacity: 0, rotation: rot - 8 }, { scale: 1, opacity: 1, rotation: rot, duration: 0.16, ease: "power4.in" }, t0); }
function shake(key, t0, amp) { const k = [[1, -.6], [-.8, .9], [.6, -.4], [-.35, .3], [.15, -.1], [0, 0]]; k.forEach((v, i) => tl.set(q(key), { x: v[0] * amp, y: v[1] * amp }, t0 + i / 30)); }
function dust(n, t0, d) { for (let i = 0; i < n; i++) { const s = ((i * 7919) % 1000) / 1000; tl.fromTo(q("d" + i), { y: 0, opacity: 0 }, { y: -60 - 140 * s, x: (s - .5) * 60, opacity: .85, duration: d, ease: "none" }, t0); } }
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def typed(p, key, text):
    out = "".join(f'<span id="{p}-{key}{i}" class="ao-ch">{esc(c) if c != " " else "&nbsp;"}</span>' for i, c in enumerate(text))
    return out, len(text)


def tag_html(p, text, src=False):
    if src:
        head, _, rest = text.partition("·")
        return f'<div id="{p}-tag" class="ao-tag src"><i></i><span><b>{esc(head.strip())}</b> · {esc(rest.strip())}</span></div>'
    return f'<div id="{p}-tag" class="ao-tag"><i></i>{esc(text)}</div>'


def lt_html(p, name, role):
    return (f'<div id="{p}-lt" class="ao-lt"><div class="bar"></div><div class="nm">{esc(name)}</div>'
            f'<div class="rl">{esc(role)}</div></div>')


def dust_html(p, n, box, seed, size=(2, 6), color="rgba(255,236,210,.85)"):
    r = random.Random(seed)
    x0, y0, x1, y1 = box
    out = []
    for i in range(n):
        s = r.uniform(*size)
        out.append(f'<span id="{p}-d{i}" style="position:absolute;left:{r.uniform(x0, x1):.0f}px;top:{r.uniform(y0, y1):.0f}px;'
                   f'width:{s:.1f}px;height:{s:.1f}px;border-radius:50%;background:{color};opacity:0"></span>')
    return "".join(out)


def smoke_html(p, k, op=0.3, extra=""):
    return (f'<img id="{p}-smk{k}" src="assets/tex/smoke{k % 3}.png" style="position:absolute;left:-200px;top:-100px;width:2320px;'
            f'height:1280px;opacity:{op};{extra}" alt="">')


def doc_lines(n, gap=26, seed=0, color=None):
    r = random.Random(n * 13 + seed)
    st = f"background:{color};" if color else ""
    return "".join(f'<div class="ao-blurline" style="{st}width:{r.randint(55, 100)}%;margin-bottom:{gap}px"></div>' for _ in range(n))


SC = {}


def scene(n):
    def deco(f):
        SC[n] = f
        return f
    return deco


def S(html="", js="", css="", fg="", mod=None, bg="#000"):
    return {"html": html, "js": js, "css": css, "fg": fg, "mod": mod, "bg": bg}
