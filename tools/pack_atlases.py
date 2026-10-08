#!/usr/bin/env python3
"""Pack normalized frames into <=2048x2048 atlas pages and generate Godot
SpriteFrames .tres resources (one per actor) referencing AtlasTextures.

Residency model (docs/TEXTURE_BUDGET.md R1): pages grouped so a scene needs
<= 7 resident pages. Groups: hero(+whip), enemies, boss, fx_props.
"""
import json, os
from PIL import Image

ROOT = os.path.expanduser("~/workspace/gothic-whip/game/art")
FRAMES = os.path.join(ROOT, "frames")
ATLAS = os.path.join(ROOT, "atlases")
RES = os.path.expanduser("~/workspace/gothic-whip/game/art/spriteframes")
PAGE = 2048

GROUPS = {
    "hero":     ["hero"],
    "enemies":  ["pursuer", "swooper", "ranged", "projectile"],
    "boss":     ["boss"],
    "fx":       ["vfx"],
}

CLIPS = {  # clip -> (group resource name, loop)
    "hero_idle": ("hero", True), "hero_walk": ("hero", True),
    "hero_start_move": ("hero", False), "hero_stop_move": ("hero", False),
    "hero_turn": ("hero", False), "hero_crouch_enter": ("hero", False),
    "hero_crouch_exit": ("hero", False), "hero_crouch_idle": ("hero", True),
    "hero_jump_takeoff": ("hero", False), "hero_jump_rise": ("hero", False),
    "hero_jump_apex": ("hero", False), "hero_fall": ("hero", True),
    "hero_land": ("hero", False),
    "hero_attack_ground": ("hero", False), "hero_attack_air": ("hero", False),
    "hero_attack_crouch": ("hero", False), "hero_hurt_recoil": ("hero", False),
    "hero_knockback": ("hero", False), "hero_knockdown": ("hero", False),
    "hero_get_up": ("hero", False), "hero_death": ("hero", False),
    "pursuer_idle": ("enemies", True), "pursuer_patrol_walk": ("enemies", True),
    "pursuer_alert": ("enemies", False), "pursuer_approach_walk": ("enemies", True),
    "pursuer_lunge_windup": ("enemies", False), "pursuer_lunge": ("enemies", False),
    "pursuer_recovery": ("enemies", False), "pursuer_hurt": ("enemies", False),
    "pursuer_death": ("enemies", False),
    "swooper_perch_idle": ("enemies", True), "swooper_cruise": ("enemies", True),
    "swooper_dive_telegraph": ("enemies", False), "swooper_dive": ("enemies", False),
    "swooper_recovery_climb": ("enemies", False), "swooper_hurt": ("enemies", False),
    "swooper_death_fall": ("enemies", False),
    "ranged_idle": ("enemies", True), "ranged_aim": ("enemies", False),
    "ranged_fire": ("enemies", False), "ranged_recover": ("enemies", False),
    "ranged_hurt": ("enemies", False), "ranged_death": ("enemies", False),
    "projectile_grave_shot": ("enemies", True),
    "boss_idle": ("boss", True), "boss_walk": ("boss", True),
    "boss_turn": ("boss", False), "boss_strike_windup": ("boss", False),
    "boss_strike_execute": ("boss", False), "boss_strike_recover": ("boss", False),
    "boss_hazard_windup": ("boss", False), "boss_hazard_execute": ("boss", False),
    "boss_hazard_recover": ("boss", False), "boss_hurt": ("boss", False),
    "boss_death": ("boss", False),
    "vfx_whip_impact": ("fx", False), "vfx_enemy_defeat": ("fx", False),
    "vfx_damage_indicator": ("fx", False),
    "vfx_checkpoint_activate": ("fx", False), "vfx_hazard_telegraph": ("fx", False),
    "vfx_hazard_eruption": ("fx", False),
    "whip_attack_ground": ("whip", False), "whip_attack_air": ("whip", False),
    "whip_attack_crouch": ("whip", False),
}
WHIP_GROUP = ("whip", ["whip_attack_ground", "whip_attack_air", "whip_attack_crouch"])

def load_clip_frames():
    clips = {}
    if not os.path.isdir(FRAMES):
        return clips
    for clip in CLIPS:
        d = os.path.join(FRAMES, clip)
        if not os.path.isdir(d):
            continue
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        if files:
            clips[clip] = [os.path.join(d, f) for f in files]
    return clips

def trim_frame(path):
    """Trim a canvas frame to its alpha bbox (+2 px). Returns (image, tx, ty)
    or (None, 0, 0) for empty frames. Trim offsets are runtime data: the
    sprite offset restores exact canvas placement (no visual change)."""
    import numpy as np
    im = Image.open(path)
    a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > 8)
    if len(xs) == 0:
        return None, 0, 0
    x0, x1 = max(0, xs.min() - 2), min(im.width, xs.max() + 3)
    y0, y1 = max(0, ys.min() - 2), min(im.height, ys.max() + 3)
    return im.crop((x0, y0, x1, y1)), int(x0), int(y0)

class MaxRects:
    """MaxRects best-short-side-fit packer (multi-page)."""
    def __init__(self, size=2048):
        self.size = size
        self.pages = []  # list of free-rect lists
    def _new_page(self):
        self.pages.append([(0, 0, self.size, self.size)])
        return len(self.pages) - 1
    def insert(self, w, h):
        if not self.pages:
            self._new_page()
        best = None  # (waste_short, page, x, y, rect_idx)
        for pi, free in enumerate(self.pages):
            for fi, (fx, fy, fw, fh) in enumerate(free):
                if w <= fw and h <= fh:
                    short = min(fw - w, fh - h)
                    if best is None or short < best[0]:
                        best = (short, pi, fx, fy, fi)
        if best is None:
            pi = self._new_page()
            free = self.pages[pi]
            fx, fy, fw, fh = free[0]
            best = (0, pi, fx, fy, 0)
        _, pi, x, y, _ = best
        self._place(pi, x, y, w, h)
        return pi, x, y
    def _place(self, pi, x, y, w, h):
        free = self.pages[pi]
        new_free = []
        for (fx, fy, fw, fh) in free:
            if x >= fx + fw or x + w <= fx or y >= fy + fh or y + h <= fy:
                new_free.append((fx, fy, fw, fh))
                continue
            if x > fx:
                new_free.append((fx, fy, x - fx, fh))
            if x + w < fx + fw:
                new_free.append((x + w, fy, fx + fw - (x + w), fh))
            if y > fy:
                new_free.append((fx, fy, fw, y - fy))
            if y + h < fy + fh:
                new_free.append((fx, y + h, fw, fy + fh - (y + h)))
        # prune contained rects
        pruned = []
        for i, a in enumerate(new_free):
            contained = False
            for j, b in enumerate(new_free):
                if i != j and a[0] >= b[0] and a[1] >= b[1] and a[0] + a[2] <= b[0] + b[2] and a[1] + a[3] <= b[1] + b[3]:
                    contained = True
                    break
            if not contained and a[2] > 0 and a[3] > 0:
                pruned.append(a)
        self.pages[pi] = pruned

def pack_group(name, clip_names, clips, regions, page_files, trims):
    items = []  # (clip, idx, trimmed_img, tx, ty)
    for clip in clip_names:
        for i, p in enumerate(clips.get(clip, [])):
            img, tx, ty = trim_frame(p)
            if img is None:
                img = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
            items.append((clip, i, img, tx, ty))
            trims.setdefault(clip, []).append([tx, ty])
    items.sort(key=lambda x: -(x[2].width * x[2].height))
    packer = MaxRects(PAGE)
    placed = []
    for clip, i, img, tx, ty in items:
        pi, x, y = packer.insert(img.width, img.height)
        placed.append((pi, x, y, img))
        regions[f"{clip}#{i}"] = dict(page=f"{name}_{pi}", x=x, y=y, w=img.width, h=img.height)
    pages = [Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0)) for _ in packer.pages]
    for pi, x, y, img in placed:
        pages[pi].paste(img, (x, y))
    for i, pg in enumerate(pages):
        fn = f"atlas_{name}_{i}.png"
        pg.save(os.path.join(ATLAS, fn))
        page_files.append(fn)
    used = sum(r["w"] * r["h"] for k, r in regions.items() if r["page"].startswith(name))
    print(f"group {name}: {len(items)} frames -> {len(pages)} page(s), fill={used/(len(pages)*PAGE*PAGE):.2f}")
    return len(pages)

def write_tres(res_name, anim_names, clips, regions, page_of_clip_frame):
    lines = []
    exts = {}   # page file -> ext id
    subs = {}   # (clip,i) -> sub id
    n = [0]
    def nid():
        n[0] += 1
        return n[0]
    # first pass over animations to assign ids in stable order
    anim_data = []
    for anim in anim_names:
        frames = []
        for i in range(len(clips.get(anim, []))):
            r = regions[f"{anim}#{i}"]
            page_fn = page_of_clip_frame[f"{anim}#{i}"]
            if page_fn not in exts:
                exts[page_fn] = len(exts) + 1
            sid = f"AtlasTexture_{nid()}"
            subs[(anim, i)] = (sid, page_fn, r)
            frames.append(sid)
        anim_data.append((anim, frames))
    lines.append('[gd_resource type="SpriteFrames" format=3]')
    lines.append("")
    for fn, eid in exts.items():
        lines.append(f'[ext_resource type="Texture2D" path="res://art/atlases/{fn}" id="{eid}"]')
    lines.append("")
    for (anim, i), (sid, page_fn, r) in subs.items():
        lines.append(f'[sub_resource type="AtlasTexture" id="{sid}"]')
        lines.append(f'atlas = ExtResource("{exts[page_fn]}")')
        lines.append(f'region = Rect2({r["x"]}, {r["y"]}, {r["w"]}, {r["h"]})')
        lines.append("")
    lines.append("[resource]")
    lines.append("animations = [")
    for anim, frames in anim_data:
        fl = ", ".join('{\n"duration": 1.0,\n"texture": SubResource("%s")\n}' % s for s in frames)
        lines.append("{\n\"frames\": [%s],\n\"loop\": %s,\n\"name\": \"%s\",\n\"speed\": 10.0\n}," % (
            fl, "true" if CLIPS.get(anim, ("", False))[1] or anim.startswith("whip") and False else "false", anim))
    lines.append("]")
    out = os.path.join(RES, f"{res_name}.tres")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", out)

def main():
    os.makedirs(ATLAS, exist_ok=True)
    os.makedirs(RES, exist_ok=True)
    clips = load_clip_frames()
    print("clips with frames:", {c: len(v) for c, v in sorted(clips.items())})
    regions, page_files = {}, []
    page_of = {}
    trims = {}

    actor_clips = {}
    for clip, (grp, _loop) in CLIPS.items():
        actor_clips.setdefault(grp, []).append(clip)

    total_pages = 0
    for grp in ["hero", "boss"]:
        have = [c for c in actor_clips.get(grp, []) if c in clips]
        total_pages += pack_group(grp, have, clips, regions, page_files, trims)
        for k, r in regions.items():
            page_of[k] = f"atlas_{r['page']}.png" if not r["page"].endswith(".png") else r["page"]
    # shared encounter set: small enemies + whip + fx in one page set
    # (residency: hero 2 + boss 3 + encounter set 2 = 7 pages peak, R1 model)
    wname, wclips = WHIP_GROUP
    shared = [c for c in actor_clips.get("enemies", []) if c in clips] \
        + [c for c in wclips if c in clips] \
        + [c for c in actor_clips.get("fx", []) if c in clips]
    if shared:
        total_pages += pack_group("enemies", shared, clips, regions, page_files, trims)
        for k, r in regions.items():
            page_of[k] = f"atlas_{r['page']}.png"

    # fix page names: pack_group stored page as f"{name}_{i}" ; normalize
    page_of2 = {}
    for k, r in regions.items():
        page_of2[k] = f"atlas_{r['page']}.png"
    write_tres("hero_frames", [c for c in actor_clips.get("hero", [])], clips, regions, page_of2)
    write_tres("whip_frames", [c for c in wclips], clips, regions, page_of2)
    write_tres("enemy_frames", actor_clips.get("enemies", []), clips, regions, page_of2)
    write_tres("boss_frames", actor_clips.get("boss", []), clips, regions, page_of2)
    write_tres("fx_frames", actor_clips.get("fx", []), clips, regions, page_of2)

    with open(os.path.join(ATLAS, "atlas_regions.json"), "w") as f:
        json.dump(regions, f, indent=1)
    resident_mb = total_pages * 16.0
    print(f"TOTAL atlas pages={total_pages} -> {resident_mb:.1f} MiB RGBA (no mips); budget 128 MiB / <=7 pages peak design")
    report = dict(pages=total_pages, page_files=[f"atlas_{p}.png" if not p.endswith('.png') else p for p in page_files],
                  resident_mib_no_mips=resident_mb)
    with open(os.path.join(ATLAS, "atlas_report.json"), "w") as f:
        json.dump(report, f, indent=1)

    # clips.json for the runtime anim helper (durations in seconds)
    raw_path = os.path.join(ROOT, "manifest_raw.json")
    if os.path.exists(raw_path):
        raw = json.load(open(raw_path))
        cj = {}
        for clip, info in raw["clips"].items():
            cj[clip] = dict(durations_s=[d / 1000.0 for d in info["durations_ms"]],
                            loop=info["loop"], canvas=info["canvas"], pivot=info["pivot"],
                            trims=trims.get(clip, []))
        # hazard vfx defaults if not in manifest yet
        with open(os.path.join(ROOT, "clips.json"), "w") as f:
            json.dump(cj, f, indent=1)
        print("clips.json:", len(cj), "clips")

if __name__ == "__main__":
    main()
