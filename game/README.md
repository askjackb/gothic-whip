# Gothic Whip

An original 2D gothic action-platformer built in **Godot 4.7.2** (GDScript, Compatibility renderer). You are a lone hunter with a braided thorn-knot whip, crossing a ruined gothic stage: train on the effigy, fight off gaunt pursuers, diving swoopers and a grave-shot cultist, pass the checkpoint, and bring down the Warden in his arena.

**▶ Play it in your browser: https://askjackb.github.io/gothic-whip-game/**
(single-threaded web build — no special server headers needed; desktop Chrome/Firefox and mobile Safari are the targets)

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | ←/→ or A/D | ◀ ▶ buttons |
| Jump | Space | JUMP |
| Whip | J | WHIP |
| Crouch (crouch-whip) | S / ↓ | ▼ |
| Pause | Esc / P | ❚❚ |

Rules of the world: the whip is your only weapon; touching an enemy hurts (1 HP of 5); there is no stomp attack. The boss's heavy strike knocks you down; his ground hazard is telegraphed before it erupts — move. Death returns you to the last checkpoint (or the stage start) with full HP.

## Debug aid (development only)

Press **F9** to warp to just outside the boss arena. It exists so screenshots and boss-flow checks don't need a full playthrough; it is not a gameplay feature.

## What's inside

- `project.godot`, `scenes/`, `scripts/` — the game. State machines are authoritative; sprites never drive logic. Gameplay numbers come from the design contracts in the companion spec repo (below).
- `art/` — production art: style-lock references (`art/source/`, hashed in `art/manifest.json`), generated sprite sheets, packed texture atlases (5 pages, 80 MiB, mipmaps off), terrain tiles, backgrounds, props, UI, and 11 original synthesized WAV files (no samples, no franchise audio).
- `tests/smoke_test.gd` — headless verification: 19 gameplay checks plus production assertions (animation clips exist and play, audio loads). Run: `godot --headless --path . --script tests/smoke_test.gd` → expect `SMOKE RESULT: PASS`.
- `docs/` — the prebuilt web export served by GitHub Pages (present in the `gothic-whip-game` repo).
- The art/audio pipeline (`tools/`, frame processing, atlas packing, audio synthesis, web verification) lives in the companion repo.

## Provenance and limitations (stated plainly)

- **Art**: AI-generated painted illustration, locked to an approved five-piece style pack (`style_lock_r01`), generated on green screen, chroma-keyed and normalized programmatically. The cast is fully original — gothic horror is the tone reference only; no franchise characters, costumes, names, or audio are used.
- **Coverage**: the full animation inventory shipped — 64 clips / 357 frames. Two clips (`hero_crouch_exit`, `hero_get_up`) are documented reverses of their counterpart clips. Minor inter-clip drift exists and is recorded in `art/manifest.json`.
- **Audio**: all sounds and both music loops are original numpy syntheses.
- **Not yet validated**: **iPhone 17 / iOS Safari physical-device testing has not happened** (no device was available during production). Touch feel and on-device performance remain open validation items. The animation is generation-grade painted art, not hand-tuned frame-by-frame work.

Design contracts, the decision ledger, and the production review live in the companion repo: https://github.com/askjackb/gothic-whip (`game/` there is this same project).
