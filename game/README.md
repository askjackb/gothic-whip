# Gothic Whip — greybox slice (game/)

A playable **greybox** of the first slice, built under the implementation
assignment of 2026-10-08 (production gates 1–2 in `../docs/WORK_PACKAGES.md`).
Engine: **Godot 4.7.2-stable**, GDScript, Compatibility renderer, single-threaded
web export. The authoritative design contracts live in the repository root
(`../SPEC.md`, `../docs/GAMEPLAY_RULES.md`, `../docs/STAGE_DESIGN.md`,
`../docs/TECHNICAL_SPEC.md`); this folder is their executable counterpart.

## GREYBOX status — read this before judging the visuals

Every visual in this build is a **flat-color rectangle/polygon placeholder**
drawn in code (`_draw()`), with a distinct silhouette per actor (hunter,
pursuer, swooper, ranged turret, boss, effigy). There is **no production
art, no animation frames, no sprite sheets** — the state machine implements
the GAMEPLAY_RULES S4 state table logically; the animation clips of
ANIMATION_SPEC.md do not exist yet and nothing here claims they do.
Telegraphs are geometric markers (color shifts, "!" glyphs), not effects.

## What is implemented

- **Hunter state machine** (all 21 P1 states): idle, start_move, walk,
  stop_move, turn, crouch_enter/idle/exit with S6 clearance cases, jump
  takeoff/rise/apex/fall by velocity region, land, attack_ground/air/crouch
  on the 150/100/250 ms timeline (hitbox x +40..+168, crouched y -48..-20),
  hurt_recoil, knockback (160 u/s), knockdown + get_up on the boss heavy hit,
  death -> checkpoint restart. Coyote time and jump buffer 100 ms each;
  fixed-height jump (-640 u/s, 1600 u/s² gravity, 240 u/s run); air steering
  600 u/s² [P1 proposal]. One hit per target per attack (attack IDs persist
  across the air->ground attack continuation); fresh whip press required;
  damage interrupts attacks the same step; 5 HP, 1 s i-frames.
- **Stage**: the full P4 blockout (104 modules, beats B1–B5) as collision
  terrain with one-way step/walkway surfaces over recovery routes. Every
  mandatory gap <= 112 u, step <= 64 u, landing >= 128 u (STAGE_DESIGN S4).
  Training effigy, checkpoint at module 64, B2 pit (kill plane), boss arena
  modules 88–101 with closing gates, exit door unlocked by boss defeat.
- **Enemies**: ground pursuer (patrol/alert/chase/lunge, 1 HP), airborne
  swooper (cruise/telegraphed dive/recovery climb, 1 HP), stationary ranged
  (tracked 900 ms aim, projectile, 2 HP), boss (advance/turn, 700 ms-tell
  heavy strike -> knockdown, 1200 ms-telegraphed ground hazard, 8 HP).
- **Flow**: checkpoint respawn (stage start before it), death/pit restart
  restores HP and resets encounters (boss re-locks the exit), victory state
  + play-again, pause (Esc / button / focus loss) with explicit resume,
  portrait rotate prompt over a paused game.
- **Camera**: horizontal follow with facing look-ahead and smoothing,
  vertical lock per zone (walkway raised), hard lock to arena bounds during
  the boss fight. 1280×720 logical view, canvas_items stretch, aspect keep.
- **Input layer** (`scripts/input_state.gd`): keyboard InputMap actions +
  on-screen touch buttons (104–160 px logical, shown on touch devices) feed
  one held/pressed state; opposing directions resolve to neutral; pause and
  focus loss clear all held input.

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | A / D or Left / Right | < > buttons |
| Jump | Space | JUMP |
| Whip | J | WHIP |
| Crouch (hold) | S or Down | CROUCH |
| Pause | Esc | II (top right) |

## Run / build

- **Play the web build**: serve `build/web/` from any static host and open
  `index.html`. The export is single-threaded (`variant/thread_support=false`),
  so no COOP/COEP headers are required.
- **Run in the editor**: open this folder as a Godot 4.7.2 project, F6/F5.
- **Re-export**: `godot --headless --export-release "Web" build/web/index.html`
  with the 4.7.2 export templates installed.
- **Smoke test** (no GUT, headless): `godot --headless --path . --script tests/smoke_test.gd`
  — loads the main scene, drives the hunter through the input layer, and
  asserts locomotion, jump rise, the whip [150, 250) ms active window,
  one-hit-per-attack, damage routing, and death->restart. Exit 0 = PASS.

`screenshot_spawn.png` / `screenshot_action.png` are captures of this build
running in headless Chromium (SwiftShader WebGL), kept as greybox evidence.

## Explicitly NOT done (do not claim otherwise)

- Production art, the P2 style pack, all animation frames, the whip as a
  separate visual layer — the next gate (production gate 3).
- Audio (music/SFX buses, tap-to-start gesture) — not in this gate.
- On-device testing: iPhone 17 / iOS Safari (D14 must-support), touch feel,
  performance protocol (TECHNICAL_SPEC S5), payload/load measurements —
  all still NOT-TESTED. Headless-browser rendering used SwiftShader and is
  not performance evidence.
- Greybox tuning of feel (VALIDATION V6/V7) and the at-limit 64 u steps /
  pre-checkpoint pit probes flagged in STAGE_DESIGN S4/S8.
