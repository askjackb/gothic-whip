#!/usr/bin/env python3
"""Crouch-zoom + boss torso/part-scale repairs (2026-10-09, user playtest
round 5; see game/art/ART_INTEGRITY_AUDIT.md addendum).

DEFECT A (hero crouch): crouch_enter/exit figures were drawn at a smaller
body-part scale than the standing figure (head 31-33 px vs standing 38),
so entering crouch reads as a ~0.9x zoom-out and standing back up as a
zoom-in. Repairs are deterministic and keep the genuine generated poses:
- enter f00: pose is the standing stance itself, so it is re-derived from
  the repaired hero_idle f00 by a feet-anchored vertical squash to the
  frame's original height (211) - head width stays exactly 38.
- enter f01/f03: horizontal rescale about the feet centre pinning the
  head (top-12-rows ink) to 38; heights and feet untouched.
- crouch_idle frames whose head reads 36 (>5% under 38): uniform rescale
  about the foot pivot, then vertical re-anchor of the bbox to the 140 px
  crouch anchor (the task-prescribed two-step).
- crouch_exit := the repaired enter frames reversed (the shipped exit is
  already pixel-identical to the reversed enter; md5-verified).

DEFECT B (boss): boss_idle / boss_turn / boss_hazard_windup shipped as
helmet+pauldron+gauntlet+cape-cone with NO lower body below the waist at
the same 352 px anchor where boss_walk is a complete, smaller-parted
knight (the hero_idle torso disease in a second actor, missed because
the audit exempted "robe" actors from the truncation clause);
boss_strike_execute was drawn at 1.15-1.5x part scale (H 404-424, helmet
run 119-216 vs the trusted 63-69). The four clips are regenerated from
new sheets (image generation available again 2026-10-09) made with
boss_walk f00 as identity reference, chroma-extracted, and normalized to
the trusted helmet anchor (max ink run in rows 2-15% of the figure:
boss_walk clean median 67.5 px) / the 352 px height anchor, placed
bbox-centre -> pivot (176, 448) exactly like the shipped boss frames.
boss_death is anatomically coherent (slump -> collapse -> armour heap)
but drawn in the oversized robe-batch; it is uniformly rescaled by the
pauldron-width ratio to the walk family, ground-anchored.

Gameplay, timings, hitboxes, frame counts: untouched.
Run order: this script -> pack_atlases.py -> audit_integrity.py /
audit_sequences.py / engine + smoke tests.
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
HEAD_TARGET = 38.0
HELM_TARGET = 67.5          # boss_walk clean-frame median (rows 2-15% run)
BOSS_ANCHOR_H = 352
BOSS_PIVOT = (176, 448)
LOG = []


def lcc(im):
    a = np.asarray(im.convert("RGBA"))[..., 3]
    mask = a > THR
    lab, n = ndimage.label(mask)
    if n == 0:
        return None
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)


def bbox_of(mask):
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def content(im):
    m = lcc(im)
    x0, y0, x1, y1 = bbox_of(m)
    return im.convert("RGBA").crop((x0, y0, x1, y1)), (x0, y0, x1, y1)


def head_top12(im):
    """Parent-verified metric: max ink width in the top 12 rows of the LCC."""
    m = lcc(im)
    x0, y0, x1, y1 = bbox_of(m)
    rows = m[y0:y1, x0:x1].sum(axis=1)
    return int(rows[:12].max())


def foot_cx(im):
    """Mean ink column of the bottom 12 rows of the figure (feet centre)."""
    m = lcc(im)
    x0, y0, x1, y1 = bbox_of(m)
    bot = m[y1 - 12:y1, x0:x1]
    xs = np.where(bot.any(axis=0))[0]
    return x0 + float(xs.mean()) if len(xs) else (x0 + x1) / 2.0


def max_run(row):
    xs = np.where(row)[0]
    if len(xs) == 0:
        return 0
    splits = np.where(np.diff(xs) >= 6)[0]
    bounds = np.concatenate(([-1], splits, [len(xs) - 1]))
    return int(max(xs[bounds[i + 1]] - xs[bounds[i] + 1] + 1
                   for i in range(len(bounds) - 1)))


def band_run(im, lo, hi):
    """Max single ink run within rows [lo, hi) of the figure height."""
    m = lcc(im)
    x0, y0, x1, y1 = bbox_of(m)
    sub = m[y0:y1, x0:x1]
    h = sub.shape[0]
    return max(max_run(sub[y]) for y in range(max(0, int(h * lo)),
                                              max(1, int(h * hi))))


def helm_run(im):
    return band_run(im, 0.02, 0.15)


def blank():
    return Image.new("RGBA", (512, 512), (0, 0, 0, 0))


def pin_head_x(im, target=HEAD_TARGET, iters=4):
    """Horizontally rescale content about the feet centre until the
    top-12-rows head ink == target (within 0.5 px). Returns canvas image."""
    cur = im
    for _ in range(iters):
        h = head_top12(cur)
        if abs(h - target) <= 0.5:
            break
        c, (x0, y0, x1, y1) = content(cur)
        fcx = foot_cx(cur)
        fx = target / h
        nw = max(1, int(round(c.width * fx)))
        c2 = c.resize((nw, c.height), Image.LANCZOS)
        left = int(round(fcx - (fcx - x0) * fx))
        out = blank()
        out.paste(c2, (left, 448 - c.height), c2)
        cur = out
    return cur


# ---------------------------------------------------------------- hero A
def repair_hero():
    print("== hero crouch ==")
    idle0 = Image.open(os.path.join(FRAMES, "hero_idle", "hero_idle_f00.png"))
    enter_dir = os.path.join(FRAMES, "hero_crouch_enter")
    old = [Image.open(os.path.join(enter_dir, f"hero_crouch_enter_f{i:02d}.png"))
           for i in range(4)]
    before = [head_top12(f) for f in old]
    new = []
    # f00: re-derived from the repaired standing frame (feet-anchored squash
    # to the frame's original 211 px height; head width stays 38)
    c, (x0, y0, x1, y1) = content(idle0)
    c2 = c.resize((c.width, 211), Image.LANCZOS)
    f00 = blank(); f00.paste(c2, (x0, 448 - 211), c2)
    new.append(f00)
    # f01: genuine pose kept; head pinned horizontally (33 -> 38)
    new.append(pin_head_x(old[1]))
    # f02: head already 37 (within 5% of 38) - untouched
    new.append(old[2].copy())
    # f03: head 36 (>5% low) - pinned
    new.append(pin_head_x(old[3]))
    after = [head_top12(f) for f in new]
    for i, f in enumerate(new):
        f.save(os.path.join(enter_dir, f"hero_crouch_enter_f{i:02d}.png"))
    exit_dir = os.path.join(FRAMES, "hero_crouch_exit")
    for i in range(4):
        new[3 - i].save(os.path.join(exit_dir, f"hero_crouch_exit_f{i:02d}.png"))
    log.append(f"hero_crouch_enter head {before} -> {after}; "
               f"exit := repaired enter reversed")
    print(f"  enter heads {before} -> {after}")

    # crouch_idle: correct only frames >5% off (head <= 36), task's two-step:
    # uniform rescale about the foot pivot, then bbox re-anchored to 140.
    idle_dir = os.path.join(FRAMES, "hero_crouch_idle")
    cb, ca = [], []
    for i in range(6):
        p = os.path.join(idle_dir, f"hero_crouch_idle_f{i:02d}.png")
        f = Image.open(p)
        h0 = head_top12(f)
        cb.append(h0)
        if h0 <= 36:
            s = HEAD_TARGET / h0
            c, bb = content(f)
            fcx = foot_cx(f)
            c2 = c.resize((max(1, int(round(c.width * s))),
                           max(1, int(round(c.height * s)))), Image.LANCZOS)
            left = int(round(fcx - (fcx - bb[0]) * s))
            tmp = blank(); tmp.paste(c2, (left, 448 - c2.height), c2)
            # re-anchor bbox height to the 140 px crouch anchor (Y only)
            c3, bb3 = content(tmp)
            c4 = c3.resize((c3.width, 140), Image.LANCZOS)
            out = blank(); out.paste(c4, (bb3[0], 448 - 140), c4)
            out = pin_head_x(out)  # final exact head pin (Y untouched)
            out.save(p)
            f = out
        ca.append(head_top12(f))
    log.append(f"hero_crouch_idle head {cb} -> {ca} "
               f"(frames >5% low: uniform rescale, then bbox -> 140)")
    print(f"  crouch_idle heads {cb} -> {ca}")


# ---------------------------------------------------------------- boss B
SHEETS = {
    "boss_idle_regen": ("media-generation-boss-idle-gen-probe-0-"
                        "464eabdc-ec4f-40c2-904b-67cd3737f0de.webp", 4),
    "boss_turn_regen": ("media-generation-boss-turn-gen-0-"
                        "a6de5c97-69a9-46f3-9024-8f569f4fd465.webp", 4),
    "boss_hazard_windup_regen": ("media-generation-boss-hazard-windup-gen-0-"
                                 "6f05bb01-9565-455f-92c0-8f484d3aaa74.webp", 8),
    "boss_strike_execute_regen": ("media-generation-boss-strike-execute-gen-0-"
                                  "78879a33-be5f-44ca-bc99-2973c1ddbf76.webp", 4),
}


def extract_figures(sheet_path, expected):
    """Chroma-key a generated sheet and split it into per-pose figure
    images (RGBA, figure content only) ordered left -> right. Detached
    specks/sparkles are dropped: only components clustered with a body
    (centroid stride) survive; hand-touching magic wisps on the windup
    sheet are part of the cast pose and are kept (documented)."""
    rgba_f, _ = pf.chroma_key(Image.open(sheet_path).convert("RGB"))
    rgba = np.clip(rgba_f, 0, 255).astype(np.uint8)
    mask = rgba[..., 3] > THR
    lab, n = ndimage.label(mask)
    comps = []
    for li in range(1, n + 1):
        ys, xs = np.where(lab == li)
        if len(ys) < 300:                      # specks / sparkle dots
            continue
        comps.append((li, (int(xs.min()), int(ys.min()),
                           int(xs.max()) + 1, int(ys.max()) + 1),
                      len(ys), float(xs.mean())))
    # bodies = the `expected` largest components; every other kept
    # component (cape tips, hand-touching magic wisps) attaches to the
    # body whose 40 px-expanded bbox it intersects most.
    # comps tuples: (label, bbox, area, centroid_x)
    bodies = sorted(comps, key=lambda t: -t[2])[:expected]
    assert len(bodies) == expected and bodies[-1][2] >= 20000, \
        f"{sheet_path}: expected {expected} bodies, got {len(bodies)}"
    body_ids = {li for li, _, _, _ in bodies}
    clusters = [[(li, bb)] for li, bb, _, _ in
                sorted(bodies, key=lambda t: t[3])]
    for li, bb, area, cx in comps:
        if li in body_ids:
            continue
        best, best_ov = None, 0
        for cl in clusters:
            bx0 = min(b[0] for _, b in cl) - 40
            by0 = min(b[1] for _, b in cl) - 40
            bx1 = max(b[2] for _, b in cl) + 40
            by1 = max(b[3] for _, b in cl) + 40
            ov = (max(0, min(bb[2], bx1) - max(bb[0], bx0)) *
                  max(0, min(bb[3], by1) - max(bb[1], by0)))
            if ov > best_ov:
                best, best_ov = cl, ov
        if best is not None:
            best.append((li, bb))
    assert len(clusters) == expected
    pose_imgs = []
    for cl in clusters:
        keep = {li for li, _ in cl}
        sel = np.isin(lab, list(keep))
        ys, xs = np.where(sel)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        crop = rgba[y0:y1, x0:x1].copy()
        crop[~sel[y0:y1, x0:x1]] = 0
        pose_imgs.append(Image.fromarray(crop))
    return pose_imgs


def place_boss(pose, s):
    c = pose.resize((max(1, int(round(pose.width * s))),
                     max(1, int(round(pose.height * s)))), Image.LANCZOS)
    out = blank()
    out.paste(c, (BOSS_PIVOT[0] - c.width // 2, BOSS_PIVOT[1] - c.height), c)
    return out


def fit_factor(pose, s):
    """Cap the scale so the figure fits the 512 canvas (6 px margins)."""
    s = min(s, 500.0 / pose.width, 470.0 / pose.height)
    return s


def save_clip(clip, frames):
    d = os.path.join(FRAMES, clip)
    for i, f in enumerate(frames):
        f.save(os.path.join(d, f"{clip}_f{i:02d}.png"))
    print(f"  {clip}: wrote {len(frames)} frames")


def repair_boss_clip(clip, sheet_key, mode, sequence):
    src_name, expected = SHEETS[sheet_key]
    poses = extract_figures(os.path.join(SRC, src_name), expected)
    report = []
    scaled = []
    ref_s = BOSS_ANCHOR_H / poses[0].height
    for p in poses:
        hr = helm_run(p)
        if mode == "height":        # upright poses: each to the 352 anchor
            s = BOSS_ANCHOR_H / p.height
        else:  # "clip": one sheet = one drawing scale; anchor pose 0 to
            # 352 and keep the sheet's internal proportions for bent poses
            s = ref_s
        s = fit_factor(p, s)
        scaled.append(place_boss(p, s))
        c, bb = content(scaled[-1])
        report.append((hr, c.height, helm_run(scaled[-1])))
    frames = [scaled[i] for i in sequence]
    save_clip(clip, frames)
    log.append(f"{clip}: regenerated from {sheet_key} "
               f"(helm_run/target {HELM_TARGET}); per-pose "
               f"(helm, ->H, ->helm) = {report}")
    for r in report:
        print(f"    pose helm={r[0]} -> H {r[1]}, helm {r[2]}")


def repair_boss():
    print("== boss ==")
    # archive the generated sheets under stable provenance names
    for name, (fn, _) in SHEETS.items():
        dst = os.path.join(SRC, f"{name}.png")
        if not os.path.exists(dst):
            Image.open(os.path.join(SRC, fn)).convert("RGB").save(dst)
    repair_boss_clip("boss_idle", "boss_idle_regen", "height",
                     [0, 1, 2, 3, 3, 2, 1, 0])          # ping-pong sway loop
    repair_boss_clip("boss_turn", "boss_turn_regen", "height", [0, 1, 2, 3])
    repair_boss_clip("boss_hazard_windup", "boss_hazard_windup_regen",
                     "height", [0, 1, 2, 3, 4, 5, 6, 7])
    repair_boss_clip("boss_strike_execute", "boss_strike_execute_regen",
                     "clip", [0, 1, 2, 3])
    # boss_death: coherent collapse, oversized batch -> uniform rescale by
    # the pauldron-width ratio to the walk family, ground-anchored
    walk_p = np.median([band_run(Image.open(os.path.join(
        FRAMES, "boss_walk", f"boss_walk_f{i:02d}.png")), 0.15, 0.30)
        for i in range(4)])
    death_dir = os.path.join(FRAMES, "boss_death")
    d0 = Image.open(os.path.join(death_dir, "boss_death_f00.png"))
    s = float(min(1.0, max(0.80, walk_p / band_run(d0, 0.15, 0.30))))
    for i in range(12):
        p = os.path.join(death_dir, f"boss_death_f{i:02d}.png")
        f = Image.open(p)
        c, bb = content(f)
        c2 = c.resize((max(1, int(round(c.width * s))),
                       max(1, int(round(c.height * s)))), Image.LANCZOS)
        cx = (bb[0] + bb[2]) // 2
        out = blank()
        out.paste(c2, (cx - c2.width // 2, 448 - c2.height), c2)
        out.save(p)
    log.append(f"boss_death: uniform rescale x{s:.3f} "
               f"(pauldron walk median {walk_p:.0f} vs death f00 "
               f"{band_run(d0, 0.15, 0.30):.0f}); collapse poses unchanged")
    print(f"  boss_death rescale x{s:.3f}")


def main():
    repair_hero()
    repair_boss()
    mp = os.path.join(ART, "manifest_raw.json")
    man = json.load(open(mp))
    man.setdefault("notes", []).append(
        "2026-10-09 round-5 crouch/boss repair (tools/repair_crouch_boss.py): "
        "hero_crouch_enter/exit re-pinned to the 38 px standing head (f00 "
        "re-derived from the repaired hero_idle f00 by feet-anchored squash; "
        "f01/f03 horizontal head-pin); hero_crouch_idle frames at head 36 "
        "uniformly rescaled then bbox-re-anchored to 140. boss_idle, "
        "boss_turn, boss_hazard_windup (7 generated poses + peak-hold "
        "frame), boss_strike_execute regenerated from sheets in art/source "
        "(boss_*_regen.png; identity reference boss_walk f00), chroma-"
        "extracted and normalized to the 352 px / 67.5 px helmet anchors. "
        "The windup sheet has 8 poses (the 7th/8th carry generated magic "
        "wisps at the hands - kept as cast art, detached specks dropped). "
        "boss_death uniformly rescaled to walk-family part scale. Pre-"
        "repair frames: art/source/frames_prefix_2026-10-09_crouchboss.zip.")
    with open(mp, "w") as fh:
        json.dump(man, fh, indent=1)
    print("\nREPAIR LOG:")
    for line in log:
        print(" -", line)


if __name__ == "__main__":
    main()
