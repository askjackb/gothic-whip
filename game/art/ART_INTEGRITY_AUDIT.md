# Art-integrity (completeness) audit — 2026-10-09

**Trigger:** user playtest round 4. Standing still, the hunter was visibly the
wrong size versus walking. Root cause found by eye (the user's), confirmed
here: `hero_idle` is a **waist-up torso** — head, chest, belt, hands; no coat,
no legs, no boots — whose head-to-belt span is 224 px, exactly the standing
anchor. Every prior audit (SCALE_AUDIT, SEQUENCE_AUDIT, ACTION_SIZE_AUDIT)
compared bounding boxes and alpha areas, so a torso at full-body height
passed all of them. The original production sheet
(`art/source/hero_idle.png`, 2026-10-08) is already waist-up: **idle has been
broken since generation**, and the user's first-ever complaint ("size changes
standing vs moving") was this defect — standing showed an oversized torso,
moving showed the true full body.

**Gameplay, timings, hitboxes: frozen.** This audit covers art integrity
only — is every figure complete, and drawn at the body scale of its actor?

## Method

1. **Visual pass (primary evidence).** Every one of the 64 clips / 357
   frames rendered as a native-resolution contact strip
   (`tests/shots/integrity/<clip>.png`, pivot crosshair drawn) and eyeballed
   frame by frame. Zooms at 2–6× for every suspect frame.
2. **Integrity gate** (`tools/audit_integrity.py`, new): anatomy metrics per
   frame — tracked head-run width, bottom-band taper (`boot_ratio`), lower-
   body narrowing (`leg_dip`). Standing-class frames of legged actors fail
   if the bottom 8% of the figure is nearly as wide as the torso with no
   narrowing below the waist (a sliced figure), and hero idle/walk frames
   fail if the head proxy deviates > 12% from the trusted reference.
   Pre-fix result: **8 DEFECTs (all of hero_idle), exit code 1**, plus 1
   FLAG adjudicated below. Note: "ink in the top/bottom 8% of the bbox" is
   vacuous (a bbox is defined by its ink) — it is logged, never used as
   evidence; the structure ratios are the gate.
3. **Component/edge scans** over all 357 frames: satellite components ≥ 2%
   of the main figure, hollow-rectangle outline components, and ink touching
   canvas edges. Every hit was zoomed and adjudicated by eye.

### Per-actor body-part references (trusted full-body frames)

| Actor | Reference frames | Head measure | Lower-body signature |
|---|---|---|---|
| hero | hero_walk (10 f) | head+ponytail run 38–42 px on a 224 px figure (median 39) | boots: bottom-band ratio ≤ 0.46, dip ≤ 0.51 |
| pursuer | pursuer_patrol_walk | elongated skull, front; head carriage varies by pose (quadruped — head gate n/a) | four legs; bottom-band ≤ 0.32 |
| ranged | ranged_idle | hooded head ~55 px on 288 px robe | robe legitimately reaches ground at full width (bottom-band 0.86) — truncation indistinguishable by silhouette; visual pass is the check |
| boss | boss_walk | horned helm; topmost feature is a 3 px horn tip (head proxy invalid — visual pass is the check) | armored legs in walk; robe/cape to ground in idle/turn |
| swooper | swooper_cruise | hooded head between wings | airborne, center-anchored; no ground signature |

## Broken-frame inventory (pre-fix, named)

### A. Broken at generation — regenerate

| Frame(s) | Defect |
|---|---|
| **hero_idle f00–f07 (all 8)** | Waist-up torso at full-body scale. Head run 62–73 px vs trusted 39 (+59…+85%); boot_ratio 0.71–0.86, leg_dip 0.59–0.77 (no legs exist). Source sheet itself is waist-up. |
| **hero_death f08** | Figure fragmented: head+hand at bottom-left, a leg/cloth strip 58 px to its right, **torso missing**, plus a floating cloth slab above. Cannot be cleaned — the body is gone. |

### B. Clipped by extraction — reprocess from source (source art intact)

| Frame(s) | Defect |
|---|---|
| **pursuer_alert f02, f03** | Reared-up head and forelimbs cropped by the 192 px canvas top. Source sheet (single row, green margins) holds the full creature. |
| **pursuer_lunge_windup f00** | Same: rearing figure taller than canvas; source cell intact (72 px top margin). |
| **swooper_dive_telegraph f01** | Spread left wing clipped at the canvas left edge (center-anchor overflow, 384 px canvas too narrow). Source intact. |

### C. Debris in frame — targeted cleanup (figure itself complete)

| Frame(s) | Debris |
|---|---|
| hero_death f05 | floating cloth slab (2051 px) above the kneeling figure |
| hero_death f06 | floating slab (2567 px) + detached boot pair (878 px) |
| hero_death f07 | floating slab (2017 px) |
| hero_fall f03 | 2×240 px vertical line artifact (482 px) left of the figure |
| hero_hurt_recoil f00 | floating teal cloak shard (331 px) |
| pursuer_lunge f00 | neighbour-cell claw tip (79 px) |
| pursuer_lunge f01 | neighbour-cell arm fragment (309 px) — confirmed against the source sheet: the next pose's arm bleeds into this cell |
| swooper_dive_telegraph f02 | neighbour wingtip speck (215 px) |
| boss_strike_recover f00, f02, f03 | source cell-border rectangle outline (1389 / 1100 / 1437 px, fill ≈ 1%) |
| boss_hazard_recover f00, f02 | same rectangle outline (1141 / 775 px) |

### D. Minor — documented, not repaired (with reasons)

- **ranged (all 31 frames):** the post the cultist is tied to is cropped
  flat at the canvas top (~12–24 px of carved post capital). Uniform across
  every ranged clip, figure anatomy complete, predates this audit (recorded
  as a nit in the round-3 fix). Repair means a canvas-contract change for a
  prop tip; risk outweighs benefit. `ranged_recover f00` claw tips likewise
  touch the right canvas edge.
- **boss_strike_execute f01–f03, boss_hurt f00:** cape wisps touch the left
  canvas edge; zoomed — wisps end naturally, nothing reads as cut.
- **vfx_whip_impact f01–f03:** burst rays end at a square frame edge;
  **vfx_enemy_defeat f00–f01:** square smoke-texture seams. Effect sprites
  (not figures), pre-reviewed in the round-2 VFX fix, on screen ≤ 150 ms.
- **projectile_grave_shot f00–f02:** soft low-res spectral blob; alpha > 40
  covers 94–100% of the 64² canvas but the falloff is semi-transparent
  (corner alpha ≈ 20), so in game it reads as a fog puff, not a square.

### FLAG adjudication

- `hero_walk f03` head-dev +15% (isolated): ponytail swung wide in one gait
  frame; full body, same man. **PASS.**

## Per-clip verdicts (visual pass, all 357 frames)

| Clip | Frames | Verdict |
|---|---|---|
| hero_idle | 8 | **BROKEN** — torso (A) |
| hero_walk | 10 | OK (f03 FLAG → PASS) |
| hero_start_move | 3 | OK |
| hero_stop_move | 3 | OK |
| hero_turn | 3 | OK |
| hero_crouch_enter | 4 | OK |
| hero_crouch_idle | 6 | OK |
| hero_crouch_exit | 4 | OK |
| hero_jump_takeoff | 3 | OK |
| hero_jump_rise | 4 | OK |
| hero_jump_apex | 3 | OK |
| hero_fall | 4 | f03 debris (C) |
| hero_land | 4 | OK |
| hero_attack_ground | 8 | OK |
| hero_attack_air | 8 | OK |
| hero_attack_crouch | 8 | OK |
| hero_hurt_recoil | 4 | f00 debris (C) |
| hero_knockback | 4 | OK |
| hero_knockdown | 6 | OK |
| hero_get_up | 6 | OK |
| hero_death | 10 | f08 **BROKEN** (A); f05–f07 debris (C) |
| whip_attack_ground | 8 | OK (legacy layer; runtime draws the whip procedurally) |
| whip_attack_air | 8 | OK |
| whip_attack_crouch | 8 | OK |
| pursuer_idle | 6 | OK (no runtime state — retained per briefs) |
| pursuer_patrol_walk | 8 | OK |
| pursuer_approach_walk | 8 | OK |
| pursuer_alert | 4 | f02, f03 **CLIPPED** (B) |
| pursuer_lunge_windup | 4 | f00 **CLIPPED** (B) |
| pursuer_lunge | 3 | f00, f01 debris (C) |
| pursuer_recovery | 4 | OK |
| pursuer_hurt | 3 | OK |
| pursuer_death | 6 | OK |
| swooper_perch_idle | 6 | OK (no runtime state — retained per briefs) |
| swooper_cruise | 8 | OK |
| swooper_dive_telegraph | 4 | f01 **CLIPPED** (B); f02 debris (C) |
| swooper_dive | 4 | OK |
| swooper_recovery_climb | 6 | OK |
| swooper_hurt | 3 | OK |
| swooper_death_fall | 5 | OK |
| ranged_idle | 6 | OK figure; post-top minor (D) |
| ranged_aim | 6 | OK (detached glyph at hand is the cast sigil, by design) |
| ranged_fire | 3 | OK |
| ranged_recover | 7 | OK figure; edge minors (D) |
| ranged_hurt | 3 | OK |
| ranged_death | 6 | OK |
| projectile_grave_shot | 3 | OK as designed (D note) |
| boss_idle | 8 | OK (robe to ground by design) |
| boss_walk | 8 | OK |
| boss_turn | 4 | OK (robe by design) |
| boss_strike_windup | 7 | OK |
| boss_strike_execute | 4 | OK (D edge note) |
| boss_strike_recover | 6 | f00, f02, f03 outline debris (C) |
| boss_hazard_windup | 8 | OK |
| boss_hazard_execute | 4 | OK |
| boss_hazard_recover | 6 | f00, f02 outline debris (C) |
| boss_hurt | 3 | OK (D edge note) |
| boss_death | 12 | OK |
| vfx_whip_impact | 6 | OK effect (D note) |
| vfx_enemy_defeat | 8 | OK effect (D note) |
| vfx_damage_indicator | 2 | OK |
| vfx_hazard_telegraph | 4 | OK (full-bleed by design) |
| vfx_hazard_eruption | 6 | OK (full-bleed by design) |
| vfx_checkpoint_activate | 8 | OK |

**Totals:** 357 frames looked at. Broken at generation: 9 frames
(hero_idle ×8, hero_death f08). Clipped by extraction: 4 frames. Debris in
frame: 17 frames. Everything else complete.

## Gate evidence (pre-fix)

```
$ python3 tools/audit_integrity.py
INTEGRITY DEFECTS: 8  (hero_idle f00–f07, truncation clause; exit code 1)
FLAGS: hero_walk f03 (+15% head-dev, isolated → visual PASS)
```

The numeric gate's standing clauses cover legged ground poses; the death,
alert, telegraph and debris defects sit outside those pose classes and were
caught by the visual pass and the component scans — which is why the visual
pass is the primary evidence and the gate is the tripwire. Post-repair, this
same gate must report 0 DEFECTs on the repaired set while still failing on
the archived pre-fix frames (`art/source/frames_prefix_2026-10-09.zip` and
the pre-repair archive taken before the fix).

---

## Repairs (same day, 2026-10-09, `tools/repair_integrity.py`)

**A1 hero_idle (all 8 frames) — rebuilt, full body.** A freshly generated
idle sheet could not be obtained: the image-generation upstream failed
on 2026-10-09 (recorded in REVIEW_RECORD). The idle was therefore
rebuilt from the game's own approved full-body standing frame
(`hero_turn` f00 — the same neutral stand the game already ships) with a
procedural breathing loop (feet-anchored vertical breath, +0.9% at
peak). This makes the idle literally the same drawing as the walk/turn
figure — same head, same coat, same boots. Flagged for the user's
visual verdict like any new art.

**A2 hero_death f08 — regenerated single frame.** Candidate sheet
generated with `hero_death` f09 as identity reference
(`art/source/hero_death_f08_source.png`); the most complete lying
figure (bottom-right, unclipped) was chroma-keyed, mirrored (the clip's
corpse lies head-left), scaled to the clip's median √area and placed on
the (256, 448) pivot; per-frame normalization then pinned it (×0.999).

**B canvas-clipped clips — reprocessed from the intact source sheets**
via `process_frames.process_sheet`, clips docs updated in
`manifest_raw.json`: `pursuer_alert` and `pursuer_lunge_windup` →
canvas 320×288, pivot (128, 256); `swooper_dive_telegraph` → canvas
512×320, pivot (256, 160). Feet/centre anchor relative to the pivot is
unchanged, so in-game placement is unchanged. Verified in the repaired
strips: alert heads/claws/feet now inside the canvas, telegraph's left
wing whole.

**C debris — removed, figures untouched** (deterministic component
removal on the shipped frames, exact figure scale preserved):
`hero_death` f05/f06/f07 slabs (+f06 detached boots), `hero_fall` f03
line, `hero_hurt_recoil` f00 cloak shard, `hero_land` f03 detached
hand, `pursuer_lunge` f00/f01 neighbour bleed,
`swooper_dive_telegraph` f02 wingtip speck. Boss recover clips: the
hollow cell-border outline components (`boss_strike_recover`
f00/f02/f03, `boss_hazard_recover` f00/f02) **plus** their flat edge
fragments — a second scan found 1–4 px-thick line pieces up to 381 px
long that the outline signature alone missed (incl. `boss_hazard_recover`
f01); the cleanup rule now covers both signatures
(`tools/repair_integrity.py: clean_outlines`).

Normalization was re-run globally as per pipeline, then every
collateral rescale outside the intended repair set was reverted from
git: the final frame diff is exactly 34 files (8 idle, 4 death, 1 fall,
1 hurt, 1 land, 2 lunge, 8 pursuer reprocess, 4 telegraph, 5 boss
recover). Whip frames and `whip_hands.json` untouched; the sequence
audit's whip-grip checks (≤6 px) still pass.

## Gate evidence (post-fix)

```
$ python3 tools/audit_integrity.py            # repaired frames
INTEGRITY DEFECTS: 0   FLAGS: 1 (hero_walk f03 ponytail, adjudicated)
exit 0
$ python3 tools/audit_integrity.py --frames-root <frames_prefix_2026-10-09.zip>
INTEGRITY DEFECTS: 10  (hero_idle f00–f07 torso; vfx_damage_indicator
f00–f01 empty — that archive predates the round-1 vignette fix)
exit 1
```

## Post-fix verification

- `tools/audit_integrity.py`: **0 DEFECTS**; every repaired clip's strip
  re-inspected frame by frame (idle full body; death f08 complete and
  matching its neighbours; alert/windup/telegraph whole).
- `tools/audit_sequences.py`: **64 clips, 0 defects, 0 warnings**.
- `tests/sequence_engine_check.gd`: **SEQUENCE ENGINE RESULT: PASS**
  (64 clips, 357 frames stepped).
- `tests/smoke_test.gd`: **SMOKE RESULT: PASS**.
- Contact sheets (`game/tests/shots/fix4/contact_hero.png`,
  `contact_actors.png`, inspected): idle/walk/attack read as the same
  man at the same 224 px; boss standing tiles 351–352; pursuer alert
  rear-up 207 as a pose on the same foot line.
- Fresh web export driven in Chromium (`tools/web_check3.js`):
  **CONSOLE_ERRORS: 0**; standing and walking screenshots show the
  same-stature full-body hunter (the 500 ms whip swing itself remains
  ungradeable from burst screenshots — covered by the sequence audit's
  whip-grip checks and the engine test).
