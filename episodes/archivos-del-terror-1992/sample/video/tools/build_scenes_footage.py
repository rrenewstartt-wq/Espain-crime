# Public-domain footage versions (sample/footage-plan.md, LICENSES.md §9). Executed after build_scenes_photo.py.
# 5th pass (video-qa 2026-11-26): magnification against the ORIGINAL masters (Prelinger 352/368 px, NARA 720 px,
# NASA 1616 px); one label chip per screen; no name/role caption over unrelated footage; no footage of another year
# under a date card; blurred, unrecognisable footage is neither labelled nor counted as real.
_fxj = os.path.join(ASSETS, "fx", "fx.json")
FXI = json.load(open(_fxj)) if os.path.exists(_fxj) else {}
MOVING = {}                # row -> seconds of recognisable moving footage on screen (union of intervals)
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


SRCF = {"fbi": "FBI (1969)", "cor": "Coronet (1941)", "army": "Ejército de EE. UU. (1941)", "bk": "EE. UU. (1960)", "pol": "EE. UU. (1953)",
        "py": "OCIAA (1945)"}


def fxmag(key, w, cam=1.0):
    i = FXI[key]
    h = w * i["h"] / i["w"]
    return max(w * cam / i["orig_w"], h * cam / i["orig_h"])


def fxmaxw(key, cam=1.0):
    i = FXI[key]
    return min(1.5 * i["orig_w"], 1.5 * i["orig_h"] * i["w"] / i["h"]) / cam


def fxvid(p, n, key, vid, x, y, w, start, dur, ms=0.0, cam=1.0, z=None):
    """A sharp clip at (x, y), width w, timed [start, start+dur) in the scene; checked against the original master."""
    i = FXI[key]
    m = fxmag(key, w, cam)
    assert m <= 1.5 + 1e-6, f"row {n}: clip {key} at {m:.2f}x of its original master"
    MAGS.setdefault(n, []).append((key, round(m, 2)))
    _mov(n, start, min(dur, i["dur"] - ms))
    h = w * i["h"] / i["w"]
    dur = min(dur, i["dur"] - ms)
    zz = f"z-index:{z};" if z else ""
    return (f'<video id="{p}-{vid}" class="clip" src="assets/fx/{key}.mp4" data-start="{start}" data-duration="{dur:.3f}" data-media-start="{ms}" '
            f'muted playsinline style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;{zz}"></video>')


def fxwin(p, n, key, vid, cx, cy, w, start, dur, rot=0.0, ms=0.0, cam=1.0, wid=None):
    """Clip in a print frame centred on (cx, cy); w is clamped to 1.5x of the original master."""
    w = min(w, fxmaxw(key, cam))
    i = FXI[key]
    h = w * i["h"] / i["w"]
    x, y = cx - w / 2, cy - h / 2
    return (f'<div id="{p}-{wid or vid + "w"}" style="position:absolute;left:{x - 14:.0f}px;top:{y - 14:.0f}px;width:{w + 28:.0f}px;height:{h + 28:.0f}px;'
            f'background:#ece3cf;box-shadow:0 40px 90px rgba(0,0,0,.75);transform:rotate({rot}deg)">'
            + fxvid(p, n, key, vid, 14, 14, w, start, dur, ms, cam) + '</div>')


def fxfill(p, n, key, vid, start, dur, ms=0.0, cam=1.0):
    """A 720-px master as large as the rule allows (1.5x → 1080 px wide), over its own blurred copy."""
    w = fxmaxw(key, cam)
    i = FXI[key]
    h = w * i["h"] / i["w"]
    bg = fxbg(p, n, key, vid + "b", start, dur, ms) if FXI[key]["bg"] else ""
    return bg + fxvid(p, n, key, vid, (1920 - w) / 2, (1080 - h) / 2, w, start, dur, ms, cam)


def fxbg(p, n, key, vid, start, dur, ms=0.0, op=1.0):
    """Pre-baked blurred background (unrecognisable: not counted, not labelled)."""
    dur = min(dur, FXI[key]["dur"] - ms)
    return (f'<video id="{p}-{vid}" class="clip" src="assets/fx/{key}_bg.mp4" data-start="{start}" data-duration="{dur:.3f}" data-media-start="{ms}" '
            f'muted playsinline style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:{op}"></video>')


def chip(p, text, key="tag", hidden=False, top=None):
    t = tag_html(p, text, src="·" in text).replace(f'id="{p}-tag"', f'id="{p}-{key}"')
    st = ("opacity:0;" if hidden else "") + (f"top:{top}px;" if top else "")
    return t.replace('class="ao-tag', f'style="{st}" class="ao-tag', 1) if st else t


def rec(src):
    return f"RECREACIÓN · imagen de archivo, {src}"


def ilu(what, src):
    return f"IMAGEN ILUSTRATIVA · {what}, {src}"


def _cutjs(js, old, new):
    assert old in js, old[:80]
    return js.replace(old, new)


# ------------------------------------------------------------------ 3: orbit (NASA, HD), night, not over Paraguay
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
        MAGS.setdefault(3, []).append(("f_orbit", round(1920 / FXI["f_orbit"]["orig_w"], 2)))
        _mov(3, 0, 0.8)
        vid = (f'<video id="{p}-orb" class="clip" src="assets/fx/f_orbit.mp4" data-start="0" data-duration="0.8" data-media-start="0" muted playsinline '
               f'style="position:absolute;left:0;top:-97px;width:1920px;height:1274px;z-index:10"></video>')
        REAL_ROWS.add(3)
        return S(base["html"] + vid, js, base["css"], fg=base["fg"] + chip(p, "IMAGEN ILUSTRATIVA · Sudamérica desde la EEI, NASA/JSC (2011)", "tago"))


# ------------------------------------------------------------------ 7: portrait (name caption) → register insert (no caption)
if hasfx("f_register"):
    @scene(7)
    def s07(p, d):
        base = SC_PREV[7](p, d)
        b = f'<div id="{p}-B" class="ao-full" style="opacity:0;background:#000">' + fxbg(p, 7, "f_register", "regb", 0.8, d - 0.8, op=.55) + fxwin(p, 7, "f_register", "reg", 960, 520, 900, 0.8, d - 0.8, -1.5) + '</div>'
        js = _cutjs(base["js"], f"/*cut*/ shot('cam', 0.8, {d}, [1.9,40,560], [1.96,40,575]);",
                    f"/*cut*/ tl.set(q('B'), {{ opacity: 1 }}, 0.8); tl.set(q('tag'), {{ opacity: 0 }}, 0.8); tl.set(q('tagr'), {{ opacity: 1 }}, 0.8); tl.set(q('lt'), {{ opacity: 0 }}, 0.8);")
        return S(base["html"] + b, js, fg=base["fg"] + chip(p, ilu("registro", SRCF["cor"]), "tagr", hidden=True))


# ------------------------------------------------------------------ 10: a man goes in (Army 1941), then the building
if hasfx("f_enter") and "comandancia" in PHI:
    _s10 = SC[10]

    @scene(10)
    def s10(p, d):
        base = _s10(p, d)
        h = base["html"]
        i1 = h.index(f'<div id="{p}-B"')
        a = f'<div id="{p}-A" class="ao-full" style="background:#000">' + fxbg(p, 10, "f_enter", "entb", 0, 1.1, op=.6) + fxwin(p, 10, "f_enter", "ent", 960, 560, 960, 0, 1.1, -1) + '</div>'
        js = base["js"].replace("tl.fromTo(q('man'), { x: -260, y: 0, scale: 1.0, filter: 'blur(10px)' }, { x: 120, y: -680, scale: 0.42, filter: 'blur(1px)', duration: 1.1, ease: 'none' }, 0);", "")
        js = js.replace("shot('A', 0, 1.1, [1.04,0,0], [1.12,0,20]);", "shot('A', 0, 1.1, [1.0,0,0], [1.03,0,0]);")
        js += "tl.set(q('tag'), { opacity: 0 }, 0); tl.set(q('tag'), { opacity: 1 }, 1.1); tl.set(q('taga'), { opacity: 0 }, 1.1);"
        return S(a + h[i1:], js, fg=base["fg"] + chip(p, rec(SRCF["army"]), "taga"))


# ------------------------------------------------------------------ 12–14: typewriter, writing hand, roller
if hasfx("f_type"):
    @scene(12)
    def s12(p, d):
        nm, n = typed(p, "t", "JOSÉ AGUSTÍN FERNÁNDEZ")
        inner = (f'<div style="font:700 26px \'Courier Prime\';letter-spacing:.2em;color:#44514f">NOMBRE</div>'
                 f'<div style="font:700 46px \'Courier Prime\';color:#1a1f1f;margin-top:30px;white-space:nowrap">{nm}</div>')
        html = (f'<div id="{p}-cam" class="ao-cam" style="{DESK()}" data-layout-allow-overflow>'
                + fxwin(p, 12, "f_type", "ty", 470, 470, 720, 0, 1.05, -2)
                + index_card(p, inner, x=960, y=330, w=820, h=440, rot=2) + '</div>')
        js = f"""type('t', {n}, 0.1, 0.035); shot('cam', 0, 1.05, [1.0,0,0], [1.03,0,0]);
/*cut*/ tl.set(q('tyw'), {{ opacity: 0 }}, 1.05); shot('cam', 1.05, {d}, [2.3,-900,180,-2], [2.36,-930,185,-2]); lt(1.1);
tl.set(q('tag'), {{ opacity: 0 }}, 1.05); tl.set(q('tagb'), {{ opacity: 1 }}, 1.05); tl.set(q('lt'), {{ opacity: 0 }}, 0); tl.set(q('lt'), {{ opacity: 1 }}, 1.05);"""
        # the name caption appears only on the name card insert, not over the archive hands
        return S(html, js, fg=lt_html(p, "José Agustín Fernández", "juez en lo criminal (1992)") + chip(p, rec(SRCF["cor"])) + chip(p, "RECREACIÓN", "tagb", hidden=True))

if hasfx("f_write"):
    _s13 = SC[13]

    @scene(13)
    def s13(p, d):
        base = _s13(p, d)
        a = (f'<div id="{p}-A" class="ao-full" style="z-index:8;{DESK()}">' + fxwin(p, 13, "f_write", "wr", 900, 530, 1080, 0, 0.9, 1)
             + f'<div id="{p}-st2" class="ao-stamp" style="position:absolute;left:900px;top:700px;font-size:70px;mix-blend-mode:normal">JUEZ EN LO CRIMINAL</div></div>')
        js = base["js"] + f"stampIn('st2', 0.55, -5); tl.set(q('A'), {{ opacity: 0 }}, 0.9); tl.set(q('tag'), {{ opacity: 0 }}, 0.9); tl.set(q('tagb'), {{ opacity: 1 }}, 0.9);"
        return S(base["html"] + a, js, fg=chip(p, rec(SRCF["fbi"])) + chip(p, "RECREACIÓN", "tagb", hidden=True))

if hasfx("f_type"):
    _s14 = SC[14]

    @scene(14)
    def s14(p, d):
        base = _s14(p, d)
        js = base["js"].replace(f"shot('cam', 0, {d}, [0.86,0,40,-1], [0.9,0,40,-1]);", f"shot('cam', 0, {d}, [0.74,0,250,-1], [0.77,0,250,-1]);")
        win = fxwin(p, 14, "f_type", "rol", 760, 250, 720, 0, d, -1, ms=0.4)
        return S(base["html"] + win, js, fg=chip(p, rec(SRCF["cor"])))


# ------------------------------------------------------------------ 16: definition over blurred archive hands (not counted, no label)
if hasfx("f_finger"):
    _s16 = SC[16]

    @scene(16)
    def s16(p, d):
        base = _s16(p, d)
        h = base["html"]
        i0 = h.index('<img src="assets/img/const1992_p42'); i1 = h.index('alt="">', i0) + len('alt="">')
        h = h[:i0] + fxbg(p, 16, "f_finger", "bg", 0, d) + '<div class="ao-full" style="background:rgba(4,6,8,.45)"></div>' + h[i1:]
        MAGS[16] = [("f_finger_bg (blurred)", 0.0)]
        REAL_ROWS.discard(16)
        return S(h, base["js"], fg=base["fg"])


# ------------------------------------------------------------------ 20: card-index office (1080 px), then a card pulled
if hasfx("f_office", "f_card_c"):
    @scene(20)
    def s20(p, d):
        html = (f'<div id="{p}-A" class="ao-full" style="background:#05080a"><div id="{p}-cw" class="ao-cam">' + fxfill(p, 20, "f_office", "of", 0, 1.0, cam=1.06) + '</div>'
                f'<div id="{p}-box" style="position:absolute;left:1180px;top:520px;width:170px;height:130px;border:6px solid {ACC};opacity:0"></div>'
                f'<div id="{p}-lab" style="position:absolute;left:1370px;top:540px;font:700 54px \'Courier Prime\';color:#f2ece0;letter-spacing:.12em;opacity:0;text-shadow:0 3px 14px #000">POLICÍA ?</div></div>'
                f'<div id="{p}-B" class="ao-full" style="opacity:0;background:#05080a">' + fxfill(p, 20, "f_card_c", "cd", 1.0, d - 1.0) + '</div>')
        js = f"""shot('cw', 0, 1.0, [1.0,0,0], [1.06,-30,-10]); tl.to(q('box'), {{ opacity: 1, duration: 0.15 }}, 0.45); tl.to(q('lab'), {{ opacity: 1, duration: 0.15 }}, 0.55);
/*cut*/ tl.set(q('A'), {{ opacity: 0 }}, 1.0); tl.set(q('B'), {{ opacity: 1 }}, 1.0); tag(0.05);"""
        REAL_ROWS.add(20)
        return S(html, js, fg=chip(p, ilu("fichero", SRCF["fbi"])))


# ------------------------------------------------------------------ 23: shadow over a framed document (Army 1941), then the memo
if hasfx("f_shadowdoc"):
    _s23 = SC[23]

    @scene(23)
    def s23(p, d):
        base = _s23(p, d)
        a = f'<div id="{p}-A" class="ao-full" style="z-index:8;background:#000">' + fxbg(p, 23, "f_shadowdoc", "sdb", 0, 1.2, op=.55) + fxwin(p, 23, "f_shadowdoc", "sd", 960, 520, 960, 0, 1.2, -1) + '</div>'
        js = base["js"] + "tl.set(q('A'), { opacity: 0 }, 1.2); tl.set(q('taga'), { opacity: 0 }, 1.2); tl.set(q('tag'), { opacity: 0 }, 0); tl.set(q('tag'), { opacity: 1 }, 1.2);"
        return S(base["html"] + a, js, fg=base["fg"] + chip(p, ilu("documento", SRCF["army"]), "taga"))


# ------------------------------------------------------------------ 33, 37, 38: knob, card, files
def _window_row(n, key, label, bgphoto=None, w=1080):
    prev = SC[n]

    @scene(n)
    def f(p, d):
        bg = (fxbg(p, n, key, "vb", 0, d, op=.55) if FXI[key]["bg"] else (cover(p, bgphoto, "bgp", "filter:blur(14px) brightness(.45)") if bgphoto and bgphoto in PHI else ""))
        html = (f'<div id="{p}-cam" class="ao-cam" style="background:#050302" data-layout-allow-overflow>{bg}'
                + fxwin(p, n, key, "v", 960, 540, w, 0, d, -1 if n % 2 else 1) + '</div>')
        js = f"shot('cam', 0, {d}, [1.0,0,0], [1.0,0,-10]); tag(0.05);"
        REAL_ROWS.add(n)
        return S(html, js, fg=chip(p, label))
    return f


if hasfx("f_knob"):
    _window_row(33, "f_knob", rec(SRCF["pol"]), "stairdoor")
if hasfx("f_card"):
    _window_row(37, "f_card", ilu("ficha", SRCF["fbi"]), "catalog")
if hasfx("f_files"):
    _window_row(38, "f_files", ilu("archivo", SRCF["fbi"]), "ledger")


# ------------------------------------------------------------------ 42 A: blurred office behind the count (not counted, one chip)
if hasfx("f_office"):
    _s42 = SC[42]

    @scene(42)
    def s42(p, d):
        base = SC_PREV[42](p, d)
        h = base["html"]
        i0 = h.index(f'<div id="{p}-A"'); i1 = h.index(f'<div id="{p}-B"')
        a = (f'<div id="{p}-A" class="ao-full" style="background:#030201">' + fxbg(p, 42, "f_office", "bg", 0, 1.1)
             + '<div class="ao-full" style="background:radial-gradient(ellipse at 50% 50%,rgba(3,2,1,.8) 0,rgba(3,2,1,.35) 50%,rgba(3,2,1,.05) 80%)"></div></div>')
        js = re.sub(r"tl\.set\(q\('g\d+'\), \{ opacity: 1 \}, [\d.]+\);", "", base["js"])
        MAGS[42] = [("f_office_bg (blurred)", 0.0)]
        REAL_ROWS.discard(42)
        return S(h[:i0] + a + h[i1:], js, fg=base["fg"])


# ------------------------------------------------------------------ 43: hands on documents (FBI) under the 20.000 count
if hasfx("f_docs"):
    _s43 = SC[43]

    @scene(43)
    def s43(p, d):
        base = _s43(p, d)
        html = f'<div id="{p}-cam" class="ao-cam" style="background:#050302">' + fxfill(p, 43, "f_docs", "dc", 0, d) + '<div class="ao-full" style="background:rgba(5,3,2,.5)"></div></div>'
        fg = base["fg"].replace(tag_html(p, UNESCO, src=True), "")
        js = "count('n', 0, 20000, 0.05, 0.75); tag(0.05);"
        REAL_ROWS.add(43)
        return S(html, js, fg=fg + chip2(p, ilu("documentos", SRCF["fbi"]), CIFRA))


# ------------------------------------------------------------------ 54: the hat at the iron door (Army 1941), 528-px print
if hasfx("f_hatdoor"):
    _s54 = SC[54]

    @scene(54)
    def s54(p, d):
        base = _s54(p, d)
        html = (f'<div id="{p}-cam" class="ao-cam" style="background:#030201" data-layout-allow-overflow>'
                f'<div id="{p}-A" class="ao-full">' + fxwin(p, 54, "f_hatdoor", "hd", 960, 720, 840, 0, 1.25) + '</div>'
                f'<div id="{p}-B" class="ao-full" style="opacity:0">' + fxbg(p, 54, "f_hatdoor", "hbg", 1.25, d - 1.25, ms=1.25) + '</div></div>')
        js = base["js"].replace(f"shot('cam', 0, 1.25, [1.0,0,0], [1.03,0,0]);", "").replace(f"shot('cam', 1.25, {d}, [1.3,300,-100], [1.33,300,-100]);", "")
        js += "tl.set(q('A'), { opacity: 0 }, 1.25); tl.set(q('B'), { opacity: 1 }, 1.25); tl.set(q('t1'), { opacity: 0 }, 1.25); tl.set(q('tag'), { opacity: 0 }, 1.25);"
        fg = base["fg"].replace(f'<div id="{p}-t1" style="position:absolute;left:0;width:1920px;top:250px;', f'<div id="{p}-t1" style="position:absolute;left:0;width:1920px;top:40px;')
        REAL_ROWS.add(54)
        return S(html, js, fg=fg + chip(p, rec(SRCF["army"])))


# ------------------------------------------------------------------ 60 neutral date card; 61 Río Paraguay 1945 with its year, then the axis; 63 soldiers
if hasfx("f_river"):
    _s61 = SC[61]

    @scene(61)
    def s61(p, d):
        base = _s61(p, d)
        a = (f'<div id="{p}-A" class="ao-full" style="z-index:45;background:#0a0705">' + fxfill(p, 61, "f_river", "rv", 0, 0.9)
             + '<div style="position:absolute;left:0;width:1920px;top:930px;text-align:center;font:400 96px Anton;color:#f2ece0;letter-spacing:.04em;text-shadow:0 4px 30px #000">RÍO PARAGUAY, 1945</div></div>')
        js = base["js"] + "tl.set(q('A'), { opacity: 0 }, 0.9); tl.set(q('tagr'), { opacity: 0 }, 0.9);"
        REAL_ROWS.add(61)
        return S(base["html"], js, base["css"], fg=base["fg"] + a + chip(p, "IMAGEN REAL · Río Paraguay, c. 1945 (OCIAA)", "tagr"))

if hasfx("f_soldiers"):
    _s63 = SC[63]

    @scene(63)
    def s63(p, d):
        base = _s63(p, d)
        a = (f'<div id="{p}-A" class="ao-full" style="z-index:45;background:#050302">' + fxfill(p, 63, "f_soldiers", "so", 0, 1.0)
             + '<div style="position:absolute;left:0;width:1920px;top:860px;text-align:center;font:400 72px Anton;color:#f2ece0;letter-spacing:.04em;text-shadow:0 4px 30px #000">EJÉRCITO PARAGUAYO, 1945</div></div>')
        js = base["js"].replace("0.3, ease: 'expo.out' }, 0.15);", "0.3, ease: 'expo.out' }, 1.05);")
        js += "/*cut:1.0*/ tl.set(q('A'), { opacity: 0 }, 1.0); tl.set(q('tagi'), { opacity: 0 }, 1.0);"
        return S(base["html"], js, base["css"], fg=base["fg"] + a + chip(p, ilu("Ejército paraguayo", SRCF["py"]), "tagi"))


# 60: the 1992→1954 roll and the MAYO · 1954 card on a neutral ground (blurred 1954 portrait, sepia); no footage of another year
@scene(60)
def s60(p, d):
    REAL_ROWS.discard(60)
    return SC_PREV[60](p, d)
