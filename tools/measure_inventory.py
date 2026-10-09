#!/usr/bin/env python3
"""Per-frame size inventory for Gothic Whip shipped frames.

Measures every frame of every clip in game/art/frames/: full alpha-bbox
H/W, largest-connected-component (LCC) H/W, alpha area (alpha>40 px),
and SQ = sqrt(LCC_H * LCC_W) — a pose-robust scale proxy (a pure scale
change moves H and W together; a pose change mostly swaps H for W).
Writes JSON (argv[1]) and prints a summary.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

FRAMES = os.path.expanduser("~/workspace/gothic-whip/game/art/frames")
THR = 40

def measure(path):
    a = np.asarray(Image.open(path).convert("RGBA"))[..., 3]
    mask = a > THR
    if not mask.any():
        return dict(bbox_h=0, bbox_w=0, h=0, w=0, area=0, sq=0.0, x0=0, y0=0, x1=0, y1=0, empty=True)
    ys, xs = np.where(mask)
    lab, n = ndimage.label(mask)
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    li = int(np.argmax(sizes)) + 1
    lys, lxs = np.where(lab == li)
    h = int(lys.max()) + 1 - int(lys.min()); w = int(lxs.max()) + 1 - int(lxs.min())
    return dict(bbox_h=int(ys.max()) + 1 - int(ys.min()), bbox_w=int(xs.max()) + 1 - int(xs.min()),
                h=h, w=w, area=int(mask.sum()), sq=round(float(np.sqrt(h * w)), 1),
                x0=int(lxs.min()), y0=int(lys.min()), x1=int(lxs.max()) + 1, y1=int(lys.max()) + 1)

def main():
    out = {}
    clips = sorted(d for d in os.listdir(FRAMES) if os.path.isdir(os.path.join(FRAMES, d)))
    for clip in clips:
        d = os.path.join(FRAMES, clip)
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        out[clip] = [dict(file=f, **measure(os.path.join(d, f))) for f in files]
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    for clip, frs in out.items():
        sqs = [f["sq"] for f in frs]
        hs = [f["h"] for f in frs]
        print(f"{clip:28s} n={len(frs):2d} SQ {min(sqs):6.1f}..{max(sqs):6.1f} "
              f"spread={100*(max(sqs)/max(1,min(sqs))-1):5.1f}%  H {min(hs)}..{max(hs)}")
    print("total clips:", len(out), "frames:", sum(len(v) for v in out.values()))

if __name__ == "__main__":
    main()
