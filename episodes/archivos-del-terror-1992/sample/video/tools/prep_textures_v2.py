# Executed from prep_assets.py (shares its namespace: np, Image, ImageDraw, ImageFilter, noise, save, out).
# v2 (2026-11-26, after video-qa): per-period palettes, surfaces for the three.js props, old-map paper,
# smooth figure silhouettes. Everything is generated here (own work); no photos.

PAL = {
    # 1992 cold morning (daylight, blue-black shadows)
    "cold": {"desk": (16, 22, 28), "paper": (228, 226, 216), "lift": (50, 64, 78)},
    # archive discovery under tungsten bulbs (warm, deep brown-black)
    "tung": {"desk": (26, 16, 8), "paper": (242, 214, 164), "lift": (150, 96, 40)},
    # 1954 sepia
    "sepia": {"desk": (30, 21, 13), "paper": (234, 212, 172), "lift": (120, 86, 50)},
}
W2, H2 = 1920, 1080
yy2, xx2 = np.mgrid[0:H2, 0:W2]
rad = np.clip(np.hypot((xx2 - W2 * 0.5) / (W2 * 0.55), (yy2 - H2 * 0.38) / (H2 * 0.75)), 0, 1.6)
for k, pal in PAL.items():
    base = np.array(pal["desk"], np.float32)
    grain_w = noise(W2, H2, 900, 31, 3)
    streak = np.asarray(Image.fromarray((noise(W2, 40, 30, 32, 3) * 255).astype(np.uint8)).resize((W2, H2), Image.BICUBIC), np.float32) / 255
    pool = np.clip(1.25 - rad, 0, 1) ** 1.6                      # light pool from a lamp above
    shade = 0.35 + 0.55 * grain_w * 0.5 + 0.35 * streak * 0.5 + 1.9 * pool
    img = base[None, None, :] * shade[..., None] + np.array(pal["lift"]) [None, None, :] * (pool ** 3)[..., None] * 0.35
    save(img, out("tex", f"desk_{k}.jpg"))
    pb = np.array(pal["paper"], np.float32)
    sh = 1 - 0.10 * n1 - 0.05 * n2 - 0.035 * fib - 0.10 * edge ** 3
    pap = pb[None, None, :] * sh[..., None]
    save(pap, out("tex", f"paper_{k}.jpg"))

# concrete facade
C = 2048
cn = noise(C, C // 2, 300, 41, 5)
cf = noise(C, C // 2, 12, 42, 2)
streaks = np.asarray(Image.fromarray((noise(C, 24, 20, 43, 3) * 255).astype(np.uint8)).resize((C, C // 2), Image.BICUBIC), np.float32) / 255
yyc = np.linspace(0, 1, C // 2)[:, None]
conc = 150 * (0.78 + 0.22 * cn) * (0.93 + 0.07 * cf) * (1 - 0.22 * np.clip(streaks - 0.45, 0, 1) * 2 * yyc)
save(np.stack([conc * 0.98, conc * 0.99, conc * 1.0], -1), out("tex", "concrete.jpg"))
# wood door planks (dark, weathered)
wd = np.zeros((2048, 1024, 3), np.float32)
xw = np.arange(1024)[None, :]
gr = noise(1024, 2048, 40, 44, 3)
lines = 0.5 + 0.5 * np.sin(xw / 3.1 + gr * 9)
plank = ((xw % 205) < 6).astype(np.float32)
v = (0.55 + 0.25 * lines + 0.2 * noise(1024, 2048, 300, 45)) * (1 - 0.8 * plank)
wd[:] = np.array([78, 66, 54])[None, None, :] * v[..., None]
save(wd, out("tex", "wood_door.jpg"))
# painted steel (filing cabinet)
mt = noise(1024, 1024, 200, 46, 4)
scr = (np.random.default_rng(47).random((1024, 1024)) > 0.9985).astype(np.float32)
scr = np.asarray(Image.fromarray((scr * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)).resize((1024, 1024)), np.float32) / 255
mtl = np.array([92, 104, 102], np.float32)[None, None, :] * (0.85 + 0.2 * mt)[..., None] + 90 * scr[..., None]
save(mtl, out("tex", "metal.jpg"))
# cardboard
cb = np.array([158, 122, 84], np.float32)[None, None, :] * (0.82 + 0.25 * noise(1024, 1024, 60, 48, 3))[..., None]
cb[440:560, :, :] = cb[440:560, :, :] * 0.8 + np.array([190, 170, 130]) * 0.2
save(cb, out("tex", "cardboard.jpg"))
# cold morning sky with low sun (left)
t = np.linspace(0, 1, H2)[:, None]
top, hor = np.array([46, 82, 124], np.float32), np.array([200, 214, 222], np.float32)
sky2 = top * (1 - t[..., None] ** 0.7) + hor * t[..., None] ** 0.7
sun = np.exp(-(((xx2 - 260) / 520) ** 2 + ((yy2 - 300) / 420) ** 2))
sky2 = sky2 + np.array([60, 48, 30]) * sun[..., None] + 30 * noise(W2, H2, 500, 49)[..., None] * 0.3
save(sky2, out("tex", "sky_cold.jpg"))
# tree silhouette billboard
TW, TH = 1200, 1400
tn = noise(TW, TH, 120, 50, 5)
ty, tx = np.mgrid[0:TH, 0:TW]
can = np.clip(1 - np.hypot((tx - 600) / 560, (ty - 520) / 460), 0, 1)
alpha = ((can * 1.6 + tn * 0.9) > 1.05).astype(np.float32)
trunk = ((np.abs(tx - 600 - (ty - 900) * 0.05) < 34) & (ty > 700)).astype(np.float32)
alpha = np.clip(alpha + trunk, 0, 1)
alpha = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)), np.float32)
rgba = np.zeros((TH, TW, 4), np.float32)
rgba[..., :3] = [12, 20, 18]
rgba[..., 3] = alpha
save(rgba, out("tex", "tree.png"), "RGBA")
# old map parchment (land) and inked sea
M = 2048
mp = noise(M, M, 500, 51, 5)
fox = np.clip(noise(M, M, 30, 52, 2) - 0.72, 0, 1) * 3
yym, xxm = np.mgrid[0:M, 0:M]
crease = np.exp(-((xxm - M * 0.5) / 4) ** 2) * 0.12 + np.exp(-((yym - M * 0.33) / 4) ** 2) * 0.10
land = np.array([216, 196, 154], np.float32)[None, None, :] * (0.84 + 0.2 * mp - 0.25 * fox - crease)[..., None]
save(land, out("tex", "oldmap_land.jpg"))
sea = np.array([66, 88, 98], np.float32)[None, None, :] * (0.8 + 0.3 * mp - 0.1 * fox)[..., None]
save(sea, out("tex", "oldmap_sea.jpg"))
# soft sprites (three.js glow / dust)
g = np.exp(-((np.mgrid[0:256, 0:256][0] - 128) ** 2 + (np.mgrid[0:256, 0:256][1] - 128) ** 2) / (2 * 40 ** 2))
rgba = np.zeros((256, 256, 4), np.float32)
rgba[..., :3] = 255
rgba[..., 3] = g * 255
save(rgba, out("tex", "glow.png"), "RGBA")


# smooth figure silhouettes: primitives unioned, blurred and re-thresholded for organic contours
def figure(name, parts, extra=None, size=(900, 1600), color=(10, 12, 14)):
    S2 = 2
    im = Image.new("L", (size[0] * S2, size[1] * S2), 0)
    d = ImageDraw.Draw(im)
    for p in parts:
        kind = p[0]
        if kind == "e":
            _, cx, cy, rx, ry = p
            d.ellipse([(cx - rx) * S2, (cy - ry) * S2, (cx + rx) * S2, (cy + ry) * S2], fill=255)
        elif kind == "c":           # capsule
            _, x1, y1, x2, y2, w = p
            d.line([x1 * S2, y1 * S2, x2 * S2, y2 * S2], fill=255, width=int(w * S2))
            for (x, y) in ((x1, y1), (x2, y2)):
                d.ellipse([(x - w / 2) * S2, (y - w / 2) * S2, (x + w / 2) * S2, (y + w / 2) * S2], fill=255)
        elif kind == "p":
            d.polygon([(x * S2, y * S2) for x, y in p[1]], fill=255)
    im = im.filter(ImageFilter.GaussianBlur(9 * S2)).point(lambda v: 255 if v > 118 else 0)
    im = im.filter(ImageFilter.GaussianBlur(1.2 * S2)).resize(size, Image.LANCZOS)
    a = np.asarray(im, np.float32)
    rgba = np.zeros((size[1], size[0], 4), np.float32)
    rgba[..., :3] = color
    rgba[..., 3] = a
    if extra:                        # light object held by the figure (paper, box) drawn on top
        ex = Image.new("RGBA", size, (0, 0, 0, 0))
        extra(ImageDraw.Draw(ex))
        e = np.asarray(ex.filter(ImageFilter.GaussianBlur(0.8)), np.float32)
        m = e[..., 3:4] / 255
        rgba[..., :3] = rgba[..., :3] * (1 - m) + e[..., :3] * m
        rgba[..., 3] = np.maximum(rgba[..., 3], e[..., 3])
    save(rgba, out("fig", name + ".png"), "RGBA")


torso = ("p", [(285, 330), (515, 330), (560, 520), (548, 800), (252, 800), (240, 520)])
figure("man_back", [("e", 400, 190, 64, 78), ("c", 400, 250, 400, 320, 74), ("c", 280, 345, 520, 345, 110), torso,
                    ("c", 270, 360, 232, 720, 76), ("c", 528, 360, 575, 650, 76),
                    ("c", 345, 790, 318, 1470, 112), ("c", 455, 790, 500, 1450, 112), ("e", 318, 1500, 62, 34), ("e", 505, 1480, 62, 34)],
       extra=lambda d: d.polygon([(520, 520), (650, 505), (668, 690), (538, 708)], fill=(214, 206, 188, 255)))
figure("guard", [("e", 400, 118, 100, 44), ("p", [(318, 120), (482, 120), (478, 176), (322, 176)]), ("e", 400, 186, 82, 18),
                 ("e", 400, 250, 60, 74), ("c", 400, 300, 400, 350, 72), ("c", 262, 372, 538, 372, 118),
                 ("p", [(275, 360), (525, 360), (552, 560), (540, 820), (260, 820), (248, 560)]),
                 ("c", 258, 385, 222, 790, 80), ("c", 540, 385, 690, 300, 76), ("c", 690, 300, 712, 90, 66), ("e", 718, 50, 46, 66),
                 ("c", 348, 810, 330, 1480, 116), ("c", 452, 810, 470, 1480, 116), ("e", 330, 1505, 64, 34), ("e", 472, 1505, 64, 34)])
figure("judge", [("e", 380, 200, 60, 74), ("e", 432, 214, 18, 12), ("c", 380, 262, 380, 330, 72), ("c", 270, 352, 500, 352, 108),
                 ("p", [(270, 340), (500, 340), (530, 540), (520, 810), (250, 810), (240, 540)]),
                 ("c", 262, 365, 238, 760, 76), ("c", 492, 365, 640, 320, 70), ("c", 640, 320, 700, 180, 62), ("e", 708, 150, 38, 46),
                 ("c", 330, 800, 312, 1480, 112), ("c", 430, 800, 448, 1480, 112), ("e", 312, 1505, 62, 34), ("e", 452, 1505, 62, 34)],
       extra=lambda d: d.polygon([(640, 10), (820, 34), (796, 270), (618, 246)], fill=(232, 226, 210, 255)))
figure("worker", [("e", 400, 200, 60, 74), ("c", 400, 262, 400, 330, 72), ("c", 275, 352, 525, 352, 110),
                  ("p", [(280, 340), (520, 340), (548, 540), (536, 810), (264, 810), (252, 540)]),
                  ("c", 272, 365, 300, 560, 74), ("c", 528, 365, 500, 560, 74),
                  ("c", 350, 800, 330, 1480, 112), ("c", 450, 800, 470, 1480, 112), ("e", 330, 1505, 62, 34), ("e", 472, 1505, 62, 34)],
       extra=lambda d: (d.rectangle([230, 470, 570, 700], fill=(120, 92, 62, 255)), d.rectangle([230, 560, 570, 586], fill=(150, 126, 92, 255))))
