#!/usr/bin/env python3
"""Derive terrain tiles, props, UI pips, sky and hazard canvases from the
style-pack sources. All derivations are recorded in manifest_extra.json.
Terrain: the approved 3x3 patch is sliced into the 14-tile kit; platform
tiles are the caps' top bands; inner corners are fill tiles with a darkened
concave corner (painted over, documented derivation, no generated seam art).
Props: chroma-keyed singles normalized onto ASSET_BRIEFS canvases/pivots.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.expanduser("~/workspace/gothic-whip/game/art")
SRC = os.path.join(ROOT, "source")
OUT_T = os.path.join(ROOT, "terrain")
OUT_P = os.path.join(ROOT, "props")
OUT_U = os.path.join(ROOT, "ui")
for d in (OUT_T, OUT_P, OUT_U):
    os.makedirs(d, exist_ok=True)

def chroma(img, thresh=40):
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    dom = g - np.maximum(r, b)
    alpha = np.clip(1.0 - (dom - 18.0) / 60.0, 0.0, 1.0)
    alpha[dom > 90] = 0.0
    out = np.dstack([arr, alpha * 255.0])
    spill = (dom > 0) & (alpha > 0)
    out[..., 1] = np.where(spill, np.minimum(out[..., 1], np.maximum(r, b) + dom * 0.15), out[..., 1])
    return Image.fromarray(out.astype(np.uint8))

def bbox_of(img):
    a = np.asarray(img)[..., 3]
    ys, xs = np.where(a > 40)
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)

def place(img, canvas, pivot, height_px=None, width_px=None):
    """Crop to bbox, scale to target height/width, paste feet-aligned."""
    x0, y0, x1, y1 = bbox_of(img)
    crop = img.crop((x0, y0, x1, y1))
    if height_px:
        s = height_px / crop.height
        crop = crop.resize((max(1, round(crop.width * s)), height_px), Image.LANCZOS)
    elif width_px:
        s = width_px / crop.width
        crop = crop.resize((width_px, max(1, round(crop.height * s))), Image.LANCZOS)
    canv = Image.new("RGBA", canvas, (0, 0, 0, 0))
    canv.paste(crop, (round(pivot[0] - crop.width / 2), round(pivot[1] - crop.height)), crop)
    return canv

log = []

# ---------------- terrain: slice the approved 3x3 patch -------------------
patch = Image.open(os.path.join(SRC, "style_terrain_patch_3x3.png")).convert("RGB")
W, H = patch.size
cw, ch = W // 3, H // 3
cells = {}
for r in range(3):
    for c in range(3):
        cells[(c, r)] = patch.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)).resize((128, 128), Image.LANCZOS)

tiles = {
    "terrain_cap_left": cells[(0, 0)], "terrain_cap_mid": cells[(1, 0)], "terrain_cap_right": cells[(2, 0)],
    "terrain_side_left": cells[(0, 1)], "terrain_fill_center": cells[(1, 1)], "terrain_side_right": cells[(2, 1)],
    "terrain_bottom_left": cells[(0, 2)], "terrain_bottom_mid": cells[(1, 2)], "terrain_bottom_right": cells[(2, 2)],
}
def top_band(img, band=46):
    band_img = img.crop((0, 0, 128, band)).resize((128, 128), Image.LANCZOS)
    return band_img
tiles["terrain_plat_end_left"] = top_band(cells[(0, 0)])
tiles["terrain_plat_mid"] = top_band(cells[(1, 0)])
tiles["terrain_plat_end_right"] = top_band(cells[(2, 0)])
# inner corners: fill with darkened concave corner wedge (derivation logged)
for name, corner in (("terrain_inner_left", "tl"), ("terrain_inner_right", "tr")):
    t = cells[(1, 1)].copy()
    d = ImageDraw.Draw(t, "RGBA")
    if corner == "tl":
        d.polygon([(0, 0), (64, 0), (0, 64)], fill=(10, 8, 18, 140))
    else:
        d.polygon([(128, 0), (64, 0), (128, 64)], fill=(10, 8, 18, 140))
    tiles[name] = t
for name, img in tiles.items():
    img.convert("RGB").save(os.path.join(OUT_T, name + ".png"))
log.append(f"terrain: {len(tiles)} tiles sliced/derived from style_terrain_patch_3x3")

# ---------------- sky: painted gradient from the distant plate's sky -----
dist = Image.open(os.path.join(SRC, "bg_distant_silhouette.png")).convert("RGB")
sky_src = dist.crop((0, 0, dist.width, int(dist.height * 0.55))).resize((1024, 1024), Image.LANCZOS)
# deepen toward abyss violet at the very bottom (behind silhouettes is fine)
grad = Image.linear_gradient("L").resize((1024, 1024))
grad_arr = (np.asarray(grad).astype(np.float32) / 255.0)[..., None]
base = np.asarray(sky_src).astype(np.float32)
dark = np.array([23, 18, 33], dtype=np.float32)
mixed = base * (1 - 0.55 * grad_arr) + dark * (0.55 * grad_arr)
Image.fromarray(mixed.astype(np.uint8)).save(os.path.join(ROOT, "bg_sky.png"))
log.append("bg_sky: 1024x1024 gradient derived from bg_distant_silhouette sky band")

# ---------------- props ----------------------------------------------------
def need(name):
    p = os.path.join(SRC, name + ".png")
    return Image.open(p) if os.path.exists(p) else None

img = need("prop_effigy")
if img:
    place(chroma(img), (128, 256), (64, 224), height_px=224).save(os.path.join(OUT_P, "prop_effigy.png"))
    log.append("prop_effigy -> 128x256 pivot(64,224)")
img = need("prop_checkpoint")
if img:
    keyed = chroma(img)
    w, h = keyed.size
    half = w // 2
    for i, nm in enumerate(("prop_checkpoint_off", "prop_checkpoint_on")):
        part = keyed.crop((i * half, 0, (i + 1) * half, h))
        place(part, (192, 320), (96, 288), height_px=288).save(os.path.join(OUT_P, nm + ".png"))
    log.append("prop_checkpoint off/on -> 192x320 pivot(96,288)")
img = need("prop_boss_gate")
if img:
    place(chroma(img), (128, 320), (64, 288), height_px=288).save(os.path.join(OUT_P, "prop_boss_gate.png"))
    log.append("prop_boss_gate -> 128x320 pivot(64,288)")
img = need("prop_exit")
if img:
    place(chroma(img), (192, 320), (96, 288), height_px=288).save(os.path.join(OUT_P, "prop_exit.png"))
    log.append("prop_exit -> 192x320 pivot(96,288)")
img = need("ui_health_pips")
if img:
    keyed = chroma(img)
    w, h = keyed.size
    half = w // 2
    for i, nm in enumerate(("ui_health_full", "ui_health_empty")):
        part = keyed.crop((i * half, 0, (i + 1) * half, h))
        x0, y0, x1, y1 = bbox_of(part)
        part.crop((x0, y0, x1, y1)).resize((64, 64), Image.LANCZOS).save(os.path.join(OUT_U, nm + ".png"))
    log.append("ui_health_full/empty -> 64x64")

# foreground frame: chroma-key the green centre
fg = need("bg_foreground_frame")
if fg:
    chroma(fg).save(os.path.join(ROOT, "bg_foreground_frame_rgba.png"))
    log.append("bg_foreground_frame_rgba: green centre keyed to alpha")

print("\n".join(log))
with open(os.path.join(ROOT, "manifest_extra.json"), "w") as f:
    json.dump({"derivations": log}, f, indent=1)
