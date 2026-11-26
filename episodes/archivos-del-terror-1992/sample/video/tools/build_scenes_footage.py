# Public-domain footage versions (sample/footage-plan.md, LICENSES.md §9). Executed after build_scenes_photo.py.
# Clips are prepared by prep_footage.py (assets/fx/fx.json): sharp clips are shown in frames/windows at most 1.5x of
# their pixels (check_mag), blurred background versions are pre-baked 1920x1080 (the only exception, clearly blurred).
# No fx08–fx12. Every unrelated clip carries IMAGEN ILUSTRATIVA + source; 1945 Asunción carries its year.
_fxj = os.path.join(ASSETS, "fx", "fx.json")
FXI = json.load(open(_fxj)) if os.path.exists(_fxj) else {}
MOVING = {}                # row -> seconds of moving footage on screen (union of clip intervals)
_MOV_IV = {}


def _mov(n, start, dur):
    iv = sorted(_MOV_IV.setdefault(n, []) + [(start, start + dur)])
    merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1] + 1e-6:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    _MOV_IV[n] = merged
    MOVING[n] = sum(b - a for a, b in merged)


def hasfx(*k):
    return all(x in FXI for x in k)


SRCF = {"fbi": "FBI, 1969", "cor": "Coronet, 1941", "army": "Ejército de EE. UU., 1941", "bk": "EE. UU., 1960", "pol": "EE. UU., 1953"}


def fxvid(p, n, key, vid, x, y, w, start, dur, ms=0.0, cam=1.0, z=None):
    """A sharp clip at (x, y), width w (height from the clip), timed [start, start+dur) inside the scene."""
    i = FXI[key]
    m = w / i["w"] * cam
    assert m <= 1.5 + 1e-6, f"row {n}: clip {key} at {m:.2f}x"
    MAGS.setdefault(n, []).append((key, round(m, 2)))
    _mov(n, start, min(dur, FXI[key]["dur"] - ms))
    h = w * i["h"] / i["w"]
    dur = min(dur, i["dur"] - ms)
    zz = f"z-index:{z};" if z else ""
    return (f'<video id="{p}-{vid}" class="clip" src="assets/fx/{key}.mp4" data-start="{start}" data-duration="{dur:.3f}" data-media-start="{ms}" '
            f'muted playsinline style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;{zz}"></video>')


def fxwin(p, n, key, vid, x, y, w, start, dur, rot=0.0, ms=0.0, cam=1.0, wid=None):
    """Clip inside a film-print frame (cream border, shadow); the wrapper is untimed, the video is timed."""
    i = FXI[key]
    h = w * i["h"] / i["w"]
    return (f'<div id="{p}-{wid or vid + "w"}" style="position:absolute;left:{x - 16:.0f}px;top:{y - 16:.0f}px;width:{w + 32:.0f}px;height:{h + 32:.0f}px;'
            f'background:#ece3cf;box-shadow:0 40px 90px rgba(0,0,0,.75);transform:rotate({rot}deg)">'
            + fxvid(p, n, key, vid, 16, 16, w, start, dur, ms, cam) + '</div>')


def fxbg(p, n, key, vid, start, dur, ms=0.0, op=1.0):
    _mov(n, start, min(dur, FXI[key]["dur"] - ms))
    dur = min(dur, FXI[key]["dur"] - ms)
    return (f'<video id="{p}-{vid}" class="clip" src="assets/fx/{key}_bg.mp4" data-start="{start}" data-duration="{dur:.3f}" data-media-start="{ms}" '
            f'muted playsinline style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:{op}"></video>')


def ilus(p, src, key="tag2", top=122, hidden=False):
    return tag2(p, f"IMAGEN ILUSTRATIVA · {src}", key, top, hidden)


def veil(html, op=0.62):
    """Turn the paper sheet of a scene into a translucent veil over a moving background."""
    return html.replace(BIGPAPER(), BIGPAPER().replace('<div style="position:absolute;left:-1500px', f'<div style="opacity:{op};position:absolute;left:-1500px'), 1)


def _cutjs(js, old, new):
    assert old in js, old[:80]
    return js.replace(old, new)


# ------------------------------------------------------------------ 3: orbit (NASA, HD) before the map
if hasfx("f_orbit"):
    _s03 = SC[3]

    @scene(3)
    def s03(p, d):
        base = _s03(p, d)
        js = base["js"]
        for a, b in (("}}, 0.05);", "}}, 0.8);"), ("0.06);", "0.81);"), ("0.67);", "1.0);")):
            js = js.replace(a, b)
        js = js.replace(f"duration: {d - 0.67:.2f}", f"duration: {d - 1.0:.2f}").replace("duration: 0.62, ease: 'expo.inOut'", "duration: 0.2, ease: 'expo.out'")
        js = js.replace("duration: 0.3, ease: 'power2.in', yoyo: true", "duration: 0.1, ease: 'power2.in', yoyo: true").replace("0.62);", "0.95);").replace("tag(0.5);", "")
        js += "tl.set(q('tag'), { opacity: 0 }, 0); tl.set(q('tag'), { opacity: 1 }, 0.8); tl.set(q('tago'), { opacity: 0 }, 0.8);"
        MAGS.setdefault(3, []).append(("f_orbit", round(1920 / FXI["f_orbit"]["w"], 2)))
        MOVING[3] = 0.8
        vid = (f'<video id="{p}-orb" class="clip" src="assets/fx/f_orbit.mp4" data-start="0" data-duration="0.8" data-media-start="0" muted playsinline '
               f'style="position:absolute;left:0;top:-97px;width:1920px;height:1274px;z-index:10"></video>')
        to = tag_html(p, "IMAGEN REAL · NASA/JSC, Estación Espacial Internacional (2011)", src=True).replace(f'id="{p}-tag"', f'id="{p}-tago"')
        REAL_ROWS.add(3)
        return S(base["html"] + vid, js, base["css"], fg=base["fg"] + to)


# ------------------------------------------------------------------ 7: insert instead of A-B-A re-crop of the portrait
if hasfx("f_register"):
    @scene(7)
    def s07(p, d):
        base = SC_PREV[7](p, d)
        b = (f'<div id="{p}-B" class="ao-full" style="opacity:0;{DESK()}">'
             + fxwin(p, 7, "f_register", "reg", 510, 200, 900, 0.8, d - 0.8, -1.5) + '</div>')
        js = _cutjs(base["js"], f"/*cut*/ shot('cam', 0.8, {d}, [1.9,40,560], [1.96,40,575]);", f"/*cut*/ tl.set(q('B'), {{ opacity: 1 }}, 0.8); tl.set(q('tag'), {{ opacity: 0 }}, 0.8); tl.set(q('tag2'), {{ opacity: 1 }}, 0.8);")
        return S(base["html"] + b, js, fg=base["fg"] + ilus(p, "registro, " + SRCF["cor"], hidden=True).replace("top:122px", "top:70px"))


# ------------------------------------------------------------------ 10: the man goes in (Army 1941), then the building
if hasfx("f_enter") and "comandancia" in PHI:
    _s10 = SC[10]

    @scene(10)
    def s10(p, d):
        base = _s10(p, d)
        h = base["html"]
        i1 = h.index(f'<div id="{p}-B"')
        a = f'<div id="{p}-A" class="ao-full" style="background:#04070a">' + fxwin(p, 10, "f_enter", "ent", 480, 200, 960, 0, 1.1) + '</div>'
        js = base["js"].replace("tl.fromTo(q('man'), { x: -260, y: 0, scale: 1.0, filter: 'blur(10px)' }, { x: 120, y: -680, scale: 0.42, filter: 'blur(1px)', duration: 1.1, ease: 'none' }, 0);", "")
        js = js.replace("shot('A', 0, 1.1, [1.04,0,0], [1.12,0,20]);", "shot('A', 0, 1.1, [1.0,0,0], [1.0,0,0]);")
        return S(a + h[i1:], js, fg=base["fg"] + ilus(p, "puerta, " + SRCF["army"], hidden=False) + "", )


# ------------------------------------------------------------------ 12–14: typewriter, writing hand, roller (Coronet 1941, FBI 1969)
if hasfx("f_type"):
    @scene(12)
    def s12(p, d):
        nm, n = typed(p, "t", "JOSÉ AGUSTÍN FERNÁNDEZ")
        inner = (f'<div style="font:700 26px \'Courier Prime\';letter-spacing:.2em;color:#44514f">NOMBRE</div>'
                 f'<div style="font:700 46px \'Courier Prime\';color:#1a1f1f;margin-top:30px;white-space:nowrap">{nm}</div>')
        html = (f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>'
                + fxwin(p, 12, "f_type", "ty", 130, 230, 720, 0, 1.05, -2)
                + index_card(p, inner, x=960, y=330, w=820, h=440, rot=2) + '</div>')
        js = f"""type('t', {n}, 0.1, 0.035); shot('cam', 0, 1.05, [1.0,0,0], [1.03,0,0]);
/*cut*/ tl.set(q('tyw'), {{ opacity: 0 }}, 1.05); shot('cam', 1.05, {d}, [2.3,-900,180,-2], [2.36,-930,185,-2]); lt(0.25); tl.set(q('tag2'), {{ opacity: 0 }}, 1.05);"""
        return S(html, js, fg=lt_html(p, "José Agustín Fernández", "juez en lo criminal (1992)") + tag_html(p, "RECREACIÓN") + ilus(p, "máquina de escribir, " + SRCF["cor"]))

if hasfx("f_write"):
    _s13 = SC[13]

    @scene(13)
    def s13(p, d):
        base = _s13(p, d)
        a = (f'<div id="{p}-A" class="ao-full" style="z-index:8;{DESK()}">' + fxwin(p, 13, "f_write", "wr", 420, 140, 900, 0, 0.9, 1)
             + f'<div id="{p}-st2" class="ao-stamp" style="position:absolute;left:840px;top:640px;font-size:70px;mix-blend-mode:normal;background:rgba(236,227,207,.0)">JUEZ EN LO CRIMINAL</div></div>')
        js = base["js"] + f"stampIn('st2', 0.55, -5); tl.set(q('A'), {{ opacity: 0 }}, 0.9); tl.set(q('tag2'), {{ opacity: 0 }}, 0.9);"
        return S(base["html"] + a, js, fg=tag_html(p, "RECREACIÓN") + ilus(p, "mano y papeles, " + SRCF["fbi"]))

if hasfx("f_roller"):
    _s14 = SC[14]

    @scene(14)
    def s14(p, d):
        base = _s14(p, d)
        js = base["js"].replace(f"shot('cam', 0, {d}, [0.86,0,40,-1], [0.9,0,40,-1]);", f"shot('cam', 0, {d}, [0.74,0,250,-1], [0.77,0,250,-1]);")
        win = fxwin(p, 14, "f_roller", "rol", 380, 40, 720, 0, d, -1)
        return S(base["html"] + win, js, fg=base["fg"] + ilus(p, "máquina de escribir, " + SRCF["cor"]))


# ------------------------------------------------------------------ 16: definition over a finger running down a file (FBI)
if hasfx("f_finger"):
    _s16 = SC[16]

    @scene(16)
    def s16(p, d):
        base = _s16(p, d)
        h = base["html"]
        i0 = h.index('<img src="assets/img/const1992_p42'); i1 = h.index('alt="">', i0) + len('alt="">')
        h = h[:i0] + fxbg(p, 16, "f_finger", "bg", 0, d) + '<div class="ao-full" style="background:rgba(4,6,8,.45)"></div>' + h[i1:]
        MAGS[16] = [("f_finger_bg", 0.0)]
        REAL_ROWS.add(16)
        return S(h, base["js"], fg=base["fg"] + ilus(p, "archivo, " + SRCF["fbi"], top=70))


# ------------------------------------------------------------------ 20: card-index office, then a card pulled (FBI)
if hasfx("f_office", "f_card_c"):
    @scene(20)
    def s20(p, d):
        html = (f'<div id="{p}-A" class="ao-full" style="{DESK()}"><div id="{p}-cw" class="ao-cam">' + fxwin(p, 20, "f_office", "of", 540, 225, 840, 0, 1.0, 0, cam=1.12) + '</div>'
                f'<div id="{p}-box" style="position:absolute;left:1090px;top:460px;width:150px;height:120px;border:6px solid {ACC};opacity:0"></div>'
                f'<div id="{p}-lab" style="position:absolute;left:1260px;top:470px;font:700 54px \'Courier Prime\';color:#f2ece0;letter-spacing:.12em;opacity:0;text-shadow:0 3px 14px #000">POLICÍA ?</div></div>'
                f'<div id="{p}-B" class="ao-full" style="opacity:0;{DESK()}">' + fxwin(p, 20, "f_card_c", "cd", 480, 180, 960, 1.0, d - 1.0) + '</div>')
        js = f"""shot('cw', 0, 1.0, [1.0,0,0], [1.12,-60,-20]); tl.to(q('box'), {{ opacity: 1, duration: 0.15 }}, 0.45); tl.to(q('lab'), {{ opacity: 1, duration: 0.15 }}, 0.55);
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.0); tl.set(q('B'), {{ opacity: 1 }}, 1.0); tag(0.05);"""
        REAL_ROWS.add(20)
        return S(html, js, fg=ilus(p, "fichero, " + SRCF["fbi"], key="tag", top=70))


# ------------------------------------------------------------------ 23: shadow over a framed document (Army 1941), then the memo
if hasfx("f_shadowdoc"):
    _s23 = SC[23]

    @scene(23)
    def s23(p, d):
        base = _s23(p, d)
        a = f'<div id="{p}-A" class="ao-full" style="z-index:8;{DESK()}">' + fxwin(p, 23, "f_shadowdoc", "sd", 480, 165, 960, 0, 1.2, -1) + '</div>'
        js = base["js"] + "tl.set(q('A'), { opacity: 0 }, 1.2); tl.set(q('tag2'), { opacity: 0 }, 1.2);"
        return S(base["html"] + a, js, fg=base["fg"] + ilus(p, "documento, " + SRCF["army"]))


# ------------------------------------------------------------------ 24, 45, 46, 64, 65: timelines over moving archive / 1945 Asunción
def _veiled(n, key, src, label, ms=0.0, key2=None, split=None, real_label=False):
    prev = SC[n]

    @scene(n)
    def f(p, d):
        base = prev(p, d)
        if key2:
            bgv = fxbg(p, n, key, "bg", 0, split) + fxbg(p, n, key2, "bg2", split, d - split)
        else:
            bgv = fxbg(p, n, key, "bg", 0, d, ms)
        h = veil(base["html"]).replace(f'data-layout-allow-overflow>{BIGPAPER().replace("<div style=", "<div style=")}', "", 0)
        h = h.replace(f'<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>', f'<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow>{bgv}', 1)
        MAGS[n] = MAGS.get(n, []) + [(key + "_bg", 0.0)]
        REAL_ROWS.add(n)
        t = tag2(p, label) if not real_label else tag_html(p, label, src=True).replace(f'id="{p}-tag"', f'id="{p}-tagr"').replace('class="ao-tag src"', 'class="ao-tag src" style="top:122px"')
        return S(h, base["js"], base["css"], fg=base["fg"] + t)
    return f


if hasfx("f_flip"):
    _veiled(24, "f_flip", None, "IMAGEN ILUSTRATIVA · fichas, " + SRCF["fbi"])
if hasfx("f_wall"):
    _veiled(45, "f_wall", None, "IMAGEN ILUSTRATIVA · fichero, " + SRCF["cor"])
    _veiled(46, "f_wall", None, "IMAGEN ILUSTRATIVA · fichero, " + SRCF["cor"], ms=1.8)
if hasfx("f_tram"):
    _veiled(64, "f_tram", None, "IMAGEN REAL · Asunción, c. 1945 (OCIAA)", real_label=True)
if hasfx("f_roofs", "f_roofs2"):
    _veiled(65, "f_roofs", None, "IMAGEN REAL · Asunción, c. 1945 (OCIAA)", key2="f_roofs2", split=1.25, real_label=True)


# ------------------------------------------------------------------ 28 B: the hand testing the door (Your Police 1953)
if hasfx("f_guardhand"):
    _s28 = SC[28]

    @scene(28)
    def s28(p, d):
        base = _s28(p, d)
        b = (f'<div id="{p}-B" class="ao-full" style="opacity:0;z-index:8">' + fxbg(p, 28, "f_guardhand", "gbg", 1.25, d - 1.25)
             + fxwin(p, 28, "f_guardhand", "gh", 705, 290, 510, 1.25, d - 1.25) + '</div>')
        js = _cutjs(base["js"], f"/*cut*/ shot('cam', 1.25, {d}, [1.25,-230,310], [1.25,-240,325]);", f"/*cut*/ tl.set(q('B'), {{ opacity: 1 }}, 1.25); tl.set(q('tag2'), {{ opacity: 1 }}, 1.25);")
        return S(base["html"] + b, js, fg=base["fg"] + ilus(p, "mano en la puerta, " + SRCF["pol"], hidden=True))


# ------------------------------------------------------------------ 31, 33, 37, 38: stairs, knob, card, files
def _window_row(n, key, label, bgphoto=None, w=960, recreation=True):
    prev = SC[n]

    @scene(n)
    def f(p, d):
        i = FXI[key]
        h = w * i["h"] / i["w"]
        bg = (cover(p, bgphoto, "bgp", "filter:blur(14px) brightness(.45)") if bgphoto and bgphoto in PHI else "")
        html = (f'<div id="{p}-cam" class="ao-cam" style="background:#050302" data-layout-allow-overflow>{bg}'
                + fxwin(p, n, key, "v", (1920 - w) / 2, (1080 - h) / 2, w, 0, d, -1 if n % 2 else 1) + '</div>')
        js = f"shot('cam', 0, {d}, [1.0,0,0], [1.0,0,-10]); tag(0.05);"
        REAL_ROWS.add(n)
        fg = (tag_html(p, "RECREACIÓN") + ilus(p, label)) if recreation else ilus(p, label, key="tag", top=70)
        return S(html, js, fg=fg)
    return f


if hasfx("f_stairs"):
    _window_row(31, "f_stairs", "escalera, " + SRCF["bk"], "stairway", 660)
if hasfx("f_knob"):
    _window_row(33, "f_knob", "cerradura, " + SRCF["pol"], "stairdoor", 960)
if hasfx("f_card"):
    _window_row(37, "f_card", "ficha, " + SRCF["fbi"], "catalog", 960, recreation=False)
if hasfx("f_files"):
    _window_row(38, "f_files", "archivo, " + SRCF["fbi"], "ledger", 960, recreation=False)


# ------------------------------------------------------------------ 42 A: the office behind the counter (FBI)
if hasfx("f_office"):
    _s42 = SC[42]

    @scene(42)
    def s42(p, d):
        base = _s42(p, d)
        h = base["html"]
        i0 = h.index(f'<div id="{p}-A"'); i1 = h.index(f'<div id="{p}-B"')
        a = (f'<div id="{p}-A" class="ao-full" style="background:#030201">' + fxbg(p, 42, "f_office", "bg", 0, 1.1)
             + '<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(3,2,1,.8) 0,rgba(3,2,1,.35) 50%,rgba(3,2,1,.05) 80%)"></div></div>')
        fg = base["fg"].replace("Fichero, EE. UU. (HABS, 1996)", "fichero, " + SRCF["fbi"])
        MAGS[42] = [("f_office_bg", 0.0)]
        return S(h[:i0] + a + h[i1:], base["js"].replace("shot('A', 0, 1.1, [1.0,0,0], [1.06,0,0]);", ""), fg=fg)


# ------------------------------------------------------------------ 50: the torch in the dark (Booked 1960) under the paper
if hasfx("f_torch"):
    _s50 = SC[50]

    @scene(50)
    def s50(p, d):
        base = _s50(p, d)
        h = base["html"]
        h = h.replace(f'<div style="position:absolute;left:140px;top:250px;width:1640px;height:560px;{PAPER()};box-shadow:0 40px 80px rgba(0,0,0,.6)"></div>',
                      f'<div style="position:absolute;left:140px;top:250px;width:1640px;height:560px;{PAPER()};opacity:.78;box-shadow:0 40px 80px rgba(0,0,0,.6)"></div>', 1)
        h = h.replace(f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>', f'<div id="{p}-cam" class="ao-cam" style="background:#000" data-layout-allow-overflow>{fxbg(p, 50, "f_torch", "bg", 0, d)}', 1)
        MAGS[50] = [("f_torch_bg", 0.0)]
        REAL_ROWS.add(50)
        return S(h, base["js"], fg=base["fg"] + tag_html(p, "RECREACIÓN") + ilus(p, "linterna, " + SRCF["bk"]))


# ------------------------------------------------------------------ 54: the hat at the iron door (Army 1941)
if hasfx("f_hatdoor"):
    _s54 = SC[54]

    @scene(54)
    def s54(p, d):
        base = _s54(p, d)
        html = (f'<div id="{p}-cam" class="ao-cam" style="background:#030201" data-layout-allow-overflow>'
                f'<div id="{p}-A" class="ao-full">' + fxwin(p, 54, "f_hatdoor", "hd", 540, 430, 840, 0, 1.25) + '</div>'
                f'<div id="{p}-B" class="ao-full" style="opacity:0">' + fxbg(p, 54, "f_hatdoor", "hbg", 1.25, d - 1.25, ms=1.25) + '</div></div>')
        js = base["js"].replace(f"shot('cam', 0, 1.25, [1.0,0,0], [1.03,0,0]);", "").replace(f"shot('cam', 1.25, {d}, [1.3,300,-100], [1.33,300,-100]);", "")
        js += "tl.set(q('A'), { opacity: 0 }, 1.25); tl.set(q('B'), { opacity: 1 }, 1.25); tl.set(q('t1'), { opacity: 0 }, 1.25);"
        fg = base["fg"].replace(f'<div id="{p}-t1" style="position:absolute;left:0;width:1920px;top:250px;', f'<div id="{p}-t1" style="position:absolute;left:0;width:1920px;top:20px;')
        REAL_ROWS.add(54)
        return S(html, js, fg=fg + tag_html(p, "RECREACIÓN") + ilus(p, "puerta, " + SRCF["army"]))


# ------------------------------------------------------------------ 60, 61, 63: 1945 Asunción and soldiers (OCIAA), years on screen
if hasfx("f_horizon"):
    _s60 = SC_PREV[60]

    @scene(60)
    def s60(p, d):
        base = _s60(p, d)
        html = (f'<div id="{p}-cam" class="ao-cam" data-layout-allow-overflow style="background:#050302">' + fxbg(p, 60, "f_horizon", "bg", 0, d)
                + '<div class="ao-full" style="background:rgba(5,3,2,.35)"></div>' + fxwin(p, 60, "f_horizon", "hz", 1240, 600, 560, 0, d, 1.5) + '</div>')
        REAL_ROWS.add(60)
        return S(html, base["js"].replace("shot('cam', 0, 1.0, [1.2,0,0], [1.25,0,0]); shot('cam', 1.0, {d}, [1.0,-200,-10], [1.04,-200,-12]);".format(d=d), ""),
                 base["css"], fg=base["fg"] + tag_html(p, "IMAGEN REAL · Asunción, c. 1945 (OCIAA)", src=True))

if hasfx("f_river"):
    _s61 = SC[61]

    @scene(61)
    def s61(p, d):
        base = _s61(p, d)
        a = (f'<div id="{p}-A" class="ao-full" style="z-index:45;{PAPER()}">' + fxwin(p, 61, "f_river", "rv", 480, 180, 960, 0, 0.9)
             + f'<div style="position:absolute;left:300px;top:560px;width:1320px;height:6px;background:{ACC}"></div>'
             f'<div class="tl-dot" style="left:300px;top:563px"></div><div style="position:absolute;left:250px;top:600px;font:700 40px Courier Prime;color:#1f1b15">1954</div></div>')
        js = base["js"] + "tl.set(q('A'), { opacity: 0 }, 0.9); tl.set(q('tagr'), { opacity: 0 }, 0.9);"
        t = tag_html(p, "IMAGEN REAL · Río Paraguay, c. 1945 (OCIAA)", src=True).replace(f'id="{p}-tag"', f'id="{p}-tagr"')
        REAL_ROWS.add(61)
        return S(base["html"], js, base["css"], fg=base["fg"] + a + t)

if hasfx("f_soldiers"):
    _s63 = SC[63]

    @scene(63)
    def s63(p, d):
        base = _s63(p, d)
        a = (f'<div id="{p}-A" class="ao-full" style="z-index:45;background:#050302">' + fxbg(p, 63, "f_soldiers", "sbg", 0, 1.0)
             + fxwin(p, 63, "f_soldiers", "so", 480, 345, 960, 0, 1.0) + '</div>')
        js = base["js"].replace("0.3, ease: 'expo.out' }}, 0.15);".replace("}}", "}"), "0.3, ease: 'expo.out' }, 1.05);")
        js += "/*cut:1.0*/ tl.set(q('A'), { opacity: 0 }, 1.0); tl.set(q('tagi'), { opacity: 0 }, 1.0);"
        t = ilus(p, "Ejército paraguayo, 1945 (OCIAA)", key="tagi", top=70)
        return S(base["html"], js, base["css"], fg=base["fg"] + a + t)
