#!/usr/bin/env python3
"""Contact sheets for scale verification: one representative frame per clip
(the median-LCC-height frame), drawn at 0.5 scale with the contract pivot
as a red crosshair and the actor's design height as a green horizontal
line above the pivot. Usage: contact_sheet.py <hero|actors> <out.png>"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/gothic-whip/game/art")
FRAMES = os.path.join(ROOT, "frames")
THR = 40

HERO_CLIPS = ["hero_idle", "hero_walk", "hero_start_move", "hero_stop_move",
              "hero_turn", "hero_crouch_enter", "hero_crouch_idle",
              "hero_crouch_exit", "hero_jump_takeoff", "hero_jump_rise",
              "hero_jump_apex", "hero_fall", "hero_land",
              "hero_attack_ground", "hero_attack_air", "hero_attack_crouch",
              "hero_hurt_recoil", "hero_knockback", "hero_knockdown",
              "hero_get_up", "hero_death"]
DESIGN = {"hero": 224, "pursuer": 112, "swooper": 170, "ranged": 300, "boss": 352}

def lcc_h(path):
    a = np.asarray(Image.open(path).convert("RGBA"))[..., 3]
    mask = a > THR
    lab, n = ndimage.label(mask)
    if n == 0:
        return 0
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    li = int(np.argmax(sizes)) + 1
    ys, _ = np.where(lab == li)
    return int(ys.max()) + 1 - int(ys.min())

def pick_frame(clip):
    d = os.path.join(FRAMES, clip)
    files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    hs = [(lcc_h(os.path.join(d, f)), f) for f in files]
    hs.sort()
    return hs[len(hs) // 2]  # (height, file) median frame

def sheet(clips, out, cols):
    meta = json.load(open(os.path.join(ROOT, "clips.json")))
    tiles = []
    for clip in clips:
        h, f = pick_frame(clip)
        info = meta[clip]
        cw, ch = info["canvas"]
        px, py = info["pivot"]
        actor = clip.split("_")[0]
        im = Image.open(os.path.join(FRAMES, clip, f)).convert("RGBA")
        tile = Image.new("RGBA", (cw, ch), (24, 24, 32, 255))
        tile.alpha_composite(im)
        dr = ImageDraw.Draw(tile)
        design = DESIGN.get(actor, 224)
        dr.line([(0, py - design), (cw, py - design)], fill=(60, 255, 60, 255), width=2)
        dr.line([(px, 0), (px, ch)], fill=(255, 60, 60, 255), width=1)
        dr.line([(0, py), (cw, py)], fill=(255, 60, 60, 255), width=1)
        dr.rectangle([px - 6, py - 6, px + 6, py + 6], outline=(255, 60, 60, 255), width=2)
        tile = tile.resize((cw // 2, ch // 2), Image.LANCZOS)
        dr = ImageDraw.Draw(tile)
        dr.rectangle([0, 0, cw // 2, 14], fill=(0, 0, 0, 255))
        dr.text((3, 3), f"{clip} h={h}", fill=(255, 255, 0, 255))
        tiles.append(tile)
    tw, th = tiles[0].size
    rows = (len(tiles) + cols - 1) // cols
    out_im = Image.new("RGBA", (cols * tw, rows * th), (10, 10, 14, 255))
    for i, t in enumerate(tiles):
        out_im.paste(t, ((i % cols) * tw, (i // cols) * th))
    out_im.save(out)
    print("wrote", out, out_im.size)

if __name__ == "__main__":
    which, out = sys.argv[1], sys.argv[2]
    if which == "hero":
        sheet(HERO_CLIPS, out, 7)
    else:
        meta = json.load(open(os.path.join(ROOT, "clips.json")))
        clips = [c for c in sorted(meta) if c.split("_")[0] in
                 ("pursuer", "swooper", "ranged", "boss")]
        sheet(clips, out, 8)
