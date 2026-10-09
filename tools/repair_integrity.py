#!/usr/bin/env python3
"""Integrity repairs for the 2026-10-09 art-integrity audit
(game/art/ART_INTEGRITY_AUDIT.md). Three repair classes:

A1 hero_idle (all 8 frames): the generated sheet was a waist-up torso.
   The image-generation upstream was unavailable for a replacement sheet
   (media.generate_image failed, 2026-10-09), so the idle is rebuilt from
   the game's own approved full-body standing frame (hero_turn f00 — the
   neutral stand, same drawing as hero_start_move f00) with a procedural
   breathing loop: feet-anchored vertical breath of +0.9% at peak. This
   guarantees the idle is literally the same man as walk/turn. Documented
   in REVIEW_RECORD; flagged for the user's visual verdict.
A2 hero_death f08: figure fragmented (torso missing). Rebuilt from a
   generated candidate sheet (art/source/hero_death_f08_source.png,
   generated 2026-10-09 with hero_death f09 as identity reference): the
   most complete lying figure is extracted, mirrored (the clip's corpse
   lies head-left), scaled to the clip's median sqrt-area and placed on
   the contract pivot. normalize_frame_scales (hero_death is SA-class)
   then pins it exactly to the clip median.
B  pursuer_alert / pursuer_lunge_windup / swooper_dive_telegraph:
   figures clipped by their canvas at extraction; the source sheets are
   intact. Reprocessed via process_frames.process_sheet with taller/wider
   per-clip canvas + pivot (same feet/centre anchor relative to pivot,
   so in-game placement is unchanged). manifest_raw.json canvas/pivot
   patched for these clips; pack_atlases rebuilds clips.json/atlases.
C  Debris cleanup on named frames: remove satellite components (neighbour
   bleed, sheet slabs, specks) or hollow cell-border rectangle outlines.
   The main figure is never touched.

Run order: this script -> pack_atlases.py -> normalize_frame_scales.py
-> pack_atlases.py -> audit_integrity.py / audit_sequences.py.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import process_frames as pf

ROOT = os.path.expanduser("~/workspace/gothic-whip/game")
ART = os.path.join(ROOT, "art")
FRAMES = os.path.join(ART, "frames")
SRC = os.path.join(ART, "source")
THR = 40
log = []


def save_frames(clip, frames):
    d = os.path.join(FRAMES, clip)
    os.makedirs(d, exist_ok=True)
    for i, fr in enumerate(frames):
        fr.save(os.path.join(d, f"{clip}_f{i:02d}.png"))
    log.append(f"{clip}: wrote {len(frames)} frames")


# ---------------------------------------------------------------- A1 idle
def repair_idle():
    base = Image.open(os.path.join(FRAMES, "hero_turn", "hero_turn_f00.png")).convert("RGBA")
    a = np.asarray(base)[..., 3]
    ys, xs = np.where(a > THR)
    x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
    crop = base.crop((x0, y0, x1, y1))
    frames = []
    for i in range(8):
        lift = (np.sin(2 * np.pi * i / 8 - np.pi / 2) + 1) / 2  # 0..1..0 smooth
        f = 1.0 + 0.009 * lift
        nh = max(1, int(round(crop.height * f)))
        c = crop.resize((crop.width, nh), Image.LANCZOS) if nh != crop.height else crop
        canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        canvas.paste(c, (x0, y1 - nh), c)  # feet line (bbox bottom) fixed
        frames.append(canvas)
    save_frames("hero_idle", frames)
    log.append(f"hero_idle: rebuilt from hero_turn f00 (bbox {x1-x0}x{y1-y0}), "
               f"breathing peak +0.9% height")


# ------------------------------------------------------------- A2 death f08
def repair_death_f08():
    sheet_path = os.path.join(SRC, "hero_death_f08_source.png")
    rgba, _stats = pf.chroma_key(Image.open(sheet_path))
    alpha = rgba[..., 3]
    mask = alpha > THR
    lab, n = ndimage.label(mask)
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    H, W = mask.shape
    best = None
    for li in range(1, n + 1):
        if sizes[li - 1] < 15000:
            continue
        ys, xs = np.where(lab == li)
        cx, cy = xs.mean(), ys.mean()
        clipped = xs.min() <= 1 or ys.min() <= 1 or xs.max() >= W - 2 or ys.max() >= H - 2
        log.append(f"death candidate comp#{li}: area={sizes[li-1]:.0f} "
                   f"centroid=({cx:.0f},{cy:.0f}) clipped={clipped}")
        if cx > W / 2 and cy > H / 2 and not clipped:
            if best is None or sizes[li - 1] > sizes[best - 1]:
                best = li
    if best is None:
        raise SystemExit("no complete bottom-right death candidate found")
    ys, xs = np.where(lab == best)
    x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
    keep = (lab[y0:y1, x0:x1] == best)
    cell = rgba[y0:y1, x0:x1].copy()
    cell[..., 3] = np.where(keep, cell[..., 3], 0)
    img = Image.fromarray(cell.astype(np.uint8), "RGBA").transpose(Image.FLIP_LEFT_RIGHT)
    # scale to the clip's median sqrt-area (excluding the broken f08)
    sas = []
    d = os.path.join(FRAMES, "hero_death")
    for i in range(10):
        if i == 8:
            continue
        aa = np.asarray(Image.open(os.path.join(d, f"hero_death_f{i:02d}.png")))[..., 3]
        sas.append(float(np.sqrt((aa > THR).sum())))
    target_sa = float(np.median(sas))
    cur_sa = float(np.sqrt(keep.sum()))
    scale = target_sa / cur_sa
    nw, nh = max(1, round(img.width * scale)), max(1, round(img.height * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    canvas.paste(img, (int(round(256 - nw / 2.0)), 448 - nh), img)  # LCC bottom-centre -> pivot
    canvas.save(os.path.join(d, "hero_death_f08.png"))
    log.append(f"hero_death f08: candidate comp#{best} area={sizes[best-1]:.0f} "
               f"SA {cur_sa:.0f} -> {target_sa:.0f} (scale {scale:.3f}), mirrored head-left")


# ------------------------------------------------------------ B reprocess
def reprocess(clip, stem, actor, cols, rows, count, loop, canvas, pivot):
    spec = pf.ACTORS[actor]
    saved = dict(spec)
    spec["canvas"], spec["pivot"] = canvas, pivot
    try:
        frames = pf.process_sheet(stem, actor, clip, cols, rows, count, loop, log)
    finally:
        spec.update(saved)
    if frames is None:
        raise SystemExit(f"reprocess failed: {clip}")
    save_frames(clip, frames)
    raw = json.load(open(os.path.join(ART, "manifest_raw.json")))
    raw["clips"][clip]["canvas"] = list(canvas)
    raw["clips"][clip]["pivot"] = list(pivot)
    with open(os.path.join(ART, "manifest_raw.json"), "w") as f:
        json.dump(raw, f, indent=1)
    log.append(f"{clip}: canvas->{canvas} pivot->{pivot} (manifest_raw patched)")


# --------------------------------------------------------------- C cleanup
def clean_satellites(path, min_area=25):
    im = Image.open(path).convert("RGBA")
    arr = np.asarray(im).copy()
    mask = arr[..., 3] > THR
    lab, n = ndimage.label(mask)
    if n <= 1:
        return 0
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    removed = 0
    for li in range(1, n + 1):
        if li != main and sizes[li - 1] >= min_area:
            arr[..., 3][lab == li] = 0
            removed += 1
    if removed:
        Image.fromarray(arr.astype(np.uint8), "RGBA").save(path)
    return removed


def clean_outlines(path):
    """Remove source cell-border rectangles from boss recover frames: the
    hollow outline component plus its flat edge fragments (a scan after the
    first pass found 1-4 px thick line pieces up to 381 px long that the
    outline signature alone missed). Line rule: >=40 px in a <=4 px thick
    run >=40 px long — cannot match organic cape/cloth shapes."""
    im = Image.open(path).convert("RGBA")
    arr = np.asarray(im).copy()
    mask = arr[..., 3] > THR
    lab, n = ndimage.label(mask)
    removed = 0
    if n <= 1:
        return 0
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    for li in range(1, n + 1):
        if li == main:
            continue
        ys, xs = np.where(lab == li)
        bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        fill = len(xs) / (bw * bh)
        outline = bw >= 150 and bh >= 150 and fill < 0.06 and len(xs) > 300
        line = len(xs) >= 40 and ((bh <= 4 and bw >= 40) or (bw <= 4 and bh >= 40))
        if outline or line:
            arr[..., 3][lab == li] = 0
            removed += 1
    if removed:
        Image.fromarray(arr.astype(np.uint8), "RGBA").save(path)
    return removed


def repair_cleanup():
    jobs = []
    for clip, idxs in [("hero_death", [5, 6, 7]), ("hero_fall", [3]),
                       ("hero_hurt_recoil", [0]), ("hero_land", [3]),
                       ("pursuer_lunge", [0, 1])]:
        for i in idxs:
            jobs.append((os.path.join(FRAMES, clip, f"{clip}_f{i:02d}.png"), clean_satellites))
    for clip in ("boss_strike_recover", "boss_hazard_recover"):
        d = os.path.join(FRAMES, clip)
        for f in sorted(os.listdir(d)):
            if f.endswith(".png"):
                jobs.append((os.path.join(d, f), clean_outlines))
    for path, fn in jobs:
        r = fn(path)
        log.append(f"cleanup {os.path.relpath(path, FRAMES)}: removed {r} component(s)")


if __name__ == "__main__":
    repair_idle()
    repair_death_f08()
    reprocess("pursuer_alert", "pursuer_alert", "pursuer", 4, 1, 4, False,
              (320, 288), (128, 256))
    reprocess("pursuer_lunge_windup", "pursuer_lunge_windup", "pursuer", 4, 1, 4, False,
              (320, 288), (128, 256))
    reprocess("swooper_dive_telegraph", "swooper_dive_telegraph", "swooper", 4, 1, 4, False,
              (512, 320), (256, 160))
    # telegraph satellites (neighbour bleed) after reprocess
    d = os.path.join(FRAMES, "swooper_dive_telegraph")
    for f in sorted(os.listdir(d)):
        if f.endswith(".png"):
            r = clean_satellites(os.path.join(d, f))
            log.append(f"cleanup swooper_dive_telegraph/{f}: removed {r} component(s)")
    repair_cleanup()
    print("\n".join(log))
    print("REPAIR PASS DONE (frames only; run pack -> normalize -> pack next)")
