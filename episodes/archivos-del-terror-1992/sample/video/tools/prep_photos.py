# Executed from prep_assets.py. Real photographs from assets/photos/ (LICENSES.md §8-1; only files whose name is
# recorded there are used). Crops drop HABS/HAER borders and catalogue numbers; the Tucson "COMANDANCIA DE POLICIA"
# lettering is blurred out (not a Paraguayan site); the Harris & Ewing frames are cropped or blurred so no face of
# a member of the public can be recognised. Toning per period (cold 1992 / tungsten archive / sepia 1954).
import json as _json

PHD = os.path.join(SRC, "photos")
_LIC = open(os.path.join(SRC, "LICENSES.md")).read()
os.makedirs(out("ph"), exist_ok=True)
TONES = {
    "cold": (np.array([0.015, 0.03, 0.05]), np.array([0.86, 0.91, 0.95])),
    "tung": (np.array([0.04, 0.02, 0.008]), np.array([1.0, 0.86, 0.64])),
    "sepia": (np.array([0.05, 0.03, 0.015]), np.array([0.97, 0.86, 0.66])),
}
# key: (file, crop box in source px, tone, [blur boxes in source px], contrast, extra blur radius)
PH = {
    "comandancia": ("habs_az0060_tucson_comandancia_policia_1937.jpg", (150, 300, 4750, 2800), "cold", [], 1.25, 0),
    "arch": ("habs_az0060_tucson_comandancia_policia_1937.jpg", (1300, 1480, 2900, 2640), "cold", [], 1.3, 0),
    "cabinets": ("habs_pa2957_file_cabinets_record_vault_1994.jpg", (1000, 600, 4600, 2625), "cold", [], 1.25, 0),
    "typewriter": ("owi_1942_battle_scarred_typewriter_liberman.jpg", (900, 700, 4100, 2500), "cold", [], 1.35, 0),
    "stairway": ("habs_pa1976_basement_stairway.jpg", (250, 350, 4800, 3450), "tung", [], 1.3, 0),
    "stairdoor": ("habs_il0937_basement_stairs_door_2008.jpg", (250, 1500, 3350, 3245), "tung", [], 1.3, 0),
    "vault": ("habs_ca2282_vault_forced_entry_1997.jpg", (100, 500, 4950, 3230), "tung", [], 1.25, 0),
    "records": ("habs_ma1170_record_storage_room_1982.jpg", (200, 1300, 3500, 3156), "tung", [], 1.3, 0),
    "records_tall": ("habs_ma1170_record_storage_room_1982.jpg", (300, 320, 3500, 4600), "tung", [], 1.3, 0),
    "catalog": ("habs_ca2248_card_catalog_drawers_1996.jpg", (400, 900, 4600, 3263), "tung", [], 1.25, 0),
    "ledger": ("haer_ne0071_handwritten_ledger_1879.jpg", (300, 700, 2700, 2050), "tung", [], 1.25, 13),
    "aisle": ("hec_1932_filing_fingerprints_mugshots.jpg", (1950, 1300, 3750, 2312), "tung", [(2050, 1640, 3350, 2160)], 1.25, 0),
    "fpcab": ("hec_1930_fingerprint_sheet_file_cabinet.jpg", (1950, 650, 3850, 1719), "tung", [], 1.25, 5),
    "palacio": ("loc_asuncion_palacio_lopez_1908-1919_npco.jpg", (300, 700, 5600, 3681), "sepia", [], 1.2, 0),
    "nasa96": ("nasa_sts072-730-079_asuncion_1996.jpg", (1000, 1600, 3600, 3062), None, [], 1.15, 0),
    "map1856": ("map_loc_1856_basin_la_plata_page_usn.jpg", (300, 300, 4150, 5400), "sepia", [], 0.55, 34),
    "cia1954": ("doc_cia_1954-05-07_paraguayan_political_crisis_p1.png", (0, 0, 2544, 4118), "sepia", [], 1.0, 9),
    "condor76": ("doc_cia_1976-07-21_condor_cable_p1.png", (0, 0, 2544, 3301), "tung", [], 1.0, 9),
}
PHINFO = {}


def clean_sign(im):
    """Cover the 'COMANDANCIA DE POLICIA' lettering on the arch rim with clean stucco from the same wall
    (x 2750–3400, y 950–1500), mirrored tiles, soft ring mask: no lettering, no blur smudge."""
    cx, cy, r_in, r_out = 2177, 1724, 440, 610
    box = (cx - r_out - 20, cy - r_out - 20, cx + r_out + 20, cy - 40)
    src = im.crop((2750, 950, 3400, 1500))
    tile = Image.new(im.mode, (src.size[0] * 2, src.size[1] * 2))
    tile.paste(src, (0, 0)); tile.paste(ImageOps.mirror(src), (src.size[0], 0))
    tile.paste(ImageOps.flip(src), (0, src.size[1])); tile.paste(ImageOps.flip(ImageOps.mirror(src)), src.size)
    w, h = box[2] - box[0], box[3] - box[1]
    fill = tile.resize((w, h), Image.BICUBIC)
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([cx - r_out - box[0], cy - r_out - box[1], cx + r_out - box[0], cy + r_out - box[1]], fill=255)
    d.ellipse([cx - r_in - box[0], cy - r_in - box[1], cx + r_in - box[0], cy + r_in - box[1]], fill=0)
    im.paste(fill, box[:2], mask.filter(ImageFilter.GaussianBlur(10)))
    return im

for key, (fname, box, tone, blurs, con, rad) in PH.items():
    src = os.path.join(PHD, fname)
    if fname not in _LIC or not os.path.exists(src):
        continue
    im = Image.open(src)
    rgb = im.mode == "RGB" and tone is None
    im = im.convert("RGB" if rgb else "L")
    if fname.startswith("habs_az0060"):
        im = clean_sign(im)
    for b in blurs:                                     # sign lettering / bystanders
        patch = im.crop(b).filter(ImageFilter.GaussianBlur(40 if key in ("comandancia", "arch") else 14))
        mask = Image.new("L", patch.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([8, 8, patch.size[0] - 8, patch.size[1] - 8], radius=40, fill=255)
        im.paste(patch, b[:2], mask.filter(ImageFilter.GaussianBlur(20)))
    im = im.crop(box)
    if rad:
        im = im.filter(ImageFilter.GaussianBlur(rad))
    cw = im.size[0]
    if im.size[0] > 2880:
        im = im.resize((2880, int(im.size[1] * 2880 / im.size[0])), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255
    if rgb:
        o = np.clip((a - 0.5) * con + 0.5, 0, 1)
        lum = o @ np.array([0.299, 0.587, 0.114])
        o = lum[..., None] * 0.45 + o * 0.55             # quieter NASA colour
    else:
        l = np.clip((a - 0.5) * con + 0.5, 0, 1)
        l = l * l * (3 - 2 * l) * 0.5 + l * 0.5          # gentle S-curve: deep blacks, kept highlights
        lo, hi = TONES[tone]
        o = lo * (1 - l[..., None]) + hi * l[..., None]
    save(o * 255, out("ph", key + ".jpg"), q=90)
    PHINFO[key] = {"w": im.size[0], "h": im.size[1], "src_w": cw, "file": fname}
_json.dump(PHINFO, open(out("ph", "ph.json"), "w"), indent=1)
print("photos:", sorted(PHINFO))
