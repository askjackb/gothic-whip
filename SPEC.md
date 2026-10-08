# Product specification — v0.1

## 1. Intent and authority

**Confirmed:** A 2D Godot platformer for mobile, playable on the web, with a future Android APK. An original hunter fights with a whip in an original gothic world. Jumping is less agile than Mario. The world is dark, gothic, highly detailed, and horrific. Castlevania is the design reference for tone and mechanics only; no franchise character or world element is part of the product identity.

**Confirmed refinement:** Primarily Castlevania as the design reference; no visible pixel art. Every supported action and pose must be fully animated, including crouch, jump, knockback/knockdown, recovery, and death. Octopath may inform depth/lighting only. See [the full animation contract](docs/ANIMATION_SPEC.md). The identity is confirmed (user decision 2026-10-08, see [the decision ledger amendments](docs/DECISIONS.md)): an original hunter in an original gothic world. The hunter's design reference is an original creation produced by the P2 art bible ([docs/ART_BIBLE.md](docs/ART_BIBLE.md)); no franchise character, costume, or world element is used.

All numerical values and slice counts below are **proposed starting points**, not measured results or confirmed user decisions.

## 2. Experience pillars

- **Whip distance matters:** the player wins through spacing, reading a tell, and committing to a strike.
- **Weight without frustration:** deliberate movement, readable landings, responsive inputs, and modest forgiveness.
- **Horror with legibility:** detailed atmosphere surrounds a clearly readable hero, enemies, and traversable surfaces.
- **Touch is primary:** the complete first slice can be played with two thumbs without precision acrobatics.

The signature proposed moment: the hunter crosses a short broken walkway, lands in a gothic courtyard, waits out an enemy's approach, and kills it with a clearly readable whip strike.

## 3. First playable slice — proposed future milestone

One hero, one 3–5 minute successful stage, three enemy archetypes, one boss with two attacks, one checkpoint, and one exit. Learning and retries may take longer. One environment kit is reused across the stage.

Loop: advance → read terrain/enemy tell → position or jump → whip → receive hit/kill feedback → reach checkpoint → defeat boss → exit/retry.

First minute: safe movement space; isolated whip target; short recoverable gap; one ground enemy; then a gap and enemy combined with safe landing space. No off-screen first-hit attacks or mandatory blind jumps.

Proposed stage beats: tutorial threshold (0–45 s), ground patrol court (45–90 s), ruined walkway (90–150 s), checkpoint and mixed encounter (150–210 s), boss gate/arena (210–300 s). These are pacing goals, not a prescribed map or speedrun timer.

Enemy archetypes: ground pursuer, slow airborne swooper with a reachable attack window, stationary telegraphed ranged threat. Names and appearances remain open. The boss tests spacing and jumping with one close-range attack and one clearly signaled ground hazard. All threats must be beatable with the base whip and base jump.

## 4. Controls and motion contract — proposed

Landscape, left/right buttons on the left; jump and whip on the right, plus a dedicated crouch button; pause separate. Desktop equivalents: arrows/A-D, Space, J, down/S for crouch, Escape. No run modifier, inventory button, directional whip, double jump, wall jump, dash, stamina, or combo chain in this slice.

Use one fixed-height jump as the initial baseline, limited air correction, no midair instant reversal. Hold crouch while grounded to lower the collision body; release to stand only when clearance exists. Crouched whip is supported, crouch-walking is excluded from the initial baseline. Jump from crouch exits into a normal jump only with standing clearance. Coyote time and jump buffering each start at 100 ms. “Heavy” must not mean delayed button registration. Opposing horizontal inputs resolve to neutral. Simultaneous move+jump+whip must be supported; releasing, cancelling, or losing focus clears held input.

Geometry is measured in the logical units defined in [ASSET_SPEC.md](docs/ASSET_SPEC.md). Starting movement proposal: horizontal top speed 240 units/s, gravity 1600 units/s², initial jump velocity -640 units/s. Without collision or attack effects, this gives a 0.4 s apex, 128-unit rise, and 192-unit same-height travel at full speed. Initial mandatory gaps should be at most 112 units, mandatory upward steps at most 64 units, and landing platforms at least 128 units wide. These conservative margins still require touch playtesting. No final map dimensions before a measured jump envelope.

Grounded whip strikes stop horizontal movement during the attack; airborne strikes preserve existing trajectory and allow no extra jump height. Facing locks until recovery ends. No repeat attack from holding the button; a fresh press is required. No attack cancelling in the initial baseline. Damage interrupts attacks and disables outgoing hitboxes. Jump requests during a grounded attack obey the normal 100 ms buffer and otherwise expire.

## 5. Combat and failure contract — proposed

Ground, crouched, and airborne whip variants use the same timeline. Crouched reach retains the same x bounds but shifts its active y interval to -48 to -20. One horizontal whip strike: 150 ms anticipation, 100 ms active, 250 ms recovery (500 ms total). Collision activates on the gameplay timeline, never inferred from opaque sprite pixels. Each target takes at most one hit per attack. At default scale, the active region is x=+40 to +168, y=-82 to -46 relative to the hunter's foot pivot while facing right; left-facing mirrors the x bounds. These are tunable candidates requiring an overlay review against the illustration.

Five health units; ordinary contact costs one; pits cause checkpoint restart after a visible fall/death transition; no limited lives or score requirement. Ordinary damage triggers animated knockback and recovery; heavy boss hits trigger knockdown and get-up. Lethal damage overrides both with a death animation and final settled pose. Invulnerability lasts 1 s after damage, indicated with a non-strobing tint. Enemy contact, including landing on an enemy, hurts the hunter in the proposed baseline; stomp kills remain an unresolved preference. Start with one hit to kill basic enemies, two for the ranged enemy, and eight for the boss. Values are intentionally provisional.

Checkpoint restart restores health and encounter state. Boss defeat unlocks the exit. An explicit retry works after death and completion. Save persistence is not required for this short slice.

## 6. Camera, readability, and mobile UX — proposed

Use a 1280×720 logical view with proportional scaling and letterboxing as needed to preserve level visibility. Camera follows horizontally with bounded look-ahead, smooths modestly, and locks vertically per encounter. Never hide the required landing zone. No camera roll or mandatory shake. Offer reduced effects and separate music/SFX controls.

Touch targets: at least 48 CSS pixels equivalent after viewport scaling, initially aim for 64. Respect display safe areas. Gameplay threats must remain readable outside thumb-covered zones. Pause on focus loss and provide an explicit resume action. Portrait displays a rotate prompt with an accessible pause state; verify actual behavior on browsers rather than relying on orientation locking.

## 7. Scope exclusions

No full Konami/Nintendo roster, character swapping, multiple worlds, exploration ability gates, campaign, narrative cutscenes, crafting, upgrades, multiplayer, backend, ads, monetization, procedural levels, or finished Android release in the first slice. They are outside the proposed baseline, not promised future work.

This repository itself ships **only planning documents, prompts, templates, and acceptance criteria**. No first playable is being built now.

## 8. Success criteria and stop conditions

The future slice passes only if real mobile touch play, combat readability, stable visual identity, and the agreed performance/device targets pass [VALIDATION.md](docs/VALIDATION.md). Pretty screenshots alone do not pass. Stop expanding content if the first mixed jump/whip encounter is frustrating or the hero cannot be distinguished from the background.

Unresolved hardware targets, visual treatment, character design reference, and horror intensity must be specified before production; they do not prevent further documentation work.
