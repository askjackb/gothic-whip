# Instructions for contributors and LLMs

The current assignment is specification development. Do not create game code, initialize a Godot project, generate production art, or publish a playable build as part of filling out this framework. A later explicit implementation assignment can change that phase.

## Implementation assignment — 2026-10-08

The user gave the explicit go ("go!", 2026-10-08) for production gates 1–2 of `docs/WORK_PACKAGES.md`: a Godot project now exists in `game/` (greybox slice implementing SPEC.md / GAMEPLAY_RULES.md / STAGE_DESIGN.md mechanics, headless smoke test, single-threaded web export in `game/build/web/`). That authorization covers the greybox and its export only. **The style pack is the next gate**: do not generate production art, animation frames, or audio, and do not claim animation or device validation, until that gate is explicitly opened. Greybox visuals in `game/` are flat-color placeholders by design; the contracts in this repository remain the authority for every number.

Read README.md, SPEC.md, docs/DECISIONS.md, and docs/ANIMATION_SPEC.md first. Then read the contract relevant to your task.

- Preserve confirmed user intent: 2D, Godot, web playable, mobile target, future Android APK, an original hunter in an original gothic world with whip combat, restrained jumping, gothic dark detailed horror, no visible pixels, and fully animated supported actions. Castlevania is a design reference for tone and mechanics only — do not substitute franchise characters, costumes, or world elements, and do not revive the earlier Mario/crossover scope.
- The latest user requirement supersedes conflicting earlier brainstorming. Never silently turn an open question or assistant proposal into a confirmed requirement.
- Record proposed changes, reasons, dependencies, and validation in the decision ledger. User confirmation is required to change confirmed product requirements; routine document refinement is within scope.
- Use one authoritative definition for each shared number. Gameplay and asset contracts must agree about scale, pivots, attack timing, and coordinate spaces.
- Do not fill unknowns with fabricated approvals, generated-asset claims, benchmark results, or licensing claims.
- Keep scope bounded to the proposed first slice unless it is explicitly revised. Do not reintroduce an all-franchise roster, metroidvania map, inventory economy, online features, or procedural generation.
- State acceptance evidence and remaining uncertainty in each handoff. A self-review is not evidence of an on-device playtest.
- Deliver documents and examples only in this phase. Templates and JSON examples are not runnable implementations or completed assets.
- Review all changed relative links and JSON examples. Only claim checks that actually ran.
