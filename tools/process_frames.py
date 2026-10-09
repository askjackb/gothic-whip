#!/usr/bin/env python3
"""Gothic Whip frame pipeline.

Consumes sprite sheets in game/art/source/ (grids declared in SHEETS below),
chroma-keys the green screen, normalizes each frame onto its contract canvas
with the foot/base pivot at the contract position, writes individual frames to
game/art/frames/<clip>/<clip>_fNN.png, packs per-actor atlases (<=2048^2),
and emits game/art/manifest.json + game/art/atlas_regions.json.

Honesty rules: alpha is verified by pixel statistics printed per sheet;
frames are NEVER rescaled per-frame to a common bbox (one uniform scale per
clip), and every transform is logged into the manifest.

Scale normalization (rewritten 2026-10-09, bug fix): the original code used
ONE anchor scale per actor (from the anchor clip's median height). Sprite
sheets were generated per clip at mutually inconsistent figure sizes, so the
anchor scale propagated each clip's drift (hero walked ~13% smaller than he
stood, crouched TALLER than standing, boss_turn ~27% oversize). The claim in
the shipped manifest of "one uniform anchor scale per actor" was therefore
wrong in effect. The fix: per clip, a uniform scale = target / reference,
where the reference is a pose-aware statistic of the figure's
largest-connected-component (LCC) bbox heights (see SCALE_SPEC), and frames
are placed by the LCC bbox so detached generation debris (thin sheet lines,
specks) can neither inflate the measurement nor anchor the feet. Small
detached debris components are removed and logged; plausible satellites
(coiled whip, weapon blades) are kept by an area/thinness rule.
"""
import json, os, sys, math
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/gothic-whip/game/art")
SRC = os.path.join(ROOT, "source")
FRAMES = os.path.join(ROOT, "frames")
ATLAS = os.path.join(ROOT, "atlases")

# actor contracts: canvas, pivot (px from top-left of canvas), align mode
# align modes: "feet" (bbox bottom -> pivot.y, bbox horizontal center -> pivot.x)
#              "center" (bbox center -> pivot), "base" (bbox bottom-center -> pivot)
ACTORS = {
    "hero":     dict(canvas=(512, 512),  pivot=(256, 448), align="feet",  ref_h=224, anchor="hero_idle"),
    "whip":     dict(canvas=(768, 512),  pivot=(276, 308), align="grip",  ref_h=None),
    "pursuer":  dict(canvas=(320, 192),  pivot=(128, 160), align="feet",  ref_h=112, anchor="pursuer_idle"),
    "swooper":  dict(canvas=(384, 256),  pivot=(192, 128), align="center", ref_h=170, anchor="swooper_cruise"),
    "ranged":   dict(canvas=(256, 320),  pivot=(128, 288), align="feet",  ref_h=300, anchor="ranged_idle"),
    "boss":     dict(canvas=(512, 512),  pivot=(176, 448), align="feet",  ref_h=352, anchor="boss_idle"),
    "vfx":      dict(canvas=(256, 256),  pivot=(128, 128), align="center", ref_h=None),
    "vfxhaz":   dict(canvas=(320, 192),  pivot=(160, 176), align="center", ref_h=None),
    "prop":     dict(canvas=(256, 320),  pivot=(128, 288), align="feet",  ref_h=None),
    "projectile": dict(canvas=(64, 64),  pivot=(32, 32),   align="center", ref_h=None),
}

# SHEETS: (source_stem, actor, clip, cols, rows, frame_count, loop, durations_ms or None)
# durations None -> filled from docs/ASSET_BRIEFS.md tables at manifest stage by GEN list
SHEETS = [
    # hero body
    ("hero_idle", "hero", "hero_idle", 4, 2, 8, True),
    ("hero_walk", "hero", "hero_walk", 5, 2, 10, True),
    ("hero_start_move", "hero", "hero_start_move", 3, 1, 3, False),
    ("hero_stop_move", "hero", "hero_stop_move", 3, 1, 3, False),
    ("hero_turn", "hero", "hero_turn", 3, 1, 3, False),
    ("hero_crouch_enter", "hero", "hero_crouch_enter", 4, 1, 4, False),
    ("hero_crouch_idle", "hero", "hero_crouch_idle", 3, 2, 6, True),
    ("hero_jump_takeoff", "hero", "hero_jump_takeoff", 3, 1, 3, False),
    ("hero_jump_rise", "hero", "hero_jump_rise", 4, 1, 4, False),
    ("hero_jump_apex", "hero", "hero_jump_apex", 3, 1, 3, False),
    ("hero_fall", "hero", "hero_fall", 4, 1, 4, True),
    ("hero_land", "hero", "hero_land", 4, 1, 4, False),
    ("hero_attack_ground", "hero", "hero_attack_ground", 4, 2, 8, False),
    ("hero_attack_air", "hero", "hero_attack_air", 4, 2, 8, False),
    ("hero_attack_crouch", "hero", "hero_attack_crouch", 4, 2, 8, False),
    ("hero_hurt_recoil", "hero", "hero_hurt_recoil", 4, 1, 4, False),
    ("hero_knockback", "hero", "hero_knockback", 4, 1, 4, False),
    ("hero_knockdown", "hero", "hero_knockdown", 6, 1, 6, False),
    ("hero_death", "hero", "hero_death", 5, 2, 10, False),
    # whip layer
    ("whip_attack_ground", "whip", "whip_attack_ground", 4, 2, 8, False),
    ("whip_attack_air", "whip", "whip_attack_air", 4, 2, 8, False),
    ("whip_attack_crouch", "whip", "whip_attack_crouch", 4, 2, 8, False),
    # pursuer
    ("pursuer_idle", "pursuer", "pursuer_idle", 3, 2, 6, True),
    ("pursuer_patrol_walk", "pursuer", "pursuer_patrol_walk", 4, 2, 8, True),
    ("pursuer_alert", "pursuer", "pursuer_alert", 4, 1, 4, False),
    ("pursuer_approach_walk", "pursuer", "pursuer_approach_walk", 4, 2, 8, True),
    ("pursuer_lunge_windup", "pursuer", "pursuer_lunge_windup", 4, 1, 4, False),
    ("pursuer_lunge", "pursuer", "pursuer_lunge", 3, 1, 3, False),
    ("pursuer_recovery", "pursuer", "pursuer_recovery", 4, 1, 4, False),
    ("pursuer_hurt", "pursuer", "pursuer_hurt", 3, 1, 3, False),
    ("pursuer_death", "pursuer", "pursuer_death", 3, 2, 6, False),
    # swooper
    ("swooper_perch_idle", "swooper", "swooper_perch_idle", 3, 2, 6, True),
    ("swooper_cruise", "swooper", "swooper_cruise", 4, 2, 8, True),
    ("swooper_dive_telegraph", "swooper", "swooper_dive_telegraph", 4, 1, 4, False),
    ("swooper_dive", "swooper", "swooper_dive", 4, 1, 4, False),
    ("swooper_recovery_climb", "swooper", "swooper_recovery_climb", 3, 2, 6, False),
    ("swooper_hurt", "swooper", "swooper_hurt", 3, 1, 3, False),
    ("swooper_death_fall", "swooper", "swooper_death_fall", 5, 1, 5, False),
    # ranged + projectile
    ("ranged_idle", "ranged", "ranged_idle", 3, 2, 6, True),
    ("ranged_aim", "ranged", "ranged_aim", 3, 2, 6, False),
    ("ranged_fire", "ranged", "ranged_fire", 3, 1, 3, False),
    ("ranged_recover", "ranged", "ranged_recover", 4, 2, 7, False),
    ("ranged_hurt", "ranged", "ranged_hurt", 3, 1, 3, False),
    ("ranged_death", "ranged", "ranged_death", 3, 2, 6, False),
    ("projectile_grave_shot", "projectile", "projectile_grave_shot", 3, 1, 3, True),
    # boss
    ("boss_idle", "boss", "boss_idle", 4, 2, 8, True),
    ("boss_walk", "boss", "boss_walk", 4, 2, 8, True),
    ("boss_turn", "boss", "boss_turn", 4, 1, 4, False),
    ("boss_strike_windup", "boss", "boss_strike_windup", 4, 2, 7, False),
    ("boss_strike_execute", "boss", "boss_strike_execute", 4, 1, 4, False),
    ("boss_strike_recover", "boss", "boss_strike_recover", 3, 2, 6, False),
    ("boss_hazard_windup", "boss", "boss_hazard_windup", 4, 2, 8, False),
    ("boss_hazard_execute", "boss", "boss_hazard_execute", 4, 1, 4, False),
    ("boss_hazard_recover", "boss", "boss_hazard_recover", 3, 2, 6, False),
    ("boss_hurt", "boss", "boss_hurt", 3, 1, 3, False),
    ("boss_death", "boss", "boss_death", 4, 3, 12, False),
    # vfx
    ("vfx_whip_impact", "vfx", "vfx_whip_impact", 3, 2, 6, False),
    ("vfx_damage_indicator", "vfx", "vfx_damage_indicator", 2, 1, 2, False),
    ("vfx_enemy_defeat", "vfx", "vfx_enemy_defeat", 4, 2, 8, False),
    ("vfx_checkpoint_activate", "vfx", "vfx_checkpoint_activate", 4, 2, 8, False),
    ("vfx_hazard_telegraph", "vfxhaz", "vfx_hazard_telegraph", 4, 1, 4, False),
    ("vfx_hazard_eruption", "vfxhaz", "vfx_hazard_eruption", 3, 2, 6, False),
]

# derived clips: reversed frame reuse (recorded honestly in the manifest)
DERIVED = [
    ("hero_crouch_exit", "hero_crouch_enter", "reversed"),
    ("hero_get_up", "hero_knockdown", "reversed"),
]

# per-clip frame durations (ms) from docs/ASSET_BRIEFS.md; default filled later
DURATIONS = {
    "hero_idle": [125]*8, "hero_walk": [80]*10, "hero_start_move": [50]*3,
    "hero_stop_move": [50]*3, "hero_turn": [50]*3, "hero_crouch_enter": [50]*4,
    "hero_crouch_exit": [50]*4, "hero_crouch_idle": [150]*6,
    "hero_jump_takeoff": [40]*3, "hero_jump_rise": [60]*4, "hero_jump_apex": [50]*3,
    "hero_fall": [100]*4, "hero_land": [40]*4,
    "hero_attack_ground": [75,75,50,50,62.5,62.5,62.5,62.5],
    "hero_attack_air": [75,75,50,50,62.5,62.5,62.5,62.5],
    "hero_attack_crouch": [75,75,50,50,62.5,62.5,62.5,62.5],
    "whip_attack_ground": [75,75,50,50,62.5,62.5,62.5,62.5],
    "whip_attack_air": [75,75,50,50,62.5,62.5,62.5,62.5],
    "whip_attack_crouch": [75,75,50,50,62.5,62.5,62.5,62.5],
    "hero_hurt_recoil": [50]*4, "hero_knockback": [75]*4, "hero_knockdown": [60]*6,
    "hero_get_up": [75]*6, "hero_death": [80]*10,
    "pursuer_idle": [150]*6, "pursuer_patrol_walk": [90]*8, "pursuer_alert": [75]*4,
    "pursuer_approach_walk": [70]*8, "pursuer_lunge_windup": [100,100,75,75],
    "pursuer_lunge": [80]*3, "pursuer_recovery": [150]*4, "pursuer_hurt": [60]*3,
    "pursuer_death": [80]*6,
    "swooper_perch_idle": [150]*6, "swooper_cruise": [90]*8,
    "swooper_dive_telegraph": [150]*4, "swooper_dive": [60]*4,
    "swooper_recovery_climb": [150]*6, "swooper_hurt": [60]*3,
    "swooper_death_fall": [70]*5,
    "ranged_idle": [150]*6, "ranged_aim": [150]*6, "ranged_fire": [50,50,100],
    "ranged_recover": [100]*7, "ranged_hurt": [60]*3, "ranged_death": [80]*6,
    "projectile_grave_shot": [80]*3,
    "boss_idle": [125]*8, "boss_walk": [80]*8, "boss_turn": [75]*4,
    "boss_strike_windup": [100]*7, "boss_strike_execute": [50]*4,
    "boss_strike_recover": [200,200,200,200,150,150],
    "boss_hazard_windup": [150]*8, "boss_hazard_execute": [100]*4,
    "boss_hazard_recover": [150]*6, "boss_hurt": [70,70,60], "boss_death": [90]*12,
    "vfx_whip_impact": [40,40,40,50,50,60], "vfx_enemy_defeat": [70]*8,
    "vfx_damage_indicator": [150, 150],
    "vfx_checkpoint_activate": [90]*8, "vfx_hazard_telegraph": [300]*4,
    "vfx_hazard_eruption": [60,60,70,70,70,70],
}

def find_source(stem):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(SRC, stem + ext)
        if os.path.exists(p):
            return p
    return None

# --- Scale normalization (2026-10-09 bug fix; see module docstring) -------
# SCALE_SPEC: clip -> (mode, target_px); one uniform scale per clip =
# target / reference, the reference being a statistic of per-frame
# largest-connected-component (LCC = the figure) bbox heights in source px.
# Modes: "median" all frames; "max" most-extended frame; "first2" median of
# the first two frames; "last" final frame; "min" most-grounded frame
# (rear-up clips: the grounded frame carries the creature's scale).
# Targets: hero standing 224 (ASSET_SPEC), crouch family 140 (0.625 x 224,
# chosen 2026-10-09; crouch collision 60u vs standing 104u); pursuer 112
# (56u shoulder, ASSET_BRIEFS S4); swooper 170 (cruise anchor contract);
# ranged 300 (150u body, ASSET_BRIEFS S6); boss 352 (176u, ASSET_BRIEFS S7).
HERO_S, HERO_C = 224.0, 140.0
SCALE_SPEC = {
    "hero_idle": ("median", HERO_S), "hero_walk": ("median", HERO_S),
    "hero_start_move": ("median", HERO_S), "hero_stop_move": ("median", HERO_S),
    "hero_turn": ("median", HERO_S), "hero_land": ("median", HERO_S),
    "hero_attack_ground": ("median", HERO_S),
    "hero_attack_air": ("median", HERO_S),
    "hero_hurt_recoil": ("median", HERO_S),
    "hero_crouch_idle": ("median", HERO_C),
    "hero_attack_crouch": ("median", HERO_C),
    "hero_crouch_enter": ("last", HERO_C),
    "hero_jump_takeoff": ("max", HERO_S), "hero_jump_rise": ("max", HERO_S),
    "hero_jump_apex": ("max", HERO_S), "hero_fall": ("max", HERO_S),
    "hero_knockback": ("max", HERO_S),
    "hero_knockdown": ("first2", HERO_S), "hero_death": ("first2", HERO_S),
    "pursuer_idle": ("median", 112.0), "pursuer_patrol_walk": ("median", 112.0),
    "pursuer_approach_walk": ("median", 112.0),
    "pursuer_hurt": ("median", 112.0), "pursuer_recovery": ("median", 112.0),
    "pursuer_alert": ("min", 112.0), "pursuer_lunge_windup": ("min", 112.0),
    "pursuer_lunge": ("max", 112.0), "pursuer_death": ("first2", 112.0),
    "swooper_perch_idle": ("median", 170.0), "swooper_cruise": ("median", 170.0),
    "swooper_dive_telegraph": ("median", 170.0),
    "swooper_dive": ("median", 170.0),
    "swooper_recovery_climb": ("median", 170.0),
    "swooper_hurt": ("median", 170.0), "swooper_death_fall": ("median", 170.0),
    "ranged_idle": ("median", 300.0), "ranged_aim": ("median", 300.0),
    "ranged_fire": ("median", 300.0), "ranged_recover": ("median", 300.0),
    "ranged_hurt": ("median", 300.0), "ranged_death": ("first2", 300.0),
    "boss_idle": ("median", 352.0), "boss_walk": ("median", 352.0),
    "boss_turn": ("median", 352.0), "boss_strike_windup": ("median", 352.0),
    "boss_strike_execute": ("median", 352.0),
    "boss_strike_recover": ("median", 352.0),
    "boss_hazard_windup": ("median", 352.0),
    "boss_hazard_execute": ("median", 352.0),
    "boss_hazard_recover": ("median", 352.0), "boss_hurt": ("median", 352.0),
    "boss_death": ("first2", 352.0),
}
# actors whose frames get debris cleaning + LCC placement; vfx/projectile/
# prop keep the exact pre-fix behavior (full-bbox placement, no cleaning)
CLEAN_ACTORS = {"hero", "whip", "pursuer", "swooper", "ranged", "boss"}


def clean_components(rgba):
    """Remove detached generation debris from a chroma-keyed cell (float
    RGBA array). Keeps the largest component plus plausible satellites
    (area >= 1% of the largest AND min bbox side > 6 px: coiled whip,
    blades, wingtips). Thin sheet-line artifacts and specks are zeroed.
    Returns (rgba, n_removed)."""
    alpha = rgba[..., 3]
    mask = alpha > 40
    lab, n = ndimage.label(mask)
    if n <= 1:
        return rgba, 0
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    li = int(np.argmax(sizes)) + 1
    lcc_area = float(sizes[li - 1])
    objs = ndimage.find_objects(lab)
    keep = np.zeros(n + 1, dtype=bool)
    keep[li] = True
    removed = 0
    for j in range(1, n + 1):
        if j == li:
            continue
        sl = objs[j - 1]
        bh = sl[0].stop - sl[0].start
        bw = sl[1].stop - sl[1].start
        if sizes[j - 1] >= 0.01 * lcc_area and min(bw, bh) > 6:
            keep[j] = True
        else:
            removed += 1
    if removed:
        out = rgba.copy()
        out[..., 3] = np.where(keep[lab], alpha, 0.0)
        return out, removed
    return rgba, 0


def lcc_bbox(alpha):
    """(x0, y0, x1, y1) of the largest connected component of alpha > 40."""
    mask = alpha > 40
    lab, n = ndimage.label(mask)
    if n == 0:
        return None
    sizes = ndimage.sum_labels(mask, lab, range(1, n + 1))
    li = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lab == li)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def reference_height(mode, heights):
    if mode == "max":
        return float(np.max(heights))
    if mode == "first2":
        return float(np.median(heights[:2]))
    if mode == "last":
        return float(heights[-1])
    if mode == "min":
        return float(np.min(heights))
    return float(np.median(heights))

def chroma_key(img):
    """Green-screen removal with distance-based alpha + green despill.
    Returns RGBA float array and stats (alpha coverage)."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    # greenness dominance
    dom = g - np.maximum(r, b)
    alpha = np.clip(1.0 - (dom - 18.0) / 60.0, 0.0, 1.0)
    # hard kill very green pixels
    alpha[dom > 90] = 0.0
    out = np.dstack([arr, alpha * 255.0]).astype(np.float32)
    # despill: where green dominates, pull g down toward max(r,b)
    spill = (dom > 0) & (alpha > 0)
    out[..., 1] = np.where(spill, np.minimum(out[..., 1], np.maximum(r, b) + dom * 0.15), out[..., 1])
    stats = dict(alpha_cov=float((alpha > 0.5).mean()),
                 alpha_zero=float((alpha == 0).mean()))
    return out, stats

def process_sheet(stem, actor, clip, cols, rows, count, loop, log):
    src = find_source(stem)
    if src is None:
        log.append(f"MISSING source for {stem}")
        return None
    if stem == "vfx_damage_indicator":
        # special case: the source is a full-screen red vignette (green
        # center, charcoal surround), not a green-screen sprite. The generic
        # chroma path produced fully transparent frames (the vignette's
        # center is the keyed color and its bbox is the whole cell, so only
        # keyed pixels landed on canvas) — found by the 2026-10-09 sequence
        # audit. Extract alpha from red dominance instead and keep the
        # full-frame composition the HUD stretches to the screen.
        img = Image.open(src).convert("RGB")
        W, H = img.size
        cw, ch = W // cols, H // rows
        arr = np.asarray(img).astype(np.float32)
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        red_dom = r - np.maximum(g, b)
        alpha = np.clip((red_dom - 8.0) / 80.0, 0.0, 1.0) * 255.0
        rgba = np.dstack([arr, alpha]).astype(np.uint8)
        canvas_w, canvas_h = ACTORS[actor]["canvas"]
        out = []
        for i in range(count):
            cx, cy = (i % cols) * cw, (i // cols) * ch
            cell = Image.fromarray(rgba[cy:cy + ch, cx:cx + cw])
            out.append(cell.resize((canvas_w, canvas_h), Image.LANCZOS))
        log.append(f"{stem}: red-vignette extraction (special case) frames={count}")
        return out
    img = Image.open(src).convert("RGB")
    W, H = img.size
    cw, ch = W // cols, H // rows
    rgba_all, stats = chroma_key(img)
    spec = ACTORS[actor]
    canvas_w, canvas_h = spec["canvas"]
    px, py = spec["pivot"]

    do_clean = actor in CLEAN_ACTORS
    raw = []  # (cell_rgba, crop_bbox, lcc_bbox) in cell coordinates
    tot_removed = 0
    for i in range(count):
        cx, cy = (i % cols) * cw, (i // cols) * ch
        cell = rgba_all[cy:cy + ch, cx:cx + cw]
        if do_clean:
            cell, nrem = clean_components(cell)
            tot_removed += nrem
        ys, xs = np.where(cell[..., 3] > 40)
        if len(xs) < 50:
            log.append(f"{stem} f{i}: nearly empty cell ({len(xs)} px)")
            raw.append(None)
            continue
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
        lcc = (lcc_bbox(cell[..., 3]) or bbox) if do_clean else bbox
        raw.append((cell, bbox, lcc))

    good = [r for r in raw if r is not None]
    if not good:
        log.append(f"{stem}: all frames empty")
        return None
    # one uniform scale per clip (never per frame): target / reference over
    # the figure's (LCC) bbox heights — see SCALE_SPEC. Whip keeps its
    # tip-reach rule, now measured on cleaned frames.
    heights = np.array([r[2][3] - r[2][1] for r in good], dtype=np.float32)
    widths = np.array([r[1][2] - r[1][0] for r in good], dtype=np.float32)
    if spec["align"] == "grip":
        # whip: widest frame's tip must reach pivot.x + 324 (168 u at 2 px/u
        # from the foot origin 256 -> tip 592; grip sits at pivot.x)
        scale = float((324.0 + 20.0) / max(1.0, float(widths.max())))
        ref_note = "tip-rule"
    elif clip in SCALE_SPEC:
        smode, target = SCALE_SPEC[clip]
        ref = reference_height(smode, heights)
        scale = float(np.clip(target / max(1.0, ref), 0.05, 3.0))
        ref_note = f"{smode} LCC h={ref:.0f} -> {target:.0f}"
    else:
        scale = 1.0
        ref_note = "unscaled"

    out_frames = []
    for i, item in enumerate(raw):
        if item is None:
            # reuse nearest good frame (documented in manifest)
            item = good[min(i, len(good) - 1)]
            log.append(f"{stem} f{i}: substituted nearest good frame")
        cell, (x0, y0, x1, y1), (lx0, ly0, lx1, ly1) = item
        crop = cell[y0:y1, x0:x1]
        nw = max(1, int(round(crop.shape[1] * scale)))
        nh = max(1, int(round(crop.shape[0] * scale)))
        crop_img = Image.fromarray(crop.astype(np.uint8)).resize((nw, nh), Image.LANCZOS)
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        mode = spec["align"]
        if mode in ("feet", "base"):
            # figure (LCC) bottom lands on pivot.y, its center-x on pivot.x
            dx = int(round(px - scale * ((lx0 + lx1) / 2.0 - x0)))
            dy = int(round(py - scale * (ly1 - y0)))
        elif mode == "grip":
            # grip = leftmost opaque pixels; their y-centroid lands on pivot.y,
            # leftmost x lands on pivot.x (the recorded hand socket)
            arr = np.asarray(crop_img)[..., 3]
            xs = np.where(arr.max(axis=0) > 40)[0]
            gx = int(xs.min()) if len(xs) else 0
            colmask = arr[:, max(0, gx):gx + 14] > 40
            ys = np.where(colmask.any(axis=1))[0]
            gy = float(ys.mean()) if len(ys) else nh / 2.0
            dx = int(round(px - gx)); dy = int(round(py - gy))
        else:  # center (LCC center for cleaned actors, bbox center else)
            dx = int(round(px - scale * ((lx0 + lx1) / 2.0 - x0)))
            dy = int(round(py - scale * ((ly0 + ly1) / 2.0 - y0)))
        canvas.paste(crop_img, (dx, dy), crop_img)
        out_frames.append(canvas)
    log.append(f"{stem}: alpha_cov={stats['alpha_cov']:.3f} scale={scale:.3f} "
               f"[{ref_note}] debris_removed={tot_removed} frames={count}")
    return out_frames

def main():
    only = sys.argv[1:] or None
    os.makedirs(FRAMES, exist_ok=True)
    os.makedirs(ATLAS, exist_ok=True)
    log = []
    manifest = {"clips": {}, "derived": [], "notes": []}
    # preserve hand-written notes (e.g. the 2026-10-09 integrity-fix note)
    _prev = os.path.join(ROOT, "manifest_raw.json")
    if os.path.exists(_prev):
        try:
            manifest["notes"] = json.load(open(_prev)).get("notes", [])
        except Exception:
            pass
    clip_frames = {}  # clip -> list[Image]

    for stem, actor, clip, cols, rows, count, loop in SHEETS:
        if only and clip not in only and stem not in only:
            continue
        frames = process_sheet(stem, actor, clip, cols, rows, count, loop, log)
        if frames is None:
            continue
        clip_frames[clip] = frames
        manifest["clips"][clip] = dict(
            actor=actor, frames=len(frames), loop=loop,
            durations_ms=DURATIONS.get(clip, [100] * len(frames)),
            canvas=list(ACTORS[actor]["canvas"]), pivot=list(ACTORS[actor]["pivot"]),
            source_sheet=stem)

    for clip, src_clip, how in DERIVED:
        if src_clip in clip_frames:
            frames = list(reversed(clip_frames[src_clip])) if how == "reversed" else clip_frames[src_clip]
            clip_frames[clip] = frames
            spec_actor = manifest["clips"][src_clip]["actor"]
            manifest["clips"][clip] = dict(
                actor=spec_actor, frames=len(frames),
                loop=manifest["clips"][src_clip]["loop"],
                durations_ms=DURATIONS.get(clip, [100] * len(frames)),
                canvas=manifest["clips"][src_clip]["canvas"],
                pivot=manifest["clips"][src_clip]["pivot"],
                derived_from=src_clip, derivation=how)
            manifest["derived"].append(f"{clip} derived from {src_clip} ({how})")

    # write individual frames
    for clip, frames in clip_frames.items():
        d = os.path.join(FRAMES, clip)
        os.makedirs(d, exist_ok=True)
        for i, fr in enumerate(frames):
            fr.save(os.path.join(d, f"{clip}_f{i:02d}.png"))

    print("\n".join(log))
    with open(os.path.join(ATLAS, "_clip_frames.json"), "w") as f:
        json.dump({c: len(v) for c, v in clip_frames.items()}, f, indent=1)
    with open(os.path.join(ROOT, "manifest_raw.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"PIPELINE: {len(clip_frames)} clips, {sum(len(v) for v in clip_frames.values())} frames")

if __name__ == "__main__":
    main()
