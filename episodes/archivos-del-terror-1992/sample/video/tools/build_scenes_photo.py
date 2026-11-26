# Photo versions of the recreation rows (sample/photo-plan.md, LICENSES.md §8-1). Executed after build_scenes_a/b:
# each override replaces SC[n] only when its photos were prepared (prep_photos.py writes assets/ph/ph.json);
# otherwise the graphic version stays. US buildings and archives are never presented as the Paraguayan site:
# every one carries RECREACIÓN or Imagen ilustrativa.
_phj = os.path.join(ASSETS, "ph", "ph.json")
PHI = json.load(open(_phj)) if os.path.exists(_phj) else {}
REAL_ROWS = set()          # rows whose picture is a real photograph or scan (for the real-footage share)


def has(*k):
    return all(x in PHI for x in k)


def cover(p, key, pid="pl", extra="", scale=1.0, dx=0, dy=0):
    """Photo covering the frame (centre), returns html and the source magnification at scale 1."""
    i = PHI[key]
    w = max(1920, 1080 * i["w"] / i["h"]) * scale
    h = w * i["h"] / i["w"]
    return (f'<img id="{p}-{pid}" src="assets/ph/{key}.jpg" style="position:absolute;left:{(1920 - w) / 2 + dx:.0f}px;top:{(1080 - h) / 2 + dy:.0f}px;'
            f'width:{w:.0f}px;height:{h:.0f}px;{extra}" alt="">')


def mag(key, scale=1.0):
    i = PHI[key]
    return max(1920, 1080 * i["w"] / i["h"]) * scale / i["src_w"]


def glow(x, y, r, color, op=1.0, blend="screen"):
    return (f'<div style="position:absolute;left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;'
            f'background:radial-gradient(circle,{color},rgba(0,0,0,0) 70%);opacity:{op};mix-blend-mode:{blend}"></div>')


def rays(p, key="rays", angle=115, color="255,236,200", op=0.5):
    return (f'<div id="{p}-{key}" style="position:absolute;left:-600px;top:-500px;width:3000px;height:2200px;mix-blend-mode:screen;opacity:{op};'
            f'background:repeating-linear-gradient({angle}deg,rgba({color},0) 0px,rgba({color},0) 120px,rgba({color},.35) 180px,rgba({color},0) 260px);filter:blur(18px)"></div>')


def check_mag(n, key, s):
    m = mag(key, s)
    assert m <= 1.5 + 1e-6, f"row {n}: {key} shown at {m:.2f}x of its source pixels"


# ------------------------------------------------------------------ apertura: police building (Tucson HABS plate, not the site)
if has("comandancia", "arch"):
    @scene(9)
    def s09(p, d):
        check_mag(9, "comandancia", 1.12); check_mag(9, "arch", 1.15)
        a = f'''<div id="{p}-A" class="ao-full" style="background:#05080a">{cover(p, "comandancia")}
{glow(260, 120, 520, "rgba(255,246,228,.75)")}{smoke_html(p, 2, 0.18, "mix-blend-mode:screen")}{dust_html(p, 30, (0, 100, 1920, 900), 9)}</div>'''
        b = f'''<div id="{p}-B" class="ao-full" style="opacity:0;background:#05080a">{cover(p, "arch", "pb")}{glow(1000, 300, 500, "rgba(255,246,228,.4)")}</div>'''
        js = f"""shot('A', 0, 0.85, [1.06,0,0], [1.12,-30,-10]); tl.fromTo(q('smk2'), {{ x: 0 }}, {{ x: -120, duration: {d}, ease: 'none' }}, 0); dust(30, 0, {d});
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 0.85); tl.set(q('B'), {{ opacity: 1 }}, 0.85); shot('B', 0.85, {d}, [1.08,0,0], [1.15,-20,10]); lt(0.15); tag(0.05);"""
        REAL_ROWS.add(9)
        return S(a + b, js, fg=tag_html(p, "RECREACIÓN") + lt_html(p, "Departamento de Producciones", "Policía · Lambaré"))

    @scene(10)
    def s10(p, d):
        check_mag(10, "arch", 1.12); check_mag(10, "comandancia", 1.08)
        a = f'''<div id="{p}-A" class="ao-full" style="background:#05080a">{cover(p, "arch")}{glow(1080, 700, 420, "rgba(255,240,214,.25)")}
<img id="{p}-man" src="assets/fig/man_back.png" style="position:absolute;left:520px;top:200px;width:844px;height:1500px;transform-origin:50% 100%" alt=""></div>'''
        b = f'''<div id="{p}-B" class="ao-full" style="opacity:0;background:#05080a">{cover(p, "comandancia", "pb")}{glow(260, 120, 520, "rgba(255,246,228,.7)")}
<img id="{p}-man2" src="assets/fig/man_back.png" style="position:absolute;left:842px;top:745px;width:101px;height:180px;filter:brightness(.4)" alt=""></div>'''
        js = f"""shot('A', 0, 1.1, [1.04,0,0], [1.12,0,20]);
tl.fromTo(q('man'), {{ x: -260, y: 0, scale: 1.0, filter: 'blur(10px)' }}, {{ x: 120, y: -680, scale: 0.42, filter: 'blur(1px)', duration: 1.1, ease: 'none' }}, 0);
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.1); tl.set(q('B'), {{ opacity: 1 }}, 1.1); shot('B', 1.1, {d}, [1.0,0,0], [1.08,-40,0]);
tl.fromTo(q('man2'), {{ x: -40, y: 18 }}, {{ x: 20, y: 0, duration: {d - 1.1:.2f}, ease: 'none' }}, 1.1); tag(0.05);"""
        REAL_ROWS.add(10)
        return S(a + b, js, fg=tag_html(p, "RECREACIÓN"))

    @scene(26)
    def s26(p, d):
        st = f'<div id="{p}-st" class="ao-stampT" style="position:absolute;left:600px;top:250px;font-size:96px;background:rgba(5,7,9,.6)">VERSIÓN POLICIAL</div>'
        html = f'<div id="{p}-cam" class="ao-cam" style="background:#030507">{cover(p, "comandancia", extra="filter:brightness(.5) contrast(1.15)")}</div>'
        js = f"shot('cam', 0, {d}, [1.0,0,0], [1.09,-20,0]); stampIn('st', 0.2, -3); tag(0.05);"
        REAL_ROWS.add(26)
        return S(html, js, fg=st + tag_html(p, "RECREACIÓN"))

    def _doorway_photo(p, glowop):
        return (cover(p, "arch") + glow(1080, 640, 380, f"rgba(236,242,246,{glowop})") +
                f'<div style="position:absolute;left:760px;top:330px;width:640px;height:700px;background:radial-gradient(ellipse at 50% 60%,rgba(232,240,244,{glowop}),rgba(232,240,244,0) 70%)"></div>')

    @scene(28)
    def s28(p, d):
        rim = "filter:drop-shadow(0 0 10px rgba(236,244,248,.6)) drop-shadow(0 0 2px rgba(255,255,255,.8))"
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#05080a" data-layout-allow-overflow>{_doorway_photo(p, .85)}
{fig_img(p, "g", "guard", 830, 300, 720, rim)}{fig_img(p, "j", "man_back", -340, 160, 1500, "filter:blur(14px) brightness(.5)")}{smoke_html(p, 1, 0.16, "mix-blend-mode:screen")}</div>'''
        js = f"""tl.fromTo(q('g'), {{ y: 30 }}, {{ y: 0, duration: 0.4, ease: 'power3.out' }}, 0.2); shot('cam', 0, 1.25, [1.0,0,0], [1.04,0,0]);
/*cut*/ shot('cam', 1.25, {d}, [2.3,-430,700], [2.36,-445,715]); lt(0.2); tag(0.05);"""
        REAL_ROWS.add(28)
        return S(html, js, fg=tag_html(p, "RECREACIÓN") + lt_html(p, "Oficial de guardia", "Policía · entrada del depósito"))

    @scene(29)
    def s29(p, d):
        base = SC_PREV[29](p, d)
        rim = "filter:drop-shadow(0 0 12px rgba(236,244,248,.55))"
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#05080a" data-layout-allow-overflow>{_doorway_photo(p, 1.0)}
{fig_img(p, "g", "guard", 880, 360, 640, "filter:blur(5px) brightness(.8)")}{fig_img(p, "j", "judge", 140, 120, 1300, rim)}{smoke_html(p, 1, 0.18, "mix-blend-mode:screen")}</div>'''
        paper = base["html"][base["html"].index(f'<div id="{p}-B"'):]
        REAL_ROWS.add(29)
        return S(html + paper, base["js"], fg=base["fg"])


# ------------------------------------------------------------------ the drawer: a real record-vault cabinet (HABS, Philadelphia)
if has("cabinets"):
    @scene(25)
    def s25(p, d):
        check_mag(25, "cabinets", 2.0 * 1.03)
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030507" data-layout-allow-overflow>{cover(p, "cabinets", extra="filter:contrast(1.1)")}
{glow(1250, 380, 300, "rgba(220,232,240,.35)")}{dust_html(p, 34, (1080, 220, 1450, 540), 25, color="rgba(220,232,240,.85)")}</div>'''
        js = f"""shot('cam', 0, 1.15, [1.0,0,0], [1.06,-30,0]); /*cut*/ shot('cam', 1.15, {d}, [2.0,-580,320], [2.06,-610,330]); dust(34, 0.3, {d - 0.3:.2f}); tag(0.05);"""
        REAL_ROWS.add(25)
        return S(html, js, fg=tag_html(p, "RECREACIÓN"))


if has("typewriter"):
    @scene(27)
    def s27(p, d):
        t, n = typed(p, "t", "NADA QUE BUSCAR")
        w = 15 * 0.6 * 150
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030507" data-layout-allow-overflow>{cover(p, "typewriter", extra="filter:blur(5px) brightness(.45)")}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(3,5,7,.2),rgba(3,5,7,.75) 80%)"></div></div>'''
        fg = f'''<div id="{p}-g" class="ao-full" style="transform-origin:50% 50%"><div style="position:absolute;left:{(1920 - w) / 2:.0f}px;top:470px;font:700 150px 'Courier Prime';color:#f1ede2;white-space:nowrap;text-shadow:0 4px 30px rgba(0,0,0,.8)">{t}<span id="{p}-cur" style="display:inline-block;width:80px;height:130px;background:{ACC};vertical-align:-14px"></span></div></div>'''
        js = f"""type('t', {n}, 0.05, 0.05); blink('cur', 0, {d}, 0.25); shot('cam', 0, 0.85, [1.0,0,0], [1.03,0,0]); shot('g', 0, 0.85, [1.0,0,0], [1.03,0,0]);
/*cut*/ shot('cam', 0.85, {d}, [1.4,-300,100,-2], [1.44,-320,100,-2]); shot('g', 0.85, {d}, [2.2,-640,-60,-2], [2.26,-680,-60,-2]); tag(0.05);"""
        REAL_ROWS.add(27)
        return S(html, js, fg=fg + tag_html(p, "IMAGEN ILUSTRATIVA · Máquina de escribir (OWI, 1942)", src=True))


# ------------------------------------------------------------------ discovery: stairs, door, vault, records (tungsten)
if has("stairway"):
    @scene(31)
    def s31(p, d):
        check_mag(31, "stairway", 1.45)
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#020101" data-layout-allow-overflow>{cover(p, "stairway")}
<div id="{p}-torch" class="ao-full" style="background:radial-gradient(circle at 72% 62%,rgba(0,0,0,0) 12%,rgba(0,0,0,.82) 34%,rgba(0,0,0,.95) 60%)"></div>
{dust_html(p, 26, (1100, 300, 1800, 900), 31)}</div>'''
        js = f"""shot('cam', 0, {d}, [1.35,-560,-80], [1.45,-640,140]); tl.fromTo(q('torch'), {{ x: 60, y: 160 }}, {{ x: -40, y: -120, duration: {d}, ease: 'none' }}, 0); dust(26, 0, {d}); tag(0.05);"""
        REAL_ROWS.add(31)
        return S(html, js, fg=tag_html(p, "RECREACIÓN"))

if has("stairdoor"):
    @scene(32)
    def s32(p, d):
        # A6 padlock (cropped from the Varlan photo, soft mask) hung on the HABS basement door at its latch
        lock = (f'<div style="position:absolute;left:770px;top:640px;width:300px;height:300px;border-radius:50%;overflow:hidden;'
                f'-webkit-mask-image:radial-gradient(circle,#000 45%,transparent 70%);mask-image:radial-gradient(circle,#000 45%,transparent 70%)">'
                f'<div style="position:absolute;left:-560px;top:-220px;width:1500px;height:1000px;background:url(assets/img/padlocks_cool.jpg) 0 0/100% 100%;filter:sepia(.5) brightness(.85)"></div></div>')
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#020101" data-layout-allow-overflow>{cover(p, "stairdoor")}{lock}
<div id="{p}-beam" class="ao-full" style="background:radial-gradient(circle at 48% 66%,rgba(0,0,0,0) 14%,rgba(0,0,0,.8) 38%,rgba(0,0,0,.95) 64%)"></div></div>'''
        js = f"shot('cam', 0, {d}, [1.0,0,0], [1.12,-40,-60], 'power1.inOut'); tl.fromTo(q('beam'), {{ x: -220, y: 80 }}, {{ x: 0, y: 0, duration: 0.7, ease: 'power2.out' }}, 0); tag(0.05);"
        REAL_ROWS.add(32)
        return S(html, js, fg=tag_html(p, "RECREACIÓN"))

if has("vault"):
    @scene(35)
    def s35(p, d):
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#020101" data-layout-allow-overflow>{cover(p, "vault")}
{dust_html(p, 40, (500, 200, 1500, 900), 35)}<div id="{p}-fl" class="ao-full" style="background:radial-gradient(circle at 50% 45%,#fff8ec,#ffe6c4 40%,rgba(255,220,180,.6) 80%)"></div></div>'''
        js = f"""tl.fromTo(q('fl'), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.55, ease: 'power2.out' }}, 0.05); shot('cam', 0, {d}, [1.15,0,0], [1.06,0,10]); dust(40, 0, {d}); tag(0.05);"""
        REAL_ROWS.add(35)
        return S(html, js, fg=tag_html(p, "RECREACIÓN"))

if has("records", "records_tall"):
    @scene(36)
    def s36(p, d):
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030201" data-layout-allow-overflow>{cover(p, "records")}
{glow(1100, 160, 360, "rgba(255,214,150,.45)")}{smoke_html(p, 0, 0.12, "mix-blend-mode:screen;filter:sepia(1)")}{dust_html(p, 34, (500, 100, 1500, 700), 36)}</div>'''
        js = f"shot('cam', 0, {d}, [1.04,40,0], [1.14,-30,10]); tl.fromTo(q('smk0'), {{ x: 0 }}, {{ x: -100, duration: {d}, ease: 'none' }}, 0); dust(34, 0, {d}); whipIn('cam', 0, 320); tag(0.05);"
        REAL_ROWS.add(36)
        return S(html, js, fg=tag_html(p, "IMAGEN ILUSTRATIVA · Archivo de registros, EE. UU. (HABS, 1982)", src=True))

    @scene(39)
    def s39(p, d):
        base = SC_PREV[39](p, d)
        a = f'<div id="{p}-A" class="ao-full" style="background:#030201">{cover(p, "records", extra="filter:blur(6px) brightness(.38)")}</div>'
        b = f'<div id="{p}-B" class="ao-full" style="opacity:0;background:#030201">{cover(p, "records_tall", "pb", "filter:brightness(.8)", 1.0, 420, 300)}</div>'
        js = base["js"].replace("shot('B', 1.1, {d}, [1.05,0,0,-3], [1.1,0,-40,-3]);".format(d=d), f"shot('B', 1.1, {d}, [1.2,0,0], [1.26,0,-20]);")
        REAL_ROWS.add(39)
        return S(a + b, js, fg=base["fg"])

    @scene(40)
    def s40(p, d):
        i = PHI["records_tall"]
        h = 1920 * i["h"] / i["w"]
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030201" data-layout-allow-overflow>
<img id="{p}-pl" src="assets/ph/records_tall.jpg" style="position:absolute;left:0;top:0;width:1920px;height:{h:.0f}px" alt="">{glow(960, 200, 400, "rgba(255,214,150,.35)")}</div>'''
        fg = f'<div style="position:absolute;left:0;width:1920px;top:250px;text-align:center;text-shadow:0 6px 40px rgba(0,0,0,.9)"><span class="ao-unit" style="font-size:130px;color:{ACC}">≈ </span><span class="ao-num" style="font-size:240px">800.000</span><div class="ao-unit" style="font-size:96px">PÁGINAS</div></div>'
        js = f"tl.fromTo(q('pl'), {{ y: {1080 - h:.0f} }}, {{ y: -120, duration: {d}, ease: 'power1.inOut' }}, 0); tag(0.0);"
        REAL_ROWS.add(40)
        return S(html, js, fg=fg + tag_html(p, UNESCO, src=True))

if has("catalog"):
    @scene(37)
    def s37(p, d):
        check_mag(37, "catalog", 2.2)
        card = f'''<div id="{p}-card" style="position:absolute;left:760px;top:420px;width:420px;height:270px;background:#e8d8b4 url(assets/tex/paper_tung.jpg) 0 0/2400px 1600px;background-blend-mode:multiply;box-shadow:0 20px 40px rgba(0,0,0,.7)">
<div style="position:absolute;left:0;right:0;top:50px;height:3px;background:#6b5c48;opacity:.75"></div>
<div style="position:absolute;left:14px;top:14px;width:390px;height:240px;background:url(assets/tex/scribble0.png) 0 0/100% 100%;opacity:.85"></div></div>'''
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030201" data-layout-allow-overflow>{cover(p, "catalog")}{glow(960, 300, 500, "rgba(255,214,150,.3)")}</div>'''
        js = f"""shot('cam', 0, {d}, [1.1,0,0], [2.0,200,-120], 'power2.in'); tl.fromTo(q('card'), {{ y: 160, opacity: 0, scale: .8 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.5, ease: 'power3.out' }}, 0.6); tag(0.05);"""
        REAL_ROWS.add(37)
        return S(html, js, fg=card + tag_html(p, "RECREACIÓN"))

    @scene(42)
    def s42(p, d):
        base = SC_PREV[42](p, d)
        h = base["html"]
        i0 = h.index(f'<div id="{p}-A"'); i1 = h.index(f'<div id="{p}-B"')
        a = f'''<div id="{p}-A" class="ao-full" style="background:#030201">{cover(p, "catalog", extra="filter:brightness(.5)")}
<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(3,2,1,.85) 0,rgba(3,2,1,.4) 45%,rgba(3,2,1,.05) 80%)"></div></div>'''
        js = re.sub(r"tl\.set\(q\('g\d+'\), \{ opacity: 1 \}, [\d.]+\);", "", base["js"])
        js += f"shot('A', 0, 1.1, [1.0,0,0], [1.06,0,0]);"
        REAL_ROWS.add(42)
        return S(h[:i0] + a + h[i1:], js, fg=base["fg"].replace(tag_html(p, UNESCO, src=True), "") + tag_html(p, UNESCO, src=True))

    @scene(56)
    def s56(p, d):
        base = SC_PREV[56](p, d)
        bg = f'<div id="{p}-ph" class="ao-full" style="opacity:0">{cover(p, "catalog", extra="filter:brightness(.42)")}</div>'
        js = base["js"] + f"tl.set(q('ph'), {{ opacity: 1 }}, 1.3); tl.set(q('wall'), {{ opacity: 0 }}, 1.3);"
        html = base["html"].replace('<div class="ao-full" style="background:rgba(5,3,2,.62)"></div>', bg + '<div class="ao-full" style="background:rgba(5,3,2,.45)"></div>')
        REAL_ROWS.add(56)
        return S(html, js, fg=base["fg"])

if has("ledger"):
    @scene(38)
    def s38(p, d):
        check_mag(38, "ledger", 1.2)
        html = f'''<div id="{p}-cam" class="ao-cam" style="background:#030201" data-layout-allow-overflow>{cover(p, "ledger")}
<div class="ao-full" style="background:linear-gradient(90deg,rgba(3,2,1,.8),rgba(3,2,1,0) 35%,rgba(3,2,1,0) 65%,rgba(3,2,1,.85))"></div></div>'''
        js = f"shot('cam', 0, {d}, [1.18,120,0,-3], [1.18,-140,-10,-3]); whipIn('cam', 0, 320); tag(0.05);"
        REAL_ROWS.add(38)
        return S(html, js, fg=tag_html(p, "IMAGEN ILUSTRATIVA · Libro de registro, EE. UU. (HAER)", src=True))

    @scene(49)
    def s49(p, d):
        base = SC_PREV[49](p, d)
        h = base["html"]
        stains = "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{int(w * .8)}px;border-radius:50%;border:9px solid rgba(70,48,24,.45);box-shadow:inset 0 0 60px rgba(70,48,24,.4)"></div>' for x, y, w in ((300, 150, 520), (1100, 520, 620), (420, 640, 360)))
        a = f'''<div id="{p}-A" class="ao-full" style="background:#050302"><div id="{p}-pa" class="ao-full">{cover(p, "ledger", extra="filter:brightness(.9)")}{stains}</div>
<div class="ao-full" style="background:linear-gradient(180deg,rgba(5,3,2,.75),rgba(5,3,2,0) 30%,rgba(5,3,2,0) 70%,rgba(5,3,2,.8))"></div></div>'''
        i1 = h.index(f'<div id="{p}-B"')
        REAL_ROWS.add(49)
        return S(a + h[i1:], base["js"], fg=base["fg"])

if has("aisle"):
    @scene(41)
    def s41(p, d):
        base = SC_PREV[41](p, d)
        h = base["html"]
        i1 = h.index(f'<div id="{p}-B"')
        a = f'''<div id="{p}-A" class="ao-full" style="background:#030201">{cover(p, "aisle")}{glow(1300, 380, 300, "rgba(255,214,150,.3)")}
<div class="ao-full" style="background:linear-gradient(180deg,rgba(3,2,1,.1),rgba(3,2,1,.55) 60%,rgba(3,2,1,.85))"></div></div>'''
        fg = base["fg"].replace(f'''<div style="position:absolute;left:0;top:500px;width:1920px;height:12px"><div id="{p}-tape" style="position:absolute;left:160px;top:0;width:1600px;height:10px;background:{ACC};transform-origin:0 50%"></div></div>''',
                                f'''<svg width="1920" height="1080" style="position:absolute;left:0;top:0"><path id="{p}-tp" d="M120,1000 L1300,470" stroke="{ACC}" stroke-width="10" stroke-dasharray="1300" stroke-dashoffset="1300"/></svg>''')
        js = base["js"].replace("tl.fromTo(q('tape'), { scaleX: 0 }, { scaleX: 1, duration: 1.0, ease: 'power2.inOut' }, 0.1);", "tl.to(q('tp'), { attr: { 'stroke-dashoffset': 0 }, duration: 1.0, ease: 'power2.inOut' }, 0.1);")
        js = js.replace("tl.fromTo(q('sh'), { x: 0 }, { x: -500, duration: 1.25, ease: 'none' }, 0);", "shot('A', 0, 1.25, [1.08,0,0], [1.16,-40,0]);")
        REAL_ROWS.add(41)
        return S(a + h[i1:], js, fg=fg.replace('top:560px;text-align:center', 'top:640px;text-align:center'))

if has("fpcab"):
    @scene(55)
    def s55(p, d):
        base = SC_PREV[55](p, d)
        b = f'<div id="{p}-B" class="ao-full" style="opacity:0;background:#030201">{cover(p, "fpcab")}</div>'
        js = base["js"].replace(f"/*cut*/ shot('cam', 1.25, {d}, [2.6,-1130,-110], [2.66,-1160,-115]);", f"/*cut*/ tl.set(q('B'), {{ opacity: 1 }}, 1.25); shot('B', 1.25, {d}, [1.05,0,0], [1.12,-30,0]); tl.set(q('tag'), {{ opacity: 0 }}, 1.25); tl.set(q('tag2'), {{ opacity: 1 }}, 1.25);")
        t2 = tag_html(p, "IMAGEN ILUSTRATIVA · Archivo de huellas, EE. UU. (1930)", src=True).replace(f'id="{p}-tag"', f'id="{p}-tag2" style="opacity:0"')
        REAL_ROWS.add(55)
        return S(base["html"] + b, js, fg=base["fg"] + t2)


# ------------------------------------------------------------------ maps and 1954
if has("nasa96"):
    @scene(4)
    def s04(p, d):
        base = SC_PREV[4](p, d)
        a = f'<div id="{p}-N" class="ao-full" style="background:#000">{cover(p, "nasa96")}</div>'
        js = base["js"].replace("0.05);\ntl.to(q('rad')", "0.65);\ntl.to(q('rad')")
        js = js.replace("duration: 0.7, ease: 'power2.inOut' }, 0.05);", "duration: 0.45, ease: 'power2.inOut' }, 0.62);").replace("duration: 0.6, ease: 'power2.inOut' }, 0.35);", "duration: 0.4, ease: 'power2.inOut' }, 0.8);")
        js = js.replace("{ opacity: 1, duration: 0.2 }, 0.6);", "{ opacity: 1, duration: 0.2 }, 1.0);").replace("{ opacity: 1, duration: 0.2 }, 0.85);", "{ opacity: 1, duration: 0.2 }, 1.1);")
        js += f"""shot('N', 0, 0.6, [1.0,0,0], [1.12,40,-30]); /*cut*/ tl.set(q('N'), {{ opacity: 0 }}, 0.6); tl.set(q('tagn'), {{ opacity: 0 }}, 0.6);
tl.set(q('tag'), {{ opacity: 0 }}, 0); tl.set(q('tag'), {{ opacity: 1 }}, 0.6);"""
        tn = tag_html(p, "IMAGEN REAL · NASA, misión STS-72 (1996)", src=True).replace(f'id="{p}-tag"', f'id="{p}-tagn"')
        REAL_ROWS.add(4)
        return S(base["html"] + a, js, fg=base["fg"] + tn)

if has("map1856"):
    _old_map_svg = map_svg

    def map_svg(p, hi=(), extra="", labels=True):
        return _old_map_svg(p, hi, extra, labels).replace('href="assets/tex/oldmap_land.jpg" width="2048" height="2048"', 'href="assets/ph/map1856.jpg" width="1600" height="900"').replace(
            'patternUnits="userSpaceOnUse" width="2048" height="2048"><image href="assets/ph/map1856.jpg"', 'patternUnits="userSpaceOnUse" width="1600" height="900"><image href="assets/ph/map1856.jpg"')

if has("palacio"):
    @scene(60)
    def s60(p, d):
        base = SC_PREV[60](p, d)
        html = f'<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow style="background:#050302">{cover(p, "palacio", extra="filter:brightness(.42)", scale=1.3)}</div>'
        tg = tag_html(p, "IMAGEN REAL · Asunción, c. 1910 (Library of Congress)", src=True)
        REAL_ROWS.add(60)
        return S(html, base["js"] + "tag(1.0);", base["css"], fg=base["fg"] + tg)

if has("cia1954"):
    @scene(63)
    def s63(p, d):
        base = SC_PREV[63](p, d)
        i = PHI["cia1954"]
        doc = (f'<img src="assets/ph/cia1954.jpg" style="position:absolute;left:1280px;top:-250px;width:480px;height:{480 * i["h"] / i["w"]:.0f}px;transform:rotate(3deg);'
               f'filter:blur(3px);box-shadow:0 30px 60px rgba(0,0,0,.5);opacity:.8" alt="">')
        html = base["html"].replace(f'{BIGPAPER()}</div>', f'{BIGPAPER()}{doc}</div>', 1)
        REAL_ROWS.add(63)
        return S(html, base["js"], base["css"], fg=base["fg"])

if has("condor76"):
    @scene(53)
    def s53(p, d):
        base = SC_PREV[53](p, d)
        i = PHI["condor76"]
        doc = (f'<img src="assets/ph/condor76.jpg" style="position:absolute;left:560px;top:-60px;width:820px;height:{820 * i["h"] / i["w"]:.0f}px;transform:rotate(-4deg);'
               f'filter:blur(5px) brightness(.45);box-shadow:0 30px 60px rgba(0,0,0,.6)" alt="">')
        html = base["html"].replace(f'style="{DESK()}" data-layout-allow-overflow>', f'style="{DESK()}" data-layout-allow-overflow>{doc}', 1)
        REAL_ROWS.add(53)
        return S(html, base["js"], fg=base["fg"])
