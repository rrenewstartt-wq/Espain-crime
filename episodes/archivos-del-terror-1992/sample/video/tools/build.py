#!/usr/bin/env python3
"""Generate the HyperFrames sample (0:00–2:01) from the shot table.

    python3 episodes/archivos-del-terror-1992/sample/video/tools/build.py

Writes video/index.html and video/compositions/sNN.html (one file per row of sample/shots.md).
Timing = ROWS below (start seconds from shots.md, 168 wpm provisional). In /voice, replace the
starts with the measured narration times and run again; nothing else needs to change.
Never edit the generated HTML by hand: change this file and rebuild.

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
HAVE = {k: os.path.exists(os.path.join(ASSETS, "img", f)) for k, f in
        (("almada", "martin_almada_2008_g.jpg"), ("museo", "museo_justicia_archivo_terror_2019_g.jpg"),
         ("tapes", "heap_of_tapes_g.jpg"), ("door", "old_door_locked_g.jpg"))}
MAP = json.load(open(os.path.join(ASSETS, "map", "southamerica.json")))

# ------------------------------------------------------------------ shared style
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
"""
BASE_CSS = FONTS + f"""
#root{{position:absolute;inset:0;overflow:hidden;background:#0c1013;color:#f1f3f2;font-family:"Work Sans",sans-serif}}
.ao-full{{position:absolute;left:0;top:0;width:1920px;height:1080px}}
.ao-cam{{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:50% 50%}}
.ao-cover{{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover}}
.ao-tag{{position:absolute;top:70px;right:110px;font:700 22px/1 "IBM Plex Mono",monospace;letter-spacing:.16em;color:#f3f5f4;
  background:rgba(7,11,14,.66);padding:11px 16px 11px 14px;display:flex;align-items:center;gap:12px;text-transform:uppercase;z-index:60}}
.ao-tag i{{width:12px;height:12px;background:{ACC};display:block;flex:none}}
.ao-tag.src{{font-weight:400;font-size:19px;letter-spacing:.07em;text-transform:none}}
.ao-tag.src b{{font-weight:700;letter-spacing:.14em;text-transform:uppercase}}
.ao-osm{{position:absolute;right:110px;bottom:60px;font:400 18px/1 "IBM Plex Mono",monospace;color:#e9eeec;background:rgba(7,11,14,.7);
  padding:8px 12px;z-index:60}}
.ao-lt{{position:absolute;left:176px;bottom:150px;z-index:55;padding:4px 30px 6px 0}}
.ao-lt .bar{{position:absolute;left:-26px;top:8px;width:10px;bottom:10px;background:{ACC}}}
.ao-lt .nm{{font:800 80px/0.95 "Barlow Condensed",sans-serif;text-transform:uppercase;color:#fff;display:inline-block;
  transform:skewX(-9deg);letter-spacing:.01em;text-shadow:0 4px 22px rgba(0,0,0,.75),0 0 2px rgba(0,0,0,.6)}}
.ao-lt .rl{{font:400 33px/1.2 "Work Sans",sans-serif;color:#eef2f0;margin-top:10px;text-shadow:0 2px 12px rgba(0,0,0,.9)}}
.ao-ch{{display:none}}
.ao-num{{font-family:"Anton",sans-serif;color:{ACC};line-height:.92;letter-spacing:.005em;font-variant-numeric:tabular-nums}}
.ao-unit{{font-family:"Anton",sans-serif;color:#f4f2ec;letter-spacing:.03em}}
.ao-mono{{font-family:"Courier Prime",monospace}}
.ao-paper{{background:url("assets/tex/paper_cream.jpg") center/cover}}
.ao-grey{{background:url("assets/tex/paper_grey.jpg") center/cover}}
.ao-desk{{background:url("assets/tex/desk_dark.jpg") center/cover}}
.ao-shadow{{box-shadow:0 30px 60px rgba(0,0,0,.55),0 6px 14px rgba(0,0,0,.4)}}
.ao-stamp{{font-family:"Anton",sans-serif;color:{ACC};border:8px solid {ACC};padding:6px 26px 2px;letter-spacing:.06em;
  display:inline-block;mix-blend-mode:multiply}}
.ao-blurline{{height:16px;background:#4a4a48;border-radius:3px;filter:blur(5px);opacity:.55;margin:0 0 26px}}
"""

JSLIB = """
const tl = gsap.timeline({ paused: true });
const q = (s) => "#" + P + "-" + s;
function type(key, n, t0, dt) { for (let i = 0; i < n; i++) tl.set(q(key + i), { display: "inline" }, t0 + i * dt); }
function blink(key, t0, t1, per) { let on = true; for (let t = t0; t < t1 - 0.001; t += per) { tl.set(q(key), { opacity: on ? 1 : 0 }, t); on = !on; } }
function fmt(n) { return Math.round(n).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, "."); }
function count(key, a, b, t0, d, pre, suf) { const F = Math.max(1, Math.round(d * 30)); for (let f = 0; f <= F; f++) { const p = f / F, e = 1 - Math.pow(1 - p, 3); tl.set(q(key), { textContent: "\u200B" + (pre || "") + fmt(a + (b - a) * e) + (suf || "") }, t0 + f / 30); } }
function shot(key, t0, t1, a, b, ease) { tl.set(q(key), { scale: a[0], x: a[1], y: a[2], rotation: a[3] || 0 }, t0); tl.to(q(key), { scale: b[0], x: b[1], y: b[2], rotation: b[3] || 0, duration: t1 - t0, ease: ease || "sine.inOut" }, t0); }
function lt(t0) { tl.fromTo(q("lt"), { clipPath: "inset(-20% 100% -20% -10%)", x: -40 }, { clipPath: "inset(-20% -5% -20% -10%)", x: 0, duration: 0.5, ease: "expo.out" }, t0); }
function tag(t0) { tl.fromTo(q("tag"), { opacity: 0, x: 20 }, { opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }, t0); }
function whipIn(key, t0, dx) { tl.fromTo(q(key), { x: dx, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.28, ease: "expo.out" }, t0); }
function stampIn(key, t0, rot) { tl.fromTo(q(key), { scale: 2.4, opacity: 0, rotation: rot - 8 }, { scale: 1, opacity: 1, rotation: rot, duration: 0.16, ease: "power4.in" }, t0); }
function shake(key, t0, amp) { const k = [[1, -.6], [-.8, .9], [.6, -.4], [-.35, .3], [.15, -.1], [0, 0]]; k.forEach((v, i) => tl.set(q(key), { x: v[0] * amp, y: v[1] * amp }, t0 + i / 30)); }
function dust(n, t0, d) { for (let i = 0; i < n; i++) { const s = ((i * 7919) % 1000) / 1000; tl.fromTo(q("d" + i), { y: 0, opacity: 0 }, { y: -60 - 140 * s, x: (s - .5) * 60, opacity: .9, duration: d, ease: "none" }, t0); } }
"""

R = random.Random(1992)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def typed(p, key, text, extra_cls=""):
    """Spans hidden until typed; returns (html, n)."""
    out = "".join(f'<span id="{p}-{key}{i}" class="ao-ch {extra_cls}">{esc(c) if c != " " else "&nbsp;"}</span>'
                  for i, c in enumerate(text))
    return out, len(text)


def tag_html(p, text, src=False):
    if src:
        head, _, rest = text.partition("·")
        return f'<div id="{p}-tag" class="ao-tag src"><i></i><span><b>{esc(head.strip())}</b> · {esc(rest.strip())}</span></div>'
    return f'<div id="{p}-tag" class="ao-tag"><i></i>{esc(text)}</div>'


def lt_html(p, name, role):
    return (f'<div id="{p}-lt" class="ao-lt"><div class="bar"></div><div class="nm">{esc(name)}</div>'
            f'<div class="rl">{esc(role)}</div></div>')


def dust_html(p, n, box, seed, size=(2, 6), color="rgba(240,238,230,.85)"):
    r = random.Random(seed)
    x0, y0, x1, y1 = box
    out = []
    for i in range(n):
        s = r.uniform(*size)
        out.append(f'<span id="{p}-d{i}" style="position:absolute;left:{r.uniform(x0, x1):.0f}px;top:{r.uniform(y0, y1):.0f}px;'
                   f'width:{s:.1f}px;height:{s:.1f}px;border-radius:50%;background:{color};opacity:0"></span>')
    return "".join(out)


def smoke_html(p, k, op=0.35, extra=""):
    return (f'<img id="{p}-smk{k}" src="assets/tex/smoke{k % 3}.png" style="position:absolute;left:-200px;top:-100px;width:2320px;'
            f'height:1280px;opacity:{op};mix-blend-mode:screen;{extra}" alt="">')


# ------------------------------------------------------------------ SVG pieces (own drawings, not photos)
def svg_building(p, dim=False):
    win = []
    for row, y in enumerate((520, 680)):
        for i in range(9):
            x = 560 + i * 96
            if row == 1 and 4 <= i <= 4:
                continue
            lit = (i * 3 + row) % 5 == 0
            win.append(f'<rect x="{x}" y="{y}" width="52" height="86" fill="{"#8d9aa3" if lit else "#1b232b"}"/>'
                       f'<g stroke="#2a333c" stroke-width="3">' + "".join(f'<line x1="{x + k * 13}" y1="{y}" x2="{x + k * 13}" y2="{y + 86}"/>' for k in (1, 2, 3)) + '</g>')
    fill = "#283039" if not dim else "#1f262e"
    return f'''<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
<defs><clipPath id="{p}-bc"><rect x="520" y="440" width="900" height="470"/><rect x="505" y="425" width="930" height="26"/></clipPath>
<linearGradient id="{p}-bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b4652"/><stop offset=".55" stop-color="{fill}"/><stop offset="1" stop-color="#1a2028"/></linearGradient></defs>
<g style="filter:drop-shadow(0 0 2px rgba(236,232,220,.55)) drop-shadow(14px 18px 22px rgba(0,0,0,.45))">
<rect x="520" y="440" width="900" height="470" fill="url(#{p}-bg)"/><rect x="505" y="425" width="930" height="26" fill="#1c232b"/>
{"".join(win)}
<rect x="928" y="760" width="96" height="150" fill="#0d1216"/><rect x="900" y="738" width="152" height="18" fill="#141a20"/>
<rect x="940" y="700" width="72" height="26" fill="#55616b"/>
<image href="assets/tex/paper_grey.jpg" x="500" y="420" width="960" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#{p}-bc)" opacity=".28" style="mix-blend-mode:multiply"/>
</g></svg>'''


def svg_tree_fence(p):
    r = random.Random(7)
    blobs = "".join(f'<circle cx="{r.uniform(60, 470):.0f}" cy="{r.uniform(220, 520):.0f}" r="{r.uniform(60, 130):.0f}"/>' for _ in range(22))
    posts = "".join(f'<rect x="{x}" y="860" width="9" height="230"/><path d="M{x - 6},860 L{x + 4.5},836 L{x + 15},860Z"/>' for x in range(0, 1930, 38))
    return f'''<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
<g fill="#10161b" style="filter:drop-shadow(0 0 2px rgba(236,232,220,.4))">{blobs}<path d="M250,500 L230,1000 L290,1000 L270,500Z"/></g>
<g fill="#0b0f12"><rect x="0" y="900" width="1920" height="14"/><rect x="0" y="1010" width="1920" height="12"/>{posts}
<rect x="1600" y="300" width="14" height="800"/><rect x="1540" y="330" width="140" height="8"/></g>
<path d="M1607,334 C1800,380 1900,360 1960,350 M1607,334 C1400,400 1250,380 1100,360" stroke="#0b0f12" stroke-width="3" fill="none"/>
</svg>'''


def svg_man_back(p, folder=True):
    f = '<rect x="78" y="-330" width="74" height="100" fill="#e9e4d6" transform="rotate(8 110 -280)"/>' if folder else ""
    return f'''<g fill="#0e1317"><ellipse cx="0" cy="-468" rx="36" ry="44"/><rect x="-22" y="-432" width="44" height="30"/>
<path d="M-98,-404 Q0,-432 98,-404 L108,-196 L-108,-196Z"/><path d="M-96,-400 L-128,-222 L-102,-216 L-74,-380Z"/>
<path d="M96,-400 L126,-250 L100,-244 L76,-380Z"/><path d="M-84,-200 L-8,-200 L-22,0 L-66,0Z"/><path d="M8,-200 L84,-200 L64,0 L20,0Z"/></g>{f}'''


def svg_guard(p):
    return f'''<g fill="#0c1115">
<path d="M-58,-536 L58,-536 L48,-490 L-48,-490Z"/><path d="M-50,-494 L50,-494 L40,-476 L-40,-476Z"/>
<ellipse cx="0" cy="-450" rx="38" ry="42"/><rect x="-24" y="-418" width="48" height="26"/>
<path d="M-110,-396 Q0,-424 110,-396 L118,-190 L-118,-190Z"/><path d="M-110,-392 L-140,-210 L-112,-204 L-84,-372Z"/>
<path d="M-90,-200 L-10,-200 L-26,0 L-72,0Z"/><path d="M10,-200 L90,-200 L72,0 L26,0Z"/>
<rect x="-118" y="-230" width="236" height="22" fill="#1d252c"/>
<g id="{p}-arm"><path d="M100,-392 L210,-470 L228,-446 L118,-360Z"/><path d="M206,-500 L246,-512 L262,-452 L222,-440Z"/></g></g>'''


def svg_judge(p):
    return f'''<g fill="#0d1216"><ellipse cx="0" cy="-470" rx="37" ry="44"/><rect x="-22" y="-434" width="44" height="30"/>
<path d="M-100,-404 Q0,-432 100,-404 L110,-196 L-110,-196Z"/><path d="M-98,-400 L-130,-222 L-104,-216 L-76,-380Z"/>
<path d="M-84,-200 L-8,-200 L-22,0 L-66,0Z"/><path d="M8,-200 L84,-200 L64,0 L20,0Z"/>
<g id="{p}-parm"><path d="M90,-398 L190,-500 L212,-480 L112,-372Z"/></g></g>
<g id="{p}-paper"><rect x="168" y="-640" width="150" height="196" fill="#f1ede2" transform="rotate(-8 240 -540)"/>
<g transform="rotate(-8 240 -540)" fill="#9c9a93"><rect x="184" y="-616" width="110" height="8"/><rect x="184" y="-596" width="96" height="8"/><rect x="184" y="-576" width="104" height="8"/><rect x="184" y="-556" width="70" height="8"/></g></g>'''


def svg_person_icon(x, y, s=1, color="#f1f3f2"):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{color}"><circle cx="0" cy="-130" r="44"/>'
            f'<path d="M-80,0 Q-80,-80 0,-80 Q80,-80 80,0Z"/></g>')


def map_svg(p, hi=(), extra=""):
    paths = []
    for name, d in MAP["countries"].items():
        if name in ("Southern Patagonian Ice Field",):
            continue
        cls = "pg" if name == "Paraguay" else ("hi" if name in hi else "ld")
        cid = f'{p}-c-{name.split()[0].lower()}'
        paths.append(f'<path id="{cid}" class="{cls}" d="{d}"/>')
    riv = "".join(f'<path d="{d}"/>' for d in MAP["rivers"])
    grat = []
    for lon in range(-85, -25, 5):
        x = (lon + 86.0) * 72 * math.cos(math.radians(25))
        grat.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{MAP["h"]}"/>')
    for lat in range(5, -60, -5):
        y = (8.0 - lat) * 72
        grat.append(f'<line x1="0" y1="{y:.0f}" x2="{MAP["w"]}" y2="{y:.0f}"/>')
    labels = "".join(
        f'<text x="{x:.0f}" y="{y:.0f}" class="lb" id="{p}-lb-{n.lower()}">{n}</text>' for n, (x, y) in MAP["labels"].items())
    return f'''<svg viewBox="0 0 {MAP["w"]} {MAP["h"]}" width="{MAP["w"]}" height="{MAP["h"]}" style="position:absolute;left:0;top:0;overflow:visible">
<defs><pattern id="{p}-pp" patternUnits="userSpaceOnUse" width="2400" height="1600"><image href="assets/tex/paper_cream.jpg" width="2400" height="1600"/></pattern></defs>
<g stroke="rgba(60,72,80,.22)" stroke-width="2">{"".join(grat)}</g>
<g style="filter:drop-shadow(0 0 10px rgba(40,60,70,.35))">{"".join(paths)}</g>
<g fill="none" stroke="#5f8796" stroke-width="2.4" opacity=".75">{riv}</g>
<g>{labels}</g>{extra}</svg>'''


MAP_CSS = f"""
.ld{{fill:url(#PFX-pp);stroke:#3a3a36;stroke-width:2.2;stroke-dasharray:9 5}}
.hi{{fill:url(#PFX-pp);stroke:#3a3a36;stroke-width:2.2;stroke-dasharray:9 5}}
.pg{{fill:{ACC};fill-opacity:.55;stroke:#0f6f67;stroke-width:4}}
.lb{{font:700 54px "Courier Prime",monospace;letter-spacing:.3em;fill:#3b3d3a;text-anchor:middle;opacity:.8}}
"""


def map_pt(name):
    return MAP["places"][name]


def cam_center(px, py, s):
    """x,y (transform-origin 0 0) that put map point (px,py) at screen centre at scale s."""
    return round(960 - px * s, 1), round(540 - py * s, 1)


# ------------------------------------------------------------------ scenes
SC = {}


def scene(n):
    def deco(f):
        SC[n] = f
        return f
    return deco


def S(p, html="", css="", js="", bg=None):
    return {"html": html, "css": css, "js": js, "bg": bg}


DATE_CSS = f"""
.dc-line{{position:absolute;left:0;white-space:pre;font-family:"Courier Prime",monospace}}
.dc-d{{color:{ACC};font-size:128px;font-weight:700;letter-spacing:.02em}}
.dc-p{{color:#eef0ee;font-size:60px;font-weight:400;letter-spacing:.24em}}
.dc-cur{{display:inline-block;width:.55em;height:.9em;background:#eef0ee;vertical-align:-.08em;margin-left:.06em}}
"""


def date_card(p, d, part, bg="#000", line1="22 · XII · 1992", line2="LAMBARÉ, PARAGUAY"):
    w1 = len(line1) * 0.6 * 128
    x1 = (1920 - w1) / 2
    l1, n1 = typed(p, "a", line1)
    l2, n2 = typed(p, "b", line2)
    js = ""
    if part == 1:
        js += f"type('a', {n1}, 0.30, {1.75 / n1:.4f});"
        cur_line = "a"
        js += f"blink('cur', 0, {d}, 0.26); shot('cam', 0, {d}, [1,0,0], [1.03,0,0], 'none');"
        l2html = ""
    else:
        js += f"tl.set(q('a'+0), {{}}, 0); for (let i = 0; i < {n1}; i++) tl.set(q('a' + i), {{ display: 'inline' }}, 0);"
        js += f"type('b', {n2}, 0.05, {0.85 / n2:.4f}); blink('cur', 0, {d}, 0.26); shot('cam', 0, {d}, [1.03,0,0], [1.09,0,-6], 'none');"
        cur_line = "b"
        l2html = l2
    cur = f'<span id="{p}-cur" class="dc-cur"></span>'
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<div class="dc-line dc-d" style="left:{x1:.0f}px;top:400px">{l1}{cur if cur_line == "a" else ""}</div>
<div class="dc-line dc-p" style="left:{x1 + 8:.0f}px;top:570px">{l2html}{cur if cur_line == "b" else ""}</div></div>'''
    return S(p, html, DATE_CSS, js, bg)


@scene(1)
def s01(p, d):
    return date_card(p, d, 1)


@scene(2)
def s02(p, d):
    return date_card(p, d, 2)


@scene(3)
def s03(p, d):
    ax, ay = map_pt("Asunción")
    x0, y0 = cam_center(MAP["w"] * 0.5, MAP["h"] * 0.52, 0.24)
    x1, y1 = cam_center(ax, ay, 1.15)
    x2, y2 = cam_center(ax, ay, 1.32)
    extra = (f'<circle id="{p}-pt" cx="{ax:.0f}" cy="{ay:.0f}" r="14" fill="{ACC}" stroke="#08302c" stroke-width="4"/>'
             f'<circle id="{p}-ring" cx="{ax:.0f}" cy="{ay:.0f}" r="14" fill="none" stroke="{ACC}" stroke-width="5"/>'
             f'<text x="{ax + 34:.0f}" y="{ay + 14:.0f}" style="font:700 46px \'Courier Prime\';fill:#102a28;letter-spacing:.12em">ASUNCIÓN</text>')
    html = f'''<div class="ao-full" style="background:#3b6782"></div>
<div id="{p}-cam" class="ao-cam" style="transform-origin:0 0" data-layout-allow-overflow>{map_svg(p, extra=extra)}</div>
{tag_html(p, "MAPA · elaboración propia, datos Natural Earth", src=True)}'''
    js = f"""tl.set(q('cam'), {{ x: {x0}, y: {y0}, scale: 0.24 }}, 0);
tl.to(q('cam'), {{ x: {x1}, y: {y1}, scale: 1.15, duration: 0.62, ease: 'expo.inOut' }}, 0.05);
tl.fromTo(q('cam'), {{ filter: 'blur(0px)' }}, {{ filter: 'blur(10px)', duration: 0.3, ease: 'power2.in', yoyo: true, repeat: 1 }}, 0.06);
tl.to(q('cam'), {{ x: {x2}, y: {y2}, scale: 1.32, duration: {d - 0.67:.2f}, ease: 'none' }}, 0.67);
tl.fromTo(q('ring'), {{ attr: {{ r: 14 }}, opacity: 1 }}, {{ attr: {{ r: 90 }}, opacity: 0, duration: 0.7, ease: 'power2.out' }}, 0.62);
tag(0.5);"""
    return S(p, html, MAP_CSS.replace("PFX", p), js)


@scene(4)
def s04(p, d):
    # M2: 1536x1792; centre (746,527), Lambaré label (865,1300), 4 km = 463 px
    cx, cy, lx, ly, r = 746, 527, 865, 1300, 463
    s0, s1 = 0.80, 0.86
    mx, my = (cx + lx) / 2 + 40, (cy + ly) / 2
    x0, y0 = round(960 - mx * s0), round(560 - my * s0)
    x1, y1 = round(960 - mx * s1), round(560 - my * s1)
    html = f'''<div class="ao-full" style="background:url(assets/map/asuncion_lambare_osm_dark.png) 40% 30%/2400px auto;filter:blur(10px) brightness(.9)"></div>
<div id="{p}-cam" class="ao-cam" style="transform-origin:0 0" data-layout-allow-overflow>
<img src="assets/map/asuncion_lambare_osm_dark.png" style="position:absolute;left:0;top:0;width:1536px;height:1792px;filter:brightness(1.35) contrast(1.05);box-shadow:0 0 80px 30px rgba(0,0,0,.6)" alt="">
<svg viewBox="0 0 1536 1792" width="1536" height="1792" style="position:absolute;left:0;top:0;overflow:visible">
<circle id="{p}-area" cx="{cx}" cy="{cy}" r="{r}" fill="{ACC}" fill-opacity=".10"/>
<circle id="{p}-circ" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACC}" stroke-width="7" stroke-dasharray="2910" stroke-dashoffset="2910" transform="rotate(-90 {cx} {cy})"/>
<line id="{p}-rad" x1="{cx}" y1="{cy}" x2="{lx}" y2="{ly - 40}" stroke="{ACC}" stroke-width="5" stroke-dasharray="12 10"/>
<circle cx="{cx}" cy="{cy}" r="16" fill="{ACC}" stroke="#062421" stroke-width="5"/>
<rect id="{p}-lamb" x="{lx - 120}" y="{ly - 52}" width="240" height="84" fill="none" stroke="{ACC}" stroke-width="6"/>
</svg></div>
<div id="{p}-lab1" style="position:absolute;left:930px;top:180px;font:700 40px 'Courier Prime';letter-spacing:.14em;color:#f3f5f4;background:rgba(7,11,14,.7);padding:8px 16px">CENTRO DE ASUNCIÓN</div>
<div id="{p}-lab2" style="position:absolute;left:1010px;top:500px;font:700 64px 'Courier Prime';color:{ACC};background:rgba(7,11,14,.72);padding:6px 18px">a 4 km del centro</div>
<div id="{p}-lab3" style="position:absolute;left:520px;top:800px;font:800 92px 'Barlow Condensed';letter-spacing:.06em;color:#fff;text-shadow:0 4px 20px #000">LAMBARÉ</div>
{tag_html(p, "MAPA · © OpenStreetMap contributors", src=True)}
<div class="ao-osm" data-layout-ignore>© OpenStreetMap contributors</div>'''
    js = f"""shot('cam', 0, {d}, [{s0},{x0},{y0}], [{s1},{x1},{y1}], 'none');
tl.fromTo(q('circ'), {{ attr: {{ 'stroke-dashoffset': 2910 }} }}, {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.8, ease: 'power2.inOut' }}, 0.05);
tl.fromTo(q('area'), {{ attr: {{ r: 0 }} }}, {{ attr: {{ r: {r} }}, duration: 0.8, ease: 'power2.inOut' }}, 0.05);
tl.fromTo(q('rad'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.55);
tl.fromTo(q('lab1'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.1);
tl.fromTo(q('lab2'), {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: 'expo.out' }}, 0.6);
tl.fromTo(q('lab3'), {{ opacity: 0, filter: 'blur(8px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.25 }}, 0.8);
tl.fromTo(q('lamb'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, 0.8);
tag(0.1);"""
    return S(p, html, "", js, "#0d1317")


@scene(5)
def s05(p, d):
    cells = []
    for i, day in enumerate(range(19, 28)):
        x = 150 + i * 182
        hl = day == 22
        nav = day == 25
        cells.append(f'<div id="{p}-cell{day}" style="position:absolute;left:{x}px;top:380px;width:166px;height:220px;background:#f3eee2;'
                     f'box-shadow:0 10px 24px rgba(0,0,0,.35);text-align:center;border-top:34px solid {"#1d2a33" if not hl else ACC}">'
                     f'<div style="font:400 120px/1.25 Anton;color:{"#232628" if not nav else "#0d6e66"}">{day}</div>'
                     f'<div style="font:700 22px Courier Prime;letter-spacing:.2em;color:#4c4c48">{"HOY" if hl else ("NAVIDAD" if nav else "DIC")}</div></div>')
    a = f'''<div id="{p}-A" class="ao-full ao-paper">
<div style="position:absolute;left:150px;top:250px;font:700 54px 'Courier Prime';letter-spacing:.3em;color:#2b2d2c">DICIEMBRE · 1992</div>
<div id="{p}-strip" style="position:absolute;left:0;top:0;width:1920px;height:1080px">{"".join(cells)}</div>
<svg width="1920" height="1080" style="position:absolute;left:0;top:0"><path id="{p}-brk" d="M{150 + 3 * 182 + 83},650 L{150 + 3 * 182 + 83},700 L{150 + 6 * 182 + 83},700 L{150 + 6 * 182 + 83},650" fill="none" stroke="{ACC}" stroke-width="10" stroke-dasharray="700" stroke-dashoffset="700"/></svg>
</div>'''
    b = f'''<div id="{p}-B" class="ao-full ao-desk" style="opacity:0">
<div style="position:absolute;left:0;width:1920px;top:250px;text-align:center"><span class="ao-unit" style="font-size:150px">FALTAN </span><span id="{p}-n" class="ao-num" style="font-size:420px">3</span><span class="ao-unit" style="font-size:150px"> DÍAS</span></div>
<div style="position:absolute;left:0;width:1920px;top:800px;text-align:center;font:700 40px 'Courier Prime';letter-spacing:.3em;color:#cfd6d4">22 DIC → 25 DIC · NAVIDAD</div></div>'''
    js = f"""tl.fromTo(q('strip'), {{ x: 120 }}, {{ x: -60, duration: 0.9, ease: 'power2.out' }}, 0);
tl.to(q('brk'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.5, ease: 'power2.inOut' }}, 0.3);
tl.set(q('A'), {{ opacity: 0 }}, 0.9); tl.set(q('B'), {{ opacity: 1 }}, 0.9);
tl.set(q('n'), {{ textContent: '5' }}, 0.9); tl.set(q('n'), {{ textContent: '4' }}, 1.0); tl.set(q('n'), {{ textContent: '3' }}, 1.1);
tl.fromTo(q('n'), {{ scale: 1.25 }}, {{ scale: 1, duration: 0.35, ease: 'expo.out' }}, 1.1);
shot('B', 0.9, {d}, [1.0,0,0], [1.06,0,0], 'none'); /*cut:0.9*/"""
    return S(p, a + b, "", js)


@scene(6)
def s06(p, d):
    page = f'''<div id="{p}-cal" style="position:absolute;left:560px;top:150px;width:800px;height:820px;background:url(assets/tex/paper_cream.jpg) center/cover;
box-shadow:0 40px 80px rgba(0,0,0,.5);transform:rotate(-3deg)">
<div style="height:110px;background:#26343d;display:flex;align-items:center;justify-content:center;font:700 56px 'Courier Prime';letter-spacing:.3em;color:#e9ece9">DICIEMBRE</div>
<div style="text-align:center;font:400 380px/1.1 Anton;color:#20262a;margin-top:20px">22</div>
<div style="text-align:center;font:700 52px 'Courier Prime';letter-spacing:.32em;color:#2d3236">MARTES · 1992</div>
<div style="position:absolute;left:-40px;right:-40px;top:-18px;height:30px;display:flex;justify-content:space-around">{"".join('<span style="width:22px;height:46px;border-radius:11px;background:#9aa3a8;box-shadow:inset 0 -6px 8px rgba(0,0,0,.35)"></span>' for _ in range(8))}</div>
</div>'''
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
<div class="ao-full" style="background:radial-gradient(ellipse at 20% 10%,rgba(255,250,235,.55),rgba(0,0,0,0) 60%)"></div>
{page}
<div id="{p}-rays" style="position:absolute;left:-600px;top:-500px;width:3000px;height:2200px;mix-blend-mode:screen;opacity:.75;
background:repeating-linear-gradient(115deg,rgba(255,252,240,0) 0px,rgba(255,252,240,0) 90px,rgba(255,252,240,.30) 150px,rgba(255,252,240,0) 230px);filter:blur(14px)"></div>
{smoke_html(p, 0, 0.22)}{smoke_html(p, 1, 0.18)}
</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""shot('cam', 0, 0.9, [1.0,0,0], [1.05,-10,0], 'none'); shot('cam', 0.9, {d}, [1.75,-40,-260,-2], [1.85,-60,-280,-2], 'none');
tl.fromTo(q('rays'), {{ x: -500 }}, {{ x: 300, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('smk0'), {{ x: 0, y: 0 }}, {{ x: -120, y: -40, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('smk1'), {{ x: -60 }}, {{ x: 60, duration: {d}, ease: 'none' }}, 0); tag(0.05);"""
    return S(p, html, "", js)


def portrait(p, d, crop, label, name=None, role=None, cut=None):
    """Sepia print collage: blurred enlargement behind, print with border in front."""
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<img src="assets/img/stroessner_sepia.jpg" style="position:absolute;left:-200px;top:-700px;width:2320px;height:3490px;object-fit:cover;filter:blur(26px) brightness(.55)" alt="">
<div id="{p}-print" style="position:absolute;left:{crop[0]}px;top:{crop[1]}px;width:{crop[2]}px;height:{crop[3]}px;background:#efe8d8;padding:22px;box-shadow:0 40px 90px rgba(0,0,0,.6);transform:rotate({crop[4]}deg)">
<div style="width:100%;height:100%;background:url(assets/img/stroessner_sepia.jpg) {crop[5]} / {crop[6]} no-repeat"></div></div>
</div>{tag_html(p, label, src=True)}'''
    if name:
        html += lt_html(p, name, role)
    return html


@scene(7)
def s07(p, d):
    html = portrait(p, d, (640, 40, 640, 960, -2, "50% 10%", "cover"), "IMAGEN REAL · Retrato oficial, 1954",
                    "Alfredo Stroessner", "gobernó Paraguay 1954–1989")
    js = f"""shot('cam', 0, 0.8, [1.0,0,0], [1.04,0,0], 'none'); shot('cam', 0.8, {d}, [1.9,40,520], [1.98,40,540], 'none');
lt(0.15); tag(0.05);"""
    return S(p, html, "", js)


TL_CSS = f"""
.tl-axis{{position:absolute;height:8px;background:#2a2d2c;transform-origin:0 50%}}
.tl-fill{{position:absolute;height:8px;background:{ACC};transform-origin:0 50%}}
.tl-dot{{position:absolute;width:44px;height:44px;border-radius:50%;background:{ACC};border:7px solid #1b1e1d;margin:-18px 0 0 -22px}}
.tl-lab{{position:absolute;font:700 46px 'Courier Prime';letter-spacing:.12em;color:#222524;white-space:nowrap}}
"""


@scene(8)
def s08(p, d):
    torn = "polygon(" + ",".join(f"{x}% {y}%" for x, y in [(0, 0), (100, 0), (100, 100), (0, 100)]) + ")"
    html = f'''<div id="{p}-cam" class="ao-cam ao-paper" data-layout-allow-overflow>
<div id="{p}-axis" class="tl-axis" style="left:300px;top:560px;width:1320px"></div>
<div id="{p}-fill" class="tl-fill" style="left:300px;top:560px;width:1320px"></div>
<div id="{p}-d1" class="tl-dot" style="left:300px;top:564px"></div><div id="{p}-d2" class="tl-dot" style="left:1620px;top:564px"></div>
<div id="{p}-l1" class="tl-lab" style="left:170px;top:620px">3 FEB 1989</div>
<div style="position:absolute;left:170px;top:680px;font:400 30px 'Work Sans';color:#3a3d3c">cae la dictadura</div>
<div id="{p}-l2" class="tl-lab" style="left:1470px;top:620px">22 DIC 1992</div>
<div id="{p}-cnt" style="position:absolute;left:0;width:1920px;top:250px;text-align:center"><span class="ao-unit" style="font-size:120px;color:#1f2322">CASI </span><span id="{p}-n" class="ao-num" style="font-size:230px">0</span><span class="ao-unit" style="font-size:120px;color:#1f2322"> AÑOS</span></div>
</div>
<div id="{p}-rip" class="ao-full" style="clip-path:{torn}" data-layout-allow-overflow>{portrait(p + "x", d, (640, 40, 640, 960, -2, "50% 10%", "cover"), "IMAGEN REAL · Retrato oficial, 1954")}</div>'''
    html = html.replace(f'id="{p}x-tag"', f'id="{p}-tagx" style="display:none"')
    js = f"""tl.fromTo(q('rip'), {{ x: 0, rotation: 0 }}, {{ x: -2100, rotation: -6, duration: 0.45, ease: 'power3.in' }}, 0.1);
tl.fromTo(q('axis'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: 'power2.out' }}, 0.4);
tl.fromTo(q('fill'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.0, ease: 'power1.inOut' }}, 0.7);
count('n', 0, 4, 0.7, 1.0);
shot('cam', 0, 1.2, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.2, {d}, [1.22,0,70,-1.5], [1.25,0,72,-1.5], 'none');"""
    return S(p, html, TL_CSS, js)


def exterior(p, d, figure="", label=None, name=None, role=None, dim=False, tagtxt="RECREACIÓN", extra=""):
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<div id="{p}-sky" class="ao-full" style="background:url(assets/tex/sky_morning.jpg) center/cover{";filter:brightness(.72) saturate(.8)" if dim else ""}"></div>
<div class="ao-full" style="background:radial-gradient(circle at 14% 12%,rgba(255,253,244,.95) 0,rgba(255,250,235,.35) 12%,rgba(255,255,255,0) 40%)"></div>
<div id="{p}-bld" class="ao-full">{svg_building(p, dim)}</div>
<svg id="{p}-fig" viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0;overflow:visible">{figure}</svg>
{smoke_html(p, 2, 0.28)}
<div id="{p}-fg" class="ao-full">{svg_tree_fence(p)}</div>{extra}
</div>{tag_html(p, tagtxt)}'''
    if name:
        html += lt_html(p, name, role)
    return html


@scene(9)
def s09(p, d):
    html = exterior(p, d, name="Departamento de Producciones", role="Policía · Lambaré")
    js = f"""shot('cam', 0, 0.85, [1.0,0,0], [1.04,-10,0], 'none'); shot('cam', 0.85, {d}, [1.7,-60,-210], [1.76,-70,-220], 'none');
tl.fromTo(q('fg'), {{ x: 0 }}, {{ x: -70, duration: {d}, ease: 'none' }}, 0); tl.fromTo(q('sky'), {{ x: 0 }}, {{ x: 12, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('smk2'), {{ x: 0 }}, {{ x: -90, duration: {d}, ease: 'none' }}, 0); lt(0.15); tag(0.05);"""
    return S(p, html, "", js)


@scene(10)
def s10(p, d):
    fig = f'<g id="{p}-man" transform="translate(860,1080) scale(1.15)">{svg_man_back(p)}</g>'
    html = exterior(p, d, figure=fig)
    js = f"""shot('cam', 0, 1.1, [1.25,-40,-80], [1.3,-50,-90], 'none'); shot('cam', 1.1, {d}, [2.3,-50,-420], [2.4,-60,-440], 'none');
tl.fromTo(q('man'), {{ attr: {{ transform: 'translate(760,1120) scale(1.25)' }} }}, {{ attr: {{ transform: 'translate(975,915) scale(.42)' }}, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('fg'), {{ x: 0 }}, {{ x: -60, duration: {d}, ease: 'none' }}, 0); tag(0.05);"""
    return S(p, html, "", js)


def doc_lines(n, widths=None, gap=26):
    r = random.Random(n * 13)
    return "".join(f'<div class="ao-blurline" style="width:{w if widths else r.randint(55, 100)}%;margin-bottom:{gap}px"></div>'
                   for w in (widths or range(n)))


def warrant(p, case_line=True, typed_case=False):
    case_html = (f'<div style="font:700 58px \'Courier Prime\';color:#1e2121;letter-spacing:.02em;margin:34px 0 8px">'
                 f'MARTÍN ALMADA s/ HÁBEAS DATA</div>'
                 f'<div id="{p}-ul" style="height:9px;background:{ACC};width:1010px;transform-origin:0 50%"></div>') if case_line else ""
    return f'''<div id="{p}-doc" style="position:absolute;left:330px;top:70px;width:1260px;height:1500px;background:url(assets/tex/paper_cream.jpg) center/cover;
box-shadow:0 40px 90px rgba(0,0,0,.6);padding:90px 110px;transform:rotate(1.2deg)">
<div class="ao-blurline" style="width:46%;height:26px;margin:0 auto 50px"></div>{doc_lines(5)}{case_html}<div style="height:40px"></div>{doc_lines(9)}</div>'''


@scene(11)
def s11(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{warrant(p)}
<div class="ao-full" style="background:linear-gradient(180deg,rgba(0,0,0,0) 60%,rgba(0,0,0,.45))"></div></div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""shot('cam', 0, 1.1, [0.78,0,60,-2], [0.82,0,50,-2], 'none'); shot('cam', 1.1, {d}, [1.9,40,90,0], [2.0,10,95,0], 'none');
tl.fromTo(q('ul'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: 'power2.inOut' }}, 1.25); tag(0.05);"""
    return S(p, html, "", js)


def index_card(p, inner, x=460, y=250, w=1000, h=600, rot=-2, cid="card"):
    return f'''<div id="{p}-{cid}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:url(assets/tex/paper_grey.jpg) center/cover;
box-shadow:0 30px 70px rgba(0,0,0,.55);transform:rotate({rot}deg);padding:60px 70px;
background-image:url(assets/tex/paper_grey.jpg)">
<div style="position:absolute;left:0;right:0;top:118px;height:3px;background:#6d8796;opacity:.7"></div>
{"".join(f'<div style="position:absolute;left:0;right:0;top:{170 + k * 64}px;height:2px;background:#8aa0ab;opacity:.45"></div>' for k in range(int((h - 190) / 64)))}
{inner}</div>'''


@scene(12)
def s12(p, d):
    nm, n = typed(p, "t", "JOSÉ AGUSTÍN FERNÁNDEZ")
    inner = f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f">NOMBRE</div><div style="font:700 62px \'Courier Prime\';color:#1d2222;margin-top:40px;white-space:nowrap">{nm}</div>'
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{index_card(p, inner)}</div>{lt_html(p, "José Agustín Fernández", "juez en lo criminal (1992)")}'''
    js = f"""type('t', {n}, 0.1, 0.035); shot('cam', 0, 1.05, [1.0,0,0], [1.04,0,0], 'none'); shot('cam', 1.05, {d}, [1.65,180,180,-3], [1.7,170,175,-3], 'none'); lt(0.25);"""
    return S(p, html, "", js)


@scene(13)
def s13(p, d):
    inner = (f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f">NOMBRE</div><div style="font:700 62px \'Courier Prime\';color:#1d2222;margin-top:40px;white-space:nowrap">JOSÉ AGUSTÍN FERNÁNDEZ</div>'
             f'<div id="{p}-st" class="ao-stamp" style="position:absolute;left:150px;top:300px;font-size:84px">JUEZ EN LO CRIMINAL</div>')
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow><div id="{p}-sh" class="ao-full">{index_card(p, inner, rot=1.5)}</div></div>'''
    js = f"""shot('cam', 0, 0.9, [1.12,0,20], [1.16,0,20], 'none'); stampIn('st', 0.35, -6); shake('sh', 0.51, 14);
shot('cam', 0.9, {d}, [1.9,-140,-280,4], [1.96,-150,-290,4], 'none');"""
    return S(p, html, "", js)


def case_cover(p, typed_html):
    return f'''<div id="{p}-cov" style="position:absolute;left:260px;top:40px;width:1400px;height:1000px;background:#9fb1b6 url(assets/tex/paper_grey.jpg) center/cover;
background-blend-mode:multiply;box-shadow:0 40px 90px rgba(0,0,0,.6);padding:70px 90px;transform:rotate(-1deg)">
<div class="ao-blurline" style="width:38%;height:24px;margin-bottom:40px;background:#2c3436"></div>
<div style="display:flex;gap:40px">{"".join('<div style="flex:1;height:90px;border:3px solid rgba(40,50,52,.5)"></div>' for _ in range(3))}</div>
<div style="margin-top:60px;border-bottom:4px solid rgba(40,50,52,.6);height:110px;position:relative">
<div style="position:absolute;left:10px;bottom:16px;font:700 70px 'Courier Prime';color:#16191a;white-space:nowrap">{typed_html}</div></div>
<div style="margin-top:60px">{doc_lines(5)}</div></div>'''


@scene(14)
def s14(p, d):
    t, n = typed(p, "t", "MARTÍN ALMADA s/ HÁBEAS DATA")
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{case_cover(p, t + f'<span id="{p}-cur" style="display:inline-block;width:30px;height:62px;background:{ACC};vertical-align:-6px"></span>')}</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""type('t', {n}, 0.1, {1.5 / n:.4f}); blink('cur', 0, {d}, 0.25);
shot('cam', 0, 1.0, [0.95,0,0], [0.98,0,0], 'none'); shot('cam', 1.0, {d}, [1.6,-80,170], [1.62,-260,170], 'none'); tag(0.05);"""
    return S(p, html, "", js)


@scene(15)
def s15(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{case_cover(p, 'MARTÍN ALMADA s/ <span style="position:relative">HÁBEAS DATA<span id="' + p + '-ul" style="position:absolute;left:0;right:0;bottom:-14px;height:12px;background:' + ACC + ';transform-origin:0 50%"></span></span>')}</div>
<div class="ao-full" style="background:radial-gradient(ellipse at 55% 50%,rgba(0,0,0,0) 30%,rgba(0,0,0,.55) 80%)"></div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""shot('cam', 0, 0.9, [2.6,-1040,560,-3], [2.75,-1120,590,-3], 'none'); shot('cam', 0.9, {d}, [3.6,-1650,800,2], [3.7,-1710,820,2], 'none');
tl.fromTo(q('ul'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: 'power2.inOut' }}, 0.25); tag(0.05);"""
    return S(p, html, "", js)


@scene(16)
def s16(p, d):
    words = "derecho a ver los datos que el Estado guarda sobre ti".split()
    spans = " ".join(f'<span id="{p}-w{i}" style="display:inline-block;opacity:0">{w}</span>' for i, w in enumerate(words))
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
<div id="{p}-term" style="position:absolute;left:0;width:1920px;top:330px;text-align:center;font:400 220px/1 Anton;color:{ACC};letter-spacing:.02em">HÁBEAS DATA</div>
<div id="{p}-def" style="position:absolute;left:260px;width:1400px;top:640px;text-align:center;font:400 64px/1.3 'Work Sans';color:#f1f3f2">{spans}</div>
</div>'''
    js = f"""tl.fromTo(q('term'), {{ opacity: 0, filter: 'blur(10px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.18 }}, 0.0);
shot('cam', 0, 0.95, [1.35,0,120], [1.4,0,125], 'none'); shot('cam', 0.95, {d}, [0.92,0,-30], [0.95,0,-30], 'none');
{"".join(f"tl.fromTo(q('w{i}'), {{ opacity: 0, filter: 'blur(6px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.13 }}, {0.98 + i * 0.07:.3f});" for i in range(len(words)))}"""
    return S(p, html, "", js)


@scene(17)
def s17(p, d):
    if HAVE["almada"]:
        html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<img src="assets/img/martin_almada_2008_g.jpg" class="ao-cover" style="filter:blur(24px) brightness(.5)" alt="">
<div style="position:absolute;left:660px;top:30px;width:600px;height:1020px;background:#efe8d8;padding:20px;box-shadow:0 40px 90px rgba(0,0,0,.6);transform:rotate(1.5deg)">
<div style="width:100%;height:100%;background:url(assets/img/martin_almada_2008_g.jpg) 50% 20%/cover"></div></div></div>
{tag_html(p, "IMAGEN REAL · Foto: 2008, Maria Stella de Almada (CC BY-SA 4.0)", src=True)}{lt_html(p, "Martín Almada", "educador")}'''
        js = f"shot('cam', 0, 1.0, [1.0,0,0], [1.04,0,0], 'none'); shot('cam', 1.0, {d}, [1.8,0,560], [1.86,0,575], 'none'); lt(0.15); tag(0.05);"
        return S(p, html, "", js)
    # fallback (A2 not downloaded): typed card + big name, no face
    t, n = typed(p, "t", "MARTÍN ALMADA")
    inner = (f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f">SOLICITANTE</div>'
             f'<div style="font:700 92px \'Courier Prime\';color:#1d2222;margin-top:34px;white-space:nowrap">{t}</div>'
             f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f;margin-top:54px">PROFESIÓN</div>'
             f'<div style="font:700 58px \'Courier Prime\';color:#1d2222;margin-top:20px">EDUCADOR</div>')
    html = f'''<div id="{p}-cam" class="ao-cam ao-paper" data-layout-allow-overflow>
<div style="position:absolute;left:-40px;top:120px;font:400 330px/0.9 Anton;color:rgba(40,46,46,.10);white-space:nowrap">ALMADA ALMADA</div>
{index_card(p, inner, x=420, y=200, w=1080, h=640, rot=2)}</div>{lt_html(p, "Martín Almada", "educador")}'''
    js = f"""type('t', {n}, 0.05, 0.03); shot('cam', 0, 1.0, [1.0,0,0], [1.04,0,0], 'none'); shot('cam', 1.0, {d}, [1.55,120,170,-2], [1.6,110,165,-2], 'none'); lt(0.2);"""
    return S(p, html, "", js)


def doc_page(p, img, w, h, x, y, rot=0, extra=""):
    return f'''<div id="{p}-pg" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-shadow:0 40px 90px rgba(0,0,0,.6);transform:rotate({rot}deg)">
<img src="assets/img/{img}" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px" alt="">{extra}</div>'''


@scene(18)
def s18(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{doc_page(p, "const1992_p01_portada.jpg", 1215, 1733, 352, 40, -1.5)}</div>
{tag_html(p, "DOCUMENTO REAL · Constitución Nacional 1992, original firmado (BACN)", src=True)}'''
    js = f"shot('cam', 0, {d}, [0.6,0,140,0], [0.82,0,220,0], 'power1.out'); tag(0.05);"
    return S(p, html, "", js)


@scene(19)
def s19(p, d):
    # D2 1227x1588; art.135 heading y~526, body lines y~590..712 (x 380..1050)
    hl = f'''<div id="{p}-box" style="position:absolute;left:180px;top:546px;width:440px;height:46px;border:6px solid {ACC}"></div>
<div id="{p}-hl1" style="position:absolute;left:408px;top:611px;width:636px;height:34px;background:{ACC};opacity:.42;mix-blend-mode:multiply;transform-origin:0 50%"></div>
<div id="{p}-hl2" style="position:absolute;left:370px;top:640px;width:674px;height:32px;background:{ACC};opacity:.42;mix-blend-mode:multiply;transform-origin:0 50%"></div>'''
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" style="transform-origin:0 0" data-layout-allow-overflow>{doc_page(p, "const1992_p42_art135_habeas_data.jpg", 1227, 1588, 0, 0, 0, hl)}</div>
{tag_html(p, "DOCUMENTO REAL · Constitución 1992, art. 135 (BACN)", src=True)}'''
    js = f"""shot('cam', 0, 0.8, [1.05,315,-90], [1.1,290,-120], 'none'); shot('cam', 0.8, {d}, [2.15,-545,-836], [2.25,-615,-900], 'none');
tl.fromTo(q('box'), {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: 'expo.out' }}, 0.15);
tl.fromTo(q('hl1'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: 'power1.inOut' }}, 0.9);
tl.fromTo(q('hl2'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: 'power1.inOut' }}, 1.3); tag(0.05);"""
    return S(p, html, "", js)


def drawer_svg(p, x, y, label="POLICÍA", q_mark=True):
    return f'''<g transform="translate({x},{y})"><rect x="0" y="0" width="420" height="520" fill="#1c252c" stroke="#e8ecea" stroke-width="6"/>
{"".join(f'<rect x="30" y="{30 + k * 160}" width="360" height="130" fill="#26323b" stroke="#e8ecea" stroke-width="4"/><rect x="170" y="{80 + k * 160}" width="80" height="16" fill="#e8ecea"/>' for k in range(3))}
<g transform="translate(300,330)"><rect x="-34" y="0" width="68" height="56" fill="{ACC}"/><path d="M-22,0 L-22,-24 A22,22 0 0 1 22,-24 L22,0" fill="none" stroke="{ACC}" stroke-width="10"/></g>
<text x="210" y="600" text-anchor="middle" style="font:700 54px 'Courier Prime';letter-spacing:.2em;fill:#e8ecea">{label}</text></g>'''


@scene(20)
def s20(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
<g id="{p}-per">{svg_person_icon(400, 700, 1.6)}</g>
<path id="{p}-arr" d="M560,560 L1150,560" stroke="{ACC}" stroke-width="16" stroke-dasharray="600" stroke-dashoffset="600"/>
<path id="{p}-head" d="M1150,520 L1210,560 L1150,600Z" fill="{ACC}" opacity="0"/>
<g id="{p}-dr">{drawer_svg(p, 1260, 280)}</g>
<text id="{p}-q" x="1700" y="430" style="font:400 260px Anton;fill:{ACC}" opacity="0">?</text>
<text x="400" y="820" text-anchor="middle" style="font:700 44px 'Courier Prime';letter-spacing:.2em;fill:#e8ecea">ALMADA</text></svg></div>'''
    js = f"""tl.to(q('arr'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.5, ease: 'power2.inOut' }}, 0.1); tl.set(q('head'), {{ opacity: 1 }}, 0.6);
tl.fromTo(q('q'), {{ opacity: 0, scale: 1.4, transformOrigin: '50% 50%' }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: 'expo.out' }}, 1.05);
shot('cam', 0, 1.0, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.0, {d}, [1.4,-714,-56], [1.44,-740,-60], 'none');"""
    return S(p, html, "", js)


def counter_block(p, num_html, unit, sub="", top=300, numsize=300, unitsize=120, color_unit="#f4f2ec"):
    return f'''<div style="position:absolute;left:0;width:1920px;top:{top}px;text-align:center;white-space:nowrap">{num_html}
<span class="ao-unit" style="font-size:{unitsize}px;color:{color_unit}">{unit}</span></div>
{f'<div style="position:absolute;left:0;width:1920px;top:{top + numsize + 40}px;text-align:center;font:700 42px Courier Prime;letter-spacing:.24em;color:#d6dcda">{sub}</div>' if sub else ""}'''


@scene(21)
def s21(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 45%,rgba(46,196,182,.12),rgba(0,0,0,0) 60%)"></div>
{counter_block(p, f'<span id="{p}-n" class="ao-num" style="font-size:330px">0</span> ', "DÍAS", "14 SEP 1992 → 22 DIC 1992", 250, 330, 150)}</div>
{tag_html(p, "FUENTE · Poder Judicial, Archivos del Terror (2008)", src=True)}'''
    js = f"count('n', 0, 99, 0.1, 1.2); shot('cam', 0, 1.0, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.0, {d}, [1.35,0,60], [1.38,0,60], 'none'); tag(0.05);"
    return S(p, html, "", js)


@scene(22)
def s22(p, d):
    months = ["SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    pages = "".join(f'''<div id="{p}-m{i}" style="position:absolute;left:560px;top:120px;width:800px;height:860px;background:url(assets/tex/paper_cream.jpg) center/cover;
box-shadow:0 30px 60px rgba(0,0,0,.5);transform-origin:50% 0;z-index:{10 - i}">
<div style="height:120px;background:#26343d;display:flex;align-items:center;justify-content:center;font:700 58px 'Courier Prime';letter-spacing:.24em;color:#e9ece9">{m}</div>
<div style="text-align:center;font:400 330px/1.3 Anton;color:{ACC if i == 3 else "#22282b"}">{["14", "·", "·", "22"][i]}</div>
<div style="text-align:center;font:700 48px 'Courier Prime';letter-spacing:.3em;color:#2d3236">1992</div></div>''' for i, m in enumerate(months))
    html = f'<div id="{p}-cam" class="ao-cam ao-desk" style="perspective:1600px" data-layout-allow-overflow>{pages}</div>'
    js = "".join(f"tl.to(q('m{i}'), {{ rotationX: -92, duration: 0.3, ease: 'power2.in' }}, {0.35 + i * 0.4:.2f}); tl.set(q('m{i}'), {{ opacity: 0 }}, {0.65 + i * 0.4:.2f});" for i in range(3))
    js += f"shot('cam', 0, {d}, [1.0,0,0], [1.08,0,0], 'none');"
    return S(p, html, "", js)


@scene(23)
def s23(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
<div style="position:absolute;left:380px;top:60px;width:1160px;height:1400px;background:url(assets/tex/paper_cream.jpg) center/cover;box-shadow:0 40px 90px rgba(0,0,0,.6);padding:90px 100px;transform:rotate(-1.2deg)">
<div style="font:700 64px 'Courier Prime';letter-spacing:.16em;color:#1d2121">RESPUESTA OFICIAL</div><div style="height:5px;background:#1d2121;margin:16px 0 50px;width:640px"></div>
{doc_lines(4)}<div id="{p}-key" style="font:700 60px 'Courier Prime';color:#151818;margin:10px 0 36px;white-space:nowrap">los documentos desaparecieron</div>{doc_lines(6)}</div>
</div>
<div style="position:absolute;left:176px;bottom:120px;font:700 italic 36px 'Work Sans';color:#fff;background:rgba(7,11,14,.72);padding:12px 22px;border-left:10px solid {ACC}">según recuerda el juez (ABC Color, 2019)</div>
{tag_html(p, "RECREACIÓN")}'''
    js = f"""shot('cam', 0, 1.2, [0.9,0,90,0], [0.93,0,80,0], 'none'); shot('cam', 1.2, {d}, [1.75,-40,-200,1], [1.8,-120,-205,1], 'none');
tl.fromTo(q('key'), {{ filter: 'blur(6px)' }}, {{ filter: 'blur(0px)', duration: 0.4 }}, 0.3); tag(0.05);"""
    return S(p, html, "", js)


@scene(24)
def s24(p, d):
    icons = "".join(f'<div id="{p}-f{i}" style="position:absolute;left:{1300 + (i % 4) * 70}px;top:{300 + (i // 4) * 90}px;width:60px;height:76px;background:#f3efe4;border:3px solid #2a2d2c;box-shadow:0 6px 10px rgba(0,0,0,.25)"></div>' for i in range(8))
    html = f'''<div id="{p}-cam" class="ao-cam ao-paper" data-layout-allow-overflow>
<div class="tl-axis" style="left:220px;top:620px;width:1480px"></div>
<div class="tl-dot" style="left:420px;top:624px"></div><div id="{p}-ph" class="tl-dot" style="left:1540px;top:624px;background:#fff"></div>
<div class="tl-lab" style="left:1390px;top:680px">22 DIC 1992</div>
<div id="{p}-st" class="ao-stamp" style="position:absolute;left:250px;top:700px;font-size:76px">2–3 FEB 1989 · GOLPE</div>
<div id="{p}-rw" style="position:absolute;left:0;width:1920px;top:150px;text-align:center;font:700 54px 'Courier Prime';letter-spacing:.4em;color:#2a2d2c">◀◀ 1992 → 1989</div>
{icons}</div>'''
    js = f"""tl.fromTo(q('ph'), {{ x: 0 }}, {{ x: -1120, duration: 0.8, ease: 'power3.inOut' }}, 0.1); stampIn('st', 0.95, -3);
{"".join(f"tl.to(q('f{i}'), {{ x: {(i * 137) % 300 - 150}, y: {-200 - (i * 53) % 200}, rotation: {(i * 47) % 90 - 45}, opacity: 0, duration: 0.8, ease: 'power2.out' }}, {1.3 + i * 0.03:.2f});" for i in range(8))}
shot('cam', 0, 1.2, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.2, {d}, [1.45,450,-60,-2], [1.5,440,-70,-2], 'none');"""
    return S(p, html, TL_CSS, js)


def cabinet(p, open_id="drw"):
    return f'''<div style="position:absolute;left:660px;top:120px;width:600px;height:900px;transform-style:preserve-3d;transform:rotateY(-18deg) rotateX(6deg)">
<div style="position:absolute;inset:0;background:linear-gradient(90deg,#55626b,#3b464e);border:4px solid #23292e;box-shadow:0 40px 80px rgba(0,0,0,.6)"></div>
{"".join(f'<div style="position:absolute;left:40px;top:{40 + k * 285}px;width:520px;height:250px;background:linear-gradient(180deg,#5c6a73,#46525a);border:3px solid #2a3238"><div style="position:absolute;left:210px;top:40px;width:100px;height:24px;background:#cfd6d8;border-radius:4px"></div><div style="position:absolute;left:200px;top:90px;width:120px;height:44px;background:#e9e4d6;border:2px solid #2a3238"></div></div>' for k in (0, 2))}
<div id="{p}-{open_id}" style="position:absolute;left:40px;top:325px;width:520px;height:250px;transform-style:preserve-3d">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,#66757e,#4d5a62);border:3px solid #2a3238;transform:translateZ(1px)"><div style="position:absolute;left:210px;top:40px;width:100px;height:24px;background:#cfd6d8;border-radius:4px"></div></div>
<div style="position:absolute;left:0;top:0;width:520px;height:600px;background:linear-gradient(0deg,#2c353b,#1b2227);transform-origin:50% 0;transform:rotateX(90deg) translateY(0)"></div>
</div></div>'''


@scene(25)
def s25(p, d):
    drawers = "".join(f'<g><rect x="680" y="{y}" width="560" height="240" fill="url(#{p}-df)" stroke="#20272c" stroke-width="5"/>'
                      f'<rect x="900" y="{y + 40}" width="120" height="26" rx="5" fill="#cfd6d8"/><rect x="890" y="{y + 90}" width="140" height="50" fill="#e9e4d6" stroke="#2a3238" stroke-width="3"/></g>'
                      for y in (180, 700))
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 18%,rgba(228,236,238,.5),rgba(0,0,0,0) 55%)"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0;overflow:visible">
<defs><linearGradient id="{p}-cf" x1="0" x2="1"><stop offset="0" stop-color="#5e6b74"/><stop offset="1" stop-color="#3a454d"/></linearGradient>
<linearGradient id="{p}-df" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6c7a83"/><stop offset="1" stop-color="#4b5860"/></linearGradient>
<linearGradient id="{p}-in" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1114"/><stop offset="1" stop-color="#2a3339"/></linearGradient></defs>
<rect x="650" y="140" width="620" height="1000" fill="url(#{p}-cf)" stroke="#1a2024" stroke-width="6" style="filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))"/>
{drawers}<rect x="680" y="440" width="560" height="240" fill="#07090b"/>
<polygon id="{p}-inner" points="680,440 1240,440 1240,440 680,440" fill="url(#{p}-in)" stroke="#59666e" stroke-width="4"/>
<g id="{p}-front"><rect x="680" y="440" width="560" height="240" fill="url(#{p}-df)" stroke="#20272c" stroke-width="5"/>
<rect x="900" y="480" width="120" height="26" rx="5" fill="#d9e0e2"/><rect x="890" y="530" width="140" height="50" fill="#e9e4d6" stroke="#2a3238" stroke-width="3"/></g>
</svg>{dust_html(p, 34, (700, 380, 1220, 620), 25)}</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""tl.fromTo(q('front'), {{ attr: {{ transform: 'translate(0,0) scale(1)' }} }}, {{ attr: {{ transform: 'translate(-205.7,65.8) scale(1.214)' }}, duration: 0.8, ease: 'power3.out' }}, 0.1);
tl.fromTo(q('inner'), {{ attr: {{ points: '680,440 1240,440 1240,440 680,440' }} }}, {{ attr: {{ points: '680,440 1240,440 1300,600 620,600' }}, duration: 0.8, ease: 'power3.out' }}, 0.1);
dust(34, 0.5, {d - 0.5:.2f});
shot('cam', 0, 1.15, [1.0,0,0], [1.05,0,0], 'none'); shot('cam', 1.15, {d}, [1.9,0,60,0], [1.96,0,66,0], 'none'); tag(0.05);"""
    return S(p, html, "", js)


@scene(26)
def s26(p, d):
    st = f'<div id="{p}-st" class="ao-stamp" style="position:absolute;left:600px;top:250px;font-size:96px;background:rgba(10,14,16,.55);mix-blend-mode:normal">VERSIÓN POLICIAL</div>'
    html = exterior(p, d, dim=True, extra=st)
    js = f"""shot('cam', 0, 0.8, [1.15,0,-40], [1.2,0,-45], 'none'); shot('cam', 0.8, {d}, [1.45,-40,10], [1.5,-45,0], 'none'); stampIn('st', 0.2, -3); tag(0.05);"""
    return S(p, html, "", js)


@scene(27)
def s27(p, d):
    t, n = typed(p, "t", "NADA QUE BUSCAR")
    html = f'''<div id="{p}-cam" class="ao-cam ao-paper" data-layout-allow-overflow>
<div style="position:absolute;left:{(1920 - 15 * 0.6 * 150) / 2:.0f}px;top:440px;font:700 150px 'Courier Prime';color:#17191a;white-space:nowrap">{t}<span id="{p}-cur" style="display:inline-block;width:80px;height:130px;background:{ACC};vertical-align:-14px"></span></div></div>'''
    js = f"type('t', {n}, 0.05, 0.06); blink('cur', 0, {d}, 0.25); shot('cam', 0, 0.8, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 0.8, {d}, [1.5,-200,0,-2], [1.54,-220,0,-2], 'none');"
    return S(p, html, "", js)


def doorway(p, figure, light=0.9):
    return f'''<div id="{p}-cam" class="ao-cam" style="background:#1a2026" data-layout-allow-overflow>
<div class="ao-full" style="background:url(assets/tex/sky_morning.jpg) center/cover;filter:brightness(.55)"></div>
<div style="position:absolute;left:700px;top:120px;width:520px;height:900px;background:radial-gradient(ellipse at 50% 60%,rgba(255,254,248,{light}),rgba(210,226,232,.7) 55%,rgba(120,140,150,.5));box-shadow:0 0 120px 40px rgba(240,246,248,.35)"></div>
<div style="position:absolute;left:640px;top:80px;width:60px;height:960px;background:#0e1317"></div><div style="position:absolute;left:1220px;top:80px;width:60px;height:960px;background:#0e1317"></div>
<div style="position:absolute;left:640px;top:60px;width:640px;height:70px;background:#0e1317"></div>
<div style="position:absolute;left:0;top:0;width:640px;height:1080px;background:linear-gradient(90deg,#141a20,#252d35)"></div><div style="position:absolute;left:1280px;top:0;width:640px;height:1080px;background:linear-gradient(270deg,#141a20,#252d35)"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0;overflow:visible">{figure}</svg>
{smoke_html(p, 1, 0.25)}</div>{tag_html(p, "RECREACIÓN")}'''


@scene(28)
def s28(p, d):
    html = doorway(p, f'<g transform="translate(960,1040) scale(1.45)">{svg_guard(p)}</g>') + lt_html(p, "Oficial de guardia", "Policía · sin nombre en los registros consultados")
    html = html.replace("sin nombre en los registros consultados", "entrada del depósito")
    js = f"""tl.fromTo(q('arm'), {{ rotation: 40, transformOrigin: '100px -392px', svgOrigin: '100 -392' }}, {{ rotation: 0, svgOrigin: '100 -392', duration: 0.35, ease: 'power3.out' }}, 0.35);
shot('cam', 0, 1.25, [1.0,0,0], [1.04,0,0], 'none'); shot('cam', 1.25, {d}, [1.8,-600,350], [1.85,-620,360], 'none'); lt(0.2); tag(0.05);"""
    return S(p, html, "", js)


@scene(29)
def s29(p, d):
    html = doorway(p, f'<g transform="translate(820,1060) scale(1.5)">{svg_judge(p)}</g><g transform="translate(1250,1080) scale(1.35)">{svg_guard(p + "g")}</g>', 1.0)
    js = f"""tl.fromTo(q('paper'), {{ y: 60 }}, {{ y: 0, duration: 0.4, ease: 'power3.out' }}, 0.1);
shot('cam', 0, 1.25, [1.0,0,0], [1.04,10,0], 'none'); shot('cam', 1.25, {d}, [2.1,-300,820], [2.15,-310,840], 'none'); tag(0.05);"""
    return S(p, html, "", js)


@scene(30)
def s30(p, d):
    cards = [("GOLPE 1989", -560, -6), ("SIN DOCUMENTOS", 0, 3), ("NADA QUE BUSCAR", 560, -2)]
    html = f'<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>' + "".join(
        f'''<div id="{p}-k{i}" style="position:absolute;left:{960 + x - 260}px;top:380px;width:520px;height:320px;background:url(assets/tex/paper_cream.jpg) center/cover;
box-shadow:0 26px 50px rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center;text-align:center;font:400 66px/1.05 Anton;color:#1d2121;padding:20px;transform:rotate({r}deg)">
<span>{t}</span><div style="position:absolute;left:0;right:0;bottom:0;height:16px;background:{ACC}"></div></div>''' for i, (t, x, r) in enumerate(cards)) + "</div>"
    js = "".join(f"tl.fromTo(q('k{i}'), {{ y: {(-1) ** i * 700}, rotation: {(-1) ** i * 20} }}, {{ y: 0, rotation: {cards[i][2]}, duration: 0.4, ease: 'expo.out' }}, {0.05 + i * 0.3:.2f});" for i in range(3))
    js += f"shot('cam', 0, 1.05, [1.15,0,0], [1.12,0,0], 'none'); shot('cam', 1.05, {d}, [0.92,0,0], [0.9,0,0], 'none'); shake('cam', 1.5, 10);"
    return S(p, html, "", js)


@scene(31)
def s31(p, d):
    steps = "".join(f'''<div style="position:absolute;left:-400px;top:0;width:800px;height:110px;transform:translateY({-k * 110}px) translateZ({-k * 160}px);transform-style:preserve-3d">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgb({30 + k * 7},{36 + k * 7},{42 + k * 7}),rgb({20 + k * 5},{24 + k * 5},{28 + k * 5}))"></div>
<div style="position:absolute;left:0;top:0;width:800px;height:160px;background:rgb({48 + k * 9},{54 + k * 9},{60 + k * 9});transform-origin:50% 0;transform:rotateX(90deg)"></div></div>''' for k in range(14))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#06080a;perspective:900px;perspective-origin:50% 30%" data-layout-allow-overflow>
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 8%,rgba(215,230,236,.55),rgba(0,0,0,0) 45%)"></div>
<div id="{p}-st" style="position:absolute;left:960px;top:900px;transform-style:preserve-3d">{steps}</div>
<div style="position:absolute;left:0;top:0;width:520px;height:1080px;background:linear-gradient(90deg,#030405,rgba(3,4,5,.2))"></div>
<div style="position:absolute;right:0;top:0;width:520px;height:1080px;background:linear-gradient(270deg,#030405,rgba(3,4,5,.2))"></div>
{dust_html(p, 26, (500, 100, 1400, 900), 31, (2, 5))}</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""tl.fromTo(q('st'), {{ y: 0, z: 0 }}, {{ y: 380, z: 700, duration: {d}, ease: 'none' }}, 0);
{"".join(f"tl.fromTo(q('st'), {{ rotation: 0 }}, {{ rotation: {0.6 if i % 2 else -0.6}, duration: {d / 4:.2f}, ease: 'sine.inOut' }}, {i * d / 4:.2f});" for i in range(4))}
dust(26, 0, {d}); tag(0.05);"""
    return S(p, html, "", js)


PAD_CROP = (1280, 0, 640, 1080)  # padlock region in the graded 2000x1333 photo, see shots.md A6


@scene(32)
def s32(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<img src="assets/img/padlocks_cool.jpg" style="position:absolute;left:-180px;top:-120px;width:2280px;height:1520px;object-fit:cover;filter:brightness(.62) contrast(1.1)" alt="">
<div class="ao-full" style="background:radial-gradient(circle at 56% 38%,rgba(255,255,255,0) 8%,rgba(0,0,0,.82) 46%)"></div>
<div id="{p}-beam" class="ao-full" style="background:radial-gradient(circle at 56% 38%,rgba(225,240,242,.35),rgba(0,0,0,0) 22%);mix-blend-mode:screen"></div></div>{tag_html(p, "RECREACIÓN")}'''
    js = f"shot('cam', 0, {d}, [1.0,0,0], [1.12,-60,40], 'power1.inOut'); tl.fromTo(q('beam'), {{ x: -160, y: 60 }}, {{ x: 0, y: 0, duration: 0.6, ease: 'power2.out' }}, 0); tag(0.05);"
    return S(p, html, "", js)


@scene(33)
def s33(p, d):
    cutter = f'''<svg id="{p}-cut" viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0;overflow:visible">
<g fill="#0a0d10" stroke="#9aa6ab" stroke-width="3"><path d="M1980,840 L1290,470 L1310,436 L2000,800Z"/><path d="M1980,560 L1300,460 L1308,424 L2000,520Z"/>
<path d="M1290,470 L1210,430 L1236,404 L1310,436Z"/><path d="M1300,460 L1220,418 L1240,396 L1308,424Z"/></g></svg>'''
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<img src="assets/img/padlocks_cool.jpg" style="position:absolute;left:-1600px;top:-520px;width:4560px;height:3040px;filter:brightness(.8) contrast(1.15)" alt="">
<div class="ao-full" style="background:radial-gradient(circle at 50% 45%,rgba(0,0,0,0) 20%,rgba(0,0,0,.7) 70%)"></div>{cutter}</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""{"".join(f"tl.to(q('cam'), {{ x: {((i * 37) % 13) - 6}, y: {((i * 53) % 11) - 5}, rotation: {(((i * 29) % 7) - 3) * 0.15:.2f}, duration: 0.1, ease: 'sine.inOut' }}, {i * 0.1:.2f});" for i in range(int(d / 0.1)))}
tl.fromTo(q('cut'), {{ x: 500 }}, {{ x: 0, duration: 0.7, ease: 'power3.out' }}, 0.2); tag(0.05);"""
    return S(p, html, "", js)


@scene(34)
def s34(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<div id="{p}-bg" class="ao-full" style="overflow:hidden"><img src="assets/img/padlocks_cool.jpg" style="position:absolute;left:-1600px;top:-520px;width:4560px;height:3040px;filter:brightness(.8) contrast(1.15)" alt=""></div>
<div id="{p}-lock" class="ao-full" style="clip-path:polygon(975px 660px,990px 420px,1050px 320px,1160px 310px,1240px 370px,1300px 470px,1460px 550px,1600px 610px,1700px 880px,1180px 1010px)"><div style="position:absolute;left:-1600px;top:-520px;width:4560px;height:3040px;background:url(assets/img/padlocks_cool.jpg) 0 0/100% 100%;filter:brightness(.9) contrast(1.2)"></div></div>
<div class="ao-full" style="background:radial-gradient(circle at 50% 45%,rgba(0,0,0,0) 20%,rgba(0,0,0,.7) 70%)"></div>
<div id="{p}-fl" class="ao-full" style="background:#fff;opacity:0"></div></div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""tl.set(q('fl'), {{ opacity: 1 }}, 0.25); tl.set(q('fl'), {{ opacity: 0.4 }}, 0.25 + 1 / 30); tl.set(q('fl'), {{ opacity: 0 }}, 0.25 + 2 / 30);
tl.set(q('bg'), {{ filter: 'brightness(.55)', x: -120, y: 430 }}, 0.25);
tl.fromTo(q('lock'), {{ y: 0, rotation: 0, filter: 'blur(0px)' }}, {{ y: 1000, rotation: 24, filter: 'blur(6px)', duration: 0.75, ease: 'power2.in' }}, 0.27);
shake('cam', 0.26, 24); shot('cam', 0.5, {d}, [1.1,0,0], [1.16,0,20], 'none'); tag(0.05);"""
    return S(p, html, "", js)


@scene(35)
def s35(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#05070a" data-layout-allow-overflow>
<div id="{p}-slit" style="position:absolute;left:950px;top:0;width:20px;height:1080px;background:linear-gradient(180deg,#e8f1f3,#ffffff 50%,#d7e5e9);box-shadow:0 0 140px 60px rgba(235,245,247,.8)"></div>
<div id="{p}-bloom" class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,#ffffff 0,rgba(236,246,248,.9) 30%,rgba(200,220,226,.4) 60%,rgba(0,0,0,0) 80%);opacity:0"></div>
{smoke_html(p, 0, 0.5)}</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""tl.fromTo(q('slit'), {{ scaleX: 1 }}, {{ scaleX: 70, duration: 0.6, ease: 'power3.in' }}, 0.05);
tl.fromTo(q('bloom'), {{ opacity: 0, scale: .6 }}, {{ opacity: 1, scale: 1.4, duration: 0.6, ease: 'power2.in' }}, 0.2);
tl.fromTo(q('smk0'), {{ x: 0 }}, {{ x: -120, duration: {d}, ease: 'none' }}, 0); tag(0.05);"""
    return S(p, html, "", js)


def paper_pile(p, seed, n=70, area=(0, 200, 1920, 1080), tints=None):
    r = random.Random(seed)
    tints = tints or ["#f0ebdf", "#e6e2d6", "#cfd8d4", "#b9c6c8", "#d9d3c2", "#9fb0b4", "#e9e4d4"]
    out = []
    for i in range(n):
        w, h = r.randint(220, 460), r.randint(150, 330)
        x, y = r.uniform(area[0] - 100, area[2] - 200), r.uniform(area[1], area[3] - 60)
        rot = r.uniform(-28, 28)
        t = r.choice(tints)
        lines = "".join(f'<div style="height:6px;margin:14px 18px 0;background:rgba(60,64,64,.35);width:{r.randint(40, 90)}%"></div>' for _ in range(r.randint(0, 5)))
        out.append(f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w}px;height:{h}px;background:{t} url(assets/tex/paper_cream.jpg) {r.randint(0, 900)}px {r.randint(0, 600)}px;background-blend-mode:multiply;'
                   f'transform:rotate({rot:.1f}deg);box-shadow:0 10px 22px rgba(0,0,0,.45);padding-top:6px">{lines}</div>')
    return "".join(out)


@scene(36)
def s36(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#20282e" data-layout-allow-overflow>
<div id="{p}-l0" class="ao-full" style="filter:brightness(.55) blur(3px)">{paper_pile(p, 36, 60, (0, 100, 1920, 900))}</div>
<div id="{p}-l1" class="ao-full" style="filter:brightness(.8)">{paper_pile(p, 37, 50, (0, 380, 1920, 1080))}</div>
<div id="{p}-l2" class="ao-full">{paper_pile(p, 38, 26, (0, 700, 1920, 1250))}</div>
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 0%,rgba(235,244,246,.45),rgba(0,0,0,0) 55%),linear-gradient(180deg,rgba(0,0,0,0) 50%,rgba(0,0,0,.45))"></div>
{dust_html(p, 30, (200, 50, 1700, 600), 36)}</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""tl.fromTo(q('l0'), {{ x: 0 }}, {{ x: -30, duration: {d}, ease: 'none' }}, 0); tl.fromTo(q('l1'), {{ x: 0 }}, {{ x: -80, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('l2'), {{ x: 0, y: 0 }}, {{ x: -160, y: -20, duration: {d}, ease: 'none' }}, 0); dust(30, 0, {d}); tag(0.05);"""
    return S(p, html, "", js)


@scene(37)
def s37(p, d):
    r = random.Random(37)
    cards = []
    for i in range(14):
        x, y, rot = r.uniform(-100, 1500), r.uniform(-80, 760), r.uniform(-25, 25)
        cards.append(f'''<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:520px;height:330px;background:url(assets/tex/paper_grey.jpg) {r.randint(0, 800)}px 0;transform:rotate({rot:.1f}deg);box-shadow:0 14px 30px rgba(0,0,0,.5)">
<div style="position:absolute;left:0;right:0;top:64px;height:3px;background:#6d8796;opacity:.7"></div>
<div style="position:absolute;left:10px;top:20px;width:500px;height:311px;opacity:.85;background:url(assets/tex/scribble{i % 3}.png) 0 0/100% 100%"></div></div>''')
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#1c2328" data-layout-allow-overflow>{"".join(cards)}
<div class="ao-full" style="background:radial-gradient(ellipse at 40% 30%,rgba(240,246,246,.25),rgba(0,0,0,.45) 75%)"></div></div>{tag_html(p, "RECREACIÓN")}'''
    js = f"shot('cam', 0, {d}, [1.25,80,40,-3], [1.4,-60,-20,-1], 'none'); tag(0.05);"
    return S(p, html, "", js)


@scene(38)
def s38(p, d):
    r = random.Random(38)
    spines, x = [], 0
    cols = ["#2d3a40", "#3a4a45", "#4b5659", "#25303a", "#56605c", "#3d4448", "#6a6f68"]
    while x < 3400:
        w = r.randint(60, 140)
        h = r.randint(560, 760)
        spines.append(f'<div style="position:absolute;left:{x}px;bottom:150px;width:{w}px;height:{h}px;background:{r.choice(cols)};box-shadow:inset -10px 0 18px rgba(0,0,0,.45),inset 6px 0 10px rgba(255,255,255,.08)">'
                      f'<div style="position:absolute;left:12%;right:12%;top:80px;height:90px;background:#e6e1d2;opacity:.85"></div></div>')
        x += w + r.randint(2, 8)
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#161b1f" data-layout-allow-overflow>
<div id="{p}-row" style="position:absolute;left:0;top:0;width:3400px;height:1080px">{"".join(spines)}<div style="position:absolute;left:0;bottom:110px;width:3400px;height:40px;background:#3e464b"></div></div>
<div class="ao-full" style="background:linear-gradient(90deg,rgba(0,0,0,.6),rgba(0,0,0,0) 30%,rgba(0,0,0,0) 70%,rgba(0,0,0,.6)),radial-gradient(ellipse at 50% 0%,rgba(230,240,242,.25),rgba(0,0,0,0) 60%)"></div></div>{tag_html(p, "RECREACIÓN")}'''
    js = f"tl.fromTo(q('row'), {{ x: 0 }}, {{ x: -900, duration: {d}, ease: 'none' }}, 0); tl.fromTo(q('cam'), {{ filter: 'blur(8px)' }}, {{ filter: 'blur(0px)', duration: 0.15 }}, 0); tag(0.05);"
    return S(p, html, "", js)


UNESCO = "FUENTE · postulación UNESCO Memoria del Mundo (2008)"


@scene(39)
def s39(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#1b2227" data-layout-allow-overflow>
<div class="ao-full" style="filter:blur(7px) brightness(.45)">{paper_pile(p, 36, 70, (0, 0, 1920, 1080))}</div>
<div id="{p}-c" class="ao-full">{counter_block(p, f'<span class="ao-unit" style="font-size:150px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:300px">0</span>', "", "PÁGINAS", 260, 300)}</div></div>
{tag_html(p, UNESCO, src=True)}'''
    html = html.replace('font:700 42px Courier Prime;letter-spacing:.24em;color:#d6dcda">PÁGINAS', 'font:400 120px Anton;letter-spacing:.06em;color:#f4f2ec">PÁGINAS')
    js = f"count('n', 0, 800000, 0.05, 1.4); shot('cam', 0, 1.1, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.1, {d}, [1.3,0,40], [1.33,0,40], 'none'); tag(0.05);"
    return S(p, html, "", js)


@scene(40)
def s40(p, d):
    sheets = "".join(f'<div id="{p}-s{i}" style="position:absolute;left:{510 + (i * 7) % 24}px;top:{1040 - i * 20}px;width:900px;height:18px;background:{["#efe9dc", "#dcd8cc", "#e6e1d3"][i % 3]};box-shadow:0 3px 4px rgba(0,0,0,.35)"></div>' for i in range(70))
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{sheets}
<div style="position:absolute;left:0;width:1920px;top:-930px;text-align:center"><span class="ao-unit" style="font-size:130px;color:{ACC}">≈ </span><span class="ao-num" style="font-size:240px">800.000</span><div class="ao-unit" style="font-size:96px">PÁGINAS</div></div></div>
{tag_html(p, UNESCO, src=True)}'''
    js = "".join(f"tl.fromTo(q('s{i}'), {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.08 }}, {i * 0.017:.3f});" for i in range(70))
    js += f"shot('cam', 0, {d}, [1.0,0,-60], [1.0,0,1120], 'power1.inOut'); tag(0.0);"
    return S(p, html, "", js)


@scene(41)
def s41(p, d):
    shelves = "".join(f'<div style="position:absolute;left:0;top:{y}px;width:3000px;height:22px;background:#4a5358;box-shadow:0 8px 12px rgba(0,0,0,.4)"></div>' for y in (330, 620, 910))
    r = random.Random(41)
    boxes = "".join(f'<div style="position:absolute;left:{x}px;top:{y - 220}px;width:{w}px;height:220px;background:{r.choice(["#8d9a9c", "#a7aea6", "#7f8b8f", "#b9bcb0"])};border:2px solid rgba(30,36,40,.6)"><div style="margin:40px auto 0;width:60%;height:40px;background:#e9e5d8"></div></div>'
                    for y in (330, 620, 910) for x, w in [(i * 190 + r.randint(0, 20), 170) for i in range(16)])
    ticks = "".join(f'<div style="position:absolute;left:{160 + i * 160}px;top:-24px;width:4px;height:{36 if i % 5 == 0 else 20}px;background:{ACC}"></div>' for i in range(11))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#1c2327" data-layout-allow-overflow>
<div id="{p}-sh" style="position:absolute;left:0;top:0;width:3000px;height:1080px;filter:brightness(.7)">{boxes}{shelves}</div>
<div style="position:absolute;left:0;top:500px;width:1920px;height:12px"><div id="{p}-tape" style="position:absolute;left:160px;top:0;width:1600px;height:12px;background:{ACC};transform-origin:0 50%"></div>{ticks}</div>
<div id="{p}-c" style="position:absolute;left:0;width:1920px;top:560px;text-align:center"><span class="ao-unit" style="font-size:110px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:250px">0</span><span class="ao-unit" style="font-size:100px"> METROS LINEALES</span></div></div>
{tag_html(p, UNESCO, src=True)}'''
    js = f"""tl.fromTo(q('tape'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.1, ease: 'power2.inOut' }}, 0.1); count('n', 0, 200, 0.1, 1.1);
tl.fromTo(q('sh'), {{ x: 0 }}, {{ x: -500, duration: {d}, ease: 'none' }}, 0);
shot('cam', 0, 1.25, [1.0,0,0], [1.02,0,0], 'none'); shot('cam', 1.25, {d}, [1.32,0,-160], [1.35,0,-165], 'none'); tag(0.05);"""
    return S(p, html, "", js)


@scene(42)
def s42(p, d):
    cols, rows = 24, 12
    cells = "".join(f'<div id="{p}-g{i}" style="position:absolute;left:{120 + (i % cols) * 70}px;top:{90 + (i // cols) * 76}px;width:60px;height:64px;background:#e7e3d6;opacity:0;border-top:6px solid #7d929b"></div>' for i in range(cols * rows))
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{cells}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(10,14,16,.85) 0,rgba(10,14,16,.6) 35%,rgba(10,14,16,0) 70%)"></div>
<div style="position:absolute;left:0;width:1920px;top:340px;text-align:center"><span id="{p}-n" class="ao-num" style="font-size:300px">0</span><div class="ao-unit" style="font-size:120px">FICHAS</div></div></div>
{tag_html(p, UNESCO, src=True)}'''
    order = list(range(cols * rows))
    random.Random(42).shuffle(order)
    js = "".join(f"tl.set(q('g{c}'), {{ opacity: 1 }}, {0.05 + k * 1.2 / len(order):.3f});" for k, c in enumerate(order))
    js += f"count('n', 0, 11225, 0.05, 1.25); shot('cam', 0, 1.1, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.1, {d}, [1.3,0,40,-2], [1.33,0,40,-2], 'none'); tag(0.05);"
    return S(p, html, "", js)


@scene(43)
def s43(p, d):
    frames = "".join(f'<div style="position:absolute;left:{60 + (i % 9) * 210}px;top:{40 + (i // 9) * 200}px;width:180px;height:150px;background:linear-gradient(160deg,#6c767a,#3d4549);border:8px solid #f2efe6;box-shadow:0 6px 12px rgba(0,0,0,.4)"></div>' for i in range(54))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#101417" data-layout-allow-overflow>
<div id="{p}-gr" style="position:absolute;left:0;top:0;width:1920px;height:1200px">{frames}</div>
<div class="ao-full" style="background:linear-gradient(180deg,rgba(8,10,12,.2),rgba(8,10,12,.85) 40%,rgba(8,10,12,.85) 60%,rgba(8,10,12,.2))"></div>
<div style="position:absolute;left:0;width:1920px;top:330px;text-align:center"><span class="ao-unit" style="font-size:120px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:290px">0</span><div class="ao-unit" style="font-size:110px">FOTOGRAFÍAS</div></div></div>
{tag_html(p, UNESCO, src=True)}'''
    js = f"count('n', 0, 20000, 0.05, 1.1); tl.fromTo(q('gr'), {{ y: 0 }}, {{ y: -120, duration: {d}, ease: 'none' }}, 0); tag(0.05);"
    return S(p, html, "", js)


def cassette_svg(x, y, s=1):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="0" y="0" width="200" height="128" rx="10" fill="#2a3135" stroke="#c9d1d3" stroke-width="4"/>'
            f'<rect x="24" y="18" width="152" height="44" fill="#e7e3d6"/><circle cx="62" cy="88" r="18" fill="none" stroke="#c9d1d3" stroke-width="5"/>'
            f'<circle cx="138" cy="88" r="18" fill="none" stroke="#c9d1d3" stroke-width="5"/><rect x="80" y="80" width="40" height="16" fill="#151a1d"/></g>')


@scene(44)
def s44(p, d):
    if HAVE["tapes"]:
        bg = f'<img id="{p}-ph" src="assets/img/heap_of_tapes_g.jpg" style="position:absolute;left:-100px;top:-400px;width:2120px;height:2590px;object-fit:cover;filter:brightness(.55)" alt="">'
        lab = "IMAGEN ILUSTRATIVA · Hmvh, Wikimedia Commons (dominio público)"
        js0 = f"tl.fromTo(q('ph'), {{ x: 0 }}, {{ x: -100, duration: {d}, ease: 'none' }}, 0);"
    else:
        r = random.Random(44)
        bg = f'<svg id="{p}-ph" viewBox="0 0 2200 1080" width="2200" height="1080" style="position:absolute;left:0;top:0;opacity:.55">' + "".join(
            cassette_svg(-60 + c * 230 + (r.randint(-8, 8)), -40 + rr * 160 + r.randint(-6, 6), 1) for rr in range(8) for c in range(10)) + "</svg>"
        lab = "RECREACIÓN"
        js0 = f"tl.fromTo(q('ph'), {{ x: 0 }}, {{ x: -160, duration: {d}, ease: 'none' }}, 0);"
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#13181b" data-layout-allow-overflow>{bg}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(10,14,16,.85) 0,rgba(10,14,16,.5) 40%,rgba(10,14,16,.1) 75%)"></div>
<div style="position:absolute;left:0;width:1920px;top:330px;text-align:center"><span id="{p}-n" class="ao-num" style="font-size:300px">0</span><div class="ao-unit" style="font-size:120px">CASETES</div></div></div>
{tag_html(p, lab, src=lab != "RECREACIÓN")}'''
    js = js0 + f"count('n', 0, 543, 0.05, 1.0); tag(0.05);"
    return S(p, html, "", js)


def stamp_tl(p, d, first):
    html = f'''<div id="{p}-cam" class="ao-cam ao-paper" data-layout-allow-overflow>
<div class="tl-axis" style="left:240px;top:560px;width:1440px"></div>
<div id="{p}-fill" class="tl-fill" style="left:240px;top:560px;width:1440px"></div>
<div class="tl-dot" style="left:240px;top:564px"></div><div id="{p}-d2" class="tl-dot" style="left:1680px;top:564px"></div>
<div id="{p}-s1" class="ao-stamp" style="position:absolute;left:120px;top:260px;font-size:120px">1927</div>
<div id="{p}-s2" class="ao-stamp" style="position:absolute;left:1360px;top:260px;font-size:110px">FEB 1989</div>
<div style="position:absolute;left:0;width:1920px;top:720px;text-align:center;font:700 44px 'Courier Prime';letter-spacing:.28em;color:#2a2d2c">FECHAS DEL INVENTARIO</div></div>
{tag_html(p, UNESCO, src=True)}'''
    if first:
        js = f"""stampIn('s1', 0.2, -4); shake('cam', 0.36, 8); tl.set(q('s2'), {{ opacity: 0 }}, 0); tl.set(q('fill'), {{ scaleX: 0 }}, 0); tl.set(q('d2'), {{ opacity: 0 }}, 0);
shot('cam', 0, 0.9, [1.4,500,40,-2], [1.44,510,40,-2], 'none'); shot('cam', 0.9, {d}, [1.0,0,0], [1.02,0,0], 'none'); tag(0.05);"""
    else:
        js = f"""tl.set(q('s1'), {{ rotation: -4 }}, 0); tl.fromTo(q('fill'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: 'power3.in' }}, 0.05);
tl.fromTo(q('d2'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, 0.62); stampIn('s2', 0.62, 3); shake('cam', 0.78, 8);
shot('cam', 0, 0.9, [1.0,0,0], [1.02,0,0], 'none'); shot('cam', 0.9, {d}, [1.55,-560,40,1], [1.6,-580,40,1], 'none'); tag(0.05);"""
    return S(p, html, TL_CSS, js)


@scene(45)
def s45(p, d):
    return stamp_tl(p, d, True)


@scene(46)
def s46(p, d):
    return stamp_tl(p, d, False)


@scene(47)
def s47(p, d):
    ticks = "".join(f'<line x1="0" y1="-300" x2="0" y2="{-262 if k % 3 else -240}" stroke="#e8ecea" stroke-width="{6 if k % 3 == 0 else 3}" transform="rotate({k * 30})"/>' for k in range(12))
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
<svg viewBox="-960 -540 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
<g transform="translate(-420,0)"><circle r="320" fill="#151b1f" stroke="#e8ecea" stroke-width="8"/>{ticks}
<path id="{p}-arc" d="M0,-280 A280,280 0 1 1 -0.1,-280" fill="none" stroke="{ACC}" stroke-width="20" stroke-dasharray="1760" stroke-dashoffset="1760" opacity=".8"/>
<line id="{p}-hh" x1="0" y1="20" x2="0" y2="-170" stroke="#e8ecea" stroke-width="16" stroke-linecap="round"/>
<line id="{p}-mh" x1="0" y1="30" x2="0" y2="-250" stroke="{ACC}" stroke-width="9" stroke-linecap="round"/><circle r="16" fill="#e8ecea"/></g></svg>
<div style="position:absolute;left:980px;top:330px"><span class="ao-unit" style="font-size:120px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:300px">0</span><div class="ao-unit" style="font-size:120px">HORAS</div></div></div>
{tag_html(p, "FUENTE · Poder Judicial, Archivos del Terror (2008)", src=True)}'''
    js = f"""tl.fromTo(q('mh'), {{ rotation: 0, svgOrigin: '0 0' }}, {{ rotation: 4320, svgOrigin: '0 0', duration: 1.4, ease: 'power2.inOut' }}, 0.05);
tl.fromTo(q('hh'), {{ rotation: 0, svgOrigin: '0 0' }}, {{ rotation: 360, svgOrigin: '0 0', duration: 1.4, ease: 'power2.inOut' }}, 0.05);
tl.to(q('arc'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 1.4, ease: 'power2.inOut' }}, 0.05); count('n', 0, 12, 0.05, 1.4);
shot('cam', 0, 1.0, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.0, {d}, [1.35,380,0], [1.38,380,0], 'none'); tag(0.05);"""
    return S(p, html, "", js)


@scene(48)
def s48(p, d):
    boxes = "".join(f'<g id="{p}-b{i}"><rect x="-120" y="-170" width="240" height="170" fill="#11161a" stroke="#6f7d84" stroke-width="3"/><rect x="-120" y="-170" width="240" height="26" fill="#1d252b"/><rect x="-40" y="-110" width="80" height="34" fill="#c9cfc9" opacity=".7"/></g>' for i in range(7))
    html = doorway(p, boxes, 1.0)
    js = "".join(f"tl.fromTo(q('b{i}'), {{ attr: {{ transform: 'translate(960,900) scale(.5)' }} }}, {{ attr: {{ transform: 'translate({1350 if i % 2 else 570},1300) scale(1.9)' }}, duration: 1.7, ease: 'power1.in' }}, {i * 0.27 - 0.7:.2f});" for i in range(7))
    js += f"shot('cam', 0, 0.95, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 0.95, {d}, [1.4,0,60], [1.45,0,60], 'none'); tag(0.05);"
    return S(p, html, "", js)


@scene(49)
def s49(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<div class="ao-full" style="background:url(assets/tex/paper_cream.jpg) 30% 40%/2400px 1600px;filter:contrast(1.15)"></div>
<div class="ao-full" style="background:radial-gradient(ellipse at 30% 40%,rgba(70,86,90,.55),rgba(70,86,90,0) 30%),radial-gradient(ellipse at 72% 62%,rgba(60,76,80,.5),rgba(60,76,80,0) 26%),radial-gradient(ellipse at 55% 20%,rgba(90,100,98,.4),rgba(90,100,98,0) 18%);mix-blend-mode:multiply"></div>
<div style="position:absolute;left:240px;top:300px;width:1500px;opacity:.45">{doc_lines(9, gap=34)}</div>
{"".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{int(w * .8)}px;border-radius:50%;border:7px solid rgba(70,82,86,.38);box-shadow:inset 0 0 40px rgba(70,82,86,.3)"></div>' for x, y, w in ((300, 150, 420), (1100, 520, 520), (760, 80, 260), (420, 650, 300)))}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 30%,rgba(0,0,0,.6) 85%)"></div></div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""shot('cam', 0, 1.1, [1.5,0,0,-4], [1.6,-60,-20,-4], 'none'); shot('cam', 1.1, {d}, [2.6,300,200,6], [2.7,280,190,6], 'none');
tl.fromTo(q('cam'), {{ filter: 'blur(4px)' }}, {{ filter: 'blur(0px)', duration: 0.6 }}, 0); tag(0.05);"""
    return S(p, html, "", js)


@scene(50)
def s50(p, d):
    t, n = typed(p, "t", "«PERDIDOS»")
    html = f'''<div id="{p}-cam" class="ao-cam ao-paper" data-layout-allow-overflow>
<div style="position:absolute;left:{(1920 - 10 * 0.6 * 170) / 2:.0f}px;top:400px;font:700 170px 'Courier Prime';color:#191b1b;white-space:nowrap;position:absolute">{t}
<div id="{p}-x" style="position:absolute;left:-20px;right:-20px;top:92px;height:18px;background:{ACC};transform-origin:0 50%"></div></div>
<div id="{p}-q" style="position:absolute;left:0;width:1920px;top:140px;text-align:center;font:400 760px/1 Anton;color:{ACC};opacity:0">?</div></div>'''
    js = f"""type('t', {n}, 0.05, 0.05); tl.fromTo(q('x'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: 'power3.in' }}, 0.7);
tl.fromTo(q('q'), {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: 'expo.out' }}, 1.15);
shot('cam', 0, 1.15, [1.0,0,0], [1.04,0,0], 'none'); shot('cam', 1.15, {d}, [1.12,0,0], [1.15,0,0], 'none');"""
    return S(p, html, "", js)


def conosur(p, d, lines):
    ax, ay = map_pt("Asunción")
    hi = ("Argentina", "Uruguay", "Chile")
    extra = f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="22" fill="{ACC}" stroke="#08302c" stroke-width="6"/>'
    if lines:
        for i, c in enumerate(("Buenos Aires", "Montevideo", "Santiago")):
            x, y = map_pt(c)
            mx, my = (x + ax) / 2, (y + ay) / 2 - 160
            extra += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="#1e2a2c"/><path id="{p}-ln{i}" d="M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {ax:.0f},{ay:.0f}" fill="none" stroke="{ACC}" stroke-width="9" '
                      f'stroke-dasharray="1600" stroke-dashoffset="1600" stroke-linecap="round"/>')
        extra += f'<text x="{ax + 40:.0f}" y="{ay - 20:.0f}" style="font:700 52px \'Courier Prime\';fill:#102a28;letter-spacing:.1em">LAMBARÉ</text>'
    cx, cy = map_pt("Montevideo")
    s = 0.42 if not lines else 0.5
    x0, y0 = cam_center((cx + ax) / 2 - 300, (cy + ay) / 2 + 60, s)
    x1, y1 = cam_center((cx + ax) / 2 - 300, (cy + ay) / 2 + 60, s * 1.05)
    html = f'''<div class="ao-full" style="background:#3b6782"></div>
<div id="{p}-cam" class="ao-cam" style="transform-origin:0 0" data-layout-allow-overflow>{map_svg(p, hi, extra)}</div>
{tag_html(p, "MAPA · elaboración propia, datos Natural Earth", src=True)}'''
    css = MAP_CSS.replace("PFX", p) + f".hi.on{{fill:{ACC};fill-opacity:.42;stroke:#0f6f67;stroke-width:4;stroke-dasharray:none}}"
    return html, css, x0, y0, x1, y1, s


@scene(51)
def s51(p, d):
    html, css, x0, y0, x1, y1, s = conosur(p, d, False)
    js = f"shot('cam', 0, {d}, [{s},{x0},{y0}], [{s * 1.05:.3f},{x1},{y1}], 'none');"
    js += "".join(f"tl.set(q('c-{c}'), {{ attr: {{ class: 'hi on' }} }}, {0.25 + i * 0.4:.2f}); tl.fromTo(q('lb-{c}'), {{ scale: 1.25, transformOrigin: '50% 50%' }}, {{ scale: 1, duration: 0.3, ease: 'expo.out' }}, {0.25 + i * 0.4:.2f});"
                  for i, c in enumerate(("argentina", "uruguay", "chile")))
    js += "tag(0.05);"
    return S(p, html, css, js)


@scene(52)
def s52(p, d):
    html, css, x0, y0, x1, y1, s = conosur(p, d, True)
    js = f"shot('cam', 0, {d}, [{s},{x0},{y0}], [{s * 1.08:.3f},{x1},{y1}], 'none');"
    js += "".join(f"tl.set(q('c-{c}'), {{ attr: {{ class: 'hi on' }} }}, 0);" for c in ("argentina", "uruguay", "chile"))
    js += "".join(f"tl.to(q('ln{i}'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.8, ease: 'power2.inOut' }}, {0.1 + i * 0.15:.2f});" for i in range(3))
    js += "tag(0.05);"
    return S(p, html, css, js)


def ficha(p, k, x, y, rot, stamp=None, photo=False, finger=False, w=520, h=330):
    st = f'<div id="{p}-st{k}" class="ao-stamp" style="position:absolute;right:26px;bottom:22px;font-size:50px;transform:rotate(-8deg)">{stamp}</div>' if stamp else ""
    ph = (f'<div style="position:absolute;left:24px;top:84px;width:{int(w * .3)}px;height:{int(h * .62)}px;border:3px solid #556;background:#d9d8d0">'
          f'<svg id="{p}-ph{k}" viewBox="-100 -170 200 200" width="100%" height="100%" style="opacity:0">{svg_person_icon(0, 30, 0.85, "#5b6468")}</svg></div>') if photo else ""
    fp = (f'<div style="position:absolute;right:24px;top:84px;width:{int(w * .26)}px;height:{int(h * .62)}px;border:3px solid #556">'
          f'<div id="{p}-fp{k}" style="width:100%;height:100%;opacity:0;background:url(assets/tex/fingerprint.png) center/contain no-repeat"></div></div>') if finger else ""
    return f'''<div id="{p}-f{k}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:url(assets/tex/paper_grey.jpg) {k * 300}px 0;transform:rotate({rot}deg);box-shadow:0 16px 34px rgba(0,0,0,.55)">
<div style="position:absolute;left:0;right:0;top:62px;height:3px;background:#6d8796;opacity:.7"></div>
<div style="position:absolute;left:24px;top:18px;width:200px;height:24px;background:rgba(60,70,74,.35);filter:blur(4px)"></div>{ph}{fp}{st}</div>'''


@scene(53)
def s53(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>
{ficha(p, 0, 130, 330, -5, "ARGENTINA")}{ficha(p, 1, 700, 380, 2, "URUGUAY")}{ficha(p, 2, 1270, 320, 6, "CHILE")}</div>{tag_html(p, "RECREACIÓN")}'''
    js = "".join(f"stampIn('st{i}', {0.15 + i * 0.4:.2f}, -8);" for i in range(3))
    js += f"shot('cam', 0, 0.85, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 0.85, {d}, [1.7,-560,-60,-3], [1.75,-600,-60,-3], 'none'); tag(0.05);"
    return S(p, html, "", js)


@scene(54)
def s54(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#0e1316" data-layout-allow-overflow>
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(46,196,182,.10),rgba(0,0,0,0) 60%)"></div>
<div id="{p}-t1" style="position:absolute;left:0;width:1920px;top:250px;text-align:center;font:400 210px/1 Anton;color:#f3f1ea;letter-spacing:.01em">NEGABA</div>
<div id="{p}-t2" style="position:absolute;left:0;width:1920px;top:480px;text-align:center;font:400 170px/1 Anton;color:{ACC};letter-spacing:.01em">HABERLOS DETENIDO</div></div>'''
    js = f"""stampIn('t1', 0.05, 0); stampIn('t2', 0.35, 0); shake('cam', 0.51, 12);
shot('cam', 0, 1.25, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.25, {d}, [1.15,0,-20,-2], [1.18,0,-22,-2], 'none');"""
    return S(p, html, "", js)


@scene(55)
def s55(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam ao-desk" data-layout-allow-overflow>{ficha(p, 0, 360, 190, -1.5, None, True, True, 1200, 760)}</div>{tag_html(p, "RECREACIÓN")}'''
    js = f"""tl.fromTo(q('ph0'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.3); tl.fromTo(q('fp0'), {{ opacity: 0, scale: 1.2 }}, {{ opacity: .95, scale: 1, duration: 0.25, ease: 'power4.in' }}, 1.4);
shot('cam', 0, 1.25, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.25, {d}, [1.9,-640,-120], [1.95,-660,-125], 'none'); tag(0.05);"""
    return S(p, html, "", js)


@scene(56)
def s56(p, d):
    r = random.Random(56)
    wall = "".join(ficha(p, 10 + i, r.randint(-200, 1700), r.randint(-150, 900), r.uniform(-12, 12), None, i % 2 == 0, i % 3 == 0) for i in range(18))
    words = ["FICHADOS", "CON FOTO", "CON HUELLAS"]
    ws = " · ".join(f'<span id="{p}-w{i}" style="color:#f3f1ea">{w}</span>' for i, w in enumerate(words))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#11171b" data-layout-allow-overflow><div id="{p}-wall" class="ao-full">{wall}</div>
<div class="ao-full" style="background:rgba(8,11,13,.55)"></div>
<div style="position:absolute;left:0;width:1920px;top:460px;text-align:center;font:400 112px/1 Anton;letter-spacing:.02em;white-space:nowrap">{ws}</div></div>'''
    js = "".join(f"tl.fromTo(q('f{10 + i}'), {{ y: -1300, opacity: 1 }}, {{ y: 0, duration: 0.3, ease: 'power3.in' }}, {0.05 + i * 0.12:.2f});" for i in range(18))
    js += "".join(f"tl.set(q('w{i}'), {{ color: '{ACC}' }}, {0.3 + i * 0.55:.2f});" for i in range(3))
    js += f"shot('cam', 0, 1.3, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.3, {d}, [1.08,0,0,1], [1.1,0,0,1], 'none');"
    return S(p, html, "", js)


TITLE = "LOS ARCHIVOS DEL TERROR"


@scene(57)
def s57(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#050607" data-layout-allow-overflow>
{smoke_html(p, 0, 0.55)}{smoke_html(p, 1, 0.45)}
<div id="{p}-t" style="position:absolute;left:0;width:1920px;top:400px;text-align:center;font:400 200px/1 Anton;color:#f2f0ea;letter-spacing:.03em;white-space:nowrap">LOS ARCHIVOS<br><span style="color:{ACC}">DEL TERROR</span></div>
{smoke_html(p, 2, 0.35)}</div>'''
    html = html.replace('top:400px;text-align:center;font:400 200px/1 Anton', 'top:300px;text-align:center;font:400 220px/1.02 Anton')
    js = f"""tl.fromTo(q('t'), {{ opacity: 0, filter: 'blur(22px)', scale: 1.08 }}, {{ opacity: 1, filter: 'blur(0px)', scale: 1, duration: 0.7, ease: 'power2.out' }}, 0.05);
tl.fromTo(q('smk0'), {{ x: 0, scale: 1 }}, {{ x: -200, scale: 1.1, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('smk1'), {{ x: -100 }}, {{ x: 120, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('smk2'), {{ x: 0, opacity: .7 }}, {{ x: 260, opacity: .2, duration: {d}, ease: 'none' }}, 0);"""
    return S(p, html, "", js)


@scene(58)
def s58(p, d):
    if HAVE["museo"]:
        bg = (f'<img src="assets/img/museo_justicia_archivo_terror_2019_g.jpg" class="ao-cover" style="filter:blur(22px) brightness(.4)" alt="">'
              f'<div style="position:absolute;left:1180px;top:150px;width:560px;height:746px;background:#efe8d8;padding:16px;box-shadow:0 40px 90px rgba(0,0,0,.6);transform:rotate(2deg)">'
              f'<div style="width:100%;height:100%;background:url(assets/img/museo_justicia_archivo_terror_2019_g.jpg) center/cover"></div></div>')
        lab = tag_html(p, "IMAGEN REAL · Archivo del Terror · Museo de la Justicia, Asunción (foto 2019)", src=True)
        tx = 'left:150px;width:1000px;text-align:left'
    else:
        bg = f'<div class="ao-full" style="filter:blur(2px) brightness(.32)">{paper_pile(p, 58, 70, (0, 0, 1920, 1080))}</div>'
        lab = ""
        tx = 'left:0;width:1920px;text-align:center'
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#0b0e10" data-layout-allow-overflow>{bg}{smoke_html(p, 1, 0.3)}
<div style="position:absolute;{tx};top:300px;font:400 220px/1.02 Anton;color:#f2f0ea;letter-spacing:.03em;white-space:nowrap">LOS ARCHIVOS<br><span style="color:{ACC}">DEL TERROR</span></div></div>{lab}'''
    if HAVE["museo"]:
        html = html.replace("font:400 220px/1.02 Anton", "font:400 150px/1.02 Anton")
    js = f"shot('cam', 0, {d}, [1.0,0,0], [1.07,0,0], 'none'); tl.fromTo(q('smk1'), {{ x: 0 }}, {{ x: -200, duration: {d}, ease: 'none' }}, 0);"
    if lab:
        js += "tag(0.05);"
    return S(p, html, "", js)


@scene(59)
def s59(p, d):
    r = random.Random(59)
    bands = "".join(f'<div id="{p}-b{i}" style="position:absolute;left:0;top:{r.randint(0, 1040)}px;width:1920px;height:{r.randint(6, 40)}px;background:rgba({r.choice(["240,244,244", "46,196,182", "120,130,134"])},{r.uniform(.35, .8):.2f})"></div>' for i in range(22))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#0b0e10" data-layout-allow-overflow>
<div id="{p}-pile" class="ao-full" style="filter:blur(3px) brightness(.5)">{paper_pile(p, 58, 70, (0, 0, 1920, 1080))}</div>
{bands}<div style="position:absolute;left:150px;top:120px;font:700 70px 'IBM Plex Mono';color:#f2f4f3">◀◀</div>
<div id="{p}-blk" class="ao-full" style="background:#000;opacity:0"></div></div>'''
    js = "".join(f"tl.fromTo(q('b{i}'), {{ y: 0 }}, {{ y: {r.choice([-1, 1]) * r.randint(200, 900)}, duration: 0.6, ease: 'none' }}, 0);" for i in range(22))
    js += f"tl.fromTo(q('pile'), {{ y: 0, scaleY: 1 }}, {{ y: 400, scaleY: 1.3, duration: 0.6, ease: 'power2.in' }}, 0); tl.set(q('blk'), {{ opacity: 1 }}, 0.6);"
    return S(p, html, "", js)


@scene(60)
def s60(p, d):
    line1 = "MAYO · 1954"
    line2 = "ASUNCIÓN"
    l1, n1 = typed(p, "a", line1)
    l2, n2 = typed(p, "b", line2)
    w1 = len(line1) * 0.6 * 128
    x1 = (1920 - w1) / 2
    digits = "".join(f'<span style="display:inline-block;width:.6em;height:1em;overflow:hidden;vertical-align:top"><span id="{p}-r{i}" style="display:block">'
                     + "".join(f"<span style='display:block;height:1em'>{c}</span>" for c in seq) + "</span></span>"
                     for i, seq in enumerate(["1", "9", "98765", "2109876543210987654"]))
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<img src="assets/img/stroessner_sepia.jpg" class="ao-cover" style="filter:blur(30px) brightness(.42)" alt="">
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,.15),rgba(0,0,0,.7) 80%)"></div>
<div id="{p}-roll" style="position:absolute;left:0;width:1920px;top:360px;text-align:center;font:700 200px/1 'Courier Prime';color:{ACC};height:200px;overflow:hidden">{digits}</div>
<div id="{p}-card" style="opacity:0">
<div class="dc-line dc-d" style="left:{x1:.0f}px;top:400px">{l1}</div>
<div class="dc-line dc-p" style="left:{x1 + 8:.0f}px;top:570px">{l2}<span id="{p}-cur" class="dc-cur"></span></div></div>
</div>'''
    js = f"""tl.fromTo(q('r2'), {{ y: 0 }}, {{ y: '-80%', duration: 0.7, ease: 'power2.inOut' }}, 0.05);
tl.fromTo(q('r3'), {{ y: 0 }}, {{ y: '-94.737%', duration: 0.7, ease: 'power2.inOut' }}, 0.05);
tl.to(q('roll'), {{ opacity: 0, duration: 0.15 }}, 0.95); tl.set(q('card'), {{ opacity: 1 }}, 1.0);
for (let i = 0; i < {n1}; i++) tl.set(q('a' + i), {{ display: 'inline' }}, 1.0 + i * 0.03);
type('b', {n2}, 1.35, 0.06); blink('cur', 1.0, {d}, 0.25);
shot('cam', 0, 1.0, [1.0,0,0], [1.03,0,0], 'none'); shot('cam', 1.0, {d}, [1.1,0,-10], [1.14,0,-12], 'none');"""
    return S(p, html, DATE_CSS, js)


def origen_tl(p, d, mode):
    yrs = "".join(f'<div style="position:absolute;left:{220 + (y - 1954) * 40}px;top:{600}px;width:3px;height:{30 if y % 5 == 0 else 14}px;background:#3d3428"></div>' for y in range(1954, 1990))
    lbls = "".join(f'<div style="position:absolute;left:{220 + (y - 1954) * 40 - 50}px;top:640px;width:100px;text-align:center;font:700 30px Courier Prime;color:#3d3428">{y}</div>' for y in (1954, 1964, 1974, 1984, 1989))
    blocks = ""
    if mode == "periods":
        blocks = "".join(f'<div id="{p}-k{i}" style="position:absolute;left:{220 + i * 200}px;top:470px;width:186px;height:110px;background:{ACC};opacity:0;border:4px solid #0f5f58"></div>' for i in range(7))
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>
<div class="ao-full" style="background:url(assets/tex/paper_cream.jpg) center/cover;filter:sepia(.45) brightness(.92)"></div>
<div id="{p}-ax" style="position:absolute;left:220px;top:592px;width:1400px;height:10px;background:#2e2820;transform-origin:0 50%"></div>
<div id="{p}-fill" style="position:absolute;left:220px;top:592px;width:1400px;height:10px;background:{ACC};transform-origin:0 50%;transform:scaleX(0)"></div>
{yrs}{lbls}<div class="tl-dot" style="left:220px;top:597px"></div>{blocks}
<div id="{p}-mk" style="position:absolute;left:150px;top:330px;font:700 54px 'Courier Prime';letter-spacing:.12em;color:#1f1b15;opacity:0;border-left:10px solid {ACC};padding-left:22px">MAYO 1954<br><span style="font-family:Anton;font-weight:400;font-size:92px;color:#0f5f58;letter-spacing:.03em">GOLPE MILITAR</span></div>
<div id="{p}-big" style="position:absolute;left:0;width:1920px;top:{720 if mode != 'periods' else 120}px;text-align:center;opacity:0">
{"<span id='" + p + "-n' class='ao-num' style='font-size:230px;color:#0f6f67'>0</span><span class='ao-unit' style='font-size:110px;color:#1f1b15'> AÑOS</span>" if mode == "years" else ""}
{"<span class='ao-unit' style='font-size:120px;color:#1f1b15'>= </span><span id='" + p + "-n' class='ao-num' style='font-size:190px;color:#0f6f67'>0</span><span class='ao-unit' style='font-size:96px;color:#1f1b15'> PERÍODOS PRESIDENCIALES</span>" if mode == "periods" else ""}</div>
<div id="{p}-g" class="ao-full" style="background:radial-gradient(circle at 220px 597px,rgba(46,196,182,.6),rgba(46,196,182,0) 14%);opacity:0"></div></div>'''
    return html


@scene(61)
def s61(p, d):
    html = origen_tl(p, d, "open")
    js = f"""tl.fromTo(q('ax'), {{ scaleX: 0.02 }}, {{ scaleX: 1, duration: 1.2, ease: 'power3.out' }}, 0.1);
shot('cam', 0, 0.9, [1.7,520,0], [1.72,500,0], 'none'); shot('cam', 0.9, {d}, [1.0,0,0], [1.02,-10,0], 'none');"""
    return S(p, html, TL_CSS, js)


@scene(62)
def s62(p, d):
    html = portrait(p, d, (560, -40, 800, 1180, 1.5, "50% 60%", "180% auto"), "IMAGEN REAL · Retrato oficial, agosto de 1954")
    js = f"""shot('cam', 0, 1.1, [1.0,0,0], [1.05,-20,0], 'none'); shot('cam', 1.1, {d}, [1.7,240,-60,-2], [1.75,230,-75,-2], 'none'); tag(0.05);
tl.fromTo(q('print'), {{ x: 30 }}, {{ x: -30, duration: {d}, ease: 'none' }}, 0);"""
    return S(p, html, "", js)


@scene(63)
def s63(p, d):
    html = origen_tl(p, d, "mark")
    js = f"""tl.fromTo(q('mk'), {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: 'expo.out' }}, 0.15);
tl.fromTo(q('g'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: 'power2.out' }}, 0.2); tl.to(q('g'), {{ opacity: 0.25, duration: 0.6 }}, 0.4);
shot('cam', 0, 1.05, [1.0,0,0], [1.02,0,0], 'none'); shot('cam', 1.05, {d}, [1.6,560,40], [1.64,560,40], 'none');"""
    return S(p, html, TL_CSS, js)


@scene(64)
def s64(p, d):
    html = origen_tl(p, d, "years")
    js = f"""tl.set(q('mk'), {{ opacity: 1 }}, 0); tl.fromTo(q('fill'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.3, ease: 'power1.inOut' }}, 0.1);
tl.set(q('big'), {{ opacity: 1 }}, 0.1); count('n', 0, 35, 0.1, 1.3);
shot('cam', 0, 1.25, [1.0,0,0], [1.02,0,0], 'none'); shot('cam', 1.25, {d}, [1.2,100,-120], [1.23,100,-125], 'none');"""
    return S(p, html, TL_CSS, js)


@scene(65)
def s65(p, d):
    html = origen_tl(p, d, "periods")
    js = f"""tl.set(q('fill'), {{ scaleX: 1 }}, 0); tl.set(q('big'), {{ opacity: 1 }}, 0);
{"".join(f"tl.fromTo(q('k{i}'), {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.15, ease: 'power3.out' }}, {0.15 + i * 0.22:.2f}); tl.set(q('n'), {{ textContent: '{i + 1}' }}, {0.15 + i * 0.22:.2f});" for i in range(7))}
shot('cam', 0, 1.25, [1.0,0,0], [1.02,0,0], 'none'); shot('cam', 1.25, {d}, [1.15,60,40], [1.17,60,40], 'none');"""
    return S(p, html, TL_CSS, js)


# ------------------------------------------------------------------ write scene files
# Shot grade alternation: every shot (scene start or internal punch-in cut) alternates between the
# open grade and a "close-up" grade (dark vignette on bright scenes, cool haze lift on dark ones), so
# each cut reads as a new shot (reference opening: ~0.9 s shots). Mean luma per scene measured on the
# first render; >= 88 counts as bright.
LUMA = [40, 41, 138, 55, 109, 125, 122, 146, 110, 92, 120, 106, 112, 105, 94, 68, 152, 96, 160, 65, 70, 91, 127, 157, 82, 94,
        157, 83, 91, 76, 57, 50, 59, 52, 136, 100, 121, 76, 84, 74, 94, 91, 70, 69, 155, 156, 66, 98, 143, 155, 110, 110, 94,
        63, 119, 69, 101, 86, 67, 52, 159, 105, 157, 155, 154]
NO_GRADE = {1, 2, 59}
PARITY = [0]
VG_DARK = ('<div id="{p}-vg" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:30;opacity:0;pointer-events:none;'
           'background:radial-gradient(ellipse at 50% 46%,rgba(0,0,0,0) 24%,rgba(0,0,0,.62) 58%,rgba(0,0,0,.92) 100%)"></div>')
VG_LIFT = ('<div id="{p}-vg" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:30;opacity:0;pointer-events:none;'
           'mix-blend-mode:screen;background:radial-gradient(ellipse at 50% 42%,rgba(222,234,236,.55),rgba(200,216,222,.18) 55%,rgba(0,0,0,0) 80%)"></div>')


def write_scene(n):
    p = f"s{n:02d}"
    d = DUR[n - 1]
    sc = SC[n](p, d)
    if n not in NO_GRADE:
        import re as _re
        cuts = [0.0] + sorted({float(m[0] or m[1]) for m in _re.findall(r"shot\('cam', ([\d.]+),|/\*cut:([\d.]+)\*/", sc["js"]) if float(m[0] or m[1]) > 0.01})
        sc["html"] += VG_DARK.replace("{p}", p) + VG_LIFT.replace("{p}-vg", "{p}-vl").replace("{p}", p)
        for t in cuts:
            o = PARITY[0] % 2
            sc["js"] += f"\ntl.set(q('vg'), {{ opacity: {o} }}, {t}); tl.set(q('vl'), {{ opacity: {o * (0.55 if LUMA[n - 1] >= 88 else 1)} }}, {t});"
            PARITY[0] += 1
    bg = f"background:{sc['bg']};" if sc.get("bg") else ""
    html = f"""<template>
<style>
{BASE_CSS}
#root{{{bg}}}
{sc['css']}
</style>
<div id="root" data-composition-id="{p}" data-width="1920" data-height="1080" data-duration="{d}">
{sc['html']}
</div>
<script>
(function () {{
const P = "{p}";
{JSLIB}
{sc['js']}
tl.set({{}}, {{}}, {d - 0.001:.3f});
window.__timelines["{p}"] = tl;
}})();
</script>
</template>
"""
    open(os.path.join(COMP, f"{p}.html"), "w").write(html)


for n in range(1, 66):
    write_scene(n)

# ------------------------------------------------------------------ fx (grain, vignette) over the whole film
grain_js = []
k = 0
t = 0.0
while t < END:
    grain_js.append(f"tl.set('#fx-grain', {{ backgroundPosition: '{(k * 137) % 512}px {(k * 211) % 512}px' }}, {t:.3f});")
    k += 1
    t += 2 / FPS
FX = f"""<template>
<style>
#root{{position:absolute;inset:0;pointer-events:none}}
#fx-grain{{position:absolute;left:0;top:0;width:1920px;height:1080px;background:url(assets/tex/grain.png);mix-blend-mode:overlay;opacity:.32}}
#fx-vig{{position:absolute;left:0;top:0;width:1920px;height:1080px;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 55%,rgba(0,0,0,.42) 100%)}}
#fx-leak{{position:absolute;left:-400px;top:-200px;width:1400px;height:1400px;border-radius:50%;background:radial-gradient(circle,rgba(220,246,244,.55),rgba(46,196,182,.18) 40%,rgba(0,0,0,0) 70%);mix-blend-mode:screen;opacity:0}}
</style>
<div id="root" data-composition-id="fx" data-width="1920" data-height="1080" data-duration="{END}">
<div id="fx-vig"></div><div id="fx-leak"></div><div id="fx-grain"></div>
</div>
<script>
(function () {{
const tl = gsap.timeline({{ paused: true }});
{"".join(grain_js)}
[[10.0, 0], [29.6, 1], [63.9, 0], [103.9, 1], [112.1, 0]].forEach(([t, s]) => {{
  tl.fromTo('#fx-leak', {{ opacity: 0, x: s ? 1300 : -200, y: s ? -100 : 200 }}, {{ opacity: 0.9, x: s ? 900 : 200, y: 0, duration: 0.25, ease: 'power2.out' }}, t - 0.12);
  tl.to('#fx-leak', {{ opacity: 0, duration: 0.45, ease: 'power2.in' }}, t + 0.13);
}});
tl.set({{}}, {{}}, {END - 0.001});
window.__timelines["fx"] = tl;
}})();
</script>
</template>
"""
open(os.path.join(COMP, "fx.html"), "w").write(FX)

# ------------------------------------------------------------------ root
hosts = []
for n in range(1, 66):
    p = f"s{n:02d}"
    hosts.append(f'<div id="{p}" data-composition-id="{p}" data-composition-src="compositions/{p}.html" data-start="{STARTS[n - 1]}" '
                 f'data-duration="{DUR[n - 1]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:1"></div>')

# audio cues: (id, file, start, duration, media_start, volume)
TW = "assets/audio/typewriter.wav"
AUD = [
    ("bed1", "assets/audio/bed.wav", 0.0, 57.55, 0.0, 0.62),
    ("bed2", "assets/audio/bed.wav", 62.9, round(END - 62.9, 2), 8.0, 0.62),
    ("tw1", TW, 0.30, 1.85, 0.4, 0.9), ("tw2", TW, 2.42, 1.0, 5.2, 0.9),
    ("tw3", TW, 20.05, 0.85, 9.0, 0.6), ("tw4", TW, 23.98, 1.55, 12.0, 0.85),
    ("tw5", TW, 49.52, 0.95, 15.3, 0.85), ("tw6", TW, 89.03, 0.55, 2.0, 0.8),
    ("tw7", TW, 109.1, 1.4, 6.6, 0.85),
    ("wh1", "assets/audio/whoosh.wav", 3.5, 1.2, 0.0, 0.8), ("wh2", "assets/audio/whoosh_b.wav", 11.62, 0.9, 0.0, 0.6),
    ("wh3", "assets/audio/whoosh_b.wav", 62.82, 0.9, 0.0, 0.9), ("wh4", "assets/audio/whoosh.wav", 107.55, 1.2, 0.0, 0.9),
    ("wh5", "assets/audio/whoosh_b.wav", 66.2, 0.9, 0.0, 0.45),
    ("st1", "assets/audio/impact.wav", 22.45, 1.6, 0.0, 0.55), ("st2", "assets/audio/impact.wav", 44.05, 1.6, 0.0, 0.5),
    ("pz", "assets/audio/impact.wav", 57.6, 2.0, 0.0, 0.9),
    ("lk", "assets/audio/lock.wav", 61.95, 0.8, 0.0, 0.9), ("lki", "assets/audio/impact.wav", 61.95, 2.0, 0.0, 0.9),
    ("q1", "assets/audio/impact.wav", 86.85, 2.0, 0.0, 0.85), ("q2", "assets/audio/impact.wav", 91.15, 2.0, 0.0, 0.85),
    ("q3", "assets/audio/impact.wav", 96.45, 2.0, 0.0, 0.95), ("zq3b", "assets/audio/impact.wav", 96.92, 2.0, 0.0, 0.6),
    ("rs1", "assets/audio/riser.wav", 100.95, 3.0, 0.0, 0.8), ("tt", "assets/audio/impact.wav", 103.95, 2.0, 0.0, 1.0),
    ("rs2", "assets/audio/riser.wav", 106.1, 1.0, 2.0, 0.8),
    ("rs0", "assets/audio/riser.wav", 58.4, 3.0, 0.0, 0.35),
]
# counter ticks (soft key ticks while numbers roll)
for name, t0, dur, step in (("k21", 36.9, 1.2, 0.09), ("k39", 67.55, 1.4, 0.09), ("k42", 73.95, 1.2, 0.08), ("k64", 116.5, 1.3, 0.1)):
    i = 0
    t = t0
    while t < t0 + dur:
        AUD.append((f"{name}_{i}", "assets/audio/tick.wav", round(t, 3), 0.06, 0.0, 0.7))
        t += step * (1 + i * 0.06)
        i += 1
def LANE(a):
    for pre, ln in (("bed", 3), ("tw", 4), ("wh", 5), ("st", 6), ("pz", 6), ("q", 6), ("tt", 6), ("lki", 6), ("lk", 7), ("rs", 8), ("k", 9)):
        if a.startswith(pre):
            return ln
    return 10


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
#review .cap span {{ display: inline-block; font: 400 28px/1.35 "Work Sans", sans-serif; color: #fff; background: rgba(0,0,0,.62); padding: 6px 16px; }}
#review-flag {{ position: absolute; left: 110px; top: 70px; font: 700 22px/1 "IBM Plex Mono", monospace; letter-spacing: .14em; color: #fff;
  background: rgba(0,0,0,.66); padding: 10px 14px; border: 2px solid #fff; }}
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
print("built", len(SC), "scenes;", "fallbacks:", {k: not v for k, v in HAVE.items()})
