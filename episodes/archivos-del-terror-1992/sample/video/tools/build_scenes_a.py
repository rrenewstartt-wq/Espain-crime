# Scenes 1–30 (apertura, 1992 cold morning). Executed by build.py in its namespace.
# Each scene: S(html=content under the grade, fg=graphics above the grade, js=timeline, mod=three.js prop).
# Comment "/*cut*/" marks an internal cut; every one is a change of material, crop or insert.

# ------------------------------------------------------------------ date card (G1)
DATE_CSS = f"""
.dc-line{{position:absolute;left:0;white-space:pre;font-family:"Courier Prime",monospace}}
.dc-d{{color:{ACC};font-size:128px;font-weight:700;letter-spacing:.02em}}
.dc-p{{color:#eef0ee;font-size:60px;font-weight:400;letter-spacing:.24em}}
.dc-cur{{display:inline-block;width:.55em;height:.9em;background:#eef0ee;vertical-align:-.08em;margin-left:.06em}}
"""


def date_card(p, d, part):
    line1, line2 = "22 · XII · 1992", "LAMBARÉ, PARAGUAY"
    x1 = (1920 - len(line1) * 0.6 * 128) / 2
    l1, n1 = typed(p, "a", line1)
    l2, n2 = typed(p, "b", line2)
    cur = f'<span id="{p}-cur" class="dc-cur"></span>'
    if part == 1:
        js = f"type('a', {n1}, 0.30, {1.75 / n1:.4f}); blink('cur', 0, {d}, 0.26); shot('fgc', 0, {d}, [1,0,0], [1.03,0,0]);"
        body = f'<div class="dc-line dc-d" style="left:{x1:.0f}px;top:400px">{l1}{cur}</div>'
    else:
        js = (f"for (let i = 0; i < {n1}; i++) tl.set(q('a' + i), {{ display: 'inline' }}, 0);"
              f"type('b', {n2}, 0.05, {0.85 / n2:.4f}); blink('cur', 0, {d}, 0.26); shot('fgc', 0, {d}, [1.03,0,0], [1.09,0,-6]);")
        body = (f'<div class="dc-line dc-d" style="left:{x1:.0f}px;top:400px">{l1}</div>'
                f'<div class="dc-line dc-p" style="left:{x1 + 8:.0f}px;top:570px">{l2}{cur}</div>')
    return S(fg=f'<div id="{p}-fgc" class="ao-full" style="transform-origin:50% 50%">{body}</div>', js=js, css=DATE_CSS)


@scene(1)
def s01(p, d):
    return date_card(p, d, 1)


@scene(2)
def s02(p, d):
    return date_card(p, d, 2)


# ------------------------------------------------------------------ maps (Natural Earth on old-map paper, handwritten names)
def map_pt(name):
    return MAP["places"][name]


def map_svg(p, hi=(), extra="", labels=True):
    paths = []
    for name, dd in MAP["countries"].items():
        if name in ("Southern Patagonian Ice Field",):
            continue
        cls = "pg" if name == "Paraguay" else ("hi" if name in hi else "ld")
        paths.append(f'<path id="{p}-c-{name.split()[0].lower()}" class="{p}{cls}" d="{dd}"/>')
    riv = "".join(f'<path d="{x}"/>' for x in MAP["rivers"])
    grat = []
    for lon in range(-85, -25, 5):
        x = (lon + 86.0) * 72 * math.cos(math.radians(25))
        grat.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{MAP["h"]}"/>')
    for lat in range(5, -60, -5):
        y = (8.0 - lat) * 72
        grat.append(f'<line x1="0" y1="{y:.0f}" x2="{MAP["w"]}" y2="{y:.0f}"/>')
    names = {"ARGENTINA": "Argentina", "URUGUAY": "Uruguay", "CHILE": "Chile", "PARAGUAY": "Paraguay", "BRASIL": "Brasil", "BOLIVIA": "Bolivia"}
    lab = "".join(f'<text x="{x:.0f}" y="{y:.0f}" id="{p}-lb-{n.lower()}" class="{p}lb">{names[n]}</text>'
                  for n, (x, y) in MAP["labels"].items()) if labels else ""
    return f'''<svg viewBox="0 0 {MAP["w"]} {MAP["h"]}" width="{MAP["w"]}" height="{MAP["h"]}" style="position:absolute;left:0;top:0;overflow:visible">
<defs><pattern id="{p}-pl" patternUnits="userSpaceOnUse" width="2048" height="2048"><image href="assets/tex/oldmap_land.jpg" width="2048" height="2048"/></pattern>
<pattern id="{p}-ps" patternUnits="userSpaceOnUse" width="2048" height="2048"><image href="assets/tex/oldmap_sea.jpg" width="2048" height="2048"/></pattern>
<pattern id="{p}-hatch" patternUnits="userSpaceOnUse" width="26" height="26" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="26" stroke="{ACC}" stroke-width="5"/></pattern></defs>
<rect x="-4000" y="-4000" width="{MAP["w"] + 8000}" height="{MAP["h"] + 8000}" fill="url(#{p}-ps)"/>
<g stroke="rgba(30,40,44,.28)" stroke-width="2">{"".join(grat)}</g>
<g style="filter:drop-shadow(0 0 6px rgba(20,30,34,.5))">{"".join(paths)}</g>
<g fill="none" stroke="#3f6676" stroke-width="2.6" opacity=".7">{riv}</g>
<g>{lab}</g>{extra}</svg>'''


def map_css(p):
    return f"""
.{p}ld,.{p}hi{{fill:url(#{p}-pl);stroke:#2f2a22;stroke-width:2.4;stroke-dasharray:10 6}}
.{p}pg{{fill:url(#{p}-hatch);fill-opacity:.32;stroke:{ACC};stroke-width:6}}
.{p}hi.on{{fill:url(#{p}-hatch);fill-opacity:.28;stroke:{ACC};stroke-width:5;stroke-dasharray:none}}
.{p}lb{{font:700 84px "Caveat",cursive;fill:#2b261e;text-anchor:middle;opacity:.85}}
"""


def cam_center(px, py, s):
    return round(960 - px * s, 1), round(540 - py * s, 1)


@scene(3)
def s03(p, d):
    ax, ay = map_pt("Asunción")
    x0, y0 = cam_center(MAP["w"] * 0.5, MAP["h"] * 0.5, 0.25)
    x1, y1 = cam_center(ax, ay, 1.15)
    x2, y2 = cam_center(ax, ay, 1.3)
    extra = (f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="13" fill="{ACC}" stroke="#0b1a1a" stroke-width="5"/>'
             f'<circle id="{p}-ring" cx="{ax:.0f}" cy="{ay:.0f}" r="13" fill="none" stroke="{ACC}" stroke-width="5"/>'
             f'<text x="{ax + 34:.0f}" y="{ay + 16:.0f}" style="font:700 70px Caveat;fill:#1d1a15">Asunción</text>')
    html = f'<div id="{p}-cam" class="ao-cam" style="transform-origin:0 0" data-layout-allow-overflow>{map_svg(p, extra=extra)}</div>'
    js = f"""tl.set(q('cam'), {{ x: {x0}, y: {y0}, scale: 0.25 }}, 0);
tl.to(q('cam'), {{ x: {x1}, y: {y1}, scale: 1.15, duration: 0.62, ease: 'expo.inOut' }}, 0.05);
tl.fromTo(q('cam'), {{ filter: 'blur(0px)' }}, {{ filter: 'blur(9px)', duration: 0.3, ease: 'power2.in', yoyo: true, repeat: 1 }}, 0.06);
tl.to(q('cam'), {{ x: {x2}, y: {y2}, scale: 1.3, duration: {d - 0.67:.2f}, ease: 'none' }}, 0.67);
tl.fromTo(q('ring'), {{ attr: {{ r: 13 }}, opacity: 1 }}, {{ attr: {{ r: 90 }}, opacity: 0, duration: 0.7, ease: 'power2.out' }}, 0.62); tag(0.5);"""
    return S(html, js, map_css(p), fg=tag_html(p, "MAPA · elaboración propia, datos Natural Earth", src=True))


@scene(4)
def s04(p, d):
    # M2 1536x1792 at 1.25 fills the width. Centre of Asunción (746,527); 4 km = 463 px (scale of the tiles).
    s = 1.25
    cx, cy, R4 = 746, 527, 463
    lx, ly = 865, 1300                                   # direction of the printed "Lambaré" label
    L = math.hypot(lx - cx, ly - cy)
    ex, ey = cx + (lx - cx) / L * R4, cy + (ly - cy) / L * R4  # 4 km point on the radius toward Lambaré
    y0, y1 = -330, -520
    html = f'''<div id="{p}-cam" class="ao-cam" style="transform-origin:0 0" data-layout-allow-overflow>
<img src="assets/map/asuncion_lambare_osm_dark.png" style="position:absolute;left:0;top:0;width:1536px;height:1792px;filter:brightness(1.25) contrast(1.15)" alt="">
<svg viewBox="0 0 1536 1792" width="1536" height="1792" style="position:absolute;left:0;top:0;overflow:visible">
<circle id="{p}-circ" cx="{cx}" cy="{cy}" r="{R4}" fill="none" stroke="{ACC}" stroke-width="5" stroke-dasharray="2910" stroke-dashoffset="2910" transform="rotate(80 {cx} {cy})"/>
<line id="{p}-rad" x1="{cx}" y1="{cy}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{ACC}" stroke-width="4" stroke-dasharray="463" stroke-dashoffset="463"/>
<circle cx="{cx}" cy="{cy}" r="11" fill="{ACC}" stroke="#061413" stroke-width="4"/><circle cx="{ex:.0f}" cy="{ey:.0f}" r="9" fill="{ACC}" stroke="#061413" stroke-width="4"/>
<text x="{cx + 26}" y="{cy - 22}" style="font:700 30px 'IBM Plex Mono';fill:#f2f4f3;letter-spacing:.12em;paint-order:stroke;stroke:#05080a;stroke-width:8px">CENTRO DE ASUNCIÓN</text>
<text id="{p}-km" x="{(cx + ex) / 2 + 24:.0f}" y="{(cy + ey) / 2:.0f}" style="font:700 40px 'IBM Plex Mono';fill:{ACC};paint-order:stroke;stroke:#05080a;stroke-width:9px">4 km</text>
<text id="{p}-lam" x="{ex + 30:.0f}" y="{ey + 14:.0f}" style="font:800 60px 'Barlow Condensed';fill:#fff;letter-spacing:.05em;paint-order:stroke;stroke:#05080a;stroke-width:10px">LAMBARÉ</text>
</svg></div>'''
    js = f"""shot('cam', 0, {d}, [{s},0,{y0}], [{s},0,{y1}]);
tl.to(q('circ'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.7, ease: 'power2.inOut' }}, 0.05);
tl.to(q('rad'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.6, ease: 'power2.inOut' }}, 0.35);
tl.fromTo(q('km'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.6); tl.fromTo(q('lam'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.85); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "MAPA · © OpenStreetMap contributors", src=True))


@scene(5)
def s05(p, d):
    cells = []
    for i, day in enumerate(range(19, 28)):
        x = 150 + i * 182
        cells.append(f'<div style="position:absolute;left:{x}px;top:380px;width:166px;height:220px;{PAPER(f"{-i * 166}px 0", "2400px 1600px")};'
                     f'box-shadow:0 12px 26px rgba(0,0,0,.55);text-align:center;border-top:30px solid #1c2730">'
                     f'<div style="font:400 120px/1.25 Anton;color:#22282c">{day}</div>'
                     f'<div style="font:700 22px Courier Prime;letter-spacing:.2em;color:#4a4c4a">{"HOY" if day == 22 else ("NAVIDAD" if day == 25 else "DIC")}</div></div>')
    a = f'''<div id="{p}-A" class="ao-full" style="{DESK()}">
<div id="{p}-strip" class="ao-full">{"".join(cells)}</div></div>'''
    b = f'''<div id="{p}-B" class="ao-full" style="opacity:0;{DESK()}">
<div style="position:absolute;left:1180px;top:120px;width:560px;height:760px;{PAPER()};transform:rotate(4deg);box-shadow:0 40px 80px rgba(0,0,0,.6)">
<div style="height:96px;background:#1c2730"></div><div style="text-align:center;font:400 380px/1.25 Anton;color:#22282c">25</div>
<div style="text-align:center;font:700 40px Courier Prime;letter-spacing:.3em;color:#3a3c3a">NAVIDAD</div></div></div>'''
    fg = f'''<svg id="{p}-brkw" width="1920" height="1080" style="position:absolute;left:0;top:0"><path id="{p}-brk" d="M{150 + 3 * 182 + 83},640 L{150 + 3 * 182 + 83},690 L{150 + 6 * 182 + 83},690 L{150 + 6 * 182 + 83},640" fill="none" stroke="{ACC}" stroke-width="8" stroke-dasharray="700" stroke-dashoffset="700"/>
<rect x="{150 + 3 * 182 - 6}" y="374" width="178" height="232" fill="none" stroke="{ACC}" stroke-width="5"/></svg>
<div id="{p}-cnt" style="position:absolute;left:150px;top:300px;opacity:0;white-space:nowrap"><div class="ao-unit" style="font-size:120px">FALTAN</div><span id="{p}-n" class="ao-num" style="font-size:360px">3</span><span class="ao-unit" style="font-size:150px"> DÍAS</span></div>'''
    js = f"""tl.fromTo(q('strip'), {{ x: 120 }}, {{ x: 0, duration: 0.9, ease: 'power2.out' }}, 0); tl.fromTo(q('brkw'), {{ x: 120 }}, {{ x: 0, duration: 0.9, ease: 'power2.out' }}, 0);
tl.to(q('brk'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.5, ease: 'power2.inOut' }}, 0.3);
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 0.9); tl.set(q('B'), {{ opacity: 1 }}, 0.9); tl.set(q('brkw'), {{ opacity: 0 }}, 0.9); tl.set(q('cnt'), {{ opacity: 1 }}, 0.9);
tl.set(q('n'), {{ textContent: '5' }}, 0.9); tl.set(q('n'), {{ textContent: '4' }}, 1.0); tl.set(q('n'), {{ textContent: '3' }}, 1.1);
shot('B', 0.9, {d}, [1.0,0,0], [1.05,-20,0]);"""
    return S(a + b, js, fg=fg)


@scene(6)
def s06(p, d):
    page = f'''<div style="position:absolute;left:560px;top:150px;width:800px;height:820px;{PAPER()};box-shadow:0 40px 80px rgba(0,0,0,.65);transform:rotate(-3deg)">
<div style="height:110px;background:#1c2730;display:flex;align-items:center;justify-content:center;font:700 56px 'Courier Prime';letter-spacing:.3em;color:#e9ece9">DICIEMBRE</div>
<div style="text-align:center;font:400 380px/1.1 Anton;color:#1d2226;margin-top:20px">22</div>
<div style="text-align:center;font:700 52px 'Courier Prime';letter-spacing:.32em;color:#2d3236">MARTES · 1992</div>
<div style="position:absolute;left:-40px;right:-40px;top:-18px;height:30px;display:flex;justify-content:space-around">{"".join('<span style="width:22px;height:46px;border-radius:11px;background:#8d969b;box-shadow:inset 0 -6px 8px rgba(0,0,0,.45)"></span>' for _ in range(8))}</div></div>'''
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{page}
<div id="{p}-rays" style="position:absolute;left:-600px;top:-500px;width:3000px;height:2200px;mix-blend-mode:soft-light;opacity:.9;
background:repeating-linear-gradient(115deg,rgba(255,244,222,0) 0px,rgba(255,244,222,0) 110px,rgba(255,240,214,.55) 170px,rgba(255,244,222,0) 250px);filter:blur(16px)"></div></div>'''
    js = f"""shot('cam', 0, 0.9, [1.0,0,0], [1.04,-10,0]); /*cut*/ shot('cam', 0.9, {d}, [2.0,520,520,-3], [2.08,520,530,-3]);
tl.fromTo(q('rays'), {{ x: -500 }}, {{ x: 300, duration: {d}, ease: 'none' }}, 0); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


def print_html(p, x, y, w, h, rot, bgpos, bgsize, img="assets/img/stroessner_sepia.jpg"):
    return (f'<div id="{p}-print" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#efe6d2;padding:22px;'
            f'box-shadow:0 40px 90px rgba(0,0,0,.7);transform:rotate({rot}deg)"><div style="width:100%;height:100%;background:url({img}) {bgpos} / {bgsize} no-repeat"></div></div>')


@scene(7)
def s07(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>
<div style="position:absolute;left:200px;top:120px;width:600px;height:860px;{PAPER()};transform:rotate(-8deg);opacity:.55;box-shadow:0 30px 60px rgba(0,0,0,.6)"></div>
{print_html(p, 660, 40, 620, 940, -2, "50% 10%", "cover")}</div>'''
    js = f"""shot('cam', 0, 0.8, [1.0,0,0], [1.04,0,0]); /*cut*/ shot('cam', 0.8, {d}, [1.9,40,560], [1.96,40,575]); lt(0.15); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "IMAGEN REAL · Retrato oficial, 1954", src=True) + lt_html(p, "Alfredo Stroessner", "gobernó Paraguay 1954–1989"))


TL_CSS = f"""
.tl-axis{{position:absolute;height:6px;background:#22201c;transform-origin:0 50%}}
.tl-fill{{position:absolute;height:6px;background:{ACC};transform-origin:0 50%}}
.tl-dot{{position:absolute;width:36px;height:36px;border-radius:50%;border:6px solid {ACC};background:#101214;margin:-15px 0 0 -18px}}
.tl-lab{{position:absolute;font:700 42px 'Courier Prime';letter-spacing:.1em;color:#1d1c19;white-space:nowrap;transform:translateX(-50%)}}
"""


@scene(8)
def s08(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>{BIGPAPER()}</div>
<div id="{p}-rip" class="ao-full" style="{DESK()};z-index:5">{print_html(p + "x", 660, 40, 620, 940, -2, "50% 10%", "cover")}</div>'''
    fg = f'''<div id="{p}-g" class="ao-full">
<div id="{p}-axis" class="tl-axis" style="left:360px;top:600px;width:1200px"></div><div id="{p}-fill" class="tl-fill" style="left:360px;top:600px;width:1200px"></div>
<div class="tl-dot" style="left:360px;top:603px"></div><div id="{p}-d2" class="tl-dot" style="left:1560px;top:603px"></div>
<div class="tl-lab" style="left:360px;top:650px">3 FEB 1989</div><div style="position:absolute;left:360px;top:710px;transform:translateX(-50%);font:400 30px 'Work Sans';color:#33332e;white-space:nowrap">cae la dictadura</div>
<div class="tl-lab" style="left:1560px;top:650px">22 DIC 1992</div>
<div style="position:absolute;left:0;width:1920px;top:250px;text-align:center"><span class="ao-unit" style="font-size:120px;color:#1c1b18">CASI </span><span id="{p}-n" class="ao-num" style="font-size:230px">0</span><span class="ao-unit" style="font-size:120px;color:#1c1b18"> AÑOS</span></div></div>'''
    js = f"""tl.fromTo(q('rip'), {{ x: 0, rotation: 0 }}, {{ x: -2200, rotation: -6, duration: 0.45, ease: 'power3.in' }}, 0.1);
tl.fromTo(q('g'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.35);
tl.fromTo(q('axis'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: 'power2.out' }}, 0.4);
tl.fromTo(q('fill'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.0, ease: 'power1.inOut' }}, 0.7); count('n', 0, 4, 0.7, 1.0);
shot('cam', 0, {d}, [1.0,0,0], [1.03,0,0]);"""
    return S(html, js, TL_CSS, fg=fg)


# ------------------------------------------------------------------ three.js exterior (G4)
BLD_A = [[0, [6.0, 1.15, 17.0], [5.0, 1.2, 15.6], [0, 3.8, 0], [0, 3.7, 0]]]


def ext3d(p, d, shots, dim=False, figure=None, ffrom=None, fto=None):
    o = {"d": d, "shots": shots, "dim": dim}
    if figure:
        o.update({"figure": figure, "figFrom": ffrom, "figTo": fto})
    return {"kind": "exterior", "opts": o}


@scene(9)
def s09(p, d):
    shots = BLD_A + [[0.85, [1.6, 1.5, 7.6], [1.3, 1.5, 7.2], [0, 2.6, 0], [0, 2.6, 0]]]  # /*cut*/ door and plate through the fence
    return S(js=f"lt(0.15); tag(0.05); /*cut:0.85*/", mod=ext3d(p, d, shots),
             fg=tag_html(p, "RECREACIÓN") + lt_html(p, "Departamento de Producciones", "Policía · Lambaré"))


@scene(10)
def s10(p, d):
    shots = [[0, [1.3, 1.78, 12.9], [1.0, 1.75, 11.2], [0, 1.8, 0], [0, 1.8, 0]],
             [1.1, [-8.0, 1.3, 11.0], [-7.4, 1.3, 10.4], [0, 1.6, 2.5], [0, 1.6, 2.0]]]   # /*cut*/ wide from across the street
    return S(js="tag(0.05); /*cut:1.1*/", mod=ext3d(p, d, shots, figure="man_back", ffrom=[0.6, 0, 10.4], fto=[0.15, 0, 5.2]),
             fg=tag_html(p, "RECREACIÓN"))


def warrant(p):
    return f'''<div id="{p}-doc" style="position:absolute;left:330px;top:70px;width:1260px;height:1500px;{PAPER()};
box-shadow:0 40px 90px rgba(0,0,0,.7);padding:90px 110px;transform:rotate(1.2deg)">
<div class="ao-blurline" style="width:46%;height:26px;margin:0 auto 50px"></div>{doc_lines(5)}
<div style="font:700 58px 'Courier Prime';color:#1a1c1c;letter-spacing:.02em;margin:34px 0 8px">MARTÍN ALMADA s/ HÁBEAS DATA</div>
<div id="{p}-ul" style="height:8px;background:{ACC};width:1010px;transform-origin:0 50%"></div><div style="height:40px"></div>{doc_lines(9)}</div>'''


@scene(11)
def s11(p, d):
    html = f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{warrant(p)}</div>'
    js = f"""shot('cam', 0, 1.1, [0.78,0,60,-2], [0.82,0,50,-2]); /*cut*/ shot('cam', 1.1, {d}, [1.9,40,90,0], [2.0,10,95,0]);
tl.fromTo(q('ul'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: 'power2.inOut' }}, 1.25); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


def index_card(p, inner, x=460, y=250, w=1000, h=600, rot=-2, cid="card"):
    lines = "".join(f'<div style="position:absolute;left:0;right:0;top:{170 + k * 64}px;height:2px;background:#7d93a0;opacity:.5"></div>' for k in range(int((h - 190) / 64)))
    return f'''<div id="{p}-{cid}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:url(assets/tex/paper_grey.jpg) center/cover;
box-shadow:0 30px 70px rgba(0,0,0,.65);transform:rotate({rot}deg);padding:60px 70px">
<div style="position:absolute;left:0;right:0;top:118px;height:3px;background:#5d7a8a;opacity:.8"></div>{lines}{inner}</div>'''


@scene(12)
def s12(p, d):
    nm, n = typed(p, "t", "JOSÉ AGUSTÍN FERNÁNDEZ")
    inner = (f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f">NOMBRE</div>'
             f'<div style="font:700 62px \'Courier Prime\';color:#1a1f1f;margin-top:40px;white-space:nowrap">{nm}</div>')
    html = f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{index_card(p, inner)}</div>'
    # /*cut*/ insert: the typed surname, extreme close, ribbon ink texture
    js = f"""type('t', {n}, 0.1, 0.035); shot('cam', 0, 1.05, [1.0,0,0], [1.04,0,0]); /*cut*/ shot('cam', 1.05, {d}, [3.0,-950,360,-2], [3.08,-990,370,-2]); lt(0.25);"""
    return S(html, js, fg=lt_html(p, "José Agustín Fernández", "juez en lo criminal (1992)"))


@scene(13)
def s13(p, d):
    inner = (f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f">NOMBRE</div><div style="font:700 62px \'Courier Prime\';color:#1a1f1f;margin-top:40px;white-space:nowrap">JOSÉ AGUSTÍN FERNÁNDEZ</div>'
             f'<div id="{p}-st" class="ao-stamp" style="position:absolute;left:150px;top:300px;font-size:84px">JUEZ EN LO CRIMINAL</div>')
    html = f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow><div id="{p}-sh" class="ao-full">{index_card(p, inner, rot=1.5)}</div></div>'
    js = f"""shot('cam', 0, 0.9, [1.12,0,20], [1.16,0,20]); stampIn('st', 0.35, -6); shake('sh', 0.51, 14);
/*cut*/ shot('cam', 0.9, {d}, [2.0,-200,-130,4], [2.06,-215,-135,4]);"""
    return S(html, js)


def case_cover(p, typed_html):
    return f'''<div id="{p}-cov" style="position:absolute;left:260px;top:40px;width:1400px;height:1000px;background:#8ea4ab url(assets/tex/paper_grey.jpg) center/cover;
background-blend-mode:multiply;box-shadow:0 40px 90px rgba(0,0,0,.7);padding:70px 90px;transform:rotate(-1deg)">
<div class="ao-blurline" style="width:38%;height:24px;margin-bottom:40px;background:#26302f"></div>
<div style="display:flex;gap:40px">{"".join('<div style="flex:1;height:90px;border:3px solid rgba(30,40,42,.55)"></div>' for _ in range(3))}</div>
<div style="margin-top:60px;border-bottom:4px solid rgba(30,40,42,.65);height:110px;position:relative">
<div style="position:absolute;left:10px;bottom:16px;font:700 70px 'Courier Prime';color:#121516;white-space:nowrap">{typed_html}</div></div>
<div style="margin-top:60px">{doc_lines(5)}</div></div>'''


@scene(14)
def s14(p, d):
    t, n = typed(p, "t", "MARTÍN ALMADA s/ HÁBEAS DATA")
    html = f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{case_cover(p, t + f"""<span id="{p}-cur" style="display:inline-block;width:30px;height:62px;background:#121516;vertical-align:-6px"></span>""")}</div>'
    js = f"type('t', {n}, 0.1, {1.5 / n:.4f}); blink('cur', 0, {d}, 0.25); shot('cam', 0, {d}, [0.86,0,40,-1], [0.9,0,40,-1]); tag(0.05);"
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


@scene(15)
def s15(p, d):
    # extreme macro, shallow depth of field: sharp band on the words, blurred paper above and below
    word = f'''<div style="position:absolute;left:-200px;top:330px;width:2400px;height:420px;background:#8ea4ab url(assets/tex/paper_grey.jpg) 0 0/2400px 1600px;background-blend-mode:multiply"></div>
<div style="position:absolute;left:160px;top:400px;font:700 300px/1 'Courier Prime';color:#121516;white-space:nowrap;letter-spacing:-.01em">HÁBEAS DATA</div>'''
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#11181b" data-layout-allow-overflow>{word}
<div class="ao-full" style="background:linear-gradient(180deg,rgba(6,9,10,.92) 0%,rgba(6,9,10,0) 34%,rgba(6,9,10,0) 66%,rgba(6,9,10,.92) 100%)"></div></div>'''
    fg = f'<div id="{p}-ul" style="position:absolute;left:170px;top:720px;width:1620px;height:14px;background:{ACC};transform-origin:0 50%"></div>'
    js = f"""shot('cam', 0, {d}, [1.0,40,0,-3], [1.06,-30,0,-3]); tl.fromTo(q('cam'), {{ filter: 'blur(6px)' }}, {{ filter: 'blur(0px)', duration: 0.35 }}, 0);
tl.fromTo(q('ul'), {{ scaleX: 0, rotation: -3 }}, {{ scaleX: 1, rotation: -3, duration: 0.55, ease: 'power2.inOut' }}, 0.3); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, "RECREACIÓN"))


@scene(16)
def s16(p, d):
    words = "derecho a ver los datos que el Estado guarda sobre ti".split()
    spans = " ".join(f'<span id="{p}-w{i}" style="display:inline-block;opacity:0">{w}</span>' for i, w in enumerate(words))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#05080a" data-layout-allow-overflow>
<img src="assets/img/const1992_p42_art135_habeas_data.jpg" style="position:absolute;left:-120px;top:-520px;width:2160px;height:2796px;filter:blur(7px) brightness(.32) contrast(1.2)" alt=""></div>'''
    fg = f'''<div id="{p}-A" class="ao-full"><div style="position:absolute;left:0;width:1920px;top:360px;text-align:center;font:400 230px/1 Anton;color:#f3f1ea;letter-spacing:.02em">HÁBEAS DATA</div>
<div style="position:absolute;left:520px;width:880px;top:640px;height:12px;background:{ACC}"></div></div>
<div id="{p}-B" class="ao-full" style="opacity:0"><div style="position:absolute;left:200px;top:250px;font:400 92px/1 Anton;color:{ACC};letter-spacing:.03em">HÁBEAS DATA =</div>
<div style="position:absolute;left:200px;width:1500px;top:400px;font:400 78px/1.25 'Work Sans';color:#f3f1ea">{spans}</div></div>'''
    js = f"""tl.fromTo(q('A'), {{ opacity: 0, filter: 'blur(10px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.2 }}, 0.0);
shot('cam', 0, 0.95, [1.0,0,0], [1.04,0,0]); /*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 0.95); tl.set(q('B'), {{ opacity: 1 }}, 0.95);
shot('cam', 0.95, {d}, [1.6,500,-300,2], [1.64,490,-310,2]);
{"".join(f"tl.fromTo(q('w{i}'), {{ opacity: 0, filter: 'blur(6px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.13 }}, {1.0 + i * 0.07:.3f});" for i in range(len(words)))}"""
    return S(html, js, fg=fg)


@scene(17)
def s17(p, d):
    if HAVE["A2"]:
        html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>
{print_html(p, 660, 30, 620, 1010, 1.5, "50% 20%", "cover", "assets/img/" + PHOTO["A2"])}</div>'''
        js = f"shot('cam', 0, 1.0, [1.0,0,0], [1.04,0,0]); /*cut*/ shot('cam', 1.0, {d}, [1.45,0,330], [1.5,0,340]); lt(0.15); tag(0.05);"
        return S(html, js, fg=tag_html(p, "IMAGEN REAL · Foto: 2008, Maria Stella de Almada (CC BY-SA 4.0)", src=True) + lt_html(p, "Martín Almada", "educador"))
    t, n = typed(p, "t", "MARTÍN ALMADA")
    inner = (f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f">SOLICITANTE</div>'
             f'<div style="font:700 92px \'Courier Prime\';color:#1a1f1f;margin-top:34px;white-space:nowrap">{t}</div>'
             f'<div style="font:700 30px \'Courier Prime\';letter-spacing:.2em;color:#44514f;margin-top:54px">PROFESIÓN</div>'
             f'<div style="font:700 58px \'Courier Prime\';color:#1a1f1f;margin-top:20px">EDUCADOR</div>')
    html = f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{index_card(p, inner, x=420, y=200, w=1080, h=640, rot=2)}</div>'
    js = f"""type('t', {n}, 0.05, 0.03); shot('cam', 0, 1.0, [1.0,0,0], [1.04,0,0]); /*cut*/ shot('cam', 1.0, {d}, [2.6,700,-250,-2], [2.7,690,-260,-2]); lt(0.2);"""
    return S(html, js, fg=lt_html(p, "Martín Almada", "educador"))


def doc_page(p, img, w, h, x, y, rot=0, extra=""):
    return (f'<div id="{p}-pg" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-shadow:0 40px 90px rgba(0,0,0,.7);transform:rotate({rot}deg)">'
            f'<img src="assets/img/{img}" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px" alt="">{extra}</div>')


@scene(18)
def s18(p, d):
    html = f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{doc_page(p, "const1992_p01_portada.jpg", 1215, 1733, 352, 40, -1.5)}</div>'
    js = f"shot('cam', 0, {d}, [0.6,0,140,0], [0.82,0,220,0], 'power1.out'); whipIn('cam', 0, 260); tag(0.05);"
    return S(html, js, fg=tag_html(p, "DOCUMENTO REAL · Constitución Nacional 1992, original firmado (BACN)", src=True))


@scene(19)
def s19(p, d):
    # D2 1227x1588: art.135 heading y 546–592, body lines y 611–672 (measured on the scan)
    fg = f'''<div id="{p}-fgc" class="ao-full" style="transform-origin:0 0"><div id="{p}-box" style="position:absolute;left:180px;top:546px;width:440px;height:46px;border:6px solid {ACC}"></div>
<div id="{p}-hl1" style="position:absolute;left:408px;top:643px;width:636px;height:5px;background:{ACC};transform-origin:0 50%"></div>
<div id="{p}-hl2" style="position:absolute;left:370px;top:671px;width:674px;height:5px;background:{ACC};transform-origin:0 50%"></div></div>'''
    html = f'<div id="{p}-cam" class="ao-cam" style="transform-origin:0 0;{DESK()}" data-layout-allow-overflow>{doc_page(p, "const1992_p42_art135_habeas_data.jpg", 1227, 1588, 0, 0)}</div>'
    js = f"""shot('cam', 0, 0.8, [1.05,315,-90], [1.1,290,-120]); shot('fgc', 0, 0.8, [1.05,315,-90], [1.1,290,-120]);
/*cut*/ shot('cam', 0.8, {d}, [2.15,-545,-836], [2.25,-615,-900]); shot('fgc', 0.8, {d}, [2.15,-545,-836], [2.25,-615,-900]);
tl.fromTo(q('box'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.15);
tl.fromTo(q('hl1'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: 'power1.inOut' }}, 0.9);
tl.fromTo(q('hl2'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: 'power1.inOut' }}, 1.3); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, "DOCUMENTO REAL · Constitución 1992, art. 135 (BACN)", src=True))


def drawer_svg(x, y, label="POLICÍA"):
    return f'''<g transform="translate({x},{y})" fill="none" stroke="#1d1f1e" stroke-width="6"><rect x="0" y="0" width="420" height="520"/>
{"".join(f'<rect x="30" y="{30 + k * 160}" width="360" height="130" stroke-width="4"/><line x1="170" y1="{88 + k * 160}" x2="250" y2="{88 + k * 160}" stroke-width="10"/>' for k in range(3))}
<text x="210" y="600" text-anchor="middle" stroke="none" fill="#1d1f1e" style="font:700 54px 'Courier Prime';letter-spacing:.2em">{label}</text></g>'''


@scene(20)
def s20(p, d):
    # hand-drawn diagram on a sheet of paper (ink), teal arrow and lock outline drawn on top
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>
<div style="position:absolute;left:150px;top:70px;width:1620px;height:940px;{PAPER()};box-shadow:0 40px 80px rgba(0,0,0,.6);transform:rotate(-1deg)"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
<g transform="translate(400,700) scale(1.6)" fill="none" stroke="#1d1f1e" stroke-width="5"><circle cx="0" cy="-130" r="44"/><path d="M-80,0 Q-80,-80 0,-80 Q80,-80 80,0Z"/></g>
<text x="400" y="820" text-anchor="middle" style="font:700 44px 'Courier Prime';letter-spacing:.2em;fill:#1d1f1e">ALMADA</text>{drawer_svg(1260, 260)}</svg></div>'''
    fg = f'''<svg id="{p}-fgs" viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0;transform-origin:50% 50%">
<path id="{p}-arr" d="M560,540 L1150,540" stroke="{ACC}" stroke-width="12" stroke-dasharray="600" stroke-dashoffset="600"/>
<path id="{p}-head" d="M1150,505 L1205,540 L1150,575Z" fill="{ACC}" opacity="0"/>
<g transform="translate(1560,590)" fill="none" stroke="{ACC}" stroke-width="9"><rect x="-38" y="0" width="76" height="62"/><path d="M-24,0 L-24,-26 A24,24 0 0 1 24,-26 L24,0"/></g>
<text id="{p}-q" x="1720" y="720" style="font:400 230px Anton;fill:{ACC}" opacity="0">?</text></svg>'''
    js = f"""tl.to(q('arr'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.5, ease: 'power2.inOut' }}, 0.1); tl.set(q('head'), {{ opacity: 1 }}, 0.6);
tl.fromTo(q('q'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, 1.05);
shot('cam', 0, 1.0, [1.0,0,0], [1.03,0,0]); shot('fgs', 0, 1.0, [1.0,0,0], [1.03,0,0]);
/*cut*/ shot('cam', 1.0, {d}, [1.8,-1040,-130], [1.85,-1070,-135]); shot('fgs', 1.0, {d}, [1.8,-1040,-130], [1.85,-1070,-135]);"""
    return S(html, js, fg=fg)


@scene(21)
def s21(p, d):
    html = f'''<div id="{p}-A" class="ao-full" style="{DESK()}"></div>
<div id="{p}-B" class="ao-full" style="opacity:0;{DESK()}"><div style="position:absolute;left:180px;top:300px;width:1560px;height:480px;{PAPER()};transform:rotate(-2deg);box-shadow:0 40px 80px rgba(0,0,0,.6)"></div></div>'''
    fg = f'''<div id="{p}-fa" class="ao-full"><div style="position:absolute;left:0;width:1920px;top:260px;text-align:center;white-space:nowrap">
<span id="{p}-n" class="ao-num" style="font-size:360px">0</span><span class="ao-unit" style="font-size:150px"> DÍAS</span></div></div>
<div id="{p}-fb" class="ao-full" style="opacity:0"><div style="position:absolute;left:0;width:1920px;top:440px;text-align:center;font:700 96px 'Courier Prime';color:#1b1c1a;transform:rotate(-2deg);white-space:nowrap">14 SEP 1992 <span style="color:{ACC}">→</span> 22 DIC 1992</div>
<div style="position:absolute;left:0;width:1920px;top:580px;text-align:center;font:400 44px 'Work Sans';color:#3a3a36;transform:rotate(-2deg)">el juzgado recibe el pedido · el juez llega a Lambaré</div></div>'''
    js = f"""count('n', 0, 99, 0.05, 0.85); /*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.0); tl.set(q('fa'), {{ opacity: 0 }}, 1.0); tl.set(q('B'), {{ opacity: 1 }}, 1.0); tl.set(q('fb'), {{ opacity: 1 }}, 1.0);
shot('B', 1.0, {d}, [1.0,0,0], [1.04,-20,0]); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, "FUENTE · Poder Judicial, Archivos del Terror (2008)", src=True))


@scene(22)
def s22(p, d):
    months = ["SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    pages = "".join(f'''<div id="{p}-m{i}" style="position:absolute;left:560px;top:120px;width:800px;height:860px;{PAPER()};
box-shadow:0 30px 60px rgba(0,0,0,.6);transform-origin:50% 0;z-index:{10 - i}">
<div style="height:120px;background:#1c2730;display:flex;align-items:center;justify-content:center;font:700 58px 'Courier Prime';letter-spacing:.24em;color:#e9ece9">{m}</div>
<div style="text-align:center;font:400 330px/1.3 Anton;color:#1e2326">{["14", "", "", "22"][i]}</div>{"" if i in (0, 3) else '<div style="position:absolute;left:80px;top:200px;width:640px;display:grid;grid-template-columns:repeat(7,1fr);gap:14px;font:700 40px Courier Prime;color:#3a3d3c;text-align:center">' + "".join(f"<span>{k}</span>" for k in range(1, 31 if i == 2 else 32)) + "</div>"}
<div style="text-align:center;font:700 48px 'Courier Prime';letter-spacing:.3em;color:#2d3236">1992</div></div>''' for i, m in enumerate(months))
    html = f'<div id="{p}-cam" class="ao-cam" style="perspective:1600px;{DESK()}" data-layout-allow-overflow>{pages}</div>'
    js = "".join(f"tl.to(q('m{i}'), {{ rotationX: -92, duration: 0.3, ease: 'power2.in' }}, {0.35 + i * 0.4:.2f}); tl.set(q('m{i}'), {{ opacity: 0 }}, {0.65 + i * 0.4:.2f});" for i in range(3))
    js += f"shot('cam', 0, {d}, [1.0,0,0], [1.08,0,0]);"
    return S(html, js)


@scene(23)
def s23(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>
<div style="position:absolute;left:380px;top:60px;width:1160px;height:1400px;{PAPER()};box-shadow:0 40px 90px rgba(0,0,0,.7);padding:90px 100px;transform:rotate(-1.2deg)">
<div style="font:700 64px 'Courier Prime';letter-spacing:.16em;color:#1a1d1d">RESPUESTA OFICIAL</div><div style="height:5px;background:#1a1d1d;margin:16px 0 50px;width:640px"></div>
{doc_lines(4)}<div id="{p}-key" style="font:700 60px 'Courier Prime';color:#111414;margin:10px 0 36px;white-space:nowrap">los documentos desaparecieron</div>{doc_lines(6)}</div></div>'''
    fg = f'<div style="position:absolute;left:176px;bottom:120px;font:700 italic 36px \'Work Sans\';color:#fff;background:rgba(5,7,9,.75);padding:12px 22px;border-left:10px solid {ACC}">según recuerda el juez (ABC Color, 2019)</div>'
    js = f"""shot('cam', 0, 1.2, [0.9,0,90,0], [0.93,0,80,0]); /*cut*/ shot('cam', 1.2, {d}, [1.75,-40,-200,1], [1.8,-120,-205,1]);
tl.fromTo(q('key'), {{ filter: 'blur(6px)' }}, {{ filter: 'blur(0px)', duration: 0.4 }}, 0.3); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, "RECREACIÓN"))


@scene(24)
def s24(p, d):
    icons = "".join(f'<div id="{p}-f{i}" style="position:absolute;left:{1240 + (i % 4) * 80}px;top:{300 + (i // 4) * 100}px;width:64px;height:82px;{PAPER()};border:3px solid #22201c;box-shadow:0 8px 12px rgba(0,0,0,.35)"></div>' for i in range(8))
    html = f'<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>{BIGPAPER()}{icons}</div>'
    fg = f'''<div id="{p}-g" class="ao-full" style="transform-origin:50% 50%"><div class="tl-axis" style="left:300px;top:620px;width:1320px"></div>
<div class="tl-dot" style="left:480px;top:623px"></div><div id="{p}-ph" class="tl-dot" style="left:1560px;top:623px;background:{ACC}"></div>
<div class="tl-lab" style="left:1560px;top:670px">22 DIC 1992</div>
<div id="{p}-rw" style="position:absolute;left:0;width:1920px;top:160px;text-align:center;font:700 54px 'Courier Prime';letter-spacing:.4em;color:#22201c">◀◀ 1992 → 1989</div>
<div id="{p}-st" class="ao-stampT" style="position:absolute;left:300px;top:700px;font-size:76px">2–3 FEB 1989 · GOLPE</div></div>'''
    js = f"""tl.fromTo(q('ph'), {{ x: 0 }}, {{ x: -1080, duration: 0.8, ease: 'power3.inOut' }}, 0.1); stampIn('st', 0.95, -3);
{"".join(f"tl.to(q('f{i}'), {{ x: {(i * 137) % 300 - 150}, y: {-200 - (i * 53) % 200}, rotation: {(i * 47) % 90 - 45}, opacity: 0, duration: 0.8, ease: 'power2.out' }}, {0.2 + i * 0.03:.2f});" for i in range(8))}
shot('cam', 0, 1.2, [1.0,0,0], [1.03,0,0]); shot('g', 0, 1.2, [1.0,0,0], [1.03,0,0]);
/*cut*/ shot('cam', 1.2, {d}, [2.2,820,-280,-2], [2.25,810,-290,-2]); shot('g', 1.2, {d}, [2.2,820,-280,-2], [2.25,810,-290,-2]);"""
    return S(html, js, TL_CSS, fg=fg)


@scene(25)
def s25(p, d):
    return S(js="tag(0.05); /*cut:1.15*/", mod={"kind": "drawer", "opts": {"d": d, "cut": 1.15}}, fg=tag_html(p, "RECREACIÓN"))


@scene(26)
def s26(p, d):
    shots = [[0, [0.0, 1.6, 19.0], [0.0, 1.7, 15.5], [0, 3.4, 0], [0, 3.2, 0]]]
    st = f'<div id="{p}-st" class="ao-stampT" style="position:absolute;left:600px;top:250px;font-size:96px;background:rgba(5,7,9,.6)">VERSIÓN POLICIAL</div>'
    return S(js="stampIn('st', 0.2, -3); tag(0.05);", mod=ext3d(p, d, shots, dim=True), fg=st + tag_html(p, "RECREACIÓN"))


@scene(27)
def s27(p, d):
    t, n = typed(p, "t", "NADA QUE BUSCAR")
    w = 15 * 0.6 * 150
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>
<div style="position:absolute;left:220px;top:250px;width:1480px;height:620px;{PAPER()};box-shadow:0 40px 80px rgba(0,0,0,.6);transform:rotate(1deg)"></div>
<div style="position:absolute;left:{(1920 - w) / 2:.0f}px;top:470px;font:700 150px 'Courier Prime';color:#141616;white-space:nowrap">{t}<span id="{p}-cur" style="display:inline-block;width:80px;height:130px;background:#141616;vertical-align:-14px"></span></div></div>'''
    js = f"type('t', {n}, 0.05, 0.05); blink('cur', 0, {d}, 0.25); shot('cam', 0, 0.85, [1.0,0,0], [1.03,0,0]); /*cut*/ shot('cam', 0.85, {d}, [2.4,-760,-100,-2], [2.46,-800,-100,-2]);"
    return S(html, js)


# ------------------------------------------------------------------ doorway scenes: backlit 2.5D (G4)
def doorway(p, layers, light="rgba(236,242,246,1)"):
    return f'''<div id="{p}-cam" class="ao-cam" style="background:#040506" data-layout-allow-overflow>
<div class="ao-full" style="background:url(assets/tex/concrete.jpg) 0 0/1400px 700px;filter:brightness(.16) contrast(1.3)"></div>
<div id="{p}-door" style="position:absolute;left:690px;top:90px;width:540px;height:960px;background:radial-gradient(ellipse at 50% 55%,{light},rgba(206,220,228,.95) 55%,rgba(150,170,182,.9))"></div>
<div style="position:absolute;left:560px;top:-60px;width:800px;height:1200px;background:radial-gradient(ellipse at 50% 55%,rgba(230,240,246,.55),rgba(230,240,246,0) 65%);mix-blend-mode:screen"></div>
<div style="position:absolute;left:640px;top:60px;width:50px;height:1000px;background:#08090a"></div><div style="position:absolute;left:1230px;top:60px;width:50px;height:1000px;background:#08090a"></div>
<div style="position:absolute;left:640px;top:40px;width:640px;height:56px;background:#08090a"></div>
{layers}{smoke_html(p, 1, 0.18, "mix-blend-mode:screen")}</div>'''


def fig_img(p, key, name, x, y, h, extra=""):
    w = h * 900 / 1600
    return f'<img id="{p}-{key}" src="assets/fig/{name}.png" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;{extra}" alt="">'


@scene(28)
def s28(p, d):
    rim = "filter:drop-shadow(0 0 10px rgba(236,244,248,.55)) drop-shadow(0 0 2px rgba(255,255,255,.8))"
    layers = (fig_img(p, "g", "guard", 740, 230, 860, rim) +
              fig_img(p, "j", "man_back", -320, 160, 1500, "filter:blur(14px) brightness(.6)"))
    html = doorway(p, layers)
    js = f"""tl.fromTo(q('g'), {{ y: 30 }}, {{ y: 0, duration: 0.4, ease: 'power3.out' }}, 0.2);
shot('cam', 0, 1.25, [1.0,0,0], [1.04,0,0]); /*cut*/ shot('cam', 1.25, {d}, [2.4,-400,680], [2.46,-415,700]); lt(0.2); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "RECREACIÓN") + lt_html(p, "Oficial de guardia", "Policía · entrada del depósito"))


@scene(29)
def s29(p, d):
    rim = "filter:drop-shadow(0 0 10px rgba(236,244,248,.5))"
    layers = (fig_img(p, "g", "guard", 800, 300, 760, "filter:blur(6px) brightness(.9)") +
              fig_img(p, "j", "judge", 160, 120, 1300, rim))
    html = doorway(p, layers)
    paper = f'''<div id="{p}-B" class="ao-full" style="opacity:0;background:#06080a">
<div style="position:absolute;left:520px;top:90px;width:900px;height:900px;background:radial-gradient(circle,rgba(236,244,248,.9),rgba(236,244,248,0) 70%)"></div>
<div style="position:absolute;left:600px;top:150px;width:760px;height:900px;{PAPER()};transform:rotate(-6deg);box-shadow:0 0 60px rgba(236,244,248,.5);padding:70px 70px">
{doc_lines(4)}<div style="font:700 40px 'Courier Prime';color:#151717;margin:20px 0 30px;white-space:nowrap">MARTÍN ALMADA s/ HÁBEAS DATA</div>{doc_lines(7)}</div>
<div style="position:absolute;left:460px;top:780px;width:300px;height:420px;border-radius:120px 120px 40px 40px;background:#090a0b;transform:rotate(-20deg);filter:blur(3px)"></div></div>'''
    js = f"""tl.fromTo(q('j'), {{ y: 40 }}, {{ y: 0, duration: 0.4, ease: 'power3.out' }}, 0.1); shot('cam', 0, 1.25, [1.0,0,0], [1.04,10,0]);
/*cut*/ tl.set(q('B'), {{ opacity: 1 }}, 1.25); shot('B', 1.25, {d}, [1.0,0,0], [1.05,0,-10]); tag(0.05);"""
    return S(html + paper, js, fg=tag_html(p, "RECREACIÓN"))


@scene(30)
def s30(p, d):
    cards = [("GOLPE 1989", -560, -6), ("SIN DOCUMENTOS", 0, 3), ("NADA QUE BUSCAR", 560, -2)]
    html = f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>' + "".join(
        f'''<div id="{p}-k{i}" style="position:absolute;left:{960 + x - 260}px;top:380px;width:520px;height:320px;{PAPER()};
box-shadow:0 26px 50px rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;text-align:center;font:400 66px/1.05 Anton;color:#1a1d1d;padding:20px;transform:rotate({r}deg)">
<span>{t}</span></div>''' for i, (t, x, r) in enumerate(cards)) + "</div>"
    js = "".join(f"tl.fromTo(q('k{i}'), {{ y: {(-1) ** i * 700}, rotation: {(-1) ** i * 20} }}, {{ y: 0, rotation: {cards[i][2]}, duration: 0.4, ease: 'expo.out' }}, {0.05 + i * 0.3:.2f});" for i in range(3))
    js += f"shot('cam', 0, 0.75, [2.0,1100,0,-4], [2.05,1110,0,-4]); /*cut*/ shot('cam', 0.75, {d}, [0.95,0,0], [0.92,0,0]); shake('cam', 1.3, 10);"
    return S(html, js)
