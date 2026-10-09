#!/usr/bin/env python3
"""Fix user-reported whip defect #2 (2026-10-09, user's manual playtest):

"the whip roll and unroll ok, but it is not holding or attached correctly
to the player - it doesn't look like he is holding a whip; the whip when
rolled is the same size as the player."

Yesterday's fix (tools/fix_whip_vfx.py) rebuilt the whip's MOTION (one
continuous coil->unfurl->crack->recoil progression per clip; that part is
user-approved and is NOT changed here) but kept the painted whip's log
proportions: ~28 px cross-section baton, a fixed grip at whip-canvas
(276, gy~308) regardless of where the painted fist is, and coils up to
257 px tall - as tall as the hero himself in attack f0 (232 px). In
composites the fat near-segment floats across his chest/face while his
actual hand reaches out empty (attack_ground f3).

This fix re-renders only the whip's RENDERING, per clip, anchored to the
painted fist of each body frame:

* HANDS: the whip-hand anchor (body-canvas px) of every attack body
  frame, read off the frames with coordinate-grid debug sheets and
  verified on body+whip composites (red cross must sit on the fist).
* AXES: the forearm direction at the fist (unit, body canvas, elbow->fist).
  The short grip (32 px long, ~11 px thick) is drawn along it, centred
  on the fist; the thong emerges from its front end.
* The thong is the original painted brown braid re-sliced thin: cross-
  section tapers 9 -> 2.5 px (handle->tip) instead of the ~28 px baton.
* Rolled frames coil compactly at the fist: coil bbox <= 55% of the
  hero's 224 px standing height (target ~100 px), not a body-size spiral.
* UNCHANGED: pose progression (coil, coil+tail, unfurl, crack, follow-
  through, recoil, coil, coil), frame timing [75,75,50,50,62.5,62.5,62.5,
  62.5] ms, canvases (whip 768x512 pivot (276,308); body 512x512 pivot
  (256,448)), 0.5 sprite scale, hitboxes, and crack tip reach (619-621
  whip-canvas px = ~172 u, the 168 u hitbox + margin, as before).

Modes:
  bank     build the braid/grip texture bank from the ORIGINAL painted
           crack frames (game/art/source/frames_prefix_2026-10-09.zip)
  debug    composite body+whip with anchor crosses -> /tmp/whipwork/fix2_*
  render   write the 24 whip PNGs into game/art/frames/
  metrics  measured verification table (grip-to-hand, coil bboxes,
           max thong thickness, crack tip reach)
  archive  zip the replaced (generation-2) whip frames to
           game/art/source/frames_prefix_2026-10-09_gen2.zip
"""
import json, math, os, sys, zipfile
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/gothic-whip/game")
FRAMES = os.path.join(ROOT, "art", "frames")
SRC_ZIP = os.path.join(ROOT, "art", "source", "frames_prefix_2026-10-09.zip")
GEN2_ZIP = os.path.join(ROOT, "art", "source",
                        "frames_prefix_2026-10-09_gen2.zip")
ASSETS = "/tmp/whip_assets_inhand"
os.makedirs(ASSETS, exist_ok=True)
CANVAS = (768, 512)
THR = 30

CLIPS = ["whip_attack_ground", "whip_attack_air", "whip_attack_crouch"]
BODY = {"whip_attack_ground": "hero_attack_ground",
        "whip_attack_air": "hero_attack_air",
        "whip_attack_crouch": "hero_attack_crouch"}

# ------------------------------------------------------------ hand anchors
# Whip-hand (fist centre) per body frame, BODY-canvas px. Found on grid
# debug sheets, refined against anchor-cross composites. The swing story:
# cocked back -> sweeping across -> fully extended -> follow-through low
# -> recovery across/at side. (f0==f1, f6/f7 near-static by source art.)
HANDS = {
    "hero_attack_ground": [
        (242, 238), (242, 238), (367, 300), (352, 284),
        (212, 296), (294, 267), (249, 337), (249, 337)],
    "hero_attack_air": [
        (209, 245), (210, 244), (232, 296), (356, 257),
        (376, 283), (338, 331), (334, 360), (337, 358)],
    "hero_attack_crouch": [
        (206, 330), (206, 330), (317, 356), (322, 354),
        (216, 375), (190, 336), (189, 354), (203, 386)],
}
# Forearm direction at the fist (unit vectors, body canvas, elbow->fist).
AXES = {
    "hero_attack_ground": [
        (-0.85, 0.45), (-0.85, 0.45), (1.0, 0.12), (1.0, 0.05),
        (-0.30, 0.95), (-0.35, -0.95), (0.0, 1.0), (0.0, 1.0)],
    "hero_attack_air": [
        (-0.90, 0.30), (-0.90, 0.30), (-1.0, 0.0), (1.0, 0.05),
        (1.0, 0.08), (0.92, 0.35), (0.30, 0.95), (0.30, 0.95)],
    "hero_attack_crouch": [
        (-1.0, 0.15), (-1.0, 0.15), (1.0, 0.10), (1.0, 0.08),
        (-0.50, 0.85), (-0.95, 0.20), (-0.95, 0.25), (-0.45, 0.90)],
}
HANDLE_BACK, HANDLE_FWD = 13, 19   # grip spans H-13A .. H+19A (32 px)

def hand_whip(clip_b, i):
    """Body-canvas hand anchor -> whip-canvas coords.
    Runtime: canvas point p -> local p - pivot; body pivot (256,448),
    whip pivot (276,308)  =>  whip_pt = body_pt + (20, -140)."""
    hx, hy = HANDS[clip_b][i]
    return (hx + 20, hy - 140)

def emerge(clip_b, i):
    hx, hy = hand_whip(clip_b, i)
    ax, ay = AXES[clip_b][i]
    n = math.hypot(ax, ay)
    return (hx + HANDLE_FWD * ax / n, hy + HANDLE_FWD * ay / n), (ax / n, ay / n)

# ------------------------------------------------------------- pose tables
# Control points relative to the thong emergence point E (whip canvas).
# Same 8-beat progression as the approved motion fix; the crack (f3) tip
# stays at its absolute whip-canvas x (619-621 px -> ~172 u).
def poses(clip, E):
    if clip == "whip_attack_ground":
        return [
            ("coil", (-36, -30), 44, 17, 1.55, None),
            ("coil", (-34, -36), 45, 18, 1.30, (34, -32)),
            ("pts", [(0, 0), (-6, -34), (10, -64), (42, -76), (76, -60),
                     (120, -48), (168, -28), (206, -8)]),
            ("pts_abs", [(0, 0), (45, -10), (105, 0), (168, 5)], 621),
            ("pts", [(0, 0), (50, 16), (110, 36), (175, 52), (232, 56)]),
            ("pts", [(0, 0), (38, 6), (84, 26), (128, 30), (160, 10)]),
            ("coil", (30, -38), 47, 18, 1.30, None),
            ("coil", (28, -40), 45, 17, 1.55, None),
        ]
    if clip == "whip_attack_air":
        return [
            ("coil", (36, -14), 41, 16, 1.50, None),
            ("coil", (38, -18), 42, 16, 1.25, (72, -46)),
            ("pts", [(0, 0), (6, -34), (20, -68), (46, -88), (80, -76),
                     (124, -58), (172, -34), (210, -12)]),
            ("pts_abs", [(0, 0), (42, -8), (100, -2), (160, 2)], 619),
            ("pts", [(0, 0), (44, 28), (94, 58), (148, 98)]),
            ("pts", [(0, 0), (30, -32), (76, -48), (122, -38), (152, -10)]),
            ("coil", (26, -38), 44, 16, 1.30, None),
            ("coil", (26, -40), 43, 16, 1.50, None),
        ]
    return [  # whip_attack_crouch
        ("coil", (36, -26), 43, 16, 1.55, None),
        ("coil", (38, -28), 44, 17, 1.30, (70, -52)),
        ("pts", [(0, 0), (7, -16), (20, -36), (45, -44), (75, -32),
                 (120, -22), (168, -12), (205, -2)]),
        ("pts_abs", [(0, 0), (45, -6), (115, 2), (180, 4)], 620),
        ("pts", [(0, 0), (48, 14), (105, 30), (175, 44), (230, 48)]),
        ("pts", [(0, 0), (35, -28), (80, -38), (125, -26), (155, -2)]),
        ("coil", (32, -34), 44, 16, 1.30, None),
        ("coil", (32, -32), 42, 15, 1.50, None),
    ]

# ------------------------------------------------------- texture bank
def build_bank():
    """Braid slices + grip-wrap slice from the ORIGINAL painted crack
    frame (pre-fix archive), the same painted source the previous fix
    used - re-sliced here for the thin render."""
    z = zipfile.ZipFile(SRC_ZIP)
    name = "game/art/frames/whip_attack_ground/whip_attack_ground_f03.png"
    src = Image.open(z.open(name)).convert("RGBA") if False else None
    import io
    src = Image.open(io.BytesIO(z.read(name))).convert("RGBA")
    a = np.asarray(src)[..., 3]
    bank = []
    for x in range(352, 612, 3):
        col = a[:, x - 3:x + 4]
        rows = np.where((col > THR).any(axis=1))[0]
        if len(rows) == 0:
            continue
        y0, y1 = int(rows.min()) - 2, int(rows.max()) + 3
        bank.append({"x": x, "patch": src.crop((x - 3, y0, x + 4, y1)),
                     "thick": y1 - y0})
    # grip-wrap patch: thin vertical strip through the painted handle
    grip = src.crop((304, 205, 311, 322))
    grip.save(os.path.join(ASSETS, "grip.png"))
    with open(os.path.join(ASSETS, "bank.json"), "w") as f:
        json.dump([b["x"] for b in bank], f)
    for i, b in enumerate(bank):
        b["patch"].save(os.path.join(ASSETS, f"bank_{i:03d}.png"))
    print(f"bank: {len(bank)} slices, source thickness "
          f"{bank[0]['thick']}->{bank[-1]['thick']} px; grip patch {grip.size}")
    return bank, grip

def load_bank():
    xs = json.load(open(os.path.join(ASSETS, "bank.json")))
    bank = []
    for i, x in enumerate(xs):
        p = Image.open(os.path.join(ASSETS, f"bank_{i:03d}.png"))
        bank.append({"x": x, "patch": p, "thick": p.height})
    grip = Image.open(os.path.join(ASSETS, "grip.png"))
    return bank, grip

# ------------------------------------------------------------ ribbon math
def catmull_rom(pts):
    p = [pts[0]] + list(pts) + [pts[-1]]
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

def spiral_ctrl(E, C, r0, r1, turns, tail):
    """Lead from E bowing into an inward spiral centred C (whip canvas)."""
    a0 = math.atan2(E[1] - C[1], E[0] - C[0])
    P = (C[0] + r0 * math.cos(a0), C[1] + r0 * math.sin(a0))
    pts = [E]
    for k in (0.33, 0.66):
        mx = E[0] + (P[0] - E[0]) * k
        my = E[1] + (P[1] - E[1]) * k - 10 * math.sin(k * math.pi)
        pts.append((mx, my))
    steps = int(turns * 40)
    for i in range(steps + 1):
        u = i / steps
        ang = a0 + u * turns * 2 * math.pi
        r = r0 + (r1 - r0) * u
        pts.append((C[0] + r * math.cos(ang), C[1] + r * math.sin(ang)))
    if tail:
        pts.append((E[0] + tail[0], E[1] + tail[1]))
    return pts

def resample(pts, step=2.0):
    pts = np.array(pts, dtype=float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    L = float(seg.sum())
    n = max(int(L / step), 2)
    cum = np.concatenate([[0], np.cumsum(seg)])
    out = []
    for d in np.linspace(0, L, n):
        i = min(np.searchsorted(cum, d, side="right") - 1, len(seg) - 1)
        u = 0 if seg[i] == 0 else (d - cum[i]) / seg[i]
        out.append(pts[i] + u * (pts[i + 1] - pts[i]))
    return out, L

def thickness_at(t):
    """Thong cross-section along its length: 9 px at the grip end,
    2.5 px at the tip (source px)."""
    return 9.0 + (2.5 - 9.0) * (t ** 0.85)

def stamp_along(img, path, L, bank, thick_fn, alpha_tip=True):
    xs = [b["x"] for b in bank]
    step = 2.2
    n = int(L / step)
    for k in range(n + 1):
        d = k * step
        t = d / L if L else 0.0
        idx = min(int(d / 2.0), len(path) - 2)
        p, q = path[idx], path[min(idx + 1, len(path) - 1)]
        ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        src_x = 352 + t * (610 - 352)
        bi = min(range(len(bank)), key=lambda i: abs(xs[i] - src_x))
        patch = bank[bi]["patch"]
        th = max(int(round(thick_fn(t))), 2)
        sp = patch.resize((patch.width, th), Image.LANCZOS)
        fade = 1.0
        if alpha_tip and d > L - 14:
            fade = max((L - d) / 14.0, 0.15)
        if d < 5:
            fade = min(fade, 0.5 + 0.5 * d / 5.0)
        st = sp.rotate(-ang, resample=Image.BICUBIC, expand=True)
        if fade < 1.0:
            st.putalpha(st.split()[3].point(lambda v: int(v * fade)))
        img.alpha_composite(st, (int(p[0] - st.width / 2),
                                 int(p[1] - st.height / 2)))

def draw_handle(img, H, A, grip):
    """Short wrapped grip through the fist, along the forearm axis."""
    back = (H[0] - HANDLE_BACK * A[0], H[1] - HANDLE_BACK * A[1])
    fwd = (H[0] + HANDLE_FWD * A[0], H[1] + HANDLE_FWD * A[1])
    n = 16
    for k in range(n + 1):
        u = k / n
        p = (back[0] + (fwd[0] - back[0]) * u,
             back[1] + (fwd[1] - back[1]) * u)
        src = grip.crop((0, int(u * (grip.height - 12)), grip.width,
                         int(u * (grip.height - 12)) + 12))
        sp = src.resize((7, 11), Image.LANCZOS)
        if k <= 2:  # darker butt cap
            arr = np.array(sp).astype(np.float32)
            arr[..., :3] *= 0.55
            sp = Image.fromarray(arr.astype(np.uint8))
        ang = math.degrees(math.atan2(A[1], A[0]))
        st = sp.rotate(-ang, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(st, (int(p[0] - st.width / 2),
                                 int(p[1] - st.height / 2)))

def render_frame(clip, i, bank, grip):
    bclip = BODY[clip]
    E, A = emerge(bclip, i)
    H = hand_whip(bclip, i)
    pose = poses(clip, E)[i]
    if pose[0] == "coil":
        _, off, r0, r1, turns, tail = pose
        C = (E[0] + off[0], E[1] + off[1])
        ctrl = spiral_ctrl(E, C, r0, r1, turns, tail)
    elif pose[0] == "pts_abs":
        rel, tip_x = pose[1], pose[2]
        ctrl = [(E[0] + dx, E[1] + dy) for dx, dy in rel]
        ctrl.append((tip_x, E[1] + 2))
    else:
        ctrl = [(E[0] + dx, E[1] + dy) for dx, dy in pose[1]]
    path, L = resample(catmull_rom(ctrl))
    img = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    stamp_along(img, path, L, bank, thickness_at)
    draw_handle(img, H, A, grip)
    return img, L

# ----------------------------------------------------------------- modes
def do_bank():
    build_bank()

def composites(tag, mark=True):
    bank, grip = load_bank()
    OUT = "/tmp/whipwork"
    for clip in CLIPS:
        bclip = BODY[clip]
        cells = []
        for i in range(8):
            body = Image.open(os.path.join(
                FRAMES, bclip, f"{bclip}_f{i:02d}.png")).convert("RGBA")
            whip, _ = render_frame(clip, i, bank, grip)
            im = Image.new("RGBA", (900, 760), (24, 24, 32, 255))
            bx, by = 100, 60
            im.alpha_composite(body, (bx, by))
            im.alpha_composite(whip, (bx - 20, by + 140))
            if mark:
                hx, hy = HANDS[bclip][i]
                cx, cy = bx + hx, by + hy
                d = ImageDraw.Draw(im)
                d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7],
                          outline=(255, 60, 60, 255), width=2)
                d.line([(cx - 12, cy), (cx + 12, cy)], fill=(255, 60, 60, 255), width=2)
                d.line([(cx, cy - 12), (cx, cy + 12)], fill=(255, 60, 60, 255), width=2)
            cells.append(im)
        cell = 460
        strip = Image.new("RGBA", (cell * 4, cell * 2), (14, 14, 20, 255))
        for i, f in enumerate(cells):
            f2 = f.resize((cell, int(cell * f.height / f.width)), Image.LANCZOS)
            strip.alpha_composite(f2, ((i % 4) * cell, (i // 4) * cell))
        p = os.path.join(OUT, f"{tag}_{clip}.png")
        strip.save(p)
        print(p)

def do_debug():
    composites("fix2_debug")

def write_hands_json():
    data = {}
    for clip in CLIPS:
        b = BODY[clip]
        data[clip] = {"body_clip": b,
                      "hands_body_canvas": HANDS[b],
                      "axes_body_canvas": AXES[b]}
    p = os.path.join(ROOT, "art", "whip_hands.json")
    with open(p, "w") as f:
        json.dump(data, f, indent=1)
    print("wrote", p)

def do_render():
    bank, grip = load_bank()
    for clip in CLIPS:
        for i in range(8):
            img, L = render_frame(clip, i, bank, grip)
            out = os.path.join(FRAMES, clip, f"{clip}_f{i:02d}.png")
            img.save(out)
            print(f"wrote {clip} f{i} (arc {L:.0f})")
    write_hands_json()

def do_strips():
    """Final evidence: body+whip composite strips (no markers)."""
    bank, grip = load_bank()
    OUTD = os.path.join(ROOT, "tests", "shots")
    os.makedirs(OUTD, exist_ok=True)
    for clip in CLIPS:
        bclip = BODY[clip]
        cells = []
        for i in range(8):
            body = Image.open(os.path.join(
                FRAMES, bclip, f"{bclip}_f{i:02d}.png")).convert("RGBA")
            whip, _ = render_frame(clip, i, bank, grip)
            im = Image.new("RGBA", (900, 760), (24, 24, 32, 255))
            im.alpha_composite(body, (100, 60))
            im.alpha_composite(whip, (80, 200))
            cells.append(im)
        cell = 460
        strip = Image.new("RGBA", (cell * 4, cell * 2), (14, 14, 20, 255))
        for i, f in enumerate(cells):
            f2 = f.resize((cell, int(cell * f.height / f.width)),
                          Image.LANCZOS)
            strip.alpha_composite(f2, ((i % 4) * cell, (i // 4) * cell))
        p = os.path.join(OUTD, f"fix2_composite_{clip}.png")
        strip.save(p)
        print(p)

def frame_stats(path, H):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)[..., 3]
    m = a > THR
    ys, xs = np.where(m)
    if len(xs) == 0:
        return {"empty": True}
    dt = ndimage.distance_transform_edt(m)
    # thong thickness: away from the grip zone (r=26 around the fist), so
    # the 11 px handle and strand crossings at the fist don't inflate it
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    away = np.hypot(xx - H[0], yy - H[1]) > 26
    return {"bbox": (int(xs.min()), int(ys.min()), int(xs.max()) + 1,
                     int(ys.max()) + 1),
            "max_thick": round(2 * float((dt * away).max()), 1)}

def do_metrics():
    print(f"{'clip':22} {'f':>2} {'attach':>7} {'gripCtr':>8} "
          f"{'bbox':>10} {'thongMax':>8} {'tipR(u)':>8}")
    for clip in CLIPS:
        bclip = BODY[clip]
        for i in range(8):
            p = os.path.join(FRAMES, clip, f"{clip}_f{i:02d}.png")
            im = Image.open(p).convert("RGBA")
            a = np.asarray(im)[..., 3]
            H = hand_whip(bclip, i)
            ys, xs = np.where(a > THR)
            # attach: distance from the fist anchor to the nearest whip px
            dt = ndimage.distance_transform_edt(a <= THR)
            attach = float(dt[H[1], H[0]])
            # grip centroid: whip alpha inside a tight r=12 disc at fist
            near = (np.hypot(xs - H[0], ys - H[1]) <= 12)
            gx = float(xs[near].mean()) if near.any() else float("nan")
            gy = float(ys[near].mean()) if near.any() else float("nan")
            ctr = math.hypot(gx - H[0], gy - H[1])
            st = frame_stats(p, H)
            bb = st.get("bbox")
            dims = f"{bb[2]-bb[0]}x{bb[3]-bb[1]}" if bb else "-"
            reach = round(((bb[2] - 276) / 2.0), 1) if bb else "-"
            print(f"{clip:22} {i:>2} {attach:>6.1f}px {ctr:>7.1f}px "
                  f"{dims:>10} {st.get('max_thick','-'):>8} {reach:>8}")

def do_archive():
    import shutil
    tmp = "/tmp/gen2_backup"
    shutil.rmtree(tmp, ignore_errors=True)
    z = zipfile.ZipFile(GEN2_ZIP, "w", zipfile.ZIP_DEFLATED)
    for clip in CLIPS:
        for i in range(8):
            rel = f"game/art/frames/{clip}/{clip}_f{i:02d}.png"
            z.write(os.path.join(ROOT, "art", "frames", clip,
                                 f"{clip}_f{i:02d}.png"), rel)
    z.close()
    print("archived generation-2 whip frames ->", GEN2_ZIP)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "debug"
    {"bank": do_bank, "debug": do_debug, "render": do_render,
     "metrics": do_metrics, "archive": do_archive,
     "strips": do_strips, "hands": write_hands_json}[mode]()

# record for the audit (grip contract = hand anchors), machine-readable
HANDS_JSON = {BODY[c]: HANDS[BODY[c]] for c in CLIPS}
