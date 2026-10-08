# Decision ledger

Captured from the scope interview on 2026-10-07. Only the user can confirm user intent; proposals below remain proposals unless accepted later.

| ID | Status | Decision / rationale |
|---|---|---|
| D01 | CONFIRMED | 2D; Godot; web playable; mobile target; Android APK later. |
| D02 | CONFIRMED | Final identity answer: Simon Belmont in Castlevania’s world, fighting with his whip. |
| D03 | CONFIRMED | Platformer with restrained jumping rather than highly agile Mario movement. |
| D04 | CONFIRMED | Gothic, dark-themed, highly detailed horror world; this supersedes the assistant's bright-world proposal. |
| D05 | CONFIRMED | Final answer: “no visible pixel.” Use non-pixel illustrated art; Octopath can inform lighting/depth, not pixel sprites. |
| D06 | CONFIRMED | Final direction: “actually mostly Castlevania, more of that.” Castlevania is the primary design/world reference; no Mario content is required in the initial scope. |
| D07 | PROPOSED | One hero, one 3–5 minute stage, three enemy archetypes, one boss, one checkpoint. |
| D08 | PROPOSED | Landscape mobile with left/right/jump/whip/crouch controls, fixed-height jump, limited air steering. |
| D09 | PROPOSED | Contact hurts; no stomp kills. Not answered by user. |
| D10 | PROPOSED | Godot 4, GDScript, Compatibility renderer, single-threaded web export baseline; exact stable version to be pinned by the technical-spec contributor. |
| D11 | PROPOSED | 1280×720 logical view, 64-unit terrain grid, 112-unit standing hero height, 2× source art density. |
| D12 | OPEN | Exact Simon incarnation, costume, and canonical reference design. Character/world identity itself is confirmed under D02; do not substitute an original hunter/world. |
| D13 | OPEN | Horror intensity: atmosphere/body horror/gore limits and intended audience. Proposed initial treatment: dread, decay, silhouettes; no explicit gore pending direction. |
| D14 | OPEN | Minimum Android hardware and browser versions; whether iOS Safari is a supported target or exploratory check. |
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

## Highest-value remaining questions

1. Which exact Simon costume/incarnation is the canonical visual reference?
2. What horror intensity and minimum phone must this support?

Ask only unresolved questions relevant to the next task; do not repeat the entire interview.
