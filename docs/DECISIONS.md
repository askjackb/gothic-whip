# Decision ledger

Captured from the scope interview on 2026-10-07. Only the user can confirm user intent; proposals below remain proposals unless accepted later.

| ID | Status | Decision / rationale |
|---|---|---|
| D01 | CONFIRMED | 2D; Godot; web playable; mobile target; Android APK later. |
| D02 | SUPERSEDED 2026-10-08 | Final identity answer: Simon Belmont in Castlevania’s world, fighting with his whip. — **Superseded by user decision 2026-10-08: original hunter in an original gothic world (shippable); Castlevania remains a design reference for tone/mechanics only. See Amendments.** |
| D03 | CONFIRMED | Platformer with restrained jumping rather than highly agile Mario movement. |
| D04 | CONFIRMED | Gothic, dark-themed, highly detailed horror world; this supersedes the assistant's bright-world proposal. |
| D05 | CONFIRMED | Final answer: “no visible pixel.” Use non-pixel illustrated art; Octopath can inform lighting/depth, not pixel sprites. |
| D06 | CONFIRMED | Final direction: “actually mostly Castlevania, more of that.” Castlevania is the primary design/world reference; no Mario content is required in the initial scope. |
| D07 | PROPOSED | One hero, one 3–5 minute stage, three enemy archetypes, one boss, one checkpoint. |
| D08 | PROPOSED | Landscape mobile with left/right/jump/whip/crouch controls, fixed-height jump, limited air steering. |
| D09 | PROPOSED | Contact hurts; no stomp kills. Not answered by user. |
| D10 | PROPOSED | Godot 4, GDScript, Compatibility renderer, single-threaded web export baseline; exact stable version to be pinned by the technical-spec contributor. |
| D11 | PROPOSED | 1280×720 logical view, 64-unit terrain grid, 112-unit standing hero height, 2× source art density. |
| D12 | SUPERSEDED 2026-10-08 | Exact Simon incarnation, costume, and canonical reference design. Character/world identity itself is confirmed under D02; do not substitute an original hunter/world. — **Superseded 2026-10-08 with D02: replaced by an original hunter design reference, to be created as a P2 (art bible) deliverable. See Amendments.** |
| D13 | CONFIRMED 2026-10-08 | Horror intensity: atmosphere/body horror/gore limits and intended audience. Proposed initial treatment: dread, decay, silhouettes; no explicit gore pending direction. — **Resolved by user 2026-10-08: the proposed treatment is confirmed ("that's fine, no need heavier"). See Amendments.** |
| D14 | CONFIRMED 2026-10-08 | Minimum Android hardware and browser versions; whether iOS Safari is a supported target or exploratory check. — **Resolved by user 2026-10-08: target device is iPhone 17, browser play in iOS Safari (must-support, not exploratory). See Amendments.** |
| D15 | CONFIRMED | Current work is scope, prompt/framework, and asset instructions/specification; publish to a new public repository; other LLMs fill in details. |
| D16 | DEFERRED | Native Android APK build and release, after browser slice validation. |
| D17 | PROPOSED | Repository name `gothic-whip-framework`; working label only. |
| D18 | CONFIRMED | Fully animated character, not a sliding/static graphic; every supported action and pose, including crouch, jumping, knockback, and death, needs complete animation. |
| D19 | PROPOSED | Interpret “crunch” as crouch and “knock off” as knockback/knockdown, as stated to the user. Detailed state inventory and frame counts are proposed in ANIMATION_SPEC.md. |

## Interview progression

1. Initial reference: modern HD Castlevania remake/remaster.
2. Expanded to a Konami character/style mixture.
3. Concrete example: Simon in Mario's world, which implies a broader crossover than Konami alone.
4. Narrowed to a platformer with Simon's whip and less agile jumping.
5. Gothic, dark, detailed horror; Octopath considered briefly as a visual reference.
6. Final refinement: primarily Castlevania, no visible pixels, and fully animated actions/poses.
7. Final identity answer: Simon Belmont in Castlevania’s world.

“All characters” is historical brainstorming, not the current slice requirement. The assistant's suggested bright illustrated world was not accepted and is superseded. No existing workspace project was selected or imported.

## How to resolve a decision

Record its ID, choice, reason, source of authority, affected documents/assets, and evidence needed. A contributor may refine a PROPOSED baseline with justification. A contributor must not claim a user confirmed an OPEN preference. If unanswered, retain the question and give a bounded recommendation.

## Amendments

### 2026-10-08 — identity (D02, D12), horror intensity (D13), target device (D14)

Recorded per "How to resolve a decision" above. All three resolutions are direct user statements dated 2026-10-08; they supersede the corresponding interview-era entries and are the resolving authority. D09 and all other entries are untouched.

**D02 / D12 — protagonist and world identity (SUPERSEDED)**
- Choice: the protagonist is an **original hunter in an original gothic world**. Castlevania remains a design reference for tone and mechanics only (whip-led combat, restrained jumping, dark gothic horror, no visible pixels). No Konami character, costume, name, or world element is used.
- Reason: D02's named-character identity cannot be licensed by this project, while D15 confirms public distribution (web build, later APK). The original identity had no lawful shipping path; the original-hunter identity does.
- Source of authority: user statement, 2026-10-08 ("Switch to an original hunter (shippable)").
- Affected documents: this ledger (D02, D12); follow-up wording pass still owed in `SPEC.md`, `README.md`, `AGENTS.md`, `docs/ART_DIRECTION.md`, `docs/ASSET_SPEC.md`, `prompts/ASSET_GENERATION.md`, `prompts/NEXT_LLM.md`, and the P0 row of `docs/WORK_PACKAGES.md` (enumerated in `docs/AUDIT.md` B1/B11 — not yet edited). D12's replacement deliverable — the original hunter design reference — belongs to P2 (art bible).
- Evidence needed: none for the decision itself. The P2 style pack must demonstrate the original design without franchise-derived elements; provenance recording per `docs/ASSET_SPEC.md` §6 applies to every asset.

**D13 — horror intensity (CONFIRMED)**
- Choice: the proposed treatment stands confirmed — dread, decay, silhouettes; **no explicit gore**, and no heavier direction.
- Reason: the user accepted the proposal as sufficient; the line is now fixed for art direction and asset review.
- Source of authority: user statement, 2026-10-08 ("that's fine, no need heavier").
- Affected documents: this ledger (D13); `docs/ART_DIRECTION.md` limits are now decidable in P2 against this line.
- Evidence needed: P2's art bible should state the enforceable limits (what counts as explicit gore) so asset review doesn't relitigate taste per asset.

**D14 — target device (CONFIRMED)**
- Choice: **iPhone 17, browser play in iOS Safari** is the target device/browser and a must-support requirement (not an exploratory check).
- Reason: user direction; fixes the anchor the performance hypotheses were missing.
- Source of authority: user statement, 2026-10-08.
- Affected documents: this ledger (D14); `docs/TECHNICAL_CONSTRAINTS.md` is **not** edited in this pass — its "agreed mid-range Android phone" performance anchor (60 fps, 95th-percentile frame ≤20 ms, ≤30 MiB cold payload, ≤12 s load) is superseded in substance and must be re-derived for iPhone 17 / iOS Safari as a P5 follow-up. The single-threaded web-export baseline (D10) aligns well with Safari constraints. Android APK remains DEFERRED (D16), unaffected.
- Evidence needed: P5 device/browser matrix plus on-device measurements (VALIDATION V5, V8) on the named hardware; nothing is validated until those run.

## Highest-value remaining questions

1. Which exact Simon costume/incarnation is the canonical visual reference? — **Answered by supersession 2026-10-08** (see Amendments): the reference is now an original hunter design, to be created in P2.
2. What horror intensity and minimum phone must this support? — **Answered 2026-10-08** (see Amendments): dread/decay/silhouettes, no explicit gore; iPhone 17 with iOS Safari.

Still open: D09 (stomp kills versus contact-hurts baseline) — the only remaining user question, and it does not block document work.
