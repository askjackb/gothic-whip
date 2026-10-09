#!/usr/bin/env python3
"""Per-frame scale-drift normalization for Gothic Whip shipped frames (2026-10-09, fix #3).

Background: the per-clip uniform scale fix (process_frames.py SCALE_SPEC)
anchored each clip's reference statistic to the actor design height, but
frames WITHIN a clip were generated at mutually inconsistent sizes, so the
hero still changed size between standing and acting (user playtest round 3).

Method (documented in game/ACTION_SIZE_AUDIT.md):
- SQ = sqrt(H*W) is REPORTED but not used for correction: for narrow
  side-profile standing frames SQ collapses (~134 vs 204 for the same man
  standing) and SQ-driven scaling would blow a standing recovery frame
  250 px tall up to ~295 px. SQ is unreliable exactly where pose swaps
  height for width.
- H (LCC height) corrects STANDING-CLASS frames of feet-anchored bipeds
  (hero/boss): an upright figure's perceived size IS its height. Standing
  class = H/design in [0.92, 1.25] and W/H <= 1.05.
- SA = sqrt(alpha area) corrects everything else (poses, transitions,
  quadruped pursuer, canvas-clipped ranged, flying swooper): under a pure
  scale change SA scales exactly linearly, while pose changes mostly
  redistribute the same ink (hero_land SA spread 4.9% across a 169..260 px
  height swing; hero SQ spread there is 16.5%).
Factors clamp to [0.85, 1.18] (frames needing more are logged as outliers).
Rescale is around the contract foot pivot (LCC bottom-centre -> pivot for
feet actors, LCC centre -> pivot for swooper). Whip, VFX and projectile
frames are EXEMPT (whip geometry is contract-locked by the in-hand fix).
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ART = os.path.expanduser("~/workspace/gothic-whip/game/art")
FRAMES = os.path.join(ART, "frames")
THR = 40
CLAMP = (0.85, 1.18)
DESIGN = {"hero": 224.0, "boss": 352.0, "pursuer": 112.0, "ranged": 300.0, "swooper": 170.0}
CROUCH_DESIGN = 140.0
CROUCH_CLIPS = {"hero_crouch_enter", "hero_crouch_exit", "hero_crouch_idle", "hero_attack_crouch"}
SA_ONLY_ACTORS = {"pursuer", "ranged", "swooper"}
SA_ONLY_CLIPS = {"hero_knockdown", "hero_get_up", "hero_death", "hero_fall",
                 "boss_death"} | CROUCH_CLIPS
EXEMPT_PREFIX = ("whip_", "vfx_")
EXEMPT_CLIPS = {"projectile_grave_shot"}
ACTOR_OF = {}
for clip in json.load(open(os.path.join(ART, "clips.json"))):
    ACTOR_OF[clip] = clip.split("_")[0] if not clip.startswith("projectile") else "projectile"
ALIGN = {"hero": "feet", "boss": "feet", "pursuer": "feet", "ranged": "feet", "swooper": "center"}


def measure(a):
    mask = a > THR
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    lab, n = ndimage.label(mask)
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    li = int(np.argmax(sizes)) + 1
    lys, lxs = np.where(lab == li)
    return dict(bbox=(int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1),
                lcc=(int(lxs.min()), int(lys.min()), int(lxs.max()) + 1, int(lys.max()) + 1),
                area=int(mask.sum()))


def frame_stats(im):
    m = measure(np.asarray(im)[..., 3])
    if m is None:
        return None
    lx0, ly0, lx1, ly1 = m["lcc"]
    h, w = ly1 - ly0, lx1 - lx0
    m["h"], m["w"] = h, w
    m["sa"] = float(np.sqrt(m["area"]))
    m["sq"] = float(np.sqrt(h * w))
    return m


def main():
    dry = "--dry-run" in sys.argv
    meta = json.load(open(os.path.join(ART, "clips.json")))
    log = []
    outliers = []
    changed = skipped = exempt = 0
    for clip in sorted(os.listdir(FRAMES)):
        d = os.path.join(FRAMES, clip)
        if not os.path.isdir(d):
            continue
        if clip.startswith(EXEMPT_PREFIX) or clip in EXEMPT_CLIPS:
            exempt += len([f for f in os.listdir(d) if f.endswith(".png")])
            continue
        actor = ACTOR_OF[clip]
        design = CROUCH_DESIGN if clip in CROUCH_CLIPS else DESIGN[actor]
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        ims = [Image.open(os.path.join(d, f)).convert("RGBA") for f in files]
        stats = [frame_stats(im) for im in ims]
        sas = sorted(s["sa"] for s in stats if s)
        med_sa = sas[len(sas) // 2]
        pw, ph = meta[clip]["canvas"]
        px, py = meta[clip]["pivot"]
        for i, (f, im, s) in enumerate(zip(files, ims, stats)):
            if s is None:
                continue
            standing = (actor not in SA_ONLY_ACTORS and clip not in SA_ONLY_CLIPS
                        and 0.92 <= s["h"] / design <= 1.25 and s["w"] / max(1, s["h"]) <= 1.05)
            # overhead guard: a frame >12% over design height whose ink (SA)
            # already matches the clip median is a pose redistribution
            # (e.g. boss weapon raised overhead), not a bigger drawing
            if standing and s["h"] / design > 1.12 and abs(s["sa"] / med_sa - 1.0) <= 0.03:
                standing = False
            raw = design / s["h"] if standing else med_sa / s["sa"]
            fac = float(np.clip(raw, *CLAMP))
            rule = "H" if standing else "SA"
            if abs(raw - fac) > 1e-9:
                outliers.append(f"{clip} f{i} rule={rule} raw_factor={raw:.3f} clamped={fac:.3f} "
                                f"H={s['h']} W={s['w']} SA={s['sa']:.0f}")
            log.append(f"{clip} f{i} rule={rule} factor={fac:.3f} (raw {raw:.3f}) H={s['h']} SA={s['sa']:.0f}")
            if abs(fac - 1.0) < 0.004:
                skipped += 1
                continue
            changed += 1
            if dry:
                continue
            x0, y0, x1, y1 = s["bbox"]
            lx0, ly0, lx1, ly1 = s["lcc"]
            crop = im.crop((x0, y0, x1, y1))
            crop = crop.resize((max(1, round(crop.width * fac)), max(1, round(crop.height * fac))),
                               Image.LANCZOS)
            out = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
            if ALIGN[actor] == "feet":
                dx = int(round(px - ((lx0 + lx1) / 2.0 - x0) * fac))
                dy = int(round(py - (ly1 - y0) * fac))
            else:
                dx = int(round(px - ((lx0 + lx1) / 2.0 - x0) * fac))
                dy = int(round(py - ((ly0 + ly1) / 2.0 - y0) * fac))
            out.paste(crop, (dx, dy), crop)
            out.save(os.path.join(d, f))
    print(f"frames changed={changed} skipped(|f-1|<0.004)={skipped} exempt={exempt}")
    print(f"outliers needing factor outside {CLAMP}: {len(outliers)}")
    for o in outliers:
        print("  OUTLIER", o)
    with open("/tmp/normalize_log.txt", "w") as fh:
        fh.write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
