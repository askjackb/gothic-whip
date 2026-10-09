#!/usr/bin/env python3
"""Art-integrity (completeness) audit for Gothic Whip shipped frames.

WHY THIS EXISTS (2026-10-09, user playtest round 4): hero_idle shipped as a
WAIST-UP TORSO (head/belt/hands only — no coat, legs or boots) whose
head-to-belt span is 224 px, so every bbox/area scale audit stamped it
"correct size". The source sheet itself was generated waist-up; three
extent-based audits (SCALE_AUDIT, SEQUENCE_AUDIT, ACTION_SIZE_AUDIT) could
not see it because they compared bounding boxes, never anatomy.

This tool measures ANATOMY on the frames as shipped, and renders a
native-res contact strip per clip for the mandatory visual pass (visual
inspection is the primary evidence; this gate is the tripwire).

Metrics per frame (LCC = largest connected component of alpha > 40):
- H, W, SA=sqrt(alpha area): figure extents (context, scale-audit inputs).
- tracked_head: width of the ink run tracked from the topmost pixel
  through the top 12% of the figure (x-overlap chain). For the hero this
  is head+ponytail. Calibrated on trusted full-body frames (hero_walk:
  38-42 px). The waist-up idle reads 62-73 px — a head drawn ~65% too
  big, invisible to any height/area check.
- multi: fraction of top-band rows whose ink splits into >= 2 runs
  separated by >= 6 px (a raised arm / whip coil occupying the band).
- boot_ratio: mean ink-run width over the bottom 8% of rows / widest row.
  Real standing figures taper to boots/feet (hero good frames <= 0.46);
  a figure sliced at the waist keeps hip width to its last row (idle:
  0.71-0.86).
- leg_dip: min ink-run width within rows 55-94% / widest row. A sliced
  figure has no narrowing anywhere in its lower half (idle: 0.59-0.77;
  good hero frames <= 0.51).

GATE (exit nonzero on any DEFECT):
1. Empty frame anywhere -> DEFECT.
2. Truncation (actors whose design has legs/boots: hero, pursuer):
   standing-class frame with boot_ratio > 0.60 AND leg_dip > 0.50
   (no lower-body structure) -> DEFECT.
3. Head scale (hero only — the only actor with a calibrated head proxy;
   the boss's topmost feature is a 3 px horn tip and the ranged cultist's
   hood changes silhouette by pose, so their head check is the visual
   pass, documented in ART_INTEGRITY_AUDIT.md): frames of the looping
   ground-state clips hero_idle / hero_walk whose tracked_head deviates
   > 12% from the trusted hero_walk median. A sheet-level generation
   error (the defect class being gated: a whole sheet drawn at the wrong
   body-part scale) deviates on EVERY frame, so frames are DEFECTs when
   a majority of their clip's gated frames deviate; an isolated frame
   (e.g. one gait frame's ponytail swing, +15%) is a FLAG for visual
   adjudication instead — single-frame hair dynamics are a known proxy
   limit, and the visual pass decides.
Robe/cape actors (ranged, boss) are exempt from check 2 by anatomy (a
robe legitimately reaches the ground at full width; a slice there is
indistinguishable from a robe by silhouette metrics alone) — they are
covered by check 3's visual equivalent: every frame is eyeballed in the
strips, and their H/SA remain scale-audited elsewhere.

Nothing is modified. Usage:
  python3 tools/audit_integrity.py [--frames-root DIR] [--strips DIR]
                                   [--json PATH] [--no-strips]
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/gothic-whip/game")
ART = os.path.join(ROOT, "art")
THR = 40
HEAD_BAND = 0.12
BOTTOM_BAND = 0.08
HEAD_DEV_MAX = 0.12
BOOT_RATIO_MAX = 0.60
LEG_DIP_MAX = 0.50

# standing-class clips per actor (gate clause 2 + reporting)
STANDING = {
    "hero": {"hero_idle", "hero_walk", "hero_start_move", "hero_stop_move",
             "hero_turn", "hero_land", "hero_attack_ground", "hero_hurt_recoil"},
    "pursuer": {"pursuer_idle", "pursuer_patrol_walk", "pursuer_approach_walk",
                "pursuer_recovery", "pursuer_hurt"},
    "ranged": {"ranged_idle", "ranged_aim", "ranged_fire", "ranged_recover",
               "ranged_hurt"},
    "boss": {"boss_idle", "boss_walk", "boss_turn", "boss_hurt",
             "boss_strike_recover", "boss_hazard_recover"},
}
LEGS_ACTORS = {"hero", "pursuer"}          # clause 2 applies (legs/boots)
HEAD_GATE_CLIPS = {"hero": {"hero_idle", "hero_walk"}}
HEAD_REF_CLIP = {"hero": "hero_walk"}      # trusted full-body reference


def actor_of(clip):
    return clip.split("_")[0] if not clip.startswith("projectile") else "projectile"


def measure(alpha):
    mask = alpha > THR
    if not mask.any():
        return None
    lab, n = ndimage.label(mask)
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    li = int(np.argmax(sizes)) + 1
    lcc = lab == li
    ys, xs = np.where(lcc)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1
    sub = lcc[y0:y1, x0:x1]
    h, w = sub.shape
    rows = sub.sum(axis=1).astype(np.float32)
    maxrow = float(rows.max())
    hb = max(1, int(round(h * HEAD_BAND)))
    bb = max(1, int(round(h * BOTTOM_BAND)))
    # tracked head run (x-overlap chain from the topmost ink pixel)
    txs = np.where(sub[0])[0]
    tracked = 0
    if len(txs):
        lo, hi = int(txs.min()), int(txs.max())
        tracked = hi - lo + 1
        for y in range(1, hb):
            xs_r = np.where(sub[y])[0]
            if len(xs_r) == 0:
                break
            segs = []
            s = p = int(xs_r[0])
            for x in xs_r[1:]:
                x = int(x)
                if x - p > 3:
                    segs.append((s, p)); s = x
                p = x
            segs.append((s, p))
            hit = [sg for sg in segs if sg[0] <= hi + 2 and sg[1] >= lo - 2]
            if not hit:
                break
            lo = min(sg[0] for sg in hit); hi = max(sg[1] for sg in hit)
            tracked = max(tracked, hi - lo + 1)
    # band purity: rows with >=2 runs separated by >=6 px
    multi = 0
    for y in range(hb):
        xs_r = np.where(sub[y])[0]
        if len(xs_r) and (np.diff(xs_r) >= 6).any():
            multi += 1
    boot_ratio = float(rows[-bb:].mean() / maxrow) if maxrow else 0.0
    dip_zone = rows[int(0.55 * h):max(int(0.55 * h) + 1, int(0.94 * h))]
    leg_dip = float(dip_zone.min() / maxrow) if len(dip_zone) and maxrow else 0.0
    return dict(lcc=(x0, y0, x1, y1), h=int(h), w=int(w),
                area=int(lcc.sum()), sa=float(np.sqrt(lcc.sum())),
                head_w=float(rows[:hb].max()), tracked_head=int(tracked),
                multi=multi / hb, boot_ratio=boot_ratio, leg_dip=leg_dip,
                top_band_ink=bool(rows[:bb].max() > 0),
                bottom_band_ink=bool(rows[-bb:].max() > 0))


def strip_png(clip, files, frames_root, out_dir, pivot, canvas):
    ims = [Image.open(os.path.join(frames_root, clip, f)).convert("RGBA") for f in files]
    cw, ch = canvas
    cols = min(4, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cw, rows * ch), (22, 22, 30, 255))
    px, py = pivot
    for i, im in enumerate(ims):
        tile = Image.new("RGBA", (cw, ch), (22, 22, 30, 255))
        tile.alpha_composite(im)
        dr = ImageDraw.Draw(tile)
        dr.line([(px, 0), (px, ch)], fill=(255, 60, 60, 160), width=1)
        dr.line([(0, py), (cw, py)], fill=(255, 60, 60, 160), width=1)
        dr.rectangle([0, 0, 64, 15], fill=(0, 0, 0, 255))
        dr.text((3, 3), f"f{i:02d}", fill=(255, 255, 0, 255))
        sheet.paste(tile, ((i % cols) * cw, (i // cols) * ch))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{clip}.png")
    sheet.save(out)
    return out


def main():
    args = sys.argv[1:]
    frames_root = os.path.join(ART, "frames")
    strips_dir = os.path.join(ROOT, "tests", "shots", "integrity")
    json_path = "/tmp/integrity_audit.json"
    make_strips = True
    i = 0
    while i < len(args):
        if args[i] == "--frames-root":
            frames_root = args[i + 1]; i += 2
        elif args[i] == "--strips":
            strips_dir = args[i + 1]; i += 2
        elif args[i] == "--json":
            json_path = args[i + 1]; i += 2
        elif args[i] == "--no-strips":
            make_strips = False; i += 1
        else:
            i += 1

    meta = json.load(open(os.path.join(ART, "clips.json")))
    results = {}
    for clip in sorted(meta):
        d = os.path.join(frames_root, clip)
        if not os.path.isdir(d):
            continue
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        frames = []
        for fi, f in enumerate(files):
            a = np.asarray(Image.open(os.path.join(d, f)).convert("RGBA"))[..., 3]
            m = measure(a)
            if m is None:
                frames.append(dict(frame=fi, empty=True))
                continue
            m["frame"] = fi
            frames.append(m)
        results[clip] = frames
        if make_strips:
            strip_png(clip, files, frames_root, strips_dir,
                      meta[clip]["pivot"], meta[clip]["canvas"])

    # trusted head reference per actor (full-body reference clip median)
    head_ref = {}
    for actor, ref_clip in HEAD_REF_CLIP.items():
        vals = [f["tracked_head"] for f in results.get(ref_clip, []) if not f.get("empty")]
        if vals:
            head_ref[actor] = float(np.median(vals))

    # head-gate pre-pass: per gated clip, does a majority of frames deviate?
    head_majority = {}
    for clip in sorted(results):
        actor = actor_of(clip)
        if clip in HEAD_GATE_CLIPS.get(actor, set()) and actor in head_ref:
            ref = head_ref[actor]
            devs = [abs((f["tracked_head"] - ref) / ref)
                    for f in results[clip] if not f.get("empty")]
            over = sum(1 for dv in devs if dv > HEAD_DEV_MAX)
            head_majority[clip] = bool(devs) and over > len(devs) / 2

    defects = []
    flags = []
    print(f"{'clip':26} {'f':>2} {'H':>4} {'W':>4} {'trkH':>5} {'multi':>5} "
          f"{'bootR':>6} {'dip':>5}  verdict")
    for clip in sorted(results):
        actor = actor_of(clip)
        standing = clip in STANDING.get(actor, set())
        for f in results[clip]:
            if f.get("empty"):
                print(f"{clip:26} {f['frame']:>2}  EMPTY FRAME")
                defects.append(f"{clip} f{f['frame']}: EMPTY")
                continue
            verdict = "ok"
            if standing and actor in LEGS_ACTORS:
                if f["boot_ratio"] > BOOT_RATIO_MAX and f["leg_dip"] > LEG_DIP_MAX:
                    verdict = (f"DEFECT truncation: boot_ratio {f['boot_ratio']:.2f} "
                               f"> {BOOT_RATIO_MAX} and leg_dip {f['leg_dip']:.2f} "
                               f"> {LEG_DIP_MAX} (no lower-body structure)")
                    defects.append(f"{clip} f{f['frame']}: " + verdict)
            if (clip in HEAD_GATE_CLIPS.get(actor, set()) and actor in head_ref):
                ref = head_ref[actor]
                dev = (f["tracked_head"] - ref) / ref
                f["head_dev"] = dev
                if abs(dev) > HEAD_DEV_MAX and verdict == "ok":
                    if head_majority.get(clip):
                        verdict = (f"DEFECT head-scale: tracked_head {f['tracked_head']} "
                                   f"vs trusted {actor} median {ref:.0f} ({dev:+.0%})")
                        defects.append(f"{clip} f{f['frame']}: " + verdict)
                    else:
                        verdict = (f"FLAG head-dev {dev:+.0%} (isolated frame; "
                                   f"visual adjudication)")
                        flags.append(f"{clip} f{f['frame']}: " + verdict)
            tag = " [standing]" if standing else ""
            if verdict != "ok" or standing:
                print(f"{clip:26} {f['frame']:>2} {f['h']:>4} {f['w']:>4} "
                      f"{f['tracked_head']:>5} {f['multi']:>5.2f} "
                      f"{f['boot_ratio']:>6.2f} {f['leg_dip']:>5.2f}  {verdict}{tag}")
    print(f"\ntrusted head references: " +
          ", ".join(f"{a}={v:.0f}px ({HEAD_REF_CLIP[a]})" for a, v in sorted(head_ref.items())))
    print(f"INTEGRITY DEFECTS: {len(defects)}")
    for d in defects:
        print("  DEFECT", d)
    print(f"FLAGS (visual adjudication): {len(flags)}")
    for fl in flags:
        print("  FLAG", fl)
    with open(json_path, "w") as fh:
        json.dump({"head_ref": head_ref, "defects": defects, "flags": flags,
                   "clips": results}, fh, indent=1)
    return 1 if defects else 0


if __name__ == "__main__":
    sys.exit(main())
