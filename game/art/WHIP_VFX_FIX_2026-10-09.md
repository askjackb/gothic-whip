# Whip pose-progression + VFX envelope fix — before/after metrics (2026-10-09)

User report (live build, 2026-10-09): "the whip action suddenly pop as a
illogical state" + "explosions like effect that pop irregularly".
Fix tool: `tools/fix_whip_vfx.py` (idempotent; restores originals from
`game/art/source/frames_prefix_2026-10-09.zip` before applying). Durations,
canvases, pivots, hitboxes and gameplay code untouched — PNG art only.

Measurement: PIL alpha>30 bbox per frame (L/T/R/B/w/h), whip grip =
leftmost opaque column + audit-style grip-row centroid, VFX center = bbox
center. Strips: `game/tests/shots/seq_*.png` (regenerated).

## Bug 1 — whip clips rebuilt as one continuous motion per clip

Method: procedural ribbon renderer. The handle plate of each clip's
original crack frame (f03, x<=344) is kept pixel-identical in all 8 frames
(constant grip by construction); the braid is re-rendered along designed
Catmull-Rom pose paths (coil wind-up → opening coil with escaping tip →
unfurling half-loop → extending arc → **curved** crack with sag + taper →
follow-through → recoil dome → re-coil → coil rest), textured with
cross-section slices of the original crack frame's braid (natural 28→16 px
taper preserved). Crouch no longer starts extended (now coiled); air no
longer alternates shape families.

Per-frame results (identical grip in every frame of every clip):

| clip | grip (x, gy) | tip R (bbox right edge) f0→f7 | max adjacent height step |
|---|---|---|---|
| whip_attack_ground | (276, 308.5) all 8 | 472→477→601→**621**→587→545→467→468 | −34.4% (f2→f3 crack flatten) |
| whip_attack_air | (276, 307.5) all 8 | 459→465→599→**619**→561→525→453→455 | −34.2% (f2→f3 crack flatten) |
| whip_attack_crouch | (276, 308.0) all 8 | 454→461→586→**620**→575→523→460→455 | −19.0% |

Acceptance checks (parent criteria):
- Grip offset variance: 0 px within each clip; gy drift vs pivot (276,308)
  ≤ 0.5 px (criterion ≤3 px) — PASS.
- Tip position: crack frame R = 619–621 → reach (R−276)/2 = 171.5–172.5 u
  (≥168 u hitbox, ≤ +372 px cap) — PASS.
- Extension phase tip monotonic (R: f1<f2<f3 in all clips), no backward
  jump >40 px mid-extension — PASS. Recovery decreases monotonically.
- Bbox height continuity: worst adjacent step −34.4% at the crack
  (a whip flattening at full extension), everything else ≤32%
  (criterion ≤35% inside a phase) — PASS.
- Before (for contrast): ground heights 281→257→233→**151**→220→232→199→183
  with f03 a dead-straight bar (no unfurl before it); crouch f00 already at
  R=580; air alternating coil/arc families (heights 169,174,253,232,...).

## Bug 2 — VFX envelopes

### vfx_whip_impact (256², pivot 128,128) — REBUILT
Before widths: 234→256→256→256→204→102 (heights 218→256→256→256→219→**20**):
instant near-full-canvas blast held 3 frames, ending in a 20 px sliver;
centers wander (124→128→128→128→111→131).
After (single starburst family rebuilt from the densest original frame,
scale/alpha envelope about the exact center):
widths = heights 86→148→**204**→162→108→58, alpha ×[0.75,0.95,1,0.78,0.52,0.30],
center (128,128) on **every** frame (drift 0 px). Peak 204 px = 102 u,
proportionate to the 128 u whip hitbox (criterion 180–220 px) — PASS.

### vfx_enemy_defeat (256², 8f) — REPAIRED (envelope + radial feather)
Before: 256×256 full-canvas grey smoke from frame 0 (all 8 frames
256 wide) that only dissipated — instant full size, plus the source smoke
is opaque to the canvas edge so in-game it read as a hard grey square.
After (per-frame scale about (128,128) × [0.50,0.68,0.85,1,1,0.92,0.80,0.65],
alpha × [0.75,0.9,1,1,0.95,0.8,0.55,0.35], radial alpha feather r 70→126):
bboxes 128→174→217→256→256→235→204→165 — grows over ~210 ms, peaks, decays;
centers within 1 px of (128,128). Size judged legitimate: an enemy death
burst centered on the enemy (~90–128 u footprint at peak for 2 frames).

### vfx_checkpoint_activate (256², 8f) — REPAIRED (envelope re-shape)
Before widths: 49→119→**81 (dip)**→198→198→184→117→115 — pillar narrows
mid-activation then jumps +144%.
After (each frame's own art re-scaled to a smooth width envelope,
base-anchored at canvas row 254, alpha tail fade):
widths 64→110→150→**168**→162→148→122→111, center x = 128 every frame,
all bases at row 254. Ignition glow → pillar grows → peak once → decays.

### vfx_hazard_eruption (320×192, pivot 160,176) — LIGHT TAIL REPAIR
Before dense widths: 237→320→312→320→320→311 (LCC core 119→222→312→320→
170→310): the tail re-widened to near-peak in the last frame.
After: f4 ×1.18 width, f5 ×0.66 + alpha 0.85 → dense core ...→201→205.
The f0→f1 jump (h 101→192) is KEPT: a ground eruption ignites at full
column height within one 250 ms frame by design; the column footprint
(320 px = 160 u) matches `zone_rect` 160 u wide. Bottom anchored (row 192)
on all frames, unchanged.

### vfx_hazard_telegraph (320×192, pivot 160,176) — PLACEMENT REPAIR
Envelope was already regular (heights 77→75→79→80, center x 160 stable,
1200 ms marked cast — PASS on envelope). BUT the crack band art sat at
canvas rows 0–80: with pivot row 176 and spawn at (zone_x, boss.y−8) it
rendered 58–88 u ABOVE the ground — a floating band, not a ground marker.
Shifted the art +108 px inside its canvas (rows 108–188; bottom at the
pivot row) so it lands on the ground at the eruption point, matching the
eruption's bottom-anchored convention (base rows 191–192). Same frames,
same timing, same spawn — art placement only.

### vfx_damage_indicator (256², 2f) — PASS, untouched
Red vignette flash: 202×218 / 222×221, centers (128,128)/(126,128.5) —
drift ≤2 px, a 2-frame screen flash by design (HUD overlay).

## Verification
- `tools/audit_sequences.py`: 64 clips, **0 defects** (strips regenerated).
- `game/tests/sequence_engine_check.gd`: **SEQUENCE ENGINE RESULT: PASS**.
- `game/tests/smoke_test.gd`: **SMOKE RESULT: PASS**.
- Engine screenshots (`tests/fix_shots.gd`, xvfb): `fix_whip_strike.png`
  (curved crack frame overlapping the effigy, proportionate starburst),
  `fix_whip_crouch.png`, `fix_whip_air.png`, `fix_enemy_defeat.png`
  (soft feathered burst), `fix_boss_telegraph.png` (telegraph on ground).
- Web export driven in Chromium (SwiftShader, route-intercepted):
  0 console/page errors; screenshots web_0..3 (see REVIEW_RECORD entry).
- Note for future repacks: after `tools/pack_atlases.py`, run
  `godot --headless --path . --import` once — plain `--script` runs use
  the cached .ctex atlas imports and will show stale atlas content at the
  new region coordinates.
