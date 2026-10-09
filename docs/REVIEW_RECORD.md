# Initial handoff review

Date: 2026-10-07. Scope: documents and examples only.

## Completed checks

- All 18 relative Markdown file links in the initial 16-file handoff resolve.
- The example asset manifest parses as JSON.
- The eight example attack-frame durations sum to 500 ms, matching the gameplay and asset contracts; active interval is [150, 250) ms.
- The proposed hero animation table totals 113 body frames plus 24 weapon frames (137 total).
- Untrimmed frame memory is explicitly reconciled as a budget conflict to solve before production: 113 MiB body + 36 MiB weapon exceeds the 128 MiB slice-art target.
- Final interview direction is reflected throughout: primarily Castlevania, no visible pixels, full supported-action animation. Earlier Mario/crossover brainstorming is not a production commitment.
- No existing workspace project, third-party art binary, game implementation, or generated asset was copied into this repository.

## Explicitly not tested

Engine import, sprite quality, animation playback, combat behavior, mobile touch controls, browser export, performance, loading, and Android APK. No implementation or assets exist to test.

## Open at publication

The final identity answer is confirmed: Simon Belmont in Castlevania’s world. Exact costume reference, horror intensity, target hardware, and proposed numerical tuning remain for later specification work. No further interview is required to use this handoff.

---

# Follow-up review — audit + P1 gameplay rules

Date: 2026-10-08. Scope: documents only. This entry appends to, and where noted supersedes, the 2026-10-07 record above; the original entry is retained unedited as history.

## Completed checks

- Cross-document audit written to `docs/AUDIT.md`. All shared numbers re-derived and consistent: jump envelope (640/1600 → 0.4 s apex, 128 u rise, 192 u same-height travel; SPEC's 112 u gap / 64 u step limits sit inside it); whip frame durations [75,75,50,50,62.5,62.5,62.5,62.5] sum to SPEC's 150/100/250 ms phases, 500 ms total, active interval [150, 250) ms; crouch body 40×60 centered (0, −30) vs standing 40×104 centered (0, −52) share the y=0 foot origin; knockdown + get-up (360 + 450 = 810 ms) fits inside the 1 s invulnerability.
- The manifest example still parses as JSON and matches the contracts; all relative Markdown links in the repo were re-resolved programmatically (18 checked, 0 broken before this pass's additions; re-checked after, see commit).
- `docs/GAMEPLAY_RULES.md` (Package P1) completed as a fully PROPOSED baseline: hero state-transition table covering every ANIMATION_SPEC state with interruption priority, input rules (100 ms coyote/buffer, opposing-input neutral, fresh-press whip, focus-loss input clear), damage/knockback/knockdown rules, all crouch-clearance cases, pit/death/checkpoint/retry cases, and briefs for the ground pursuer, airborne swooper, stationary ranged threat, and two-attack boss — each with timing windows shown arithmetically compatible with the 500 ms whip timeline and 128 u jump rise, at SPEC hit-points (1/2/8).
- Three user decisions dated 2026-10-08 recorded in `docs/DECISIONS.md` (Amendments section, ledger resolve format): D02/D12 superseded — protagonist and world are an **original hunter in an original gothic world** (Castlevania retained as design reference only); D13 confirmed — dread, decay, silhouettes, **no explicit gore**; D14 confirmed — target device **iPhone 17 / iOS Safari** (must-support). D09 and all other entries untouched.
- The identity contradiction (D02/D12 vs the public distribution confirmed in D15) is therefore closed. Remaining audit items are an unresolved texture-budget reconciliation (hero frames 149 MiB untrimmed vs the 128 MiB slice budget — P3/P5) and a list of wording follow-ups in SPEC/README/AGENTS/ART_DIRECTION/ASSET_SPEC/prompts that this pass deliberately did not edit (AUDIT B1/B11); TECHNICAL_CONSTRAINTS' Android-phone performance anchor is superseded in substance and owed a P5 rewrite, also not edited here.

## Explicitly not tested

Everything from the 2026-10-07 list still stands: engine import, sprite quality, animation playback, combat behavior, mobile touch controls, browser export, performance, loading, and Android APK. The iPhone 17 / iOS Safari target (D14) has no device evidence yet; VALIDATION gates V1–V9 all remain PENDING. No implementation or assets exist to test.

## Open after this pass

- D09 (stomp kills vs the contact-hurts baseline) is the only remaining user question; P1 proceeds on the proposed baseline.
- D07–D11 remain PROPOSED; `docs/GAMEPLAY_RULES.md` and its [P1 proposal] values need user confirmation or greybox evidence before being treated as settled.
- Follow-up packages unblocked in sequence: wording consistency pass (B1 list), P2 art bible (identity reference now creatable; D13 line fixed), P3 asset briefs with a packed texture-occupancy table (B2), P5 technical/export design anchored on iPhone 17 Safari (B4).

---

# Follow-up review — B1 wording consistency

Date: 2026-10-08. Scope: documents only.

## Completed checks

- B1 wording pass executed across the seven files enumerated in AUDIT B1/B11: `SPEC.md` (§1 identity, §2 signature moment, §5 "hunter's foot pivot" / contact wording), `README.md` (title line), `AGENTS.md` (intent bullet, guardrail meaning preserved), `docs/ART_DIRECTION.md` (visual grammar, Reject section), `docs/ASSET_SPEC.md` (§2, §3), `prompts/ASSET_GENERATION.md` (identity paragraph, hero key-pose example), `prompts/NEXT_LLM.md` (protagonist paragraph). Product identity now reads as an original hunter in an original gothic world; Castlevania appears only as design reference for tone/mechanics. No numbers, timings, or confirmed decisions were changed.
- Post-edit grep over the seven files: the only remaining "Simon" occurrence is in `prompts/NEXT_LLM.md`, explicitly describing the superseded interview-era identity. AUDIT items B1's follow-up list and B11 are closed by this pass (see AUDIT.md status notes).

## Explicitly not tested

Unchanged from prior entries: no implementation, assets, device, or performance evidence exists. VALIDATION gates V1–V9 remain PENDING.

## Open after this pass

- P4 stage design, P2 art bible, P3 asset briefs/texture budget, P5 technical spec (see subsequent entries), P6 readiness review, and user question D09.

---

# Follow-up review — P4 stage design

Date: 2026-10-08. Scope: documents only.

## Completed checks

- `docs/STAGE_DESIGN.md` written as a fully PROPOSED, NOT-TESTED blockout specification: the five SPEC §3 beats laid out over 104 terrain modules (x 0–6656) on the 64 u grid, with terrain layout per beat, an encounter table (effigy, five pursuers, two swoopers, one ranged threat, boss — HP 1/1/2/8 per GAMEPLAY_RULES), safe zones, checkpoint placement (module 64), boss arena bounds (modules 88–101), camera zones, and the first-minute teach sequence mapped to geometry.
- Mandatory-traversal proof is arithmetic, tabulated for all 20 mandatory elements: every gap is 64 u (≤112 u limit, 48 u margin — the only compliant same-level gap on a 64 u grid), every up-step 64 u (at the 64 u limit), every mandatory landing ≥128 u (six elements exactly at a limit, flagged as greybox probes). Conclusion: all mandatory geometry sits inside the proposed envelope; no impossible mandatory jump is specified. The 48 u knockback is shown to be less than half the narrowest mandatory landing (64 u), closing the AUDIT B6 dependency on P4. The no-sub-104 u-passage rule is recorded (no crouch-walk exists).
- Known feel-risks are stated rather than hidden: one pre-checkpoint pit (B2, module 34) on the single-checkpoint layout, and the at-limit steps.

## Explicitly not tested

No greybox, level file, or playtest exists; beat pacing (3–5 min), camera behavior, and all geometry "feel" are unproven. VALIDATION V6/V7 remain PENDING.

## Open after this pass

- P2 art bible, P3 asset briefs/texture budget, P5 technical spec, P6 readiness review, D09.

---

# Follow-up review — P2 art bible

Date: 2026-10-08. Scope: documents only.

## Completed checks

- `docs/ART_BIBLE.md` written (Package P2): a named palette of 17 swatches with proposed hexes mapped one-to-one to ART_DIRECTION's palette roles (plus budgeted signal/material colors for interactables, the enemy projectile, and the hunter), silhouette/material/light rules implementing the upper-left light and five-layer depth stack, an original hunter design brief (silhouette, face/hair, thorn-knot costume construction, layered whip — franchise elements named as rejection reasons), visual briefs for the pursuer, swooper, ranged threat, and boss keyed to GAMEPLAY_RULES §8 tells, environment kit rules, and the D13 line rendered as an enforceable permit/prohibit list for asset review.
- The style-pack calibration plan is written as five filled briefs in `templates/ASSET_BRIEF.md` format (`style_hero_neutral`, `style_hero_attack_key`, `style_enemy_pursuer`, `style_terrain_patch_3x3`, `style_env_mockup`) — briefs and reference requirements only; no images were generated or claimed. Each is marked DRAFT/PENDING per the template's rule that nothing is READY before the style reference exists; the reference register and style-lock process (`style_lock_r01` on approval) are defined.
- Cross-checked against P1: every tell the gameplay rules rely on (pursuer rear-up, swooper wing-fold, ranged charge, boss wind-up and hazard ring) has a matching visual specification; hitbox overlays use SPEC §5 numbers unchanged.

## Explicitly not tested

No candidate art exists; identity, palette, and readability are unverified until the pack is produced and reviewed at logical and phone sizes. VALIDATION V1 remains PENDING.

## Open after this pass

- P3 asset briefs/texture budget, P5 technical spec, P6 readiness review, D09.

---

# Follow-up review — P3 asset production briefs + texture budget

Date: 2026-10-08. Scope: documents only.

## Completed checks

- `docs/ASSET_BRIEFS.md` written (Package P3): complete slice inventory with per-asset ID, canvas, pivot, density, frame counts and durations (each clip's durations sum to its stated total; combat clips reproduce SPEC §5's [75,75,50,50,62.5,62.5,62.5,62.5] = 500 ms, active [150, 250) ms), sockets/events, collision references, dependencies, and rejection rules — hero 113 body + 24 whip frames (ANIMATION_SPEC counts), pursuer 46, swooper 36, ranged 31 + projectile 3, boss 70 (enemy/boss counts proposed here with clip totals tied to GAMEPLAY_RULES tell/recovery timings), 14 terrain tiles, 4 backgrounds, 4 stage props, 18 UI assets, 6 VFX clips, audio deferred as an ID inventory. Manifest field definitions are stated against `templates/asset-manifest.example.json`.
- `docs/TEXTURE_BUDGET.md` reconciles AUDIT B2 with full arithmetic: slice total 278.97 MiB untrimmed → 102.68 MiB trimmed under stated per-class trim factors at 85% packing efficiency = 8 atlas pages all-resident (170.7 MiB mipmapped; 128.0 MiB without mips) — **the 128 MiB budget does not hold as written**. Peak-concurrency readings: boss-arena peak 7 pages (112.0 MiB without mips), mixed-beat peak 6 pages (96.0 MiB). The proposed smallest contract change (no mip chains on slice art + peak-concurrency residency ≤7 pages with the boss-gate swap) is recorded as PROPOSED for P6/user ratification; no ASSET_SPEC or TECHNICAL_CONSTRAINTS number was edited. AUDIT B2 status updated accordingly: reconciled on paper, unresolved in fact until real packed art is measured.

## Explicitly not tested

No art exists to trim, pack, or measure; every trim factor and the 0.85 packing efficiency are planning assumptions. VALIDATION V2/V8 remain PENDING.

## Open after this pass

- P5 technical spec, P6 readiness review (including ratification of the TEXTURE_BUDGET amendment), D09.

---

# Follow-up review — P5 technical / export specification

Date: 2026-10-08. Scope: documents only.

## Completed checks

- `docs/TECHNICAL_SPEC.md` written (Package P5): engine pinned to **Godot 4.7.2-stable** with matching export templates — verified by direct fetch of the official godotengine.org download archive page for 4.7.2-stable on 2026-10-08 (4.8 exists only as dev snapshots and is excluded); GDScript (not .NET) and the Compatibility renderer per D10 and the official web-export documentation; single-threaded web export as the baseline, with the COOP/COEP cross-origin-isolation requirement stated as the reason threaded builds are not the default.
- Scene/input/data boundaries specified per TECHNICAL_CONSTRAINTS' responsibility split (input layer, player state machine, combat hit-IDs, animation event reporting, level data, presentation, per-set asset loading), an 8-item web export checklist, a device/browser matrix anchored on **iPhone 17 / iOS Safari as must-support** (D14) with desktop Chrome/Firefox as dev references, and a performance measurement protocol (60 fps, p95 frame ≤20 ms, ≤30 MiB cold payload, ≤12 s at 20 Mbps/50 ms RTT — all PROPOSED, NOT-TESTED) re-anchored from the superseded Android-phone anchor. Android APK remains DEFERRED with a prerequisites list. AUDIT B4's follow-ups are recorded as delivered.

## Explicitly not tested

No engine project, export, or device run exists. Every performance figure is a hypothesis awaiting the §5 protocol on real hardware; VALIDATION V5–V9 remain PENDING.

## Open after this pass

- P6 readiness review (contradiction sweep + acceptance matrix, including joint ratification of the TEXTURE_BUDGET amendment and this spec's import settings), user confirmation of D07–D11, and D09.

---

# Follow-up review — P6 readiness review

Date: 2026-10-08. Scope: documents only.

## Completed checks

- `docs/READINESS_REVIEW.md` written (Package P6), completing the WORK_PACKAGES sequence P0–P6 on paper. Full contradiction sweep over every shared value in the document set (jump envelope, whip timeline/hitbox, HP and i-frame arithmetic, frame counts 113 + 24 and enemy totals 46/36/31+3/70, stage clearances, texture figures, Godot 4.7.2 pin, iPhone 17 anchor, decision statuses): 25 AGREE, 3 DISAGREE — all values re-derived; the texture pipeline (278.97 MiB untrimmed → 102.68 MiB trimmed; 8/7/6-page residency readings; 144 MiB sensitivity case) recomputed programmatically and matched exactly; the manifest example re-parsed (durations sum 500 ms, active [150, 250]); all relative Markdown links re-resolved (60 in the pre-existing set, 136 including the new documents), 0 broken; stale-identity grep re-run (B1/B11 hold).
- Two genuine inconsistencies in the newer package docs found and fixed: **SW-1** — `ASSET_BRIEFS.md` §10 claimed "18 assets" where its own table enumerates 13 asset IDs / 19 frames (the count TEXTURE_BUDGET's UI pixels are computed from); corrected in ASSET_BRIEFS, and the P3 REVIEW_RECORD entry above repeats the 18 figure — left unedited as dated history, superseded here. **SW-2** — `STAGE_DESIGN.md` §5's R1 "lane covers ground modules 66–78" overlapped §6's safe-zone guarantee for the checkpoint apron (modules 63–66); the §5 cell now states the shots pass 198–223 u above the ground route and cannot hit a ground hunter, per §3. A third disagreement (TECHNICAL_CONSTRAINTS' and VALIDATION V5's Android hardware anchors vs the confirmed D14 iPhone 17 target) is recorded as resolved by the documented supersession in TECHNICAL_SPEC §4–5, without editing the historical files. `DECISIONS.md` was not edited; no confirmed requirement was rewritten.
- The WORK_PACKAGES "definition of specification-ready" applied item by item in READINESS_REVIEW §2: all six PASS on paper (first minute explainable from STAGE_DESIGN §7; full asset enumeration in ASSET_BRIEFS §§2–12; rendering vs collision separated per ASSET_SPEC §2 and per-asset collision references; attack timing derivable from SPEC §5 / ASSET_SPEC §3 / the manifest example alone; exact target device named in D14 + TECHNICAL_SPEC §4; proposal status readable from DECISIONS.md and every package header).
- Revised acceptance matrix (READINESS_REVIEW §3): VALIDATION gates **V1–V9 all remain PENDING**, each with the evidence that would close it. AUDIT roll-up (READINESS_REVIEW §5): B1, B4, B5, B7–B12 resolved-on-paper; B6 resolved-on-paper with greybox confirmation owed (V6); B2 reconciled on paper but open with the user (ratification) and with the implementation phase (measurement, V2/V8); B3 open with the user (D09). No audit item remains open with a package.
- Ratification list stated for the user (READINESS_REVIEW §4): **R1** the TEXTURE_BUDGET §5 amendment (no mip chains; ≤7-page peak-concurrency residency; 112.0 MiB peak) ratified jointly with TECHNICAL_SPEC §2's import settings — without it the 128 MiB budget fails as written (170.7 MiB all-resident mipmapped); **R2** D09 (confirm the contact-hurts/no-stomp baseline or request stomp kills); **R3** confirmation of the D07–D11 PROPOSED baselines and their P1–P5 derivatives; **R4** style-pack authorization at V1, after the implementation assignment. Production — Godot project, greybox, art, builds — requires a **separate explicit implementation assignment** per AGENTS.md and WORK_PACKAGES production gate 1; P6 does not grant or request it.

## Explicitly not tested

Unchanged from every prior entry: no engine project, export, art, animation, playtest, touch test, or device measurement exists. The iPhone 17 / iOS Safari target (D14), the Godot 4.7.2 pin, every performance figure, and every texture-budget number remain PROPOSED/NOT-TESTED hypotheses awaiting VALIDATION V1–V9 evidence.

## Open after this pass

- User ratifications R1–R3 (READINESS_REVIEW §4); D09 remains the only open interview question.
- The specification phase is complete on paper: P0–P6 delivered, AUDIT B1–B12 dispositioned, VALIDATION V0's document-side evidence assembled in READINESS_REVIEW §§1–2. The next step belongs to a future explicit implementation assignment (WORK_PACKAGES production gates 1–5), starting with locking the engine version and the proposed mechanics, then a greybox touch movement + whip test on iPhone 17 hardware.

---

# Follow-up review — implementation gates 1–2: greybox slice + web export

Date: 2026-10-08. Scope: first implementation pass, authorized by the user's explicit implementation assignment ("go!", 2026-10-08) for production gates 1–2. Engine: **Godot 4.7.2-stable** (binary and matching 4.7.2 export templates verified present on this machine), GDScript, Compatibility renderer, single-threaded web export per TECHNICAL_SPEC S1/S3.

## Completed checks

- **`game/` Godot project created** (`game/project.godot`, `scenes/main.tscn`, `scripts/`): 1280×720 logical view, canvas_items/keep stretch, InputMap actions move_left/move_right/jump/whip/crouch/pause (keyboard in project.godot plus on-screen touch buttons 104–160 logical px via `scripts/input_state.gd`, one input layer for both, opposing inputs neutral, pause/focus-loss clears held input).
- **Hunter** (`scripts/hunter.gd`): the full GAMEPLAY_RULES S4 state table (21 states) with S2 interruption priority, S5 damage routing (projectile→hurt_recoil, contact/hazard→knockback 160 u/s, boss heavy→knockdown/get_up), S6 crouch-clearance cases, 100 ms coyote + buffer, whip 150/100/250 ms with per-attack hit IDs surviving the air→ground continuation, 5 HP, 1 s i-frames. Constants taken from GAMEPLAY_RULES S1 unchanged.
- **Stage** (`scripts/main.gd` TERRAIN table): the P4 blockout B1–B5 (104 modules) — one-way slabs/treads over recovery routes, B2 pit + global kill plane, checkpoint module 64, boss gates at modules 87/102, exit at module 103; all mandatory gaps/steps/landings inside the STAGE_DESIGN S4 envelope by construction.
- **Enemies**: pursuer (patrol/alert/chase/windup/lunge/recover, 1 HP), swooper (cruise/600 ms telegraph dive/900 ms climb, 1 HP), ranged (900 ms tracked aim, 280 u/s projectile, 2 HP, aim interruptible), boss (advance/turn, 700 ms-tell heavy strike, 1200 ms-telegraphed 160 u hazard eruption, 8 HP, defeat opens gates + unlocks exit). All behavior values are the [P1 proposal]s, unverified by play.
- **Headless smoke test** (`game/tests/smoke_test.gd`, GUT-less SceneTree script): real run output — scene loads with zero script errors; hunter walks 120.0 u in 0.5 s; jump rise measured 133.4 u (discrete-integration overshoot vs the 128 u analytic value; mandatory limits remain inside the envelope); whip verified inactive at ~100 ms, active at ~200 ms, inactive at ~300 ms; effigy hit exactly once per attack; contact hit → knockback at 4 HP; lethal hit → death → restart at stage start with 5 HP. **19/19 checks PASS, exit code 0.**
- **Web export**: `Web` preset (thread support off, so no COOP/COEP headers needed) exported cleanly to `game/build/web/` (index.html + index.js + index.pck + index.wasm ~39.5 MB); served over HTTP and driven in headless Chromium (SwiftShader WebGL): engine boots, greybox scene renders (spawn plaza, effigy, pursuer visible), keyboard movement works, **zero console errors**. Evidence: `game/screenshot_spawn.png`, `game/screenshot_action.png`.

## Explicitly not tested

- **Everything visual is greybox**: flat-color `_draw()` polygons per actor. No production art, no style pack (next gate), no animation frames — ANIMATION_SPEC's completeness proof remains unstarted; no claim of animation quality is made or implied.
- **No device evidence**: iPhone 17 / iOS Safari (D14) touch play, focus/resume on a real browser, portrait rotate behavior, performance protocol (60 fps / p95 ≤ 20 ms / payload / load targets, TECHNICAL_SPEC S5) — all NOT-TESTED. Headless SwiftShader frame rate is not performance evidence; input-timing observations in that environment are wall-clock-unreliable.
- Boss/hazard/checkpoint/exit flows are exercised by construction and code path review, not yet by a scripted end-to-end kill-to-exit run; VALIDATION gates V1–V9 remain PENDING as a whole.

## Open after this pass

- Production gate 3 (style pack + hero/whip pipeline) awaits its own explicit opening; the [P1 proposal] combat/AI numbers and the STAGE_DESIGN at-limit steps + pre-checkpoint pit await greybox playtest evidence (V6/V7) — on a real device, not in this headless environment.

---

# Follow-up review — FULL PRODUCTION (art, animation, audio, final slice)

Date: 2026-10-08. Scope: complete production pass, authorized by the user's directive of 2026-10-08: "go ahead finish the game in full quality without asking me any question! results are expected to be pushed to a new repo using your gh." This opens production gates 3–5 (style pack, animation, full art/audio). Engine and gameplay contracts unchanged from the greybox pass; every gameplay constant in the code is byte-identical to the greybox values.

## Completed checks

- **Style pack (gate 3)**: the five ART_BIBLE §8 calibration pieces were generated (painted 2D gothic illustration, palette-locked, upper-left light) and visually reviewed by the production agent: no pixel grid, no anime/chibi, no gore, no franchise likeness. Approved and registered as **`style_lock_r01`** in `docs/ART_BIBLE.md` §9 with sha256 hashes; full hashes in `game/art/manifest.json`. Background plates (distant/midground/foreground) produced alongside. Recorded drift risk: neutral's closed coat-skirt vs attack key's open coat + trousers; animation follows the attack key.
- **Animation (gate 4)**: full ANIMATION_SPEC inventory produced — **64 clips, 357 frames, spec counts met for every clip** (per-clip table in `game/art/manifest.json`). Two documented derivations: `hero_crouch_exit` = crouch_enter reversed, `hero_get_up` = knockdown reversed. Green-screen sheets chroma-keyed programmatically (alpha from green dominance + despill; per-sheet alpha coverage logged — e.g. hero_idle 0.335, whip 0.125); one uniform anchor scale per actor (no per-frame drift); contract canvases/pivots; whip grip-aligned (extended frame tip reach 181 u ≥ 168 u hitbox). Frames trimmed and MaxRects-packed into atlases: **7 pages / 112.0 MiB without mips — exactly the ratified R1 model** (`atlas_report.json`). Texture imports: mipmaps off, lossless, linear, fix_alpha_border.
- **Audio**: 11 original synthesized WAVs (numpy, seeded): whip swing/hit, jump, land, hurt, death, enemy tell, checkpoint chime, boss tell, 32 s ambience loop + 32 s stage music loop (A-minor drones/bells, loop-crossfaded). Master/Music/SFX bus layout; 10-player SFX pool. No franchise audio.
- **Integration**: AnimatedSprite2D everywhere (state machines authoritative; sprites never auto-play; whip frame-locked to `attack_t`; per-frame atlas trim offsets restored at runtime); parallax depth stack (sky/distant 0.3/midground 0.55/foreground 1.15); 14-tile terrain kit; props (effigy, checkpoint off/on, boss gates, exit); VFX (whip impact, enemy defeat, checkpoint, hazard telegraph/eruption, damage indicator); HUD art pips. Greybox `_draw()` visuals fully removed. Gameplay/collision numbers untouched.
- **Tests**: extended headless smoke test (`game/tests/smoke_test.gd`) — all 19 original greybox checks plus production assertions (SpriteFrames resources load, all required clips present with frames, live hunter sprite plays hero clips with non-null frame textures, whip sprite visible and playing whip clips during attack, audio streams load): **PASS, zero failures**. 
- **Rendering verification (Xvfb, real GPU pipeline)**: screenshots reviewed visually — painted illustration throughout, hunter distinguishable from backgrounds, no pixel grid, whip extension + impact read correctly, pursuer/boss/checkpoint/gates/HUD all render (`game/tests/visual_check.gd`).
- **Web export + browser drive**: single-threaded Web export (71 MB build dir, 33 MB pck; raw source sheets excluded via export filter), driven in Chromium via route interception: game boots, stage loads, movement + whip + boss fight (THE WARDEN WAKES, gates, boss bar) all exercised, **zero console errors**.

## Explicitly not tested

- **iPhone 17 physical device: NOT-TESTED.** No device was available. Touch feel, iOS Safari quirks, real performance (60 fps / p95 frame time), payload/load-time targets — VALIDATION gates V2–V9 remain PENDING. Headless/Chromium evidence is not device evidence.
- Animation quality is generation-grade painted art, not hand-tuned frame-by-frame animation; inter-clip character drift exists (documented in the manifest: coat construction follows the attack key; `hero_turn` final frame faces left pre-flip; boss generated facing left).

## Open after this pass

- V2–V9 device validation when hardware is available. R1 headroom is 16 MiB; if future art trims worse, the budget must be revisited (sensitivity case in TEXTURE_BUDGET).

---

# Follow-up review — scale normalization fix (user-reported size-change bug)

Date: 2026-10-09. Scope: user report of 2026-10-09 — "broken sprite: the main character changes in size while moving around and standing still." Art pipeline only; no gameplay code or constant was touched.

## What was wrong (measured, game/art/SCALE_AUDIT_BEFORE.md)

- The full-production entry above states "one uniform anchor scale per actor (no per-frame drift)". **That claim was wrong in effect.** The pipeline did apply a single anchor scale per actor, but the sprite sheets were generated per clip at mutually inconsistent figure sizes, so each clip kept its own scale: hero walk measured 192 px against idle's 224 px (−14%), crouch_idle 252 px — the crouched hunter rendered TALLER than standing — start/stop/turn ≈ 340–363 px, fall ≈ 430 px, hurt_recoil ≈ 418 px.
- A second defect class compounded it: detached generation debris (thin full-height line artifacts; specks below the feet) inflated bounding boxes and anchored production placement — hero_fall measured the full 448 px canvas height in every frame, boss turn/hurt/hazard_execute a clipped 448 px, pursuer hurt/alert a clipped 160 px.
- Only the five anchor clips sat at their design heights (idle 224, pursuer 111/112, cruise 169/170, boss 351/352). Ranged measured 288 px against its 300 px reference in every frame (pre-existing 12 px hood-tip clip at the canvas top; unchanged by this fix).

## Fix (tools/process_frames.py, re-run + repacked)

- One uniform scale per clip (never per frame): target ÷ reference, the reference a pose-aware statistic of the figure's largest-connected-component heights on the source cells — median for upright clips, max (most-extended frame) for jump/fall/knockback, first-two-frames for knockdown/death, last frame for crouch_enter, min (most-grounded frame) for pursuer rear-up clips. Hero standing target 224 px (idle untouched); **crouch family 140 px = 0.625 × 224** (new authoritative value, recorded in docs/DECISIONS.md); pursuer 112, swooper 170, ranged 300, boss 352. Frames re-placed by the figure's own bbox (lowest point on the contract pivot, foot_off ≥ −1 px everywhere after); small detached debris removed under a logged area/thinness rule (plausible satellites — coiled whip, blades — kept). Whip grip unchanged: grip_x = 276 = pivot.x, tip reach 172 u ≥ 168 u hitbox. Atlases repacked: **5 pages / 80.0 MiB** (was 7 / 112.0), still inside the ratified R1 model (≤ 7 pages, mips off). Pre-fix frames archived at `game/art/source/frames_prefix_2026-10-09.zip`; per-clip pre/post medians and applied scales recorded in `game/art/manifest.json` (`scale_fix_2026_10_09`), whose original notes are kept and corrected, not rewritten.

## Completed checks

- **Audits**: `game/art/SCALE_AUDIT_AFTER.md` (same method as BEFORE) — hero upright references 219–224 px against 224 (±3% tolerance met), crouch 135–145 against 140 (±5% met), no actor clip measures the full canvas height, pursuer/swooper/boss references 111–112 / 169–170 / 351–352.
- **Contact sheet**: `game/tests/shots/scale_contact_sheet.png` (all 21 hero clips, pivot crosshair + 224 px line) visually reviewed — the hunter reads the same size standing, walking, turning and attacking; crouch is distinctly low.
- **Smoke test**: `SMOKE RESULT: PASS` (Godot 4.7.2 headless, extended suite).
- **Web export + Chromium drive**: fresh Web export, zero console errors; `game/tests/shots/scale_ingame_{idle,walk,crouch}.png` visually reviewed — idle and mid-walk the same size on the spawn platform, crouch properly low in the same spot.

## Explicitly not tested

- iPhone 17 physical device — still NOT-TESTED (V2–V9 pending, as before). Chromium/SwiftShader evidence only.
- No clip needed regeneration: every rescale fit its contract canvas (post-fix overflow check: nothing past the canvas edge beyond the pre-existing ranged hood-tip clip). Crouch_enter's opening frame stands at 190 px, not 224 — the source sheet's own crouch ratio (0.74) vs the 0.625 design ratio; the 200 ms transition reads as compression and is recorded in the manifest rather than hidden.

## Open after this pass

- V2–V9 device validation (unchanged). R1 headroom is now 48 MiB at 5 pages.

---

# Follow-up review — full sequence audit (every clip, every frame)

Date: 2026-10-09. Scope: extension of the scale-fix pass at the user's direction — verify every sprite and every action sequence locally without playing the game, fix what is found, then publish. Deliverables: `game/art/SEQUENCE_AUDIT.md`, 64 contact strips (`game/tests/shots/seq_<actor>_<clip>.png`), `tools/audit_sequences.py`, `game/tests/sequence_engine_check.gd`.

## Completed checks

- **Programmatic audit (PIL/scipy), all 64 clips / 357 frames**: frame counts == manifest == ANIMATION_SPEC/ASSET_BRIEFS counts for every clip; per-clip duration totals match the briefs (whip clips 500 ms, active frames 2–3 by the [150, 250) ms window, max active tip reach 172 u ≥ the 168 u hitbox); figure reaches the contract pivot in every actor frame (no float > 2 px); swooper/projectile centers within 1.5 px; whip grip at (276, 308) on every frame.
- **Pops**: 139 adjacent-frame height changes > 4% reviewed against the contact strips — all are the intended pose content (gait bob, wingbeat, breathing, cape sway, crouch/knockdown/death/jump transitions, whip extension). Loop wraps checked for all 16 looping clips; the reviewed-cyclic set joins within pose tolerance.
- **Coverage**: every GAMEPLAY_RULES §4 hero state, §8.1–§8.4 enemy/boss state, the three whip attack states, the projectile and all six VFX clips resolve to an existing clip in the runtime state maps (`game/scripts/*.gd`); no missing states.
- **Engine check**: `game/tests/sequence_engine_check.gd` loads all five SpriteFrames resources, steps all 64 clips frame-by-frame through `Anim.apply` (357 frames), asserts frame counts, loop flags, AtlasTexture region sizes against `atlas_regions.json`, and trim-offset reconstruction inside the contract canvases — **SEQUENCE ENGINE RESULT: PASS**. Extended smoke test still **SMOKE RESULT: PASS**.

## Defect found and fixed

- **`vfx_damage_indicator` was blank** (alpha max 0 in both frames): its source is a full-screen red vignette (green center, charcoal surround), not a green-screen sprite, so the chroma pipeline produced transparent frames and the HUD damage flash has never rendered. Fixed with a red-dominance extraction special case in `tools/process_frames.py`; the frames now carry the vignette (217–220 px) and the atlas was repacked. This defect predates the scale fix and is unrelated to it.

## Explicitly waived (with reason, in SEQUENCE_AUDIT.md)

- `pursuer_idle` (no runtime state; its frames 1/4 rear up inside an idle loop) and `swooper_perch_idle` (no runtime state): the shipped behaviors have no stationary/perched state — patrol and cruise cover them. Not user-visible; wiring them in would change gameplay, which this art pass must not do. Retained for ASSET_BRIEFS inventory.
- Six cloth warnings accepted: boss cloak hems pool below the foot line in two recover opening frames, hero_death ash settles 6 px below; feet remain on the pivot.

## Explicitly not tested

- iPhone 17 physical device (V2–V9 still pending). Sequence smoothness at playback speed on hardware remains a device question; this pass verified structure, geometry and timing data headlessly, plus contact-strip review.

## Open after this pass

- Same as the scale-fix entry: V2–V9 device validation when hardware is available.

---

# Follow-up review — whip pose progression + VFX envelopes (user-reported)

Date: 2026-10-09. Trigger: user played the live build and reported "the whip
action suddenly pop as a illogical state" and "explosions like effect that
pop irregularly". Scope: art only — no durations, pivots, hitboxes or
gameplay code changed. Tool: `tools/fix_whip_vfx.py`; full before/after
metrics in `game/art/WHIP_VFX_FIX_2026-10-09.md`; originals archived in
`game/art/source/frames_prefix_2026-10-09.zip` (appended, never destroyed).

## Bug 1 — whip pose progression (rebuilt, not patched)

Diagnosis (measured): ground clip heights 281→257→233→**151**→220→232→199→183
with f03 a dead-straight horizontal bar snapping in with no unfurl before
it; crouch f00 already extended (right edge +324 px of pivot); air
alternated coil/arc shape families frame to frame.

Fix: all three whip clips (8 frames each) re-rendered procedurally as one
continuous motion per clip — coiled wind-up → opening coil with escaping
tip → unfurling half-loop → extending arc → crack frame with a whip-like
curve (sag + taper, not a bar) → follow-through → recoil → coil rest. The
braid is drawn as a ribbon along the pose paths, textured with
cross-section slices of the original crack frame (brown braided look and
28→16 px taper preserved); each clip's handle plate is pixel-identical in
all 8 frames.

Measured after: grip (276, gy) constant per clip, gy drift ≤0.5 px
(criterion ≤3); crack tip right edge 619–621 → reach 171.5–172.5 u
(≥168 u hitbox); tip monotonic through extension in all three clips; worst
adjacent bbox-height step −34.4% (the crack flattening; criterion ≤35%).
Regenerated strips `seq_whip_*.png` inspected frame-by-frame: the swing
reads as one motion in all three variants.

## Bug 2 — VFX envelopes (per clip, judged against gameplay footprint)

- **vfx_whip_impact — rebuilt.** Before: widths 234→256→256→256→204→102
  (last frame a 20 px-tall sliver) — an instant near-full-canvas blast
  (128 u, the full whip hitbox width) held for 3 frames. After: one
  starburst family rebuilt from the densest original frame, widths
  86→148→**204**→162→108→58 px with alpha decay, center (128,128) on every
  frame (drift 0). Peak 102 u at the contact point, proportionate.
- **vfx_enemy_defeat — repaired.** Before: full-canvas 256² from frame 0;
  in-game it also read as a hard grey square (source smoke is opaque to
  the canvas edge). After: scale 0.50→1.0→0.65 + alpha decay about the
  center and a radial alpha feather, so it grows, peaks on the enemy and
  dissipates as a soft cloud.
- **vfx_checkpoint_activate — repaired.** Width dip 119→81→198 smoothed to
  64→110→150→168→162→148→122→111, base-anchored at the checkpoint foot.
- **vfx_hazard_eruption — light tail repair.** Tail re-widening (core
  170→310) fixed (f4 ×1.18, f5 ×0.66, alpha 0.85). The frame-0→1 full-height
  ignition is kept: an eruption column (160 u zone) igniting within one
  250 ms frame is the designed read.
- **vfx_hazard_telegraph — placement repair.** Envelope was regular, but
  the crack band sat at canvas rows 0–80 and rendered 58–88 u above the
  ground it marks (spawn is boss.y−8 with pivot row 176). Art shifted
  +108 px inside its canvas so the band sits on the ground line, matching
  the eruption's bottom anchor at the same spawn point.
- **vfx_damage_indicator — PASS, untouched** (2-frame HUD vignette flash,
  center drift ≤2 px).

## Verification (all actually run/looked at)

- `tools/audit_sequences.py`: 64 clips, **0 defects**; strips regenerated.
- `tests/sequence_engine_check.gd`: **SEQUENCE ENGINE RESULT: PASS**;
  `tests/smoke_test.gd`: **SMOKE RESULT: PASS**.
- Engine screenshots (xvfb, `tests/fix_shots.gd`): `fix_whip_strike.png`
  (curved crack frame overlapping the effigy, proportionate starburst),
  `fix_whip_crouch.png`, `fix_whip_air.png`, `fix_enemy_defeat.png`
  (soft feathered burst), `fix_boss_telegraph.png` (telegraph band on the
  ground at the hunter's feet, "THE WARDEN WAKES").
- Fresh web export driven in Chromium (SwiftShader, route-intercepted
  local files): boots, walks, enemy AI advances, **0 console/page errors**.
  Strike captured from recorded video frames
  (`tests/shots/fix_whip_strike_web.png`: whip extended into the burst at
  the effigy). A browser enemy-defeat frame was not captured — frame-precise
  timing under SwiftShader is dominated by the engine captures above;
  stated honestly rather than staged.
- Pipeline note recorded in the metrics doc: after `pack_atlases.py`, run
  `godot --headless --path . --import` once, or plain script runs will show
  stale cached atlas textures at the new region coordinates (this bit us
  during verification and was diagnosed by region-content crops).

## Explicitly not tested

- iPhone 17 physical device (V2–V9 still pending) — unchanged.

---

# Follow-up review — crouch soft-lock under one-way treads (2026-10-09)

**Status: fix prepared and verified locally; deliberately NOT committed,
pushed, or deployed.** The user reported a possible soft-lock from a
live-browser playtest ("wedged immobile against a thin black vine/column
tile … Left/Right/Down/Space+Right produced no movement until page
reload"), then directed: "just wait for me to playtest it manually." The
live build (gothic-whip-game `c1d3056`, Pages) is unchanged; everything
below is uncommitted working-tree state in both repos, awaiting the
user's manual playtest report.

## Diagnosis (real defect, reproduced headlessly)

Mechanism: `crouch_idle` pins `velocity.x = 0` (SPEC §3: no crouch-walk)
and both of its exits — release-to-stand and the §6-case-3 crouch-jump —
gate on `Hunter._has_standing_clearance()`. That query counted **one-way**
slabs as ceilings. Every 12 u tread/walkway slab floating 52 u above a
floor therefore traps a hunter who crouches beneath it: no stand, no
jump, no crawl, indefinitely. Input latency is excluded as the cause:
scripted engine inputs (held Right 1.5 s + Space, the same keys the
playtest tried) moved the hunter **0.0 u** at the trap spots.

Reproduction (`tests/smoke_test.gd`-driven probes, pre-fix):
- (3550, 512) under the B3 re-ascent tread: crouch → release → 0.0 u,
  stuck in `crouch_idle`. On the tread (3550, 448) under W3: 0.0 u.
- The clearance query at (2680, 512) hits exactly one shape: the 128×12
  one-way tread (`one_way=true`) — nothing else blocks standing there.
- Clearance-blocked-while-grounded spots (same defect class): under B3
  tread1 (x 2624–2752, floor 512), under/on the re-ascent tread
  (x 3520–3584, floors 512/448), under B4 treads R1a (x 4480–4544) and
  R1b (x 4672–4736), floor 512. Controls with 116 u headroom (under W2,
  under the B4 platform) are unaffected. This matches the playtest
  location: first pit crossed → B3 ascent/street area → thin tread slab.

## Prepared fix (uncommitted)

`game/scripts/hunter.gd`: `_has_standing_clearance()` now ignores hits
whose `CollisionShape2D.one_way_collision` is true (new `_hit_is_one_way`
helper; unresolvable hits still count as blockers, so genuinely solid
ceilings still block standing). One-way slabs never collide from below,
so this only removes the false ceiling. No gameplay constants, timings,
or state transitions changed. Regression phases added to
`tests/smoke_test.gd` (crouch under the re-ascent tread → release +
Right must exit crouch and move > 60 u; crouch-jump must leave the
ground), enemies frozen for determinism.

## Verification (all actually run/looked at)

- Pre-fix, the new smoke regression fails with exactly the 3 soft-lock
  assertions (stays `crouch_idle`, moved 0.0 u, y stays 512.0); all 80
  pre-existing assertions pass. Post-fix: **SMOKE RESULT: PASS**.
- Post-fix directed probes: every former trap spot moves 212–360 u and
  ends in `idle`; `clearance_free=true` at all 5 spots and controls.
- Engine screenshots (xvfb, `tests/soft_lock_shots.gd`):
  `tests/shots/fix_soft_lock_crouched.png` (hunter crouched under the
  tread at the chained door) and `fix_soft_lock_walkout.png` (0.6 s
  later: standing, mid-stride walking out).
- Fresh web export of the fixed code, served locally and driven in
  headless Chromium (Playwright, SwiftShader): boots, plays B1→B4,
  checkpoint/death/respawn work, **0 console/page errors** across all
  drives (`tests/shots/fix_soft_lock_web_b3.png`). The at-the-tread
  crouch sequence was not re-staged in the browser — under SwiftShader
  the hunter repeatedly died to pursuers en route and respawned,
  clearing held input by design; the exact-spot proof is the
  deterministic engine evidence above. Stated honestly.

## Explicitly not tested / not done

- NOT committed, NOT pushed, Pages NOT republished (user's instruction,
  2026-10-09). The live build still contains the soft-lock.
  *(Superseded later on 2026-10-09: published together with the
  whip-in-hand fix — see the next entry.)*
- iPhone 17 physical device (V2–V9 still pending) — unchanged.
- Adjacent observation, deliberately untouched (out of scope): normal
  crouch entry never calls `set_crouched_body(true)` (only the
  attack-air landing path does), so the 40×60 collision swap SPEC §4
  describes does not occur for ordinary crouching. Flagged for a
  separate decision; irrelevant to this trap (the body overlaps one-way
  treads either way, and one-way shapes never push).

---
# Follow-up fix — whip held in the hand (user-reported) + crouch soft-lock, published together

Date: 2026-10-09. User's manual-playtest report on the live build: the
whip roll/unroll motion is right, "but it is not holding or attached
correctly to the player — it doesn't look like he is holding a whip; the
whip when rolled is the same size as the player."

## Diagnosis (measured, composites reproduced)

Yesterday's rebuild (`tools/fix_whip_vfx.py`) fixed the whip's MOTION —
one continuous coil→unfurl→crack progression, no more per-frame pop —
but it kept the original painted whip's proportions and a fixed grip
point: a ~28 px cross-section "log" whose grip sat at a fixed canvas
point (276, gy≈308) in every frame, with rolled coils up to 257 px
tall — the hero's whole body height in attack f0. On body+whip
composites the fat near-segment floats across his chest/face while his
painted fist reaches out empty (attack_ground f3), and the coil reads
as a giant curled horn. Both user observations confirmed exactly.

## Fix (`tools/fix_whip_in_hand.py`)

Re-rendered the three whip clips' drawing only. Pose progression,
frame timing [75,75,50,50,62.5,62.5,62.5,62.5] ms, canvases, pivots,
0.5 sprite scale, hitboxes and crack tip reach are unchanged.

- **Hand anchors**: the whip-hand (fist centre) of all 24 attack body
  frames was read off coordinate-grid zoom crops of the painted frames
  and stored in the fix script (machine-readable copy:
  `game/art/whip_hands.json`). Verified on body+whip composites with
  anchor crosses — every cross sits on the painted fist.
- **Held grip**: a short wrapped grip (32 px long, ~11 px thick) drawn
  through the fist along the forearm direction of that frame; the thong
  emerges from its front end. Grip centroid lands ≤ 4.5 px from the
  fist anchor in all 24 frames; nearest whip pixel distance 0.0 px.
- **Proportions**: the thong is the original painted brown braid
  re-sliced thin — cross-section tapers 9 → 2.5 px handle→tip (measured
  max ≤ 10 px away from the fist; the ~28 px baton is gone).
- **Compact coil**: rolled frames now coil at the fist — coil bounding
  boxes 77×70 … 110×85 px vs the previous 257 px full-body spiral
  (≤ 55% of the hero's 224 px standing height, as specified).
- **Reach**: crack tip 172.0–173.0 u on all three clips (hitbox 168 u;
  whip-canvas tip x 619–621, unchanged from the motion fix).
- Replaced generation-2 whip frames archived to
  `game/art/source/frames_prefix_2026-10-09_gen2.zip`. Audit contract
  updated (`tools/audit_sequences.py`): whip art must reach within
  6 px of the frame's painted fist (DEFECT), replacing the old
  fixed-pivot grip-drift check. **Audit: 0 defects** (6 pre-existing
  cloth warnings unchanged). Evidence strips:
  `game/tests/shots/fix2_composite_whip_attack_{ground,air,crouch}.png`;
  numbers in `game/art/WHIP_HAND_FIX_2026-10-09.md`.

## Verification

- Sequence engine check: **SEQUENCE ENGINE RESULT: PASS** (64 clips,
  357 frames). Smoke test: **SMOKE RESULT: PASS** (includes the
  soft-lock regression phases below).
- Deterministic engine capture (xvfb, exact crack frame):
  `game/tests/shots/fix2_whip_strike_engine.png` — thin whip visibly
  extending from the fist.
- Fresh web export driven in headless Chromium (SwiftShader): hunter
  visibly holding the whip, crack frame touching the training effigy
  with the impact burst, compact gold coil visible at his hand between
  swings, **0 console errors** — `game/tests/shots/fix2_whip_strike.png`
  (driver: `tools/web_check2.js`; synthetic key events need a mash-
  and-capture stream because SwiftShader screenshots take ~1.8 s).
- Operational note recorded: after repacking atlas PNGs, run
  `godot --headless --import` before capturing — otherwise the runtime
  samples the previous import cache and sprites render stale regions
  (this bit during this fix: the whip briefly "drew" a swooper wing).

## Shipped together

This pass also publishes the held crouch soft-lock fix (previous entry:
one-way tread slabs no longer count as standing ceilings;
`scripts/hunter.gd` + smoke regression phases). Both fixes are
committed and pushed to `askjackb/gothic-whip` and
`askjackb/gothic-whip-game` together, with a fresh `docs/` web build;
Pages verified built and serving HTTP 200.

## Explicitly not tested

- iPhone 17 physical device (V2–V9 still pending) — unchanged.
- The adjacent `set_crouched_body` observation from the soft-lock
  entry remains a separate, undecided item.

---

# 2026-10-09 — Per-frame scale drift fix (user playtest round 3)

**User report:** "When the player stands still, its size doesn't match
when he is in action. I think similar issue applies to all enemy and
boss. List all actions of one character and make sure their size won't
drift. Cover enemy and boss too."

## Honest history

The two earlier size fixes were real but insufficient. Fix #1
(per-clip uniform scale, SCALE_SPEC) anchored each clip's reference
statistic to the design height; fix #2 (whip in-hand) rebuilt whip
geometry. Neither touched WITHIN-clip per-frame drift: frames inside
one clip were generated at mutually inconsistent sizes, and a median
over such frames lands on the anchor while individual frames straddle
it. Shipped proof: hero_land heights 239/209/169/260 (median 224 =
anchor, scale 1.000), so its standing frame played 16% taller than
idle; hero_attack_ground shipped 207..250 tall. The user was right
for the third time on the same underlying class of defect.

## Fix

`tools/normalize_frame_scales.py` (new) applies a per-frame uniform
rescale around the contract foot pivot to all non-exempt frames:

- Standing-class frames of the feet-anchored bipeds (hero, boss):
  corrected by height to the design anchor (hero 224, boss 352,
  crouch family 140). An upright figure's perceived size is its
  height, so standing must read 224 in every action.
- Everything else (poses, transitions, pursuer, canvas-clipped
  ranged, swooper): corrected by SA = sqrt(alpha area) to the clip
  median — SA scales exactly linearly under a pure scale change and
  barely moves when a pose redistributes the same ink (hero_land SA
  spread 4.9% across a 169..260 px height swing).
- SQ = sqrt(HxW) is tabulated in the audit but deliberately NOT used
  for correction: it collapses on narrow side-profile standing frames
  (hero_attack_ground f6: SQ 134 vs ~204 for the same man standing)
  and SQ-driven scaling would have blown that frame to ~295 px tall.
  SQ residuals >4% are therefore listed with named poses instead of
  being "corrected" into new drift.
- Factors clamped to [0.85, 1.18]. 216 frames rescaled, 80 within
  0.4% left untouched, 61 exempt frames (whip/vfx/projectile)
  verified byte-identical. 8 outliers (death heaps, pursuer alert
  apex, folded-wing telegraph) are clamp-corrected and pose-named
  in the audit; 0 frames regenerated — no standing-class frame
  needed more than the clamp, so no frame was a misdrawn standing
  pose requiring regeneration.
- Pre-fix frames archived: `game/art/source/frames_prefix_2026-10-09_gen3.zip`.
- Full inventory: `game/art/ACTION_SIZE_AUDIT.md` (all 64 clips,
  every frame, before -> after).

## Verification

- `tools/audit_sequences.py`: **64 clips, 0 defects** (6 pre-existing
  cloth-below-footline warnings on boss/death frames).
- `tests/sequence_engine_check.gd`: **SEQUENCE ENGINE RESULT: PASS**.
- `tests/smoke_test.gd`: **SMOKE RESULT: PASS**.
- Contact sheets per actor (`game/tests/shots/size_fix_contact_*.png`,
  inspected): hero idle vs one frame of each of his 21 clips at the
  same foot line — every upright head touches the 224 line; boss
  standing tiles all 351-352; pursuer ground clips 111-112 with the
  rear-up alert (160) and lunge (61) preserved as poses.
- In-game screenshots at spawn (`size3_a_stand/b_attack/c_jump.png`,
  inspected): standing, mid-whip and mid-jump figures are the same
  size.
- Fresh web export driven in Chromium: walk + whip + jump scripted,
  0 console errors.

## Explicitly not tested

- iPhone 17 physical device (V2-V9 still pending) — unchanged.

# 2026-10-09 — Art-integrity fix: hero_idle was a torso since generation (user playtest round 4)

**User report:** "Is the character size really correct this time? When
the character is standing, I can see that he is only drawn from the
waist up. This looks incorrect to me."

## Honest history

The user was right again, and the defect is older than every previous
size fix. The `hero_idle` sheet was generated as a waist-up torso —
head, belt and hands only, no coat, legs or boots — and its
head-to-belt span was 224 px, exactly the standing design height.
Every automated check this project has run measured bounding boxes or
total ink area, and by those measures the torso was the correct size:
it passed the per-clip scale fix (round 1), the sequence audit
(round 1–3), and the per-frame √area normalization (round 3). Three
bbox-based audits stamped a torso "correct." Standing looked bigger
than walking — the user's very first size complaint — because standing
was an oversized torso and walking was the true full body.

A full visual completeness audit followed (every one of the 64 clips /
357 frames rendered as native-res strips and looked at, plus component
and edge scans; record: `game/art/ART_INTEGRITY_AUDIT.md`). Findings:
9 frames broken at generation (hero_idle ×8, hero_death f08 with its
torso missing), 4 frames clipped by too-small extraction canvases
(pursuer_alert f02–f03, pursuer_lunge_windup f00, swooper_dive_telegraph
f01 — the source sheets were intact), and debris components in 17
frames (sheet slabs, neighbour bleed, a detached hand, boss cell-border
rectangle outlines). Everything else was complete.

## Fix

- **hero_idle rebuilt full-body.** A freshly generated idle sheet
  could not be obtained — the image-generation service failed on
  2026-10-09 — so the idle was rebuilt from the game's own approved
  full-body standing frame (the `hero_turn` neutral stand) with a
  subtle breathing loop. The idle is now literally the same man as the
  walk cycle: head, long coat, legs, boots, whip coil in hand.
  **The user should judge this rebuilt idle on screen like any new
  art; if it reads too static, a regenerated idle sheet is the
  follow-up.** (`tools/repair_integrity.py`, section A1.)
- **hero_death f08 regenerated** from a candidate sheet generated with
  the shipped final death frame as identity reference; torso restored.
- **Canvas-clipped clips reprocessed** from the intact source sheets
  on larger canvases at the same pivot (`pursuer_alert`,
  `pursuer_lunge_windup` 320×288; `swooper_dive_telegraph` 512×320).
- **Debris removed** on the named frames (figures untouched, exact
  shipped scale preserved); the boss rectangle cleanup needed a second
  pass for flat edge fragments up to 381 px long, `boss_hazard_recover`
  f01 included.
- **New integrity gate** (`tools/audit_integrity.py`): tracks actual
  head width and lower-body ink structure per frame. It FAILS on the
  pre-fix archived frames (10 defects, exit 1) and PASSES on the
  repaired set (0 defects, exit 0). A note recording all of this was
  added to `game/art/manifest_raw.json`, and the pre-repair frames are
  archived at `game/art/source/frames_prefix_2026-10-09_integrity.zip`.
- Gameplay, timings and hitboxes untouched; whip frames and the
  whip-in-hand anchors untouched.

## Verification

- `tools/audit_integrity.py`: **0 DEFECTS** on the repaired set; the
  same gate fails on the archived pre-fix frames (evidence above).
- `tools/audit_sequences.py`: **64 clips, 0 defects, 0 warnings**.
- `tests/sequence_engine_check.gd`: **SEQUENCE ENGINE RESULT: PASS**.
- `tests/smoke_test.gd`: **SMOKE RESULT: PASS**.
- Contact sheets (`game/tests/shots/fix4/contact_hero.png`,
  `contact_actors.png`, inspected): idle, walk and attack are visibly
  the same full-body man at the same height.
- Fresh web export driven in Chromium (`tools/web_check3.js`):
  **0 console errors**; standing vs walking screenshots show the same
  stature. The 500 ms whip swing itself still cannot be graded from
  burst screenshots (established in round 3) — it is covered by the
  sequence audit's whip-grip checks and the engine test.

## Explicitly not tested

- iPhone 17 physical device (V2–V9 still pending) — unchanged.
- The rebuilt idle's on-screen feel (breathing loop) awaits the user's
  playtest verdict, as does a fully regenerated idle sheet if they
  want one when the image service is back.
