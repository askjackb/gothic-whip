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
