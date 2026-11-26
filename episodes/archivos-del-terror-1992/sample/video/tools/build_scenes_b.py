# Scenes 31–65 (discovery under tungsten, questions, title, origen 1954). Executed by build.py.

@scene(31)
def s31(p, d):
    return S(js="tag(0.05);", mod={"kind": "stairs", "opts": {"d": d, "mode": "stairs"}}, fg=tag_html(p, "RECREACIÓN"))


# padlock photo (A6, 2000x1333): never shown above 1.5x of its pixels
PAD_W = 3000
PAD_POLY = [(854, 536), (864, 378), (903, 313), (976, 306), (1028, 346), (1068, 411), (1173, 464), (1265, 503), (1331, 681), (989, 767)]


def padlock_img(extra="", left=-840, top=-240, w=PAD_W):
    return f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{w * 1333 / 2000:.0f}px;background:url(assets/img/padlocks_cool.jpg) 0 0/100% 100%;{extra}"></div>'


@scene(32)
def s32(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030303" data-layout-allow-overflow>
<div style="position:absolute;left:-180px;top:-120px;width:2280px;height:1520px;background:url(assets/img/padlocks_cool.jpg) 0 0/100% 100%;filter:brightness(.75) contrast(1.25) sepia(.35)"></div>
<div id="{p}-beam" class="ao-full" style="background:radial-gradient(circle at 56% 38%,rgba(0,0,0,0) 10%,rgba(0,0,0,.86) 34%,rgba(0,0,0,.97) 60%)"></div></div>'''
    js = f"shot('cam', 0, {d}, [1.0,0,0], [1.12,-60,40], 'power1.inOut'); tl.fromTo(q('beam'), {{ x: -220, y: 80 }}, {{ x: 0, y: 0, duration: 0.7, ease: 'power2.out' }}, 0); tag(0.05);"
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


CUTTER = '''<svg id="{p}-cut" viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0;overflow:visible;filter:blur(2px)">
<defs><linearGradient id="{p}-cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8c7a64"/><stop offset=".35" stop-color="#2a2622"/><stop offset="1" stop-color="#0b0a09"/></linearGradient></defs>
<g fill="url(#{p}-cg)"><path d="M2000,880 Q1640,700 1290,500 L1318,462 Q1680,640 2020,820Z"/><path d="M2000,560 Q1640,500 1300,470 L1312,430 Q1660,450 2020,500Z"/>
<path d="M1290,500 L1180,452 Q1170,430 1196,420 L1318,462Z"/><path d="M1300,470 L1190,410 Q1186,388 1212,382 L1312,430Z"/></g></svg>'''


@scene(33)
def s33(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030303" data-layout-allow-overflow>
{padlock_img("filter:brightness(.85) contrast(1.25) sepia(.3)")}
<div class="ao-full" style="background:radial-gradient(circle at 52% 48%,rgba(0,0,0,0) 22%,rgba(0,0,0,.8) 62%)"></div>{CUTTER.replace("{p}", p)}</div>'''
    js = f"""{"".join(f"tl.to(q('cam'), {{ x: {((i * 37) % 13) - 6}, y: {((i * 53) % 11) - 5}, rotation: {(((i * 29) % 7) - 3) * 0.15:.2f}, duration: 0.1, ease: 'sine.inOut' }}, {i * 0.1:.2f});" for i in range(int(d / 0.1)))}
tl.fromTo(q('cut'), {{ x: 520 }}, {{ x: 0, duration: 0.7, ease: 'power3.out' }}, 0.15); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


@scene(34)
def s34(p, d):
    poly = ",".join(f"{x}px {y}px" for x, y in PAD_POLY)
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030303" data-layout-allow-overflow>
<div id="{p}-bg" class="ao-full">{padlock_img("filter:brightness(.85) contrast(1.25) sepia(.3)")}</div>
<div id="{p}-lock" class="ao-full" style="clip-path:polygon({poly})">{padlock_img("filter:brightness(.95) contrast(1.25) sepia(.3)")}</div>
<div class="ao-full" style="background:radial-gradient(circle at 52% 48%,rgba(0,0,0,0) 22%,rgba(0,0,0,.8) 62%)"></div>{CUTTER.replace("{p}", p)}
<div id="{p}-fl" class="ao-full" style="background:#fff3e2;opacity:0"></div></div>'''
    # the break: one bright frame (the spark of the cutter, shots.md row 34), the lock drops out of frame
    js = f"""tl.set(q('fl'), {{ opacity: .85 }}, 0.25); tl.set(q('fl'), {{ opacity: .25 }}, 0.25 + 1 / 30); tl.set(q('fl'), {{ opacity: 0 }}, 0.25 + 2 / 30);
tl.set(q('bg'), {{ filter: 'brightness(.6)', x: -60, y: 260 }}, 0.25); tl.set(q('cut'), {{ x: 60, y: -30, rotation: -4 }}, 0.25);
tl.fromTo(q('lock'), {{ y: 0, rotation: 0, filter: 'blur(0px)' }}, {{ y: 1000, rotation: 24, filter: 'blur(6px)', duration: 0.75, ease: 'power2.in' }}, 0.27);
shake('cam', 0.26, 24); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


@scene(35)
def s35(p, d):
    return S(js="tag(0.05);", mod={"kind": "stairs", "opts": {"d": d, "mode": "door"}}, fg=tag_html(p, "RECREACIÓN"))


def paper_pile(seed, n=70, area=(0, 200, 1920, 1080), pal="tung"):
    r = random.Random(seed)
    tints = ["#f0e2c4", "#e4d3b0", "#cdbf9e", "#b8a582", "#d9c8a4", "#8f7f66", "#e9dcbc"]
    out = []
    for i in range(n):
        w, h = r.randint(220, 460), r.randint(150, 330)
        x, y = r.uniform(area[0] - 100, area[2] - 200), r.uniform(area[1], area[3] - 60)
        rot = r.uniform(-28, 28)
        t = r.choice(tints)
        lines = "".join(f'<div style="height:6px;margin:14px 18px 0;background:rgba(50,44,36,.35);width:{r.randint(40, 90)}%"></div>' for _ in range(r.randint(0, 5)))
        out.append(f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w}px;height:{h}px;background:{t} url(assets/tex/paper_{pal}.jpg) {r.randint(0, 900)}px {r.randint(0, 600)}px;background-blend-mode:multiply;'
                   f'transform:rotate({rot:.1f}deg);box-shadow:0 10px 22px rgba(0,0,0,.55);padding-top:6px">{lines}</div>')
    return "".join(out)


TUNG_TOP = "radial-gradient(ellipse at 50% -10%,rgba(255,196,120,.42),rgba(255,180,100,0) 55%)"


@scene(36)
def s36(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#070403" data-layout-allow-overflow>
<div id="{p}-l0" class="ao-full" style="filter:brightness(.35) blur(4px)">{paper_pile(36, 60, (0, 60, 1920, 900))}</div>
<div id="{p}-l1" class="ao-full" style="filter:brightness(.7)">{paper_pile(37, 50, (0, 360, 1920, 1080))}</div>
<div id="{p}-l2" class="ao-full" style="filter:brightness(.95)">{paper_pile(38, 26, (0, 700, 1920, 1250))}</div>
<div class="ao-full" style="background:{TUNG_TOP};mix-blend-mode:screen"></div>
<div class="ao-full" style="background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0) 40%,rgba(0,0,0,0) 70%,rgba(0,0,0,.6))"></div>
{dust_html(p, 34, (200, 50, 1700, 600), 36)}</div>'''
    js = f"""tl.fromTo(q('l0'), {{ x: 0 }}, {{ x: -30, duration: {d}, ease: 'none' }}, 0); tl.fromTo(q('l1'), {{ x: 0 }}, {{ x: -80, duration: {d}, ease: 'none' }}, 0);
tl.fromTo(q('l2'), {{ x: 0, y: 0 }}, {{ x: -170, y: -20, duration: {d}, ease: 'none' }}, 0); dust(34, 0, {d}); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


@scene(37)
def s37(p, d):
    # macro on one index card, shallow focus: the rest of the pile is soft
    r = random.Random(37)
    back = "".join(f'''<div style="position:absolute;left:{r.uniform(-200, 1600):.0f}px;top:{r.uniform(-120, 760):.0f}px;width:520px;height:330px;background:#d8c9a6 url(assets/tex/paper_tung.jpg) {r.randint(0, 800)}px 0;background-blend-mode:multiply;transform:rotate({r.uniform(-25, 25):.1f}deg);box-shadow:0 14px 30px rgba(0,0,0,.6)">
<div style="position:absolute;left:0;right:0;top:64px;height:3px;background:#6b5c48;opacity:.7"></div></div>''' for _ in range(12))
    hero = f'''<div style="position:absolute;left:250px;top:160px;width:1420px;height:860px;background:#e8d8b4 url(assets/tex/paper_tung.jpg) 0 0/2400px 1600px;background-blend-mode:multiply;transform:rotate(-4deg);box-shadow:0 30px 60px rgba(0,0,0,.7)">
<div style="position:absolute;left:0;right:0;top:150px;height:5px;background:#6b5c48;opacity:.75"></div>
<div style="position:absolute;left:40px;top:40px;width:1300px;height:800px;background:url(assets/tex/scribble1.png) 0 0/100% 100%;opacity:.9"></div></div>'''
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#060302" data-layout-allow-overflow>
<div class="ao-full" style="filter:blur(9px) brightness(.5)">{back}</div>{hero}
<div class="ao-full" style="background:linear-gradient(90deg,rgba(6,3,2,.85),rgba(6,3,2,0) 30%,rgba(6,3,2,0) 60%,rgba(6,3,2,.8)),{TUNG_TOP}"></div></div>'''
    js = f"shot('cam', 0, {d}, [1.15,60,30,-2], [1.25,-40,0,-1]); tag(0.05);"
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


@scene(38)
def s38(p, d):
    r = random.Random(38)
    spines, x = [], 0
    cols = ["#2a2018", "#3a2c1e", "#4a3826", "#2d2a22", "#5a4630", "#3d3024", "#6a5236"]
    while x < 3400:
        w = r.randint(60, 140)
        h = r.randint(560, 760)
        spines.append(f'<div style="position:absolute;left:{x}px;bottom:150px;width:{w}px;height:{h}px;background:{r.choice(cols)};box-shadow:inset -12px 0 18px rgba(0,0,0,.6),inset 6px 0 10px rgba(255,220,170,.12)">'
                      f'<div style="position:absolute;left:14%;right:14%;top:80px;height:90px;background:#d9c49c;opacity:.8"></div></div>')
        x += w + r.randint(2, 8)
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#050302" data-layout-allow-overflow>
<div id="{p}-row" style="position:absolute;left:0;top:0;width:3400px;height:1080px">{"".join(spines)}<div style="position:absolute;left:0;bottom:110px;width:3400px;height:40px;background:#2c2218"></div></div>
<div class="ao-full" style="background:radial-gradient(ellipse at 20% 30%,rgba(255,190,110,.35),rgba(0,0,0,0) 45%);mix-blend-mode:screen"></div>
<div class="ao-full" style="background:linear-gradient(90deg,rgba(0,0,0,.3),rgba(0,0,0,0) 30%,rgba(0,0,0,.4) 70%,rgba(0,0,0,.92))"></div></div>'''
    js = f"tl.fromTo(q('row'), {{ x: 0 }}, {{ x: -900, duration: {d}, ease: 'none' }}, 0); whipIn('cam', 0, 320); tag(0.05);"
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


UNESCO = "FUENTE · postulación UNESCO Memoria del Mundo (2008)"


@scene(39)
def s39(p, d):
    html = f'''<div id="{p}-A" class="ao-full" style="background:#070403"><div class="ao-full" style="filter:blur(8px) brightness(.4)">{paper_pile(36, 70, (0, 0, 1920, 1080))}</div></div>
<div id="{p}-B" class="ao-full" style="opacity:0;background:#070403">{"".join(f'<div style="position:absolute;left:-100px;top:{120 + i * 26}px;width:2200px;height:22px;background:#e3cfa6 url(assets/tex/paper_tung.jpg) {i * 50}px 0;background-blend-mode:multiply;transform:rotate({(i % 5 - 2) * 0.3}deg);box-shadow:0 4px 5px rgba(0,0,0,.6)"></div>' for i in range(34))}
<div class="ao-full" style="background:linear-gradient(90deg,rgba(7,4,3,.9),rgba(7,4,3,0) 40%),{TUNG_TOP}"></div></div>'''
    fg = f'''<div id="{p}-fa" class="ao-full"><div style="position:absolute;left:0;width:1920px;top:250px;text-align:center;white-space:nowrap"><span class="ao-unit" style="font-size:150px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:300px">0</span></div>
<div class="ao-unit" style="position:absolute;left:0;width:1920px;top:600px;text-align:center;font-size:120px">PÁGINAS</div></div>
<div id="{p}-fb" class="ao-full" style="opacity:0"><div style="position:absolute;left:150px;top:150px;white-space:nowrap"><span class="ao-num" style="font-size:130px">≈ 800.000</span><div class="ao-unit" style="font-size:64px">PÁGINAS</div></div></div>'''
    js = f"""count('n', 0, 800000, 0.05, 1.0); /*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.1); tl.set(q('fa'), {{ opacity: 0 }}, 1.1); tl.set(q('B'), {{ opacity: 1 }}, 1.1); tl.set(q('fb'), {{ opacity: 1 }}, 1.1);
shot('B', 1.1, {d}, [1.05,0,0,-3], [1.1,0,-40,-3]); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, UNESCO, src=True))


@scene(40)
def s40(p, d):
    sheets = "".join(f'<div id="{p}-s{i}" style="position:absolute;left:{510 + (i * 7) % 24}px;top:{1040 - i * 20}px;width:900px;height:18px;background:{["#ecdcba", "#dcc9a4", "#e5d2ae"][i % 3]};box-shadow:0 3px 4px rgba(0,0,0,.5)"></div>' for i in range(70))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#060302" data-layout-allow-overflow>{sheets}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 30%,rgba(255,190,110,.3),rgba(0,0,0,0) 60%);mix-blend-mode:screen"></div></div>'''
    fg = f'<div id="{p}-n" style="position:absolute;left:0;width:1920px;top:-930px;text-align:center"><span class="ao-unit" style="font-size:130px;color:{ACC}">≈ </span><span class="ao-num" style="font-size:240px">800.000</span><div class="ao-unit" style="font-size:96px">PÁGINAS</div></div>'
    js = "".join(f"tl.fromTo(q('s{i}'), {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.08 }}, {i * 0.017:.3f});" for i in range(70))
    js += f"shot('cam', 0, {d}, [1.0,0,-60], [1.0,0,1120], 'power1.inOut'); tl.fromTo(q('n'), {{ y: -60 }}, {{ y: 1120, duration: {d}, ease: 'power1.inOut' }}, 0); tag(0.0);"
    return S(html, js, fg=fg + tag_html(p, UNESCO, src=True))


@scene(41)
def s41(p, d):
    r = random.Random(41)
    shelves = "".join(f'<div style="position:absolute;left:0;top:{y}px;width:3000px;height:22px;background:#3a2c1e;box-shadow:0 8px 12px rgba(0,0,0,.6)"></div>' for y in (330, 620, 910))
    boxes = "".join(f'<div style="position:absolute;left:{x}px;top:{y - 220}px;width:{w}px;height:220px;background:{r.choice(["#7a6248", "#8a7052", "#6c5640", "#957a58"])} url(assets/tex/cardboard.jpg) {r.randint(0, 600)}px 0;background-blend-mode:multiply;border:2px solid rgba(20,14,8,.6)"><div style="margin:40px auto 0;width:60%;height:40px;background:#e2d0aa;opacity:.85"></div></div>'
                    for y in (330, 620, 910) for x, w in [(i * 190 + r.randint(0, 20), 170) for i in range(16)])
    html = f'''<div id="{p}-A" class="ao-full" style="background:#060302"><div id="{p}-sh" style="position:absolute;left:0;top:0;width:3000px;height:1080px;filter:brightness(.62)">{boxes}{shelves}</div>
<div class="ao-full" style="background:radial-gradient(ellipse at 30% 20%,rgba(255,190,110,.3),rgba(0,0,0,0) 55%);mix-blend-mode:screen"></div></div>
<div id="{p}-B" class="ao-full" style="opacity:0;background:#060302"><div style="position:absolute;left:-200px;top:520px;width:2400px;height:150px;background:#c8a060;box-shadow:0 20px 40px rgba(0,0,0,.6)">
{"".join(f'<div style="position:absolute;left:{i * 48}px;top:0;width:4px;height:{60 if i % 10 == 0 else 32}px;background:#1a140c"></div>' for i in range(50))}
{"".join(f'<div style="position:absolute;left:{i * 480 + 10}px;top:70px;font:700 56px Courier Prime;color:#1a140c">{190 + i * 10 // 10 * 0}</div>' for i in range(0))}</div>
<div style="position:absolute;left:1180px;top:430px;width:620px;height:340px;background:radial-gradient(circle,rgba(255,200,130,.45),rgba(0,0,0,0) 70%);mix-blend-mode:screen"></div></div>'''
    fg = f'''<div id="{p}-fa" class="ao-full"><div style="position:absolute;left:0;top:500px;width:1920px;height:12px"><div id="{p}-tape" style="position:absolute;left:160px;top:0;width:1600px;height:10px;background:{ACC};transform-origin:0 50%"></div></div>
<div style="position:absolute;left:0;width:1920px;top:560px;text-align:center;white-space:nowrap"><span class="ao-unit" style="font-size:110px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:250px">0</span><span class="ao-unit" style="font-size:100px"> METROS LINEALES</span></div></div>
<div id="{p}-fb" class="ao-full" style="opacity:0"><div style="position:absolute;left:1240px;top:400px;width:6px;height:400px;background:{ACC}"></div>
<div style="position:absolute;left:1280px;top:300px;font:400 150px Anton;color:{ACC}">200 m</div></div>'''
    js = f"""tl.fromTo(q('tape'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.0, ease: 'power2.inOut' }}, 0.1); count('n', 0, 200, 0.1, 1.0);
tl.fromTo(q('sh'), {{ x: 0 }}, {{ x: -500, duration: 1.25, ease: 'none' }}, 0);
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.25); tl.set(q('fa'), {{ opacity: 0 }}, 1.25); tl.set(q('B'), {{ opacity: 1 }}, 1.25); tl.set(q('fb'), {{ opacity: 1 }}, 1.25);
shot('B', 1.25, {d}, [1.0,0,0], [1.05,-40,0]); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, UNESCO, src=True))


def ficha(p, k, x, y, rot, stamp=None, photo=False, finger=False, w=520, h=330, pal="tung"):
    st = f'<div id="{p}-st{k}" class="ao-stamp" style="position:absolute;right:26px;bottom:22px;font-size:50px;transform:rotate(-8deg)">{stamp}</div>' if stamp else ""
    ph = (f'<div style="position:absolute;left:24px;top:84px;width:{int(w * .3)}px;height:{int(h * .62)}px;border:3px solid #4a4236;background:#cdbf9f">'
          f'<div id="{p}-ph{k}" style="width:100%;height:100%;opacity:0;background:radial-gradient(ellipse 34% 26% at 50% 34%,rgba(40,34,28,.85),rgba(40,34,28,0) 100%),radial-gradient(ellipse 60% 40% at 50% 100%,rgba(40,34,28,.8),rgba(40,34,28,0) 100%),url(assets/tex/paper_grey.jpg) center/300% auto;filter:blur(2.5px) sepia(.4)"></div></div>') if photo else ""
    fp = (f'<div style="position:absolute;right:24px;top:84px;width:{int(w * .26)}px;height:{int(h * .62)}px;border:3px solid #4a4236">'
          f'<div id="{p}-fp{k}" style="width:100%;height:100%;opacity:0;background:url(assets/tex/fingerprint.png) center/contain no-repeat"></div></div>') if finger else ""
    return f'''<div id="{p}-f{k}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#e2d2ae url(assets/tex/paper_{pal}.jpg) {k * 300}px 0;background-blend-mode:multiply;transform:rotate({rot}deg);box-shadow:0 16px 34px rgba(0,0,0,.65)">
<div style="position:absolute;left:0;right:0;top:62px;height:3px;background:#6b5c48;opacity:.75"></div>
<div style="position:absolute;left:24px;top:18px;width:200px;height:24px;background:rgba(60,50,40,.35);filter:blur(4px)"></div>{ph}{fp}{st}</div>'''


@scene(42)
def s42(p, d):
    cols, rows = 24, 12
    cells = "".join(f'<div id="{p}-g{i}" style="position:absolute;left:{120 + (i % cols) * 70}px;top:{90 + (i // cols) * 76}px;width:60px;height:64px;background:#d9c6a0;opacity:0;border-top:6px solid #6b5c48"></div>' for i in range(cols * rows))
    html = f'''<div id="{p}-A" class="ao-full" style="background:#070403">{cells}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(7,4,3,.92) 0,rgba(7,4,3,.7) 35%,rgba(7,4,3,.1) 72%)"></div></div>
<div id="{p}-B" class="ao-full" style="opacity:0;background:#070403">{ficha(p, 99, 260, 170, -3, None, True, True, 1400, 880)}</div>'''
    fg = f'''<div id="{p}-fa" class="ao-full"><div style="position:absolute;left:0;width:1920px;top:330px;text-align:center"><span id="{p}-n" class="ao-num" style="font-size:300px">0</span><div class="ao-unit" style="font-size:120px">FICHAS</div></div></div>'''
    order = list(range(cols * rows))
    random.Random(42).shuffle(order)
    js = "".join(f"tl.set(q('g{c}'), {{ opacity: 1 }}, {0.05 + k * 0.95 / len(order):.3f});" for k, c in enumerate(order))
    js += f"""count('n', 0, 11225, 0.05, 0.95); /*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.1); tl.set(q('fa'), {{ opacity: 0 }}, 1.1); tl.set(q('B'), {{ opacity: 1 }}, 1.1);
tl.set(q('ph99'), {{ opacity: 1 }}, 1.1); tl.set(q('fp99'), {{ opacity: .9 }}, 1.1); shot('B', 1.1, {d}, [1.0,0,0], [1.05,0,0]); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, UNESCO, src=True))


@scene(43)
def s43(p, d):
    frames = "".join(f'<div style="position:absolute;left:{60 + (i % 9) * 210}px;top:{40 + (i // 9) * 200}px;width:180px;height:150px;background:linear-gradient(160deg,#5c5246,#2e2820);border:8px solid #efe2c6;box-shadow:0 6px 12px rgba(0,0,0,.5)"></div>' for i in range(54))
    strip = "".join(f'<div style="position:absolute;left:{80 + i * 460}px;top:270px;width:420px;height:340px;background:linear-gradient(160deg,#5c5246,#2e2820);border:16px solid #efe2c6"></div>' for i in range(5))
    html = f'''<div id="{p}-A" class="ao-full" style="background:#060403"><div id="{p}-gr" style="position:absolute;left:0;top:0;width:1920px;height:1200px">{frames}</div>
<div class="ao-full" style="background:linear-gradient(180deg,rgba(6,4,3,.2),rgba(6,4,3,.9) 40%,rgba(6,4,3,.9) 60%,rgba(6,4,3,.2))"></div></div>
<div id="{p}-B" class="ao-full" style="opacity:0;background:#0b0705"><div id="{p}-st" style="position:absolute;left:0;top:0;width:2400px;height:1080px">
<div style="position:absolute;left:0;top:220px;width:2400px;height:440px;background:#17110c"></div>{strip}</div>
<div class="ao-full" style="background:{TUNG_TOP};mix-blend-mode:screen"></div></div>'''
    fg = f'''<div id="{p}-fa" class="ao-full"><div style="position:absolute;left:0;width:1920px;top:330px;text-align:center"><span class="ao-unit" style="font-size:120px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:290px">0</span><div class="ao-unit" style="font-size:110px">FOTOGRAFÍAS</div></div></div>'''
    js = f"""count('n', 0, 20000, 0.05, 0.75); tl.fromTo(q('gr'), {{ y: 0 }}, {{ y: -80, duration: 0.8, ease: 'none' }}, 0);
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 0.8); tl.set(q('fa'), {{ opacity: 0 }}, 0.8); tl.set(q('B'), {{ opacity: 1 }}, 0.8);
tl.fromTo(q('st'), {{ x: 0 }}, {{ x: -260, duration: {d - 0.8:.2f}, ease: 'none' }}, 0.8); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, UNESCO, src=True))


def cassette_svg(x, y, s=1):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="0" y="0" width="200" height="128" rx="10" fill="#241c15" stroke="#8a7a62" stroke-width="4"/>'
            f'<rect x="24" y="18" width="152" height="44" fill="#d9c6a0"/><circle cx="62" cy="88" r="18" fill="none" stroke="#8a7a62" stroke-width="5"/>'
            f'<circle cx="138" cy="88" r="18" fill="none" stroke="#8a7a62" stroke-width="5"/><rect x="80" y="80" width="40" height="16" fill="#0e0a07"/></g>')


@scene(44)
def s44(p, d):
    if HAVE["A5"]:
        bg = f'<img id="{p}-ph" src="assets/img/{PHOTO["A5"]}" style="position:absolute;left:-100px;top:-400px;width:2120px;height:2590px;object-fit:cover;filter:brightness(.55)" alt="">'
        lab = tag_html(p, "IMAGEN ILUSTRATIVA · Hmvh, Wikimedia Commons (dominio público)", src=True)
    else:
        r = random.Random(44)
        bg = f'<svg id="{p}-ph" viewBox="0 0 2200 1080" width="2200" height="1080" style="position:absolute;left:0;top:0;opacity:.75">' + "".join(
            cassette_svg(-60 + c * 230 + r.randint(-8, 8), -40 + rr * 160 + r.randint(-6, 6), 1) for rr in range(8) for c in range(10)) + "</svg>"
        lab = tag_html(p, "RECREACIÓN")
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#060403" data-layout-allow-overflow>{bg}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(6,4,3,.9) 0,rgba(6,4,3,.6) 40%,rgba(6,4,3,.15) 75%)"></div></div>'''
    fg = f'<div style="position:absolute;left:0;width:1920px;top:330px;text-align:center"><span id="{p}-n" class="ao-num" style="font-size:300px">0</span><div class="ao-unit" style="font-size:120px">CASETES</div></div>'
    js = f"tl.fromTo(q('ph'), {{ x: 0 }}, {{ x: -160, duration: {d}, ease: 'none' }}, 0); count('n', 0, 543, 0.05, 1.0); tag(0.05);"
    return S(html, js, fg=fg + lab)


def stamp_tl(p, d, first):
    html = f'<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>{BIGPAPER()}</div>'
    fg = f'''<div id="{p}-g" class="ao-full" style="transform-origin:50% 50%">
<div class="tl-axis" style="left:300px;top:560px;width:1320px"></div><div id="{p}-fill" class="tl-fill" style="left:300px;top:560px;width:1320px"></div>
<div class="tl-dot" style="left:300px;top:563px"></div><div id="{p}-d2" class="tl-dot" style="left:1620px;top:563px"></div>
<div id="{p}-s1" class="ao-stampT" style="position:absolute;left:200px;top:280px;font-size:120px">1927</div>
<div id="{p}-s2" class="ao-stampT" style="position:absolute;left:1340px;top:280px;font-size:110px">FEB 1989</div>
<div style="position:absolute;left:0;width:1920px;top:700px;text-align:center;font:700 44px 'Courier Prime';letter-spacing:.28em;color:#22201c">FECHAS DEL INVENTARIO</div></div>'''
    if first:   # A: the stamp hitting the paper, close; /*cut*/ B: the whole line
        js = f"""stampIn('s1', 0.15, -4); tl.set(q('s2'), {{ opacity: 0 }}, 0); tl.set(q('fill'), {{ scaleX: 0 }}, 0); tl.set(q('d2'), {{ opacity: 0 }}, 0);
shot('cam', 0, 0.9, [2.2,1250,520,-2], [2.25,1260,525,-2]); shot('g', 0, 0.9, [2.2,1250,520,-2], [2.25,1260,525,-2]);
/*cut*/ shot('cam', 0.9, {d}, [1.0,0,0], [1.02,0,0]); shot('g', 0.9, {d}, [1.0,0,0], [1.02,0,0]); tag(0.05);"""
    else:       # A: the line running; /*cut*/ B: the FEB 1989 stamp, close
        js = f"""tl.set(q('s1'), {{ rotation: -4 }}, 0); tl.fromTo(q('fill'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: 'power3.in' }}, 0.05);
tl.fromTo(q('d2'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, 0.62); tl.set(q('s2'), {{ opacity: 0 }}, 0); stampIn('s2', 0.95, 3);
shot('cam', 0, 0.9, [1.0,0,0], [1.02,0,0]); shot('g', 0, 0.9, [1.0,0,0], [1.02,0,0]);
/*cut*/ shot('cam', 0.9, {d}, [2.0,-1000,540,1], [2.05,-1030,550,1]); shot('g', 0.9, {d}, [2.0,-1000,540,1], [2.05,-1030,550,1]); tag(0.05);"""
    return S(html, js, TL_CSS, fg=fg + tag_html(p, UNESCO, src=True))


@scene(45)
def s45(p, d):
    return stamp_tl(p, d, True)


@scene(46)
def s46(p, d):
    return stamp_tl(p, d, False)


@scene(47)
def s47(p, d):
    ticks = "".join(f'<line x1="0" y1="-300" x2="0" y2="{-262 if k % 3 else -240}" stroke="#e9dcc0" stroke-width="{6 if k % 3 == 0 else 3}" transform="rotate({k * 30})"/>' for k in range(12))
    clock = f'''<g><circle r="320" fill="#1a130d" stroke="#e9dcc0" stroke-width="8"/>{ticks}
<line id="{p}-hh" x1="0" y1="20" x2="0" y2="-170" stroke="#e9dcc0" stroke-width="16" stroke-linecap="round"/>
<line id="{p}-mh" x1="0" y1="30" x2="0" y2="-250" stroke="#e9dcc0" stroke-width="9" stroke-linecap="round"/><circle r="16" fill="#e9dcc0"/></g>'''
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#070403" data-layout-allow-overflow>
<svg viewBox="-960 -540 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0"><g transform="translate(-420,0)">{clock}</g></svg>
<div class="ao-full" style="background:radial-gradient(ellipse at 30% 40%,rgba(255,190,110,.25),rgba(0,0,0,0) 50%);mix-blend-mode:screen"></div></div>'''
    fg = f'''<div id="{p}-fa" class="ao-full"><svg viewBox="-960 -540 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0"><g transform="translate(-420,0)">
<path id="{p}-arc" d="M0,-280 A280,280 0 1 1 -0.1,-280" fill="none" stroke="{ACC}" stroke-width="10" stroke-dasharray="1760" stroke-dashoffset="1760"/></g></svg>
<div style="position:absolute;left:980px;top:330px"><span class="ao-unit" style="font-size:120px;color:{ACC}">≈ </span><span id="{p}-n" class="ao-num" style="font-size:300px">0</span><div class="ao-unit" style="font-size:120px">HORAS</div></div></div>'''
    js = f"""tl.fromTo(q('mh'), {{ rotation: 0, svgOrigin: '0 0' }}, {{ rotation: 4320, svgOrigin: '0 0', duration: 1.6, ease: 'power2.inOut' }}, 0.05);
tl.fromTo(q('hh'), {{ rotation: 0, svgOrigin: '0 0' }}, {{ rotation: 360, svgOrigin: '0 0', duration: 1.6, ease: 'power2.inOut' }}, 0.05);
tl.to(q('arc'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.9, ease: 'power2.inOut' }}, 0.05); count('n', 0, 12, 0.05, 0.9);
shot('cam', 0, 1.0, [1.0,0,0], [1.03,0,0]); /*cut*/ tl.set(q('fa'), {{ opacity: 0 }}, 1.0); shot('cam', 1.0, {d}, [2.6,1100,0,8], [2.7,1140,0,8]); tag(0.05);"""
    return S(html, js, fg=fg + tag_html(p, "FUENTE · Poder Judicial, Archivos del Terror (2008)", src=True))


@scene(48)
def s48(p, d):
    return S(js="tag(0.05); /*cut:0.95*/", mod={"kind": "boxes", "opts": {"d": d, "cut": 0.95}}, fg=tag_html(p, "RECREACIÓN"))


@scene(49)
def s49(p, d):
    # damp paper, macro under the bulb: water rings, mildew, typed lines soft in the depth of field
    stains = "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{int(w * .8)}px;border-radius:50%;border:9px solid rgba(70,48,24,.45);box-shadow:inset 0 0 60px rgba(70,48,24,.4),0 0 30px rgba(70,48,24,.25)"></div>' for x, y, w in ((300, 150, 520), (1100, 520, 620), (760, 60, 300), (420, 640, 360)))
    a = f'''<div id="{p}-A" class="ao-full" style="background:#050302"><div id="{p}-pa" class="ao-full" style="background:#e3c99a url(assets/tex/paper_tung.jpg) 30% 40%/2400px 1600px;background-blend-mode:multiply">
<img src="assets/tex/smoke1.png" style="position:absolute;left:0;top:0;width:1920px;height:1080px;mix-blend-mode:multiply;opacity:.55;filter:sepia(1) brightness(.6)" alt="">{stains}
<div style="position:absolute;left:240px;top:330px;width:1500px;opacity:.8">{doc_lines(7, 40, 49, "#3a2614")}</div></div>
<div class="ao-full" style="background:linear-gradient(180deg,rgba(5,3,2,.75),rgba(5,3,2,0) 30%,rgba(5,3,2,0) 70%,rgba(5,3,2,.8)),radial-gradient(ellipse at 40% 30%,rgba(255,196,120,.25),rgba(0,0,0,0) 50%)"></div></div>'''
    b = f'''<div id="{p}-B" class="ao-full" style="opacity:0;background:#040201">
<div style="position:absolute;left:380px;top:180px;width:1700px;height:1100px;background:#d8bd8c url(assets/tex/paper_tung.jpg) 0 0/2400px 1600px;background-blend-mode:multiply;transform:rotate(-14deg);border-radius:0 0 0 120px;box-shadow:-30px 30px 60px rgba(0,0,0,.8)"></div>
<div style="position:absolute;left:360px;top:600px;width:420px;height:420px;background:radial-gradient(circle at 40% 40%,rgba(120,80,40,.6),rgba(120,80,40,0) 60%)"></div>
<div style="position:absolute;left:560px;top:870px;width:26px;height:34px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 35% 30%,#fff6e6,rgba(160,120,70,.5) 60%)"></div>
<div class="ao-full" style="background:radial-gradient(ellipse at 60% 30%,rgba(255,190,110,.28),rgba(0,0,0,0) 55%)"></div></div>'''
    js = f"""shot('A', 0, 1.1, [1.25,0,0,-4], [1.32,-50,-20,-4]); tl.fromTo(q('pa'), {{ filter: 'blur(5px)' }}, {{ filter: 'blur(0px)', duration: 0.6 }}, 0);
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.1); tl.set(q('B'), {{ opacity: 1 }}, 1.1); shot('B', 1.1, {d}, [1.0,0,0], [1.06,-30,0]); tag(0.05);"""
    return S(a + b, js, fg=tag_html(p, "RECREACIÓN"))


@scene(50)
def s50(p, d):
    t, n = typed(p, "t", "«PERDIDOS»")
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>
<div style="position:absolute;left:140px;top:250px;width:1640px;height:560px;{PAPER()};box-shadow:0 40px 80px rgba(0,0,0,.6)"></div>
<div style="position:absolute;left:200px;top:440px;font:700 170px 'Courier Prime';color:#151513;white-space:nowrap">{t}</div></div>'''
    fg = f'''<div id="{p}-g" class="ao-full" style="transform-origin:50% 50%"><div id="{p}-x" style="position:absolute;left:180px;top:530px;width:1060px;height:16px;background:{ACC};transform-origin:0 50%"></div>
<div id="{p}-q" style="position:absolute;left:1360px;top:250px;font:400 520px/1 Anton;color:{ACC};opacity:0">?</div></div>'''
    js = f"""type('t', {n}, 0.05, 0.05); tl.fromTo(q('x'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: 'power3.in' }}, 0.7);
shot('cam', 0, 1.15, [1.0,0,0], [1.03,0,0]); shot('g', 0, 1.15, [1.0,0,0], [1.03,0,0]);
/*cut*/ tl.set(q('q'), {{ opacity: 1 }}, 1.15); shot('cam', 1.15, {d}, [1.35,-420,40], [1.38,-440,40]); shot('g', 1.15, {d}, [1.35,-420,40], [1.38,-440,40]);"""
    return S(html, js, fg=fg)


def conosur(p, d, lines, s, center):
    ax, ay = map_pt("Asunción")
    hi = ("Argentina", "Uruguay", "Chile")
    extra = f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="20" fill="{ACC}" stroke="#0b1a1a" stroke-width="6"/>'
    if lines:
        for i, c in enumerate(("Buenos Aires", "Montevideo", "Santiago")):
            x, y = map_pt(c)
            mx, my = (x + ax) / 2, (y + ay) / 2 - 160
            extra += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="#1d1a15"/><path id="{p}-ln{i}" d="M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {ax:.0f},{ay:.0f}" fill="none" stroke="{ACC}" stroke-width="9" '
                      f'stroke-dasharray="4000" stroke-dashoffset="4000" stroke-linecap="round"/>')
        extra += f'<text x="{ax + 40:.0f}" y="{ay - 20:.0f}" style="font:700 86px Caveat;fill:#1d1a15">Asunción</text>'
    x0, y0 = cam_center(center[0], center[1], s)
    x1, y1 = cam_center(center[0], center[1], s * 1.05)
    html = f'<div id="{p}-cam" class="ao-cam" style="transform-origin:0 0" data-layout-allow-overflow>{map_svg(p, hi, extra)}</div>'
    return html, x0, y0, x1, y1


@scene(51)
def s51(p, d):
    ax, ay = map_pt("Asunción")
    mx, my = map_pt("Montevideo")
    html, x0, y0, x1, y1 = conosur(p, d, False, 0.4, ((mx + ax) / 2 - 300, (my + ay) / 2 + 60))
    _, bx0, by0, bx1, by1 = conosur(p, d, False, 0.85, (mx - 220, my - 80))
    js = f"tl.set(q('cam'), {{ x: {x0}, y: {y0}, scale: 0.4 }}, 0); tl.to(q('cam'), {{ x: {x1}, y: {y1}, scale: 0.42, duration: 1.0, ease: 'none' }}, 0);"
    js += f"/*cut*/ tl.set(q('cam'), {{ x: {bx0}, y: {by0}, scale: 0.85 }}, 1.0); tl.to(q('cam'), {{ x: {bx1}, y: {by1}, scale: 0.89, duration: {d - 1.0:.2f}, ease: 'none' }}, 1.0);"
    js += "".join(f"tl.set(q('c-{c}'), {{ attr: {{ class: '{p}hi on' }} }}, {0.2 + i * 0.3:.2f});" for i, c in enumerate(("argentina", "uruguay", "chile")))
    js += "tag(0.05);"
    return S(html, js, map_css(p), fg=tag_html(p, "MAPA · elaboración propia, datos Natural Earth; base: mapa de 1856 (LOC)", src=True))


@scene(52)
def s52(p, d):
    ax, ay = map_pt("Asunción")
    mx, my = map_pt("Montevideo")
    html, x0, y0, x1, y1 = conosur(p, d, True, 0.5, ((mx + ax) / 2 - 300, (my + ay) / 2 + 60))
    js = f"shot('cam', 0, {d}, [0.5,{x0},{y0}], [0.54,{x1},{y1}]); tl.set(q('cam'), {{ transformOrigin: '0 0' }}, 0);"
    js += "".join(f"tl.set(q('c-{c}'), {{ attr: {{ class: '{p}hi on' }} }}, 0);" for c in ("argentina", "uruguay", "chile"))
    js += "".join(f"tl.to(q('ln{i}'), {{ attr: {{ 'stroke-dashoffset': 0 }}, duration: 0.8, ease: 'power2.inOut' }}, {0.1 + i * 0.15:.2f});" for i in range(3))
    js += "tag(0.05);"
    return S(html, js, map_css(p), fg=tag_html(p, "MAPA · elaboración propia, datos Natural Earth; base: mapa de 1856 (LOC)", src=True))


@scene(53)
def s53(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>
{ficha(p, 0, 180, 330, -5, "ARGENTINA")}{ficha(p, 1, 700, 380, 2, "URUGUAY")}{ficha(p, 2, 1220, 320, 5, "CHILE")}</div>'''
    js = "".join(f"stampIn('st{i}', {0.12 + i * 0.25:.2f}, -8);" for i in range(3))
    js += f"shot('cam', 0, 0.85, [0.95,0,0], [0.98,0,0]); /*cut*/ shot('cam', 0.85, {d}, [2.4,-250,-271,-4], [2.46,-258,-280,-4]); tag(0.05);"
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


def fichas_wall(p, seed, n=22):
    r = random.Random(seed)
    return "".join(ficha(p, 200 + i, r.randint(-200, 1700), r.randint(-150, 900), r.uniform(-12, 12), None, i % 2 == 0, i % 3 == 0) for i in range(n))


@scene(54)
def s54(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#050302" data-layout-allow-overflow><div class="ao-full" style="filter:blur(6px) brightness(.35)">{fichas_wall(p, 54)}</div></div>'''
    fg = f'''<div id="{p}-g" class="ao-full" style="transform-origin:50% 50%">
<div id="{p}-t1" style="position:absolute;left:0;width:1920px;top:250px;text-align:center;font:400 210px/1 Anton;color:#f3ead8;letter-spacing:.01em">NEGABA</div>
<div id="{p}-t2" style="position:absolute;left:0;width:1920px;top:480px;text-align:center;font:400 170px/1 Anton;color:{ACC};letter-spacing:.01em">HABERLOS DETENIDO</div></div>'''
    js = f"""stampIn('t1', 0.05, 0); tl.set(q('t2'), {{ opacity: 0 }}, 0); shot('cam', 0, 1.25, [1.0,0,0], [1.03,0,0]); shot('g', 0, 1.25, [1.25,0,260], [1.28,0,265]);
/*cut*/ stampIn('t2', 1.25, 0); shake('g', 1.41, 12); shot('cam', 1.25, {d}, [1.3,300,-100], [1.33,300,-100]);"""
    return S(html, js, fg=fg)


@scene(55)
def s55(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{ficha(p, 0, 360, 190, -1.5, None, True, True, 1200, 760)}</div>'''
    js = f"""tl.fromTo(q('ph0'), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.3); tl.fromTo(q('fp0'), {{ opacity: 0, scale: 1.2 }}, {{ opacity: .95, scale: 1, duration: 0.25, ease: 'power4.in' }}, 1.4);
shot('cam', 0, 1.25, [1.0,0,0], [1.03,0,0]); /*cut*/ shot('cam', 1.25, {d}, [2.6,-1130,-110], [2.66,-1160,-115]); tag(0.05);"""
    return S(html, js, fg=tag_html(p, "RECREACIÓN"))


@scene(56)
def s56(p, d):
    r = random.Random(56)
    wall = "".join(ficha(p, 10 + i, r.randint(-200, 1700), r.randint(-150, 900), r.uniform(-12, 12), None, i % 2 == 0, i % 3 == 0) for i in range(18))
    words = ["FICHADOS", "CON FOTO", "CON HUELLAS"]
    ws = (f'<span id="{p}-w0x"><span id="{p}-w0" style="color:#f3ead8">{words[0]}</span><span style="color:#f3ead8"> · </span></span>'
          + '<span style="color:#f3ead8"> · </span>'.join(f'<span id="{p}-w{i}" style="color:#f3ead8">{w}</span>' for i, w in enumerate(words) if i))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#050302" data-layout-allow-overflow><div id="{p}-wall" class="ao-full">{wall}</div>
<div class="ao-full" style="background:rgba(5,3,2,.62)"></div></div>'''
    fg = f'<div id="{p}-g" class="ao-full" style="transform-origin:50% 50%"><div style="position:absolute;left:0;width:1920px;top:460px;text-align:center;font:400 112px/1 Anton;letter-spacing:.02em;white-space:nowrap">{ws}</div></div>'
    js = "".join(f"tl.fromTo(q('f{10 + i}'), {{ y: -1300 }}, {{ y: 0, duration: 0.3, ease: 'power3.in' }}, {0.05 + i * 0.1:.2f});" for i in range(18))
    js += "".join(f"tl.set(q('w{i}'), {{ color: '{ACC}' }}, {0.3 + i * 0.55:.2f});" for i in range(3))
    js += f"shot('cam', 0, 1.3, [1.0,0,0], [1.03,0,0]); /*cut*/ shot('cam', 1.3, {d}, [1.8,500,300,2], [1.85,500,300,2]); shot('g', 1.3, {d}, [1.35,-462,0], [1.37,-470,0]); tl.set(q('w0x'), {{ opacity: 0 }}, 1.3);"
    return S(html, js, fg=fg)


@scene(57)
def s57(p, d):
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#020202" data-layout-allow-overflow>
{smoke_html(p, 0, 0.32, "mix-blend-mode:screen;filter:brightness(.7) sepia(.4)")}{smoke_html(p, 2, 0.22, "mix-blend-mode:screen;filter:brightness(.6) sepia(.4)")}</div>'''
    fg = f'<div id="{p}-t" style="position:absolute;left:0;width:1920px;top:300px;text-align:center;font:400 220px/1.02 Anton;color:#f2ece0;letter-spacing:.03em;white-space:nowrap">LOS ARCHIVOS<br><span style="color:{ACC}">DEL TERROR</span></div>'
    js = f"""tl.fromTo(q('t'), {{ opacity: 0, filter: 'blur(22px)', scale: 1.08 }}, {{ opacity: 1, filter: 'blur(0px)', scale: 1, duration: 0.7, ease: 'power2.out' }}, 0.05);
tl.fromTo(q('smk0'), {{ x: 0, y: 120 }}, {{ x: -200, y: -60, duration: {d}, ease: 'none' }}, 0); tl.fromTo(q('smk2'), {{ x: 0, y: 200 }}, {{ x: 260, y: 0, duration: {d}, ease: 'none' }}, 0);"""
    return S(html, js, fg=fg)


@scene(58)
def s58(p, d):
    if HAVE["A4"]:
        bg = (f'<img src="assets/img/{PHOTO["A4"]}" class="ao-full" style="object-fit:cover;filter:blur(22px) brightness(.4)" alt="">'
              f'<div style="position:absolute;left:1180px;top:150px;width:560px;height:746px;background:#efe6d2;padding:16px;box-shadow:0 40px 90px rgba(0,0,0,.7);transform:rotate(2deg)">'
              f'<div style="width:100%;height:100%;background:url(assets/img/{PHOTO["A4"]}) center/cover"></div></div>')
        lab = tag_html(p, "IMAGEN REAL · Archivo del Terror · Museo de la Justicia, Asunción (foto 2019)", src=True)
        tx, fs = "left:150px;width:1000px;text-align:left", 150
    else:
        bg = f'<div class="ao-full" style="filter:blur(2px) brightness(.4)">{paper_pile(58, 70, (0, 0, 1920, 1080))}</div><div class="ao-full" style="background:{TUNG_TOP};mix-blend-mode:screen"></div>'
        lab, tx, fs = "", "left:0;width:1920px;text-align:center", 220
    html = f'<div id="{p}-cam" class="ao-cam" style="background:#050302" data-layout-allow-overflow>{bg}</div>'
    fg = f'<div style="position:absolute;{tx};top:300px;font:400 {fs}px/1.02 Anton;color:#f2ece0;letter-spacing:.03em;white-space:nowrap">LOS ARCHIVOS<br><span style="color:{ACC}">DEL TERROR</span></div>'
    js = f"shot('cam', 0, {d}, [1.0,0,0], [1.07,0,0]);" + ("tag(0.05);" if lab else "")
    return S(html, js, fg=fg + lab)


@scene(59)
def s59(p, d):
    r = random.Random(59)
    bands = "".join(f'<div id="{p}-b{i}" style="position:absolute;left:0;top:{r.randint(0, 1040)}px;width:1920px;height:{r.randint(6, 40)}px;background:rgba({r.choice(["240,234,220", "200,190,170", "120,110,96"])},{r.uniform(.35, .8):.2f})"></div>' for i in range(22))
    html = f'''<div id="{p}-cam" class="ao-cam" style="background:#050302" data-layout-allow-overflow>
<div id="{p}-pile" class="ao-full" style="filter:blur(3px) brightness(.45)">{paper_pile(58, 70, (0, 0, 1920, 1080))}</div>{bands}
<div style="position:absolute;left:150px;top:120px;font:700 70px 'IBM Plex Mono';color:#f2f4f3">◀◀</div><div id="{p}-blk" class="ao-full" style="background:#000;opacity:0"></div></div>'''
    js = "".join(f"tl.fromTo(q('b{i}'), {{ y: 0 }}, {{ y: {r.choice([-1, 1]) * r.randint(200, 900)}, duration: 0.6, ease: 'none' }}, 0);" for i in range(22))
    js += "tl.fromTo(q('pile'), { y: 0, scaleY: 1 }, { y: 400, scaleY: 1.3, duration: 0.6, ease: 'power2.in' }, 0); tl.set(q('blk'), { opacity: 1 }, 0.6);"
    return S(html, js)


@scene(60)
def s60(p, d):
    line1, line2 = "MAYO · 1954", "ASUNCIÓN"
    l1, n1 = typed(p, "a", line1)
    l2, n2 = typed(p, "b", line2)
    x1 = (1920 - len(line1) * 0.6 * 128) / 2
    digits = "".join(f'<span style="display:inline-block;width:.6em;height:1em;overflow:hidden;vertical-align:top"><span id="{p}-r{i}" style="display:block">'
                     + "".join(f"<span style='display:block;height:1em'>{c}</span>" for c in seq) + "</span></span>"
                     for i, seq in enumerate(["1", "9", "98765", "2109876543210987654"]))
    html = f'''<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow style="background:#050302">
{f'<img src="assets/img/{NEWPH["palacio"]}" class="ao-full" style="object-fit:cover;filter:brightness(.45)" alt="">' if NEWOK["palacio"] else '<img src="assets/img/stroessner_sepia.jpg" style="position:absolute;left:0;top:-500px;width:1920px;height:2886px;object-fit:cover;filter:blur(34px) brightness(.38)" alt="">'}</div>'''
    fg = f'''<div id="{p}-roll" style="position:absolute;left:0;width:1920px;top:400px;text-align:center;font:700 200px/1 'Courier Prime';color:{ACC};height:200px;overflow:hidden">{digits}</div>
<div id="{p}-card" style="opacity:0"><div class="dc-line dc-d" style="left:{x1:.0f}px;top:400px">{l1}</div>
<div class="dc-line dc-p" style="left:{x1 + 8:.0f}px;top:570px">{l2}<span id="{p}-cur" class="dc-cur"></span></div></div>'''
    js = f"""tl.fromTo(q('r2'), {{ y: 0 }}, {{ y: '-80%', duration: 0.7, ease: 'power2.inOut' }}, 0.05);
tl.fromTo(q('r3'), {{ y: 0 }}, {{ y: '-94.737%', duration: 0.7, ease: 'power2.inOut' }}, 0.05);
/*cut*/ tl.set(q('roll'), {{ opacity: 0 }}, 1.0); tl.set(q('card'), {{ opacity: 1 }}, 1.0);
for (let i = 0; i < {n1}; i++) tl.set(q('a' + i), {{ display: 'inline' }}, 1.0 + i * 0.03);
type('b', {n2}, 1.35, 0.06); blink('cur', 1.0, {d}, 0.25);
shot('cam', 0, 1.0, [1.2,0,0], [1.25,0,0]); shot('cam', 1.0, {d}, [1.0,-200,-10], [1.04,-200,-12]);"""
    return S(html, js, DATE_CSS, fg=fg)


def origen(p, mode):
    yrs = "".join(f'<div style="position:absolute;left:{260 + (y - 1954) * 40}px;top:600px;width:3px;height:{30 if y % 5 == 0 else 14}px;background:#3d3428"></div>' for y in range(1954, 1990))
    lbls = "".join(f'<div style="position:absolute;left:{260 + (y - 1954) * 40 - 50}px;top:640px;width:100px;text-align:center;font:700 30px Courier Prime;color:#3d3428">{y}</div>' for y in (1954, 1964, 1974, 1984, 1989))
    html = f'<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>{BIGPAPER()}</div>'
    blocks = ""
    if mode == "periods":
        blocks = "".join(f'<div id="{p}-k{i}" style="position:absolute;left:{260 + i * 200}px;top:470px;width:186px;height:110px;border:5px solid {ACC};opacity:0"><div style="font:400 64px/100px Anton;color:#2a2219;text-align:center">{i + 1}</div></div>' for i in range(7))
    big = ""
    if mode == "years":
        big = f"<span id='{p}-n' class='ao-num' style='font-size:230px'>0</span><span class='ao-unit' style='font-size:110px;color:#1f1b15'> AÑOS</span>"
    if mode == "periods":
        big = f"<span class='ao-unit' style='font-size:110px;color:#1f1b15'>= </span><span id='{p}-n' class='ao-num' style='font-size:190px'>0</span><span class='ao-unit' style='font-size:92px;color:#1f1b15'> PERÍODOS PRESIDENCIALES</span>"
    fg = f'''<div id="{p}-g" class="ao-full" style="transform-origin:50% 50%">
<div id="{p}-ax" style="position:absolute;left:260px;top:592px;width:1400px;height:8px;background:#2e2820;transform-origin:0 50%"></div>
<div id="{p}-fill" style="position:absolute;left:260px;top:592px;width:1400px;height:8px;background:{ACC};transform-origin:0 50%;transform:scaleX(0)"></div>
{yrs}{lbls}<div class="tl-dot" style="left:260px;top:596px"></div>{blocks}
<div id="{p}-mk" style="position:absolute;left:190px;top:330px;font:700 54px 'Courier Prime';letter-spacing:.12em;color:#1f1b15;opacity:0;border-left:10px solid {ACC};padding-left:22px">MAYO 1954<br><span style="font-family:Anton;font-weight:400;font-size:92px;color:#1f1b15;letter-spacing:.03em">GOLPE MILITAR</span></div>
<div id="{p}-big" style="position:absolute;left:0;width:1920px;top:{720 if mode != 'periods' else 140}px;text-align:center;opacity:0;white-space:nowrap">{big}</div></div>'''
    return html, fg


@scene(61)
def s61(p, d):
    html, fg = origen(p, "open")
    js = f"""tl.fromTo(q('ax'), {{ scaleX: 0.02 }}, {{ scaleX: 1, duration: 1.2, ease: 'power3.out' }}, 0.1);
shot('cam', 0, 0.9, [2.2,1150,-120], [2.25,1140,-120]); shot('g', 0, 0.9, [2.2,1150,-120], [2.25,1140,-120]);
/*cut*/ shot('cam', 0.9, {d}, [1.0,0,0], [1.02,-10,0]); shot('g', 0.9, {d}, [1.0,0,0], [1.02,-10,0]);"""
    return S(html, js, TL_CSS, fg=fg)


@scene(62)
def s62(p, d):
    # print at 1x; the close crop stays within 1.5x of the 1206 px scan
    html = f'''<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>{print_html(p, 660, 0, 640, 1000, 1.5, "50% 0%", "cover")}</div>'''
    js = f"""shot('cam', 0, 1.1, [1.0,0,0], [1.04,-10,0]); /*cut*/ shot('cam', 1.1, {d}, [1.65,0,360,-2], [1.7,0,370,-2]); tag(0.05);
tl.fromTo(q('print'), {{ x: 20 }}, {{ x: -20, duration: {d}, ease: 'none' }}, 0);"""
    return S(html, js, fg=tag_html(p, "IMAGEN REAL · Alfredo Stroessner, agosto de 1954 (Casa Resck)", src=True))


@scene(63)
def s63(p, d):
    html, fg = origen(p, "mark")
    js = f"""tl.fromTo(q('mk'), {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: 'expo.out' }}, 0.15);
shot('cam', 0, {d}, [1.0,0,0], [1.03,0,0]); shot('g', 0, {d}, [1.0,0,0], [1.03,0,0]);"""
    return S(html, js, TL_CSS, fg=fg)


@scene(64)
def s64(p, d):
    html, fg = origen(p, "years")
    js = f"""tl.set(q('mk'), {{ opacity: 1 }}, 0); tl.fromTo(q('fill'), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.15, ease: 'power1.inOut' }}, 0.05);
tl.set(q('big'), {{ opacity: 1 }}, 0.05); count('n', 0, 35, 0.05, 1.15);
shot('cam', 0, 1.25, [1.0,0,0], [1.02,0,0]); shot('g', 0, 1.25, [1.0,0,0], [1.02,0,0]);
/*cut*/ shot('cam', 1.25, {d}, [1.9,0,-800], [1.94,0,-815]); shot('g', 1.25, {d}, [1.9,0,-800], [1.94,0,-815]);"""
    return S(html, js, TL_CSS, fg=fg)


@scene(65)
def s65(p, d):
    html, fg = origen(p, "periods")
    js = f"""tl.set(q('fill'), {{ scaleX: 1 }}, 0); tl.set(q('big'), {{ opacity: 1 }}, 0);
{"".join(f"tl.fromTo(q('k{i}'), {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.15, ease: 'power3.out' }}, {0.1 + i * 0.15:.2f}); tl.set(q('n'), {{ textContent: '{i + 1}' }}, {0.1 + i * 0.15:.2f});" for i in range(7))}
shot('cam', 0, 1.25, [1.15,0,150], [1.17,0,150]); shot('g', 0, 1.25, [1.15,0,150], [1.17,0,150]);
/*cut*/ shot('cam', 1.25, {d}, [1.0,0,0], [1.02,0,0]); shot('g', 1.25, {d}, [1.0,0,0], [1.02,0,0]);"""
    return S(html, js, TL_CSS, fg=fg)
