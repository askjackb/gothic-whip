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
