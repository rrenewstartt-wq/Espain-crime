#!/usr/bin/env python3
"""Render a thumbnail in the reference grammar (docs/thumbnail-formula.md).

    python3 scripts/thumbnail.py episodes/<ep>            # reads thumbnail/spec.json → thumbnail/out.png
    python3 scripts/thumbnail.py --demo /tmp/demo.png     # synthetic images, to try the look

spec.json:
{
  "text": "69 DÍAS",                         # 1~4 words, rendered upper-case
  "subject": "assets/…/person.png",          # centre subject (PNG with transparency works best), optional
  "collage": ["a.jpg", "b.jpg", "c.jpg"],    # documents / screens / photos behind, optional
  "eye_bar": [[x1, y1, x2, y2]],             # black bars in output pixels (1280×720), optional
  "accent": null                             # null → config/format.json thumbnail.accent
}
Every image used must have a licence noted in shots.md (Créditos).
"""
import argparse
import json
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE, FMT  # noqa: E402

W, H = FMT["thumbnail"]["size"]
FONT = f"{BASE}/assets/fonts/Anton-Regular.ttf"


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cover(im, w, h):
    return ImageOps.fit(im.convert("RGBA"), (w, h), Image.LANCZOS)


def collage(paths, seed=7):
    base = Image.new("RGBA", (W, H), (10, 10, 10, 255))
    rnd = random.Random(seed)
    for i, p in enumerate(paths[:6]):
        im = Image.open(p).convert("RGBA")
        scale = rnd.uniform(0.45, 0.65)
        tw = int(W * scale)
        im = ImageOps.contain(im, (tw, int(H * 0.9)))
        im = im.rotate(rnd.uniform(-8, 8), expand=True, resample=Image.BICUBIC)
        x = int((i % 3) * W / 3 + rnd.uniform(-80, 40))
        y = int((i // 3) * H / 2 + rnd.uniform(-60, 40))
        base.alpha_composite(im, (max(-100, x), max(-100, y)))
    return base


def grade(im, accent):
    """Monochrome tone: shadows → black, mids → accent, top highlights → light accent."""
    g = ImageOps.autocontrast(im.convert("L"), cutoff=2)
    lut = {c: [] for c in range(3)}
    for v in range(256):
        t = v / 255
        mid = min(1.0, t * 1.15) ** 2.0
        hi = max(0.0, (t - 0.86) / 0.14) * 0.35
        for c in range(3):
            lut[c].append(int(min(255, accent[c] * mid + (255 - accent[c]) * hi)))
    return Image.merge("RGB", [g.point(lut[c]) for c in range(3)])


def vignette(im, strength=0.75):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for i in range(60):
        k = i / 60
        d.ellipse([-W * 0.25 + k * W * 0.25, -H * 0.35 + k * H * 0.3, W * 1.25 - k * W * 0.25, H * 1.35 - k * H * 0.3],
                  fill=int(255 * k))
    mask = mask.filter(ImageFilter.GaussianBlur(60))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(im, Image.blend(im, dark, strength), mask)


def draw_text(im, text, accent):
    text = text.upper()
    size = int(H * 0.22)
    font = ImageFont.truetype(FONT, size)
    while font.getbbox(text)[2] > W * 0.9 and size > 40:
        size -= 4
        font = ImageFont.truetype(FONT, size)
    x0, y0, x1, y1 = font.getbbox(text)
    tw, th = x1 - x0, y1 - y0
    x, y = (W - tw) // 2 - x0, int(H * 0.56 - th / 2) - y0
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((x, y), text, font=font, fill=accent + (255,), stroke_width=10, stroke_fill=accent + (255,))
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    im = im.convert("RGBA")
    im.alpha_composite(glow)
    im.alpha_composite(glow)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x, y), text, font=font, fill=accent + (255,), stroke_width=4, stroke_fill=(255, 255, 255, 255))
    im.alpha_composite(lay)
    return im.convert("RGB"), {"text_height_ratio": round(th / H, 3), "font_size": size}


def render(spec, out):
    accent = hex2rgb(spec.get("accent") or FMT["thumbnail"]["accent"])
    forb = [f.lower() for f in FMT["thumbnail"]["forbidden_accents"]]
    if (spec.get("accent") or "").lower() in forb:
        sys.exit("금지된 강조색입니다 (레퍼런스 빨강). docs/originality.md")
    canvas = collage(spec.get("collage", [])) if spec.get("collage") else Image.new("RGBA", (W, H), (18, 18, 18, 255))
    canvas = Image.blend(canvas, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.62)  # background stays dark
    if spec.get("subject"):
        sub = Image.open(spec["subject"]).convert("RGBA")
        sub = ImageOps.contain(sub, (int(W * 0.6), int(H * 0.95)))
        canvas.alpha_composite(sub, ((W - sub.width) // 2, H - sub.height))
    im = vignette(grade(canvas, accent))
    d = ImageDraw.Draw(im)
    for box in spec.get("eye_bar", []):
        d.rectangle(box, fill=(0, 0, 0))
    im, info = draw_text(im, spec["text"], accent)
    im = ImageChops.add(im, Image.effect_noise((W, H), 18).convert("RGB").point(lambda v: max(0, v - 120) // 6))
    im.save(out)
    im.resize((168, 94), Image.LANCZOS).save(out.replace(".png", "-168.png"))
    print(f"저장: {out} (+168px 미리보기) {info}")
    return info


def demo(out):
    tmp = os.path.dirname(os.path.abspath(out))
    rnd = random.Random(3)
    paths = []
    for i in range(4):
        im = Image.new("RGB", (900, 640), (235, 230, 215))
        d = ImageDraw.Draw(im)
        for k in range(26):
            d.rectangle([60, 60 + k * 22, 60 + rnd.randint(300, 780), 72 + k * 22], fill=(60, 60, 60))
        p = f"{tmp}/demo-doc{i}.png"
        im.save(p)
        paths.append(p)
    person = Image.new("RGBA", (600, 800), (0, 0, 0, 0))
    d = ImageDraw.Draw(person)
    d.ellipse([190, 80, 410, 330], fill=(205, 205, 205, 255))
    d.rounded_rectangle([90, 320, 510, 800], 120, fill=(150, 150, 150, 255))
    pp = f"{tmp}/demo-person.png"
    person.save(pp)
    return render({"text": "69 DÍAS", "subject": pp, "collage": paths, "eye_bar": [[565, 170, 715, 205]]}, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?")
    ap.add_argument("--demo")
    a = ap.parse_args()
    if a.demo:
        demo(a.demo)
        return
    ep = a.episode.rstrip("/")
    spec = json.load(open(f"{ep}/thumbnail/spec.json", encoding="utf-8"))
    for k in ("subject",):
        if spec.get(k) and not os.path.isabs(spec[k]):
            spec[k] = os.path.join(BASE, spec[k])
    spec["collage"] = [c if os.path.isabs(c) else os.path.join(BASE, c) for c in spec.get("collage", [])]
    render(spec, f"{ep}/thumbnail/out.png")


if __name__ == "__main__":
    main()
