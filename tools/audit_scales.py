#!/usr/bin/env python3
"""Scale audit: measure alpha-bbox and largest-connected-component (LCC)
bbox height/width and pivot offsets for every frame of every clip in
game/art/frames/, per the runtime contract in art/clips.json.
Usage: audit_scales.py <output.md> <label>
Threshold alpha > 40 (matches process_frames.py placement convention).
The LCC is the actual figure; stray generation debris (thin lines, specks)
shows up as non-LCC components and is listed separately."""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/gothic-whip/game/art")
FRAMES = os.path.join(ROOT, "frames")
THR = 40

def measure(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)[..., 3]
    mask = a > THR
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    full = dict(w=int(xs.max()) + 1 - int(xs.min()), h=int(ys.max()) + 1 - int(ys.min()),
                x0=int(xs.min()), y0=int(ys.min()), x1=int(xs.max()) + 1, y1=int(ys.max()) + 1)
    lab, n = ndimage.label(mask)
    if n == 0:
        return dict(full=full, lcc=None, ncomp=0, canvas=list(im.size))
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    li = int(np.argmax(sizes)) + 1
    lys, lxs = np.where(lab == li)
    lcc = dict(w=int(lxs.max()) + 1 - int(lxs.min()), h=int(lys.max()) + 1 - int(lys.min()),
               x0=int(lxs.min()), y0=int(lys.min()), x1=int(lxs.max()) + 1, y1=int(lys.max()) + 1,
               area=int(sizes[li - 1]))
    return dict(full=full, lcc=lcc, ncomp=int(n), canvas=list(im.size))

def grip_stats(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)[..., 3]
    colmax = a.max(axis=0)
    xs = np.where(colmax > THR)[0]
    if len(xs) == 0:
        return None
    gx = int(xs.min())
    colmask = a[:, gx:gx + 14] > THR
    ys = np.where(colmask.any(axis=1))[0]
    gy = float(ys.mean()) if len(ys) else float("nan")
    return dict(grip_x=gx, grip_y=gy, tip_x=int(xs.max()) + 1)

def med(v):
    return float(np.median(np.array(v, dtype=np.float32)))

def main():
    out_path, label = sys.argv[1], sys.argv[2]
    clips_meta = json.load(open(os.path.join(ROOT, "clips.json")))
    lines = [f"# Scale audit — {label}", "",
             "Alpha threshold > 40. `h` = full alpha-bbox height; `lcc_h` = largest-connected-"
             "component (the figure) bbox height; `foot_off` = pivot.y − LCC bbox bottom "
             "(0 = figure's lowest point exactly on the pivot; negative = figure extends below "
             "pivot); `ncomp` = component count (>1 means detached debris/satellites present). "
             "Whip rows add grip/tip stats vs pivot.", ""]
    summary = []
    for clip in sorted(os.listdir(FRAMES)):
        d = os.path.join(FRAMES, clip)
        if not os.path.isdir(d):
            continue
        meta = clips_meta.get(clip, {})
        pivot = meta.get("pivot", [0, 0])
        actor = clip.split("_")[0]
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        rows = []
        for f in files:
            m = measure(os.path.join(d, f))
            g = grip_stats(os.path.join(d, f)) if clip.startswith("whip") else None
            rows.append((f, m, g))
        hs = [r[1]["full"]["h"] for r in rows if r[1]]
        ls = [r[1]["lcc"]["h"] for r in rows if r[1] and r[1]["lcc"]]
        if not hs:
            lines.append(f"## {clip}\n\nALL FRAMES EMPTY\n")
            continue
        summary.append((clip, actor, len(hs), min(hs), med(hs), max(hs),
                        min(ls), med(ls), max(ls)))
        lines.append(f"## {clip}  (actor={actor}, canvas={meta.get('canvas')}, pivot={pivot})")
        lines.append("")
        lines.append("| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for f, m, g in rows:
            if m is None:
                lines.append(f"| {f} | EMPTY | | | | | | | |")
                continue
            lcc = m["lcc"]
            foot = pivot[1] - lcc["y1"] if lcc else ""
            gx = str(g["grip_x"]) if g else ""
            gy = ("%.0f" % g["grip_y"]) if g else ""
            tip = str(g["tip_x"]) if g else ""
            lines.append(f"| {f} | {m['full']['h']} | {lcc['h'] if lcc else ''} | "
                         f"{lcc['w'] if lcc else ''} | {foot:+d} | {m['ncomp']} | "
                         f"{gx} | {gy} | {tip} |")
        lines.append(f"| **median** | **{med(hs):.0f}** | **{med(ls):.0f}** | | | | | | |")
        lines.append("")
    lines.insert(3, "## Summary (per clip)\n\n| clip | actor | n | full_h min/med/max | lcc_h min/med/max |\n|---|---|---|---|---|\n" +
                 "\n".join(f"| {c} | {a} | {n} | {lo}/{md:.0f}/{hi} | {llo}/{lmd:.0f}/{lhi} |"
                           for c, a, n, lo, md, hi, llo, lmd, lhi in summary) + "\n")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    for c, a, n, lo, md, hi, llo, lmd, lhi in summary:
        print(f"{c:28s} {a:10s} n={n:2d} full {lo:4d}/{md:5.0f}/{hi:4d}  lcc {llo:4d}/{lmd:5.0f}/{lhi:4d}")
    print("wrote", out_path)

if __name__ == "__main__":
    main()
