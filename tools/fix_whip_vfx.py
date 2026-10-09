#!/usr/bin/env python3
"""Fix user-reported whip pose-progression + VFX envelope bugs (2026-10-09).

BUG 1: whip clips snapped between unrelated pose families (dead-straight
rod crack frame, crouch starting extended, air alternating families).
Fix: re-render all 3 whip clips (8 frames each) as one continuous motion
per clip - coiled wind-up -> unfurling -> extending arc -> CURVED crack ->
follow-through -> recoil -> coil rest. The braid is rendered as a ribbon
along designed Catmull-Rom paths, textured with cross-section slices of
the original crack frame's braid, so the painted brown-braid look, the
handle plate and the grip point are byte-identical anchors across frames.

BUG 2: VFX envelopes popped (impact instant-full + held + slivers; enemy
defeat full-size from frame 0; checkpoint width dip; eruption tail
re-widening; telegraph art floating at canvas top instead of the ground).
Fix: procedural scale/alpha envelopes about each clip's gameplay anchor,
plus a within-canvas placement repair for the telegraph.

This tool only rewrites PNGs under game/art/frames/. It never touches
durations, canvases, pivots or gameplay code. Originals are archived in
game/art/source/frames_prefix_2026-10-09.zip before this runs.
"""
import json, math, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.expanduser("~/workspace/gothic-whip/game")
FRAMES = os.path.join(ROOT, "art", "frames")
ASSETS = "/tmp/whip_assets"
os.makedirs(ASSETS, exist_ok=True)
CANVAS = (768, 512)
THR = 30

# ---------------------------------------------------------------- metrics
def metrics(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > THR)
    if len(xs) == 0:
        return {"empty": True}
    gx = int(xs.min())
    band = a[:, gx:gx + 14]
    rows = np.where((band > THR).any(axis=1))[0]
    gy = float(rows.mean()) if len(rows) else None
    return {"L": gx, "T": int(ys.min()), "R": int(xs.max()) + 1,
            "B": int(ys.max()) + 1, "w": int(xs.max()) + 1 - gx,
            "h": int(ys.max()) + 1 - int(ys.min()),
            "gy": round(gy, 1) if gy is not None else None,
            "cx": round((xs.min() + xs.max() + 1) / 2.0, 1),
            "cy": round((ys.min() + ys.max() + 1) / 2.0, 1)}

def table(clip, stage):
    d = os.path.join(FRAMES, clip)
    rows = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".png"):
            m = metrics(os.path.join(d, f))
            rows.append((f[-7:-4], m))
    print(f"[{stage}] {clip}")
    for name, m in rows:
        if m.get("empty"):
            print(f"  {name}: EMPTY")
        else:
            print(f"  {name}: L={m['L']} T={m['T']} R={m['R']} B={m['B']} "
                  f"w={m['w']} h={m['h']} gy={m['gy']} c=({m['cx']},{m['cy']})")
    return rows

# ------------------------------------------------------- whip asset build
def extract_assets():
    """Handle plates (per clip, from its crack frame f03, x<=344) and the
    braid cross-section bank (from ground f03, the straight run)."""
    plates = {}
    for clip in ["whip_attack_ground", "whip_attack_air", "whip_attack_crouch"]:
        src = Image.open(os.path.join(
            FRAMES, clip, f"{clip}_f03.png")).convert("RGBA")
        arr = np.array(src)
        plate = np.zeros_like(arr)
        plate[:, :345] = arr[:, :345]
        # keep only alpha-bearing pixels (already transparent elsewhere)
        pim = Image.fromarray(plate)
        pim.save(os.path.join(ASSETS, f"plate_{clip}.png"))
        plates[clip] = pim
    # braid bank from ground f03
    src = Image.open(os.path.join(
        FRAMES, "whip_attack_ground",
        "whip_attack_ground_f03.png")).convert("RGBA")
    a = np.asarray(src)[..., 3]
    bank = []  # (src_x, patch_img, thickness)
    for x in range(360, 613, 3):
        col = a[:, x - 3:x + 4]
        rows = np.where((col > THR).any(axis=1))[0]
        if len(rows) == 0:
            continue
        y0, y1 = rows.min() - 2, rows.max() + 3
        patch = src.crop((x - 3, y0, x + 4, y1))
        bank.append((x, patch, y1 - y0))
    with open(os.path.join(ASSETS, "bank.json"), "w") as f:
        json.dump([b[0] for b in bank], f)
    for i, (x, patch, th) in enumerate(bank):
        patch.save(os.path.join(ASSETS, f"bank_{i:03d}.png"))
    print(f"assets: plates={list(plates)} bank_slices={len(bank)} "
          f"thickness {bank[0][2]}->{bank[-1][2]}")
    return plates, bank

def load_assets():
    plates = {}
    for clip in ["whip_attack_ground", "whip_attack_air", "whip_attack_crouch"]:
        plates[clip] = Image.open(os.path.join(ASSETS, f"plate_{clip}.png"))
    xs = json.load(open(os.path.join(ASSETS, "bank.json")))
    bank = []
    for i, x in enumerate(xs):
        patch = Image.open(os.path.join(ASSETS, f"bank_{i:03d}.png"))
        bank.append((x, patch, patch.height))
    return plates, bank

# ------------------------------------------------------------ ribbon math
def catmull_rom(pts, closed=False):
    p = list(pts)
    if not closed:
        p = [p[0]] + p + [p[-1]]
    out = []
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = p[i], p[i + 1], p[i + 2], p[i + 3]
        for t in np.linspace(0, 1, 24, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append((
                0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    out.append(tuple(pts[-1]))
    return out

def spiral_pts(S, C, r0, r1, turns, entry_pull=0.55):
    """Lead from S into an inward-winding spiral centred C."""
    a0 = math.atan2(S[1] - C[1], S[0] - C[0])
    E = (C[0] + r0 * math.cos(a0), C[1] + r0 * math.sin(a0))
    pts = [S]
    for k in (0.25, 0.5, 0.75):
        # quadratic lead: S -> E bowing away from centre
        mx = S[0] + (E[0] - S[0]) * k
        my = S[1] + (E[1] - S[1]) * k - 14 * math.sin(k * math.pi)
        pts.append((mx, my))
    steps = int(turns * 40)
    for i in range(steps + 1):
        u = i / steps
        ang = a0 + u * turns * 2 * math.pi
        r = r0 + (r1 - r0) * u
        pts.append((C[0] + r * math.cos(ang), C[1] + r * math.sin(ang)))
    return pts

def resample(pts, step=2.0):
    pts = np.array(pts, dtype=float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    L = seg.sum()
    n = max(int(L / step), 2)
    cum = np.concatenate([[0], np.cumsum(seg)])
    out = []
    for d in np.linspace(0, L, n):
        i = min(np.searchsorted(cum, d, side="right") - 1, len(seg) - 1)
        u = 0 if seg[i] == 0 else (d - cum[i]) / seg[i]
        out.append(pts[i] + u * (pts[i + 1] - pts[i]))
    return out, L

def render_whip(ctrl, plate, bank, S):
    """Draw braid ribbon along ctrl path, handle plate over the root."""
    path, L = resample(catmull_rom(ctrl))
    img = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    xs = [b[0] for b in bank]
    step = 3.0
    n = int(L / step)
    for k in range(n + 1):
        d = k * step
        t = d / L
        # point + tangent by arc length
        idx = min(int(d / 2.0), len(path) - 2)
        p = path[idx]
        q = path[min(idx + 1, len(path) - 1)]
        ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        src_x = 360 + t * (612 - 360)
        bi = min(range(len(bank)), key=lambda i: abs(xs[i] - src_x))
        patch = bank[bi][1]
        # fade tip (last 16 px) and root (first 6 px)
        fade = 1.0
        if d > L - 16:
            fade = max((L - d) / 16.0, 0.15)
        if d < 6:
            fade = min(fade, 0.4 + 0.6 * d / 6.0)
        stamp = patch.rotate(-ang, resample=Image.BICUBIC, expand=True)
        if fade < 1.0:
            alpha = stamp.split()[3].point(lambda v: int(v * fade))
            stamp.putalpha(alpha)
        img.alpha_composite(stamp, (int(p[0] - stamp.width / 2),
                                    int(p[1] - stamp.height / 2)))
    img.alpha_composite(plate)
    return img, L

# ------------------------------------------------------------- pose tables
# Control points per frame. S = braid emergence (under the handle plate).
POSES = {
    "whip_attack_ground": {
        "S": (344, 195),
        "frames": [
            ("spiral", (404, 150), 76, 33, 1.55),
            ("spiral_tail", (410, 140), 82, 36, 1.22, (352, 92)),
            ("pts", [(344, 195), (334, 146), (356, 106), (398, 96),
                     (440, 118), (498, 128), (556, 152), (598, 180)]),
            ("pts", [(344, 195), (398, 180), (480, 202), (554, 206),
                     (620, 202)]),
            ("pts", [(344, 195), (404, 192), (492, 220), (584, 266)]),
            ("pts", [(344, 195), (386, 152), (452, 140), (512, 152),
                     (540, 182)]),
            ("spiral", (410, 160), 62, 36, 1.15),
            ("spiral", (402, 152), 74, 33, 1.50),
        ]},
    "whip_attack_air": {
        "S": (346, 230),
        "frames": [
            ("spiral", (400, 150), 68, 30, 1.50),
            ("spiral_tail", (406, 142), 74, 32, 1.20, (356, 102)),
            ("pts", [(346, 230), (352, 186), (368, 140), (400, 110),
                     (438, 126), (492, 142), (550, 168), (596, 200)]),
            ("pts", [(346, 230), (408, 198), (496, 186), (618, 190)]),
            ("pts", [(346, 230), (424, 236), (500, 290), (556, 360)]),
            ("pts", [(346, 230), (386, 172), (452, 160), (522, 204)]),
            ("spiral", (402, 158), 58, 32, 1.15),
            ("spiral", (398, 152), 66, 30, 1.50),
        ]},
    "whip_attack_crouch": {
        "S": (344, 166),
        "frames": [
            ("spiral", (396, 140), 62, 28, 1.50),
            ("spiral_tail", (402, 144), 68, 30, 1.20, (354, 98)),
            ("pts", [(344, 166), (352, 148), (368, 124), (398, 114),
                     (432, 128), (486, 140), (542, 152), (584, 164)]),
            ("pts", [(344, 166), (400, 158), (486, 172), (556, 174),
                     (618, 166)]),
            ("pts", [(344, 166), (412, 182), (496, 216), (572, 262)]),
            ("pts", [(344, 166), (386, 138), (452, 130), (520, 156)]),
            ("spiral", (404, 146), 64, 30, 1.15),
            ("spiral", (398, 142), 62, 28, 1.50),
        ]},
}

def build_whips():
    if os.path.exists(os.path.join(ASSETS, "bank.json")):
        plates, bank = load_assets()
        print("assets loaded from /tmp/whip_assets")
    else:
        plates, bank = extract_assets()
    for clip, spec in POSES.items():
        S = spec["S"]
        plate = plates[clip]
        for i, pose in enumerate(spec["frames"]):
            if pose[0] == "spiral":
                _, C, r0, r1, turns = pose
                ctrl = spiral_pts(S, C, r0, r1, turns)
            elif pose[0] == "spiral_tail":
                _, C, r0, r1, turns, tail = pose
                ctrl = spiral_pts(S, C, r0, r1, turns) + [tail]
            else:
                ctrl = list(pose[1])
            img, L = render_whip(ctrl, plate, bank, S)
            out = os.path.join(FRAMES, clip, f"{clip}_f{i:02d}.png")
            img.save(out)
            tip = ctrl[-1][0]
            print(f"  {clip} f{i}: arc={L:.0f} ctrl_tip_x={tip:.0f}")

# ------------------------------------------------------------------- VFX
def load_frame(clip, i):
    return Image.open(os.path.join(
        FRAMES, clip, f"{clip}_f{i:02d}.png")).convert("RGBA")

def save_frame(clip, i, img):
    img.save(os.path.join(FRAMES, clip, f"{clip}_f{i:02d}.png"))

def alpha_scale(img, factor):
    if factor == 1.0:
        return img
    a = img.split()[3].point(lambda v: int(v * factor))
    out = img.copy()
    out.putalpha(a)
    return out

def scale_about(img, sx, sy, anchor):
    """Scale content about an anchor point on the same canvas."""
    w, h = img.size
    nw, nh = max(int(w * sx), 1), max(int(h * sy), 1)
    scaled = img.resize((nw, nh), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(scaled, (int(anchor[0] - anchor[0] * sx),
                                 int(anchor[1] - anchor[1] * sy)))
    return out

def fix_impact():
    clip = "vfx_whip_impact"
    src = load_frame(clip, 2)  # densest burst frame = the one shape family
    a = np.asarray(src)[..., 3]
    ys, xs = np.where(a > 25)
    core = src.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    widths = [86, 148, 204, 162, 108, 58]
    alphas = [0.75, 0.95, 1.0, 0.78, 0.52, 0.30]
    for i, (tw, al) in enumerate(zip(widths, alphas)):
        s = tw / core.width
        fr = core.resize((tw, max(int(core.height * s), 1)), Image.LANCZOS)
        out = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        out.alpha_composite(fr, (128 - tw // 2, 128 - fr.height // 2))
        save_frame(clip, i, alpha_scale(out, al))
    print(f"impact rebuilt from f02 core {core.size} -> widths {widths}")

def fix_enemy_defeat():
    clip = "vfx_enemy_defeat"
    scales = [0.50, 0.68, 0.85, 1.0, 1.0, 0.92, 0.80, 0.65]
    alphas = [0.75, 0.90, 1.0, 1.0, 0.95, 0.80, 0.55, 0.35]
    # radial feather: the source smoke is opaque to the canvas edge, so at
    # full scale it renders as a hard grey square. A soft radial falloff
    # (1.0 inside r=70, 0 at r=126) turns it into a cloud with no edge.
    yy, xx = np.mgrid[0:256, 0:256]
    r = np.hypot(xx - 128, yy - 128)
    feather = np.clip((126 - r) / 56.0, 0.0, 1.0)
    feather = feather * feather * (3 - 2 * feather)
    for i, (s, al) in enumerate(zip(scales, alphas)):
        fr = scale_about(load_frame(clip, i), s, s, (128, 128))
        arr = np.array(fr).astype(np.float32)
        arr[..., 3] *= feather
        fr = Image.fromarray(arr.astype(np.uint8))
        save_frame(clip, i, alpha_scale(fr, al))
    print("enemy_defeat growth/decay envelope + radial feather applied")

def fix_checkpoint():
    clip = "vfx_checkpoint_activate"
    widths = [64, 110, 150, 168, 162, 148, 124, 112]
    alphas = [1.0, 1.0, 1.0, 1.0, 0.95, 0.88, 0.80, 0.72]
    for i, (tw, al) in enumerate(zip(widths, alphas)):
        fr = load_frame(clip, i)
        a = np.asarray(fr)[..., 3]
        ys, xs = np.where(a > 25)
        content = fr.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        s = tw / content.width
        nh = min(int(content.height * s), 254)
        content = content.resize((tw, nh), Image.LANCZOS)
        out = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        out.alpha_composite(content, (128 - tw // 2, 254 - nh))  # base-fixed
        save_frame(clip, i, alpha_scale(out, al))
    print("checkpoint width envelope smoothed, base-anchored")

def fix_eruption():
    clip = "vfx_hazard_eruption"
    # widths before: [119,222,312,320,170,310]; smooth the tail only.
    sx = [1.0, 1.0, 1.0, 1.0, 1.18, 0.66]
    alphas = [1.0, 1.0, 1.0, 1.0, 1.0, 0.85]
    for i, (s, al) in enumerate(zip(sx, alphas)):
        fr = scale_about(load_frame(clip, i), s, 1.0, (160, 191))
        save_frame(clip, i, alpha_scale(fr, al))
    print("eruption tail widths smoothed (f4 x1.18, f5 x0.66 a0.85)")

def fix_telegraph():
    clip = "vfx_hazard_telegraph"
    DY = 108  # band rows 0..76 -> 108..184: bottom lands on the pivot row
    for i in range(4):
        fr = load_frame(clip, i)
        out = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        out.alpha_composite(fr, (0, DY))
        save_frame(clip, i, out)
    print(f"telegraph art shifted +{DY}px (ground placement repair)")

# ------------------------------------------------------------------ main
RESTORE_CLIPS = ["whip_attack_ground", "whip_attack_air", "whip_attack_crouch",
                 "vfx_whip_impact", "vfx_enemy_defeat",
                 "vfx_checkpoint_activate", "vfx_hazard_eruption",
                 "vfx_hazard_telegraph"]

def restore_originals():
    """Re-extract the pre-fix frames from the backup zip so the whole fix
    is idempotent (safe to re-run while iterating on poses)."""
    import subprocess, shutil
    repo = os.path.expanduser("~/workspace/gothic-whip")
    for c in RESTORE_CLIPS:
        shutil.rmtree(os.path.join(FRAMES, c), ignore_errors=True)
    for c in RESTORE_CLIPS:
        subprocess.run(["unzip", "-q", "-o",
                        "game/art/source/frames_prefix_2026-10-09.zip",
                        f"game/art/frames/{c}/*"], cwd=repo, check=True)
        # .import sidecars are not art; drop any that rode along
        for f in os.listdir(os.path.join(FRAMES, c)):
            pass
    shutil.rmtree(ASSETS, ignore_errors=True)
    os.makedirs(ASSETS, exist_ok=True)
    print("originals restored from backup zip")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    clips_whip = ["whip_attack_ground", "whip_attack_air", "whip_attack_crouch"]
    clips_vfx = ["vfx_whip_impact", "vfx_enemy_defeat",
                 "vfx_checkpoint_activate", "vfx_hazard_eruption",
                 "vfx_hazard_telegraph", "vfx_damage_indicator"]
    if mode in ("all", "before"):
        for c in clips_whip + clips_vfx:
            table(c, "BEFORE")
    if mode in ("all", "fix"):
        restore_originals()
        build_whips()
        fix_impact(); fix_enemy_defeat(); fix_checkpoint()
        fix_eruption(); fix_telegraph()
    if mode in ("all", "after"):
        for c in clips_whip + clips_vfx:
            table(c, "AFTER")
