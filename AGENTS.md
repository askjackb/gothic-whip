# Instructions for contributors and LLMs

## Full production assignment — 2026-10-08 (current)

The user directed on 2026-10-08: "go ahead finish the game in full quality without asking me any question! results are expected to be pushed to a new repo using your gh." This opened ALL production gates (style pack, animation, audio, full art) and forbids asking the user questions — work autonomously and document decisions. Status: production is COMPLETE as of 2026-10-08 (see `docs/REVIEW_RECORD.md`, full-production entry): style lock `style_lock_r01`, 64 clips / 357 frames, 11 synthesized audio files, 7 atlas pages / 112.0 MiB, extended smoke test PASS, web export verified in Chromium with zero console errors. The playable repo is `askjackb/gothic-whip-game` (Godot project + `docs/` web build on GitHub Pages). Outstanding: VALIDATION V2–V9 device evidence (iPhone 17) — pending hardware; never claim it exists.

Earlier phase text (specification-only phase; greybox gates 1–2 authorization) is superseded by this assignment and retained in git history.

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
