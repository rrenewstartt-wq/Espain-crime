# Executed from prep_assets.py. Public-domain footage (assets/footage/, LICENSES.md §9): only files recorded there,
# never fx08–fx12 (Basic Typing 1944, © 1943 notice not cleared). Each clip is trimmed, cropped, de-identified
# (faces of members of the public and English lettering blurred or cropped out), toned to the period palette and
# converted from 23.976 to 30 fps by mapping every source frame to one output frame (no 3:2 judder, no blend ghosts;
# motion plays 1.25x, the cadence of silent-era footage). The NASA clip (24 fps) is mapped the same way. Two outputs per clip:
#   assets/fx/<key>.mp4     sharp, native crop size (shown at most 1.5x in the scenes)
#   assets/fx/<key>_bg.mp4  1920x1080, heavily blurred and darkened (background use only)
def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


FXD = os.path.join(SRC, "footage")
os.makedirs(out("fx"), exist_ok=True)
_LICF = open(os.path.join(SRC, "LICENSES.md")).read()
BANNED = ("fx08", "fx09", "fx10", "fx11", "fx12")
LUT = {"cold": ((4, 8, 13), (222, 232, 242)), "tung": ((10, 5, 2), (255, 222, 166)), "sepia": ((13, 8, 4), (248, 222, 172))}
# key: (file stem, start s, duration s, crop (x, y, w, h) or None, tone, [blur boxes in crop px (x, y, w, h, radius)], make_bg, reverse)
FX = {
    "f_type": ("fx14_coronet1941_manos_maquina", 0.3, 2.4, None, "cold", [(380, 0, 260, 120, 6)], False, False),
    "f_roller": ("fx14_coronet1941_manos_maquina", 2.0, 2.3, (160, 0, 480, 300), "cold", [(220, 0, 260, 120, 6)], False, False),
    "f_write": ("fx07_fbi1969_mano_escribe_papeles", 1.0, 2.1, None, "cold", [(0, 120, 640, 360, 5)], False, False),
    "f_finger": ("fx06_fbi1969_dedo_recorre_archivo", 0.2, 2.2, None, "cold", [(0, 0, 640, 480, 3)], True, False),
    "f_office": ("fx01_fbi1969_fichero_oficina", 0.2, 2.4, None, "cold", [(380, 140, 140, 90, 14), (220, 160, 60, 60, 12), (160, 0, 80, 70, 10)], True, False),
    "f_card": ("fx02_fbi1969_mano_saca_ficha", 0.3, 2.4, None, "tung", [(250, 270, 190, 130, 10), (0, 0, 150, 480, 4)], False, False),
    "f_card_c": ("fx02_fbi1969_mano_saca_ficha", 1.2, 1.4, None, "cold", [(250, 270, 190, 130, 10), (0, 0, 150, 480, 4)], False, False),
    "f_shadowdoc": ("fx19_army1941_documento_sombra", 0.1, 1.5, None, "cold", [(80, 40, 440, 360, 6)], False, False),
    "f_flip": ("fx03_fbi1969_mano_hojea_fichas", 0.0, 2.6, None, "cold", [(250, 270, 190, 130, 10)], True, True),
    "f_wall": ("fx13_coronet1941_muro_ficheros", 0.0, 3.8, None, "tung", [(190, 0, 160, 130, 14), (380, 110, 130, 140, 14), (470, 290, 120, 140, 14), (500, 0, 140, 120, 12)], True, False),
    "f_torch": ("fx22_booked1960_linterna_oscuro", 0.0, 2.2, (380, 160, 260, 320), "tung", [], True, False),
    "f_hatdoor": ("fx16_army1941_sombra_en_puerta", 0.2, 2.6, None, "tung", [], True, False),
    "f_river": ("fx36_ociaa1945_rio_paraguay", 0.3, 1.9, None, "sepia", [], False, False),
    "f_tram": ("fx31_ociaa1945_asuncion_tranvia", 0.5, 2.6, None, "sepia", [], True, False),
    "f_roofs": ("fx29_ociaa1945_asuncion_tejados", 0.2, 1.4, None, "sepia", [], True, False),
    "f_roofs2": ("fx29b_ociaa1945_asuncion_tejados2", 0.1, 1.4, None, "sepia", [], True, False),
    "f_horizon": ("fx28_ociaa1945_asuncion_horizonte", 0.2, 2.3, None, "sepia", [], True, False),
    "f_soldiers": ("fx34_ociaa1945_soldados_contrapicado", 0.3, 1.1, (0, 220, 640, 260), "sepia", [(0, 0, 640, 40, 8)], True, False),
    "f_enter": ("fx17_army1941_abre_puerta_entra", 2.2, 1.2, None, "cold", [(330, 100, 120, 120, 14)], False, False),
    "f_guardhand": ("fx27_police1953_agente_prueba_puerta", 0.2, 1.4, (300, 170, 340, 310), "cold", [], True, False),
    "f_stairs": ("fx21_booked1960_escalera_policia", 0.95, 1.25, (200, 120, 440, 320), "tung", [(120, 0, 200, 70, 12)], False, False),
    "f_knob": ("fx25_police1953_mano_pomo_cerradura", 0.2, 1.2, None, "tung", [], False, False),
    "f_files": ("fx05_fbi1969_manos_hojean_archivo", 0.2, 1.3, None, "tung", [(60, 40, 560, 380, 4)], False, False),
    "f_register": ("fx15_coronet1941_lapiz_registro", 0.4, 0.9, None, "sepia", [(0, 0, 640, 330, 5)], False, False),
    "f_orbit": ("fx37_nasa2011_sudamerica_amanecer", 0.0, 0.85, None, None, [], False, False),
}
FXINFO = {}


def _lut(tone):
    lo, hi = LUT[tone]
    return "lutrgb=" + ":".join(f"{c}='{lo[i]}+val*({hi[i]}-{lo[i]})/255'" for i, c in enumerate("rgb"))


for key, (stem, ss, dur, crop, tone, blurs, mkbg, rev) in FX.items():
    src = os.path.join(FXD, stem + ".mp4")
    RATE = 24.0 if stem.startswith("fx37") else 24000 / 1001
    if stem.startswith(BANNED) or (stem + ".mp4") not in _LICF or not os.path.exists(src):
        continue
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", src],
                           capture_output=True, text=True).stdout.strip().split(",")
    sw, sh = int(probe[0]), int(probe[1])
    cx, cy, cw, ch = crop or (0, 0, sw, sh)
    cw, ch = cw // 2 * 2, ch // 2 * 2
    chain = [f"[0:v]crop={cw}:{ch}:{cx}:{cy}[c0]"]
    last = "c0"
    for i, (bx, by, bw, bh, r) in enumerate(blurs):
        bw, bh = min(bw, cw - bx), min(bh, ch - by)
        chain.append(f"[{last}]split[m{i}][s{i}];[s{i}]crop={bw}:{bh}:{bx}:{by},boxblur={r}:2[b{i}];[m{i}][b{i}]overlay={bx}:{by}[c{i + 1}]")
        last = f"c{i + 1}"
    tonef = (f"format=gray,eq=contrast=1.18,format=rgb24,{_lut(tone)}" if tone else "eq=contrast=1.08:saturation=0.75")
    revf = ",reverse" if rev else ""
    chain.append(f"[{last}]{tonef}{revf},setpts=(PTS-STARTPTS)*{RATE}/30,fps=30,format=yuv420p[v]")
    ff("-ss", str(ss), "-t", f"{dur * 30 / RATE:.3f}", "-i", src, "-filter_complex", ";".join(chain), "-map", "[v]", "-an",
       "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-r", "30", out("fx", key + ".mp4"))
    if mkbg:
        ff("-i", out("fx", key + ".mp4"), "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=18,eq=brightness=-0.12",
           "-an", "-c:v", "libx264", "-crf", "18", "-r", "30", "-pix_fmt", "yuv420p", out("fx", key + "_bg.mp4"))
    FXINFO[key] = {"w": cw, "h": ch, "dur": dur, "src": stem + ".mp4", "bg": mkbg}
_json.dump(FXINFO, open(out("fx", "fx.json"), "w"), indent=1)
print("footage:", sorted(FXINFO))
