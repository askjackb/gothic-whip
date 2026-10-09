# Scale audit — AFTER (scale normalization fix, 2026-10-09)

Method: identical measurement to SCALE_AUDIT_BEFORE.md (alpha > 40, full
bounding box and largest-connected-component bbox of the figure, on the
final packed frames; foot_off = pivot.y − LCC bbox bottom, + = floats).

## Findings (measured)

- Hero standing-scale references (LCC medians of upright clips): idle 224,
  walk 224, start_move 224, stop_move 224, turn 224, land 224,
  attack_ground 224, hurt_recoil 224 — all exact against the 224 target
  (±3% tolerance). attack_air 219 (−2.2%). Extension references of
  jump_takeoff/jump_rise/jump_apex/fall/knockback: max 223–224.
  knockdown/death opening frames: 224 (clip max 229, +2.2%).
- Hero crouch family against the 140 target (±5% = 133–147): crouch_idle
  135–145 (median 140), attack_crouch 135–143 (median 140). crouch_enter /
  crouch_exit run 190 → 140 (anchored on the crouched end frame; the
  190 px opening is the sheet's own shallower transition pose).
- foot_off ≥ −1 px across all actor frames (two frames at −1 = rounding):
  feet sit on the contract pivot; airborne mid-stride frames float by
  pose only.
- Debris gone: no actor clip measures the full canvas height any more
  (pre-fix: hero_fall 448, boss turn/hurt/hazard_execute 448, pursuer
  hurt/alert 160 with the figure clipped at the canvas top). Boss
  turn 352, hurt 352 (were clipped 448); pursuer hurt 112 (was 160).
- Pursuer references 111–112 against 112 (alert/lunge_windup anchored on
  their most-grounded frame at 111–112; the rear-up pose still reaches
  132–160 by design). Swooper medians 169–170 against 170. Boss medians
  351–352 against 352 (strike_execute reaches 424 with the weapon
  overhead — pose, inside the 448 px headroom).
- Ranged: all six clips now mutually consistent at a measured 288 px —
  the 300 px design figure on a canvas with only 288 px above the
  pivot; the ~12 px hood-tip clip is pre-existing (identical in the
  BEFORE audit and in the shipped 2026-10-08 build), not a fix
  regression. Recover rose 269 → 288 to match the family.
- Whip grip/tip unchanged: grip_x = 276 = pivot.x, grip_y 308–310 vs
  pivot.y 308, max tip_x 620 → 172 u of reach from the node origin
  (hitbox needs 168 u). Per-frame component counts fell (debris removed),
  registration did not move.
- Within-clip spread that remains is pose, not scale: land 169–260
  (descent extension → impact compression), jump_apex 189 tucked vs
  224 extended, pursuer_lunge 47–112 (tucked mid-leap), death clips
  collapsing to ash (hero_death down to 42 px).
- vfx_damage_indicator measured empty at alpha > 40 in the BEFORE audit
  and in the first AFTER audit: its source is a full-screen red vignette,
  not a green-screen sprite, so the chroma path produced blank frames
  (the HUD damage flash never rendered). Fixed in the sequence-audit
  pass (red-dominance extraction in tools/process_frames.py); it now
  measures 217–220 px of vignette content. See SEQUENCE_AUDIT.md.

---

Alpha threshold > 40. `h` = full alpha-bbox height; `lcc_h` = largest-connected-component (the figure) bbox height; `foot_off` = pivot.y − LCC bbox bottom (0 = figure's lowest point exactly on the pivot; negative = figure extends below pivot); `ncomp` = component count (>1 means detached debris/satellites present). Whip rows add grip/tip stats vs pivot.
## Summary (per clip)

| clip | actor | n | full_h min/med/max | lcc_h min/med/max |
|---|---|---|---|---|
| boss_death | boss | 12 | 143/232/365 | 141/232/364 |
| boss_hazard_execute | boss | 4 | 310/352/373 | 310/352/373 |
| boss_hazard_recover | boss | 6 | 348/365/369 | 245/351/361 |
| boss_hazard_windup | boss | 8 | 347/352/359 | 346/352/359 |
| boss_hurt | boss | 3 | 339/352/352 | 339/352/352 |
| boss_idle | boss | 8 | 329/351/358 | 329/351/358 |
| boss_strike_execute | boss | 4 | 276/352/424 | 276/352/424 |
| boss_strike_recover | boss | 6 | 370/374/374 | 280/351/374 |
| boss_strike_windup | boss | 7 | 345/352/361 | 345/352/361 |
| boss_turn | boss | 4 | 347/352/356 | 347/352/355 |
| boss_walk | boss | 8 | 335/352/369 | 335/352/369 |
| hero_attack_air | hero | 8 | 206/238/271 | 205/219/227 |
| hero_attack_crouch | hero | 8 | 135/140/143 | 135/140/143 |
| hero_attack_ground | hero | 8 | 207/224/250 | 207/224/250 |
| hero_crouch_enter | hero | 4 | 140/165/190 | 140/165/190 |
| hero_crouch_exit | hero | 4 | 140/165/190 | 140/165/190 |
| hero_crouch_idle | hero | 6 | 135/140/145 | 135/140/145 |
| hero_death | hero | 10 | 78/214/232 | 42/179/229 |
| hero_fall | hero | 4 | 203/218/241 | 203/218/224 |
| hero_get_up | hero | 6 | 123/144/229 | 123/144/229 |
| hero_hurt_recoil | hero | 4 | 205/224/243 | 205/224/243 |
| hero_idle | hero | 8 | 222/224/226 | 222/224/226 |
| hero_jump_apex | hero | 3 | 178/189/224 | 178/189/224 |
| hero_jump_rise | hero | 4 | 174/210/224 | 174/210/224 |
| hero_jump_takeoff | hero | 3 | 164/221/223 | 164/221/223 |
| hero_knockback | hero | 4 | 185/212/224 | 185/212/224 |
| hero_knockdown | hero | 6 | 123/144/229 | 123/144/229 |
| hero_land | hero | 4 | 169/224/260 | 169/224/260 |
| hero_start_move | hero | 3 | 219/224/239 | 219/224/239 |
| hero_stop_move | hero | 3 | 223/224/241 | 223/224/241 |
| hero_turn | hero | 3 | 212/224/225 | 212/224/225 |
| hero_walk | hero | 10 | 215/226/242 | 215/224/231 |
| projectile_grave_shot | projectile | 3 | 64/64/64 | 64/64/64 |
| pursuer_alert | pursuer | 4 | 111/160/160 | 111/160/160 |
| pursuer_approach_walk | pursuer | 8 | 96/111/123 | 96/111/123 |
| pursuer_death | pursuer | 6 | 45/84/126 | 41/82/126 |
| pursuer_hurt | pursuer | 3 | 94/112/135 | 93/112/135 |
| pursuer_idle | pursuer | 6 | 109/111/148 | 109/111/148 |
| pursuer_lunge | pursuer | 3 | 47/62/112 | 47/61/112 |
| pursuer_lunge_windup | pursuer | 4 | 112/132/159 | 111/132/159 |
| pursuer_patrol_walk | pursuer | 8 | 106/111/124 | 106/111/124 |
| pursuer_recovery | pursuer | 4 | 84/112/139 | 84/112/139 |
| ranged_aim | ranged | 6 | 288/288/288 | 288/288/288 |
| ranged_death | ranged | 6 | 288/288/288 | 288/288/288 |
| ranged_fire | ranged | 3 | 288/288/288 | 288/288/288 |
| ranged_hurt | ranged | 3 | 288/288/288 | 288/288/288 |
| ranged_idle | ranged | 6 | 288/288/288 | 288/288/288 |
| ranged_recover | ranged | 7 | 288/288/288 | 288/288/288 |
| swooper_cruise | swooper | 8 | 132/169/182 | 132/169/182 |
| swooper_death_fall | swooper | 5 | 80/170/240 | 80/170/240 |
| swooper_dive | swooper | 4 | 155/170/174 | 155/170/174 |
| swooper_dive_telegraph | swooper | 4 | 108/170/235 | 108/170/235 |
| swooper_hurt | swooper | 3 | 128/170/184 | 128/170/184 |
| swooper_perch_idle | swooper | 6 | 168/169/173 | 168/169/173 |
| swooper_recovery_climb | swooper | 6 | 125/169/175 | 125/169/175 |
| vfx_checkpoint_activate | vfx | 8 | 97/256/256 | 29/256/256 |
| vfx_damage_indicator | vfx | 2 | 217/218/220 | 217/218/220 |
| vfx_enemy_defeat | vfx | 8 | 246/256/256 | 32/256/256 |
| vfx_hazard_eruption | vfx | 6 | 97/192/192 | 67/137/192 |
| vfx_hazard_telegraph | vfx | 4 | 75/78/80 | 75/78/80 |
| vfx_whip_impact | vfx | 6 | 18/237/256 | 2/94/256 |
| whip_attack_air | whip | 8 | 169/209/253 | 169/209/252 |
| whip_attack_crouch | whip | 8 | 191/244/270 | 191/244/270 |
| whip_attack_ground | whip | 8 | 151/226/281 | 151/226/281 |


## boss_death  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_death_f00.png | 365 | 364 | 188 | +0 | 4 |  |  |  |
| boss_death_f01.png | 339 | 339 | 227 | +0 | 2 |  |  |  |
| boss_death_f02.png | 316 | 316 | 240 | +0 | 2 |  |  |  |
| boss_death_f03.png | 280 | 280 | 257 | +0 | 2 |  |  |  |
| boss_death_f04.png | 266 | 266 | 285 | +0 | 1 |  |  |  |
| boss_death_f05.png | 235 | 235 | 299 | +1 | 1 |  |  |  |
| boss_death_f06.png | 228 | 228 | 325 | +0 | 4 |  |  |  |
| boss_death_f07.png | 210 | 210 | 352 | +0 | 6 |  |  |  |
| boss_death_f08.png | 205 | 205 | 361 | +0 | 3 |  |  |  |
| boss_death_f09.png | 169 | 168 | 361 | +1 | 3 |  |  |  |
| boss_death_f10.png | 173 | 173 | 361 | +0 | 7 |  |  |  |
| boss_death_f11.png | 143 | 141 | 361 | +1 | 6 |  |  |  |
| **median** | **232** | **232** | | | | | | |

## boss_hazard_execute  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_execute_f00.png | 373 | 373 | 214 | +0 | 10 |  |  |  |
| boss_hazard_execute_f01.png | 310 | 310 | 343 | +0 | 11 |  |  |  |
| boss_hazard_execute_f02.png | 332 | 332 | 354 | +0 | 11 |  |  |  |
| boss_hazard_execute_f03.png | 372 | 372 | 123 | +0 | 1 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_hazard_recover  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_recover_f00.png | 369 | 245 | 284 | +0 | 2 |  |  |  |
| boss_hazard_recover_f01.png | 368 | 254 | 267 | +0 | 15 |  |  |  |
| boss_hazard_recover_f02.png | 369 | 354 | 270 | +1 | 4 |  |  |  |
| boss_hazard_recover_f03.png | 359 | 359 | 232 | +0 | 3 |  |  |  |
| boss_hazard_recover_f04.png | 362 | 361 | 241 | +0 | 6 |  |  |  |
| boss_hazard_recover_f05.png | 348 | 348 | 242 | +0 | 2 |  |  |  |
| **median** | **365** | **351** | | | | | | |

## boss_hazard_windup  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_windup_f00.png | 348 | 348 | 158 | +0 | 2 |  |  |  |
| boss_hazard_windup_f01.png | 347 | 346 | 222 | +0 | 4 |  |  |  |
| boss_hazard_windup_f02.png | 351 | 351 | 285 | +0 | 5 |  |  |  |
| boss_hazard_windup_f03.png | 352 | 352 | 313 | +0 | 1 |  |  |  |
| boss_hazard_windup_f04.png | 355 | 355 | 318 | +0 | 6 |  |  |  |
| boss_hazard_windup_f05.png | 352 | 352 | 326 | +0 | 12 |  |  |  |
| boss_hazard_windup_f06.png | 359 | 359 | 336 | +0 | 7 |  |  |  |
| boss_hazard_windup_f07.png | 359 | 359 | 349 | +0 | 6 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_hurt  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hurt_f00.png | 352 | 352 | 353 | +0 | 4 |  |  |  |
| boss_hurt_f01.png | 339 | 339 | 300 | +0 | 5 |  |  |  |
| boss_hurt_f02.png | 352 | 352 | 225 | +0 | 2 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_idle  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_idle_f00.png | 351 | 351 | 157 | +0 | 1 |  |  |  |
| boss_idle_f01.png | 351 | 351 | 272 | +0 | 4 |  |  |  |
| boss_idle_f02.png | 353 | 353 | 302 | +0 | 4 |  |  |  |
| boss_idle_f03.png | 329 | 329 | 323 | +0 | 3 |  |  |  |
| boss_idle_f04.png | 358 | 358 | 170 | +0 | 3 |  |  |  |
| boss_idle_f05.png | 347 | 347 | 289 | +0 | 5 |  |  |  |
| boss_idle_f06.png | 335 | 335 | 329 | +0 | 5 |  |  |  |
| boss_idle_f07.png | 353 | 353 | 158 | +0 | 1 |  |  |  |
| **median** | **351** | **351** | | | | | | |

## boss_strike_execute  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_execute_f00.png | 424 | 424 | 244 | +0 | 1 |  |  |  |
| boss_strike_execute_f01.png | 408 | 408 | 356 | +0 | 1 |  |  |  |
| boss_strike_execute_f02.png | 295 | 295 | 378 | +0 | 2 |  |  |  |
| boss_strike_execute_f03.png | 276 | 276 | 370 | +0 | 1 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_strike_recover  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_recover_f00.png | 374 | 280 | 353 | +0 | 3 |  |  |  |
| boss_strike_recover_f01.png | 373 | 283 | 330 | +1 | 20 |  |  |  |
| boss_strike_recover_f02.png | 374 | 341 | 263 | +0 | 6 |  |  |  |
| boss_strike_recover_f03.png | 374 | 361 | 190 | +0 | 4 |  |  |  |
| boss_strike_recover_f04.png | 370 | 369 | 363 | +0 | 17 |  |  |  |
| boss_strike_recover_f05.png | 374 | 374 | 363 | +0 | 1 |  |  |  |
| **median** | **374** | **351** | | | | | | |

## boss_strike_windup  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_windup_f00.png | 360 | 360 | 152 | +0 | 1 |  |  |  |
| boss_strike_windup_f01.png | 345 | 345 | 230 | +0 | 4 |  |  |  |
| boss_strike_windup_f02.png | 351 | 351 | 268 | +0 | 4 |  |  |  |
| boss_strike_windup_f03.png | 347 | 347 | 305 | +0 | 3 |  |  |  |
| boss_strike_windup_f04.png | 352 | 352 | 263 | +0 | 5 |  |  |  |
| boss_strike_windup_f05.png | 354 | 354 | 304 | +0 | 2 |  |  |  |
| boss_strike_windup_f06.png | 361 | 361 | 326 | +0 | 4 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_turn  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_turn_f00.png | 347 | 347 | 344 | +0 | 1 |  |  |  |
| boss_turn_f01.png | 356 | 355 | 330 | +0 | 10 |  |  |  |
| boss_turn_f02.png | 350 | 350 | 289 | +0 | 13 |  |  |  |
| boss_turn_f03.png | 354 | 354 | 352 | +0 | 5 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_walk  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_walk_f00.png | 369 | 369 | 227 | +0 | 3 |  |  |  |
| boss_walk_f01.png | 363 | 363 | 266 | +0 | 3 |  |  |  |
| boss_walk_f02.png | 352 | 352 | 298 | +0 | 3 |  |  |  |
| boss_walk_f03.png | 352 | 352 | 339 | +0 | 2 |  |  |  |
| boss_walk_f04.png | 337 | 337 | 305 | +0 | 4 |  |  |  |
| boss_walk_f05.png | 351 | 351 | 318 | +0 | 2 |  |  |  |
| boss_walk_f06.png | 346 | 345 | 345 | +0 | 2 |  |  |  |
| boss_walk_f07.png | 335 | 335 | 324 | +0 | 2 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## hero_attack_air  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_air_f00.png | 271 | 222 | 211 | +0 | 22 |  |  |  |
| hero_attack_air_f01.png | 249 | 226 | 213 | -1 | 3 |  |  |  |
| hero_attack_air_f02.png | 257 | 216 | 235 | +0 | 4 |  |  |  |
| hero_attack_air_f03.png | 271 | 205 | 267 | +31 | 20 |  |  |  |
| hero_attack_air_f04.png | 206 | 206 | 260 | +0 | 1 |  |  |  |
| hero_attack_air_f05.png | 208 | 208 | 199 | +0 | 1 |  |  |  |
| hero_attack_air_f06.png | 223 | 223 | 175 | +0 | 1 |  |  |  |
| hero_attack_air_f07.png | 227 | 227 | 181 | +0 | 1 |  |  |  |
| **median** | **238** | **219** | | | | | | |

## hero_attack_crouch  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_crouch_f00.png | 140 | 140 | 122 | +0 | 1 |  |  |  |
| hero_attack_crouch_f01.png | 140 | 140 | 123 | +0 | 1 |  |  |  |
| hero_attack_crouch_f02.png | 135 | 135 | 153 | +0 | 1 |  |  |  |
| hero_attack_crouch_f03.png | 137 | 137 | 154 | +0 | 1 |  |  |  |
| hero_attack_crouch_f04.png | 140 | 140 | 135 | +0 | 1 |  |  |  |
| hero_attack_crouch_f05.png | 140 | 140 | 136 | +0 | 1 |  |  |  |
| hero_attack_crouch_f06.png | 140 | 140 | 135 | +0 | 1 |  |  |  |
| hero_attack_crouch_f07.png | 143 | 143 | 132 | +0 | 1 |  |  |  |
| **median** | **140** | **140** | | | | | | |

## hero_attack_ground  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_ground_f00.png | 232 | 232 | 179 | +0 | 2 |  |  |  |
| hero_attack_ground_f01.png | 232 | 232 | 179 | +0 | 1 |  |  |  |
| hero_attack_ground_f02.png | 216 | 216 | 222 | +0 | 1 |  |  |  |
| hero_attack_ground_f03.png | 207 | 207 | 250 | +0 | 1 |  |  |  |
| hero_attack_ground_f04.png | 209 | 209 | 211 | +0 | 1 |  |  |  |
| hero_attack_ground_f05.png | 215 | 215 | 192 | +0 | 1 |  |  |  |
| hero_attack_ground_f06.png | 250 | 250 | 72 | +0 | 1 |  |  |  |
| hero_attack_ground_f07.png | 250 | 250 | 72 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_crouch_enter  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_enter_f00.png | 190 | 190 | 59 | +0 | 1 |  |  |  |
| hero_crouch_enter_f01.png | 184 | 184 | 83 | +0 | 1 |  |  |  |
| hero_crouch_enter_f02.png | 146 | 146 | 94 | +0 | 1 |  |  |  |
| hero_crouch_enter_f03.png | 140 | 140 | 95 | +0 | 2 |  |  |  |
| **median** | **165** | **165** | | | | | | |

## hero_crouch_exit  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_exit_f00.png | 140 | 140 | 95 | +0 | 2 |  |  |  |
| hero_crouch_exit_f01.png | 146 | 146 | 94 | +0 | 1 |  |  |  |
| hero_crouch_exit_f02.png | 184 | 184 | 83 | +0 | 1 |  |  |  |
| hero_crouch_exit_f03.png | 190 | 190 | 59 | +0 | 1 |  |  |  |
| **median** | **165** | **165** | | | | | | |

## hero_crouch_idle  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_idle_f00.png | 145 | 145 | 115 | +0 | 1 |  |  |  |
| hero_crouch_idle_f01.png | 139 | 139 | 119 | +0 | 1 |  |  |  |
| hero_crouch_idle_f02.png | 135 | 135 | 120 | +0 | 1 |  |  |  |
| hero_crouch_idle_f03.png | 140 | 140 | 119 | +0 | 1 |  |  |  |
| hero_crouch_idle_f04.png | 140 | 140 | 119 | +0 | 1 |  |  |  |
| hero_crouch_idle_f05.png | 140 | 140 | 119 | +0 | 1 |  |  |  |
| **median** | **140** | **140** | | | | | | |

## hero_death  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_death_f00.png | 229 | 229 | 119 | +0 | 1 |  |  |  |
| hero_death_f01.png | 219 | 219 | 132 | +0 | 1 |  |  |  |
| hero_death_f02.png | 214 | 214 | 183 | +0 | 1 |  |  |  |
| hero_death_f03.png | 194 | 194 | 164 | +0 | 1 |  |  |  |
| hero_death_f04.png | 192 | 192 | 205 | +0 | 1 |  |  |  |
| hero_death_f05.png | 232 | 166 | 208 | +0 | 2 |  |  |  |
| hero_death_f06.png | 219 | 130 | 183 | +0 | 3 |  |  |  |
| hero_death_f07.png | 215 | 88 | 239 | +0 | 2 |  |  |  |
| hero_death_f08.png | 209 | 42 | 145 | +0 | 3 |  |  |  |
| hero_death_f09.png | 78 | 78 | 235 | +0 | 1 |  |  |  |
| **median** | **214** | **179** | | | | | | |

## hero_fall  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_fall_f00.png | 203 | 203 | 106 | +0 | 1 |  |  |  |
| hero_fall_f01.png | 215 | 215 | 118 | +0 | 1 |  |  |  |
| hero_fall_f02.png | 222 | 222 | 118 | +0 | 1 |  |  |  |
| hero_fall_f03.png | 241 | 224 | 113 | +0 | 2 |  |  |  |
| **median** | **218** | **218** | | | | | | |

## hero_get_up  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_get_up_f00.png | 123 | 123 | 134 | +0 | 1 |  |  |  |
| hero_get_up_f01.png | 136 | 136 | 121 | +0 | 1 |  |  |  |
| hero_get_up_f02.png | 130 | 128 | 133 | +0 | 4 |  |  |  |
| hero_get_up_f03.png | 153 | 153 | 134 | +0 | 3 |  |  |  |
| hero_get_up_f04.png | 219 | 219 | 128 | +0 | 3 |  |  |  |
| hero_get_up_f05.png | 229 | 229 | 129 | +0 | 1 |  |  |  |
| **median** | **144** | **144** | | | | | | |

## hero_hurt_recoil  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_hurt_recoil_f00.png | 243 | 243 | 77 | +0 | 2 |  |  |  |
| hero_hurt_recoil_f01.png | 228 | 228 | 122 | +0 | 1 |  |  |  |
| hero_hurt_recoil_f02.png | 205 | 205 | 129 | +0 | 1 |  |  |  |
| hero_hurt_recoil_f03.png | 220 | 220 | 125 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_idle  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_idle_f00.png | 223 | 223 | 133 | +0 | 1 |  |  |  |
| hero_idle_f01.png | 224 | 224 | 139 | +0 | 1 |  |  |  |
| hero_idle_f02.png | 225 | 225 | 142 | +0 | 1 |  |  |  |
| hero_idle_f03.png | 222 | 222 | 146 | +0 | 2 |  |  |  |
| hero_idle_f04.png | 226 | 226 | 182 | +0 | 1 |  |  |  |
| hero_idle_f05.png | 224 | 224 | 151 | +0 | 1 |  |  |  |
| hero_idle_f06.png | 224 | 224 | 178 | +0 | 1 |  |  |  |
| hero_idle_f07.png | 223 | 223 | 152 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_jump_apex  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_apex_f00.png | 224 | 224 | 176 | +0 | 1 |  |  |  |
| hero_jump_apex_f01.png | 178 | 178 | 218 | +0 | 2 |  |  |  |
| hero_jump_apex_f02.png | 189 | 189 | 188 | +0 | 1 |  |  |  |
| **median** | **189** | **189** | | | | | | |

## hero_jump_rise  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_rise_f00.png | 174 | 174 | 136 | +0 | 1 |  |  |  |
| hero_jump_rise_f01.png | 224 | 224 | 133 | +0 | 2 |  |  |  |
| hero_jump_rise_f02.png | 211 | 211 | 139 | +0 | 1 |  |  |  |
| hero_jump_rise_f03.png | 208 | 208 | 138 | +0 | 1 |  |  |  |
| **median** | **210** | **210** | | | | | | |

## hero_jump_takeoff  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_takeoff_f00.png | 164 | 164 | 170 | +0 | 1 |  |  |  |
| hero_jump_takeoff_f01.png | 223 | 223 | 163 | +0 | 1 |  |  |  |
| hero_jump_takeoff_f02.png | 221 | 221 | 183 | +0 | 1 |  |  |  |
| **median** | **221** | **221** | | | | | | |

## hero_knockback  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_knockback_f00.png | 224 | 224 | 123 | +0 | 1 |  |  |  |
| hero_knockback_f01.png | 220 | 220 | 123 | +0 | 1 |  |  |  |
| hero_knockback_f02.png | 185 | 185 | 120 | +0 | 2 |  |  |  |
| hero_knockback_f03.png | 204 | 204 | 117 | +0 | 1 |  |  |  |
| **median** | **212** | **212** | | | | | | |

## hero_knockdown  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_knockdown_f00.png | 229 | 229 | 129 | +0 | 1 |  |  |  |
| hero_knockdown_f01.png | 219 | 219 | 128 | +0 | 3 |  |  |  |
| hero_knockdown_f02.png | 153 | 153 | 134 | +0 | 3 |  |  |  |
| hero_knockdown_f03.png | 130 | 128 | 133 | +0 | 4 |  |  |  |
| hero_knockdown_f04.png | 136 | 136 | 121 | +0 | 1 |  |  |  |
| hero_knockdown_f05.png | 123 | 123 | 134 | +0 | 1 |  |  |  |
| **median** | **144** | **144** | | | | | | |

## hero_land  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_land_f00.png | 239 | 239 | 121 | +0 | 1 |  |  |  |
| hero_land_f01.png | 209 | 209 | 126 | +0 | 1 |  |  |  |
| hero_land_f02.png | 169 | 169 | 139 | +0 | 1 |  |  |  |
| hero_land_f03.png | 260 | 260 | 82 | +0 | 3 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_start_move  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_start_move_f00.png | 239 | 239 | 80 | +0 | 2 |  |  |  |
| hero_start_move_f01.png | 219 | 219 | 176 | +0 | 1 |  |  |  |
| hero_start_move_f02.png | 224 | 224 | 172 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_stop_move  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_stop_move_f00.png | 223 | 223 | 206 | +0 | 1 |  |  |  |
| hero_stop_move_f01.png | 224 | 224 | 203 | +0 | 1 |  |  |  |
| hero_stop_move_f02.png | 241 | 241 | 85 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_turn  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_turn_f00.png | 225 | 225 | 84 | +0 | 2 |  |  |  |
| hero_turn_f01.png | 212 | 212 | 186 | +0 | 3 |  |  |  |
| hero_turn_f02.png | 224 | 224 | 88 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_walk  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_walk_f00.png | 229 | 229 | 122 | +0 | 2 |  |  |  |
| hero_walk_f01.png | 231 | 231 | 135 | +0 | 2 |  |  |  |
| hero_walk_f02.png | 227 | 227 | 152 | +0 | 1 |  |  |  |
| hero_walk_f03.png | 215 | 215 | 162 | +0 | 1 |  |  |  |
| hero_walk_f04.png | 219 | 219 | 161 | +0 | 1 |  |  |  |
| hero_walk_f05.png | 223 | 223 | 144 | +0 | 5 |  |  |  |
| hero_walk_f06.png | 241 | 227 | 152 | +0 | 4 |  |  |  |
| hero_walk_f07.png | 242 | 224 | 152 | +0 | 2 |  |  |  |
| hero_walk_f08.png | 224 | 224 | 150 | +0 | 1 |  |  |  |
| hero_walk_f09.png | 220 | 220 | 153 | +0 | 3 |  |  |  |
| **median** | **226** | **224** | | | | | | |

## projectile_grave_shot  (actor=projectile, canvas=[64, 64], pivot=[32, 32])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| projectile_grave_shot_f00.png | 64 | 64 | 64 | -32 | 1 |  |  |  |
| projectile_grave_shot_f01.png | 64 | 64 | 64 | -32 | 1 |  |  |  |
| projectile_grave_shot_f02.png | 64 | 64 | 64 | -32 | 1 |  |  |  |
| **median** | **64** | **64** | | | | | | |

## pursuer_alert  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_alert_f00.png | 111 | 111 | 203 | +1 | 2 |  |  |  |
| pursuer_alert_f01.png | 160 | 160 | 211 | +0 | 2 |  |  |  |
| pursuer_alert_f02.png | 160 | 160 | 175 | +0 | 3 |  |  |  |
| pursuer_alert_f03.png | 160 | 160 | 108 | +0 | 3 |  |  |  |
| **median** | **160** | **160** | | | | | | |

## pursuer_approach_walk  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_approach_walk_f00.png | 96 | 96 | 183 | +1 | 2 |  |  |  |
| pursuer_approach_walk_f01.png | 104 | 104 | 179 | +1 | 2 |  |  |  |
| pursuer_approach_walk_f02.png | 123 | 123 | 174 | +0 | 2 |  |  |  |
| pursuer_approach_walk_f03.png | 115 | 115 | 175 | +1 | 4 |  |  |  |
| pursuer_approach_walk_f04.png | 107 | 107 | 184 | +1 | 4 |  |  |  |
| pursuer_approach_walk_f05.png | 111 | 111 | 179 | +1 | 3 |  |  |  |
| pursuer_approach_walk_f06.png | 111 | 111 | 179 | +1 | 5 |  |  |  |
| pursuer_approach_walk_f07.png | 111 | 111 | 181 | +1 | 3 |  |  |  |
| **median** | **111** | **111** | | | | | | |

## pursuer_death  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_death_f00.png | 126 | 126 | 130 | +0 | 4 |  |  |  |
| pursuer_death_f01.png | 98 | 98 | 117 | +0 | 6 |  |  |  |
| pursuer_death_f02.png | 97 | 96 | 118 | +1 | 5 |  |  |  |
| pursuer_death_f03.png | 71 | 69 | 126 | +3 | 3 |  |  |  |
| pursuer_death_f04.png | 45 | 41 | 127 | +0 | 7 |  |  |  |
| pursuer_death_f05.png | 47 | 41 | 127 | +0 | 4 |  |  |  |
| **median** | **84** | **82** | | | | | | |

## pursuer_hurt  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_hurt_f00.png | 135 | 135 | 137 | +0 | 2 |  |  |  |
| pursuer_hurt_f01.png | 94 | 93 | 114 | +1 | 2 |  |  |  |
| pursuer_hurt_f02.png | 112 | 112 | 124 | +0 | 4 |  |  |  |
| **median** | **112** | **112** | | | | | | |

## pursuer_idle  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_idle_f00.png | 111 | 111 | 156 | +1 | 2 |  |  |  |
| pursuer_idle_f01.png | 148 | 148 | 163 | +1 | 3 |  |  |  |
| pursuer_idle_f02.png | 111 | 111 | 155 | +1 | 2 |  |  |  |
| pursuer_idle_f03.png | 110 | 110 | 159 | +1 | 3 |  |  |  |
| pursuer_idle_f04.png | 140 | 140 | 162 | +1 | 3 |  |  |  |
| pursuer_idle_f05.png | 109 | 109 | 159 | +1 | 2 |  |  |  |
| **median** | **111** | **111** | | | | | | |

## pursuer_lunge  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_lunge_f00.png | 112 | 112 | 122 | +0 | 6 |  |  |  |
| pursuer_lunge_f01.png | 62 | 61 | 119 | -1 | 6 |  |  |  |
| pursuer_lunge_f02.png | 47 | 47 | 126 | +0 | 8 |  |  |  |
| **median** | **62** | **61** | | | | | | |

## pursuer_lunge_windup  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_lunge_windup_f00.png | 159 | 159 | 93 | +1 | 2 |  |  |  |
| pursuer_lunge_windup_f01.png | 150 | 150 | 83 | +1 | 4 |  |  |  |
| pursuer_lunge_windup_f02.png | 112 | 111 | 93 | +1 | 6 |  |  |  |
| pursuer_lunge_windup_f03.png | 115 | 115 | 87 | +1 | 1 |  |  |  |
| **median** | **132** | **132** | | | | | | |

## pursuer_patrol_walk  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_patrol_walk_f00.png | 115 | 115 | 166 | +1 | 4 |  |  |  |
| pursuer_patrol_walk_f01.png | 124 | 124 | 154 | +0 | 5 |  |  |  |
| pursuer_patrol_walk_f02.png | 122 | 122 | 162 | +1 | 3 |  |  |  |
| pursuer_patrol_walk_f03.png | 112 | 112 | 161 | +1 | 3 |  |  |  |
| pursuer_patrol_walk_f04.png | 107 | 107 | 166 | +0 | 2 |  |  |  |
| pursuer_patrol_walk_f05.png | 108 | 108 | 163 | +1 | 2 |  |  |  |
| pursuer_patrol_walk_f06.png | 110 | 110 | 164 | +1 | 5 |  |  |  |
| pursuer_patrol_walk_f07.png | 106 | 106 | 163 | +1 | 3 |  |  |  |
| **median** | **111** | **111** | | | | | | |

## pursuer_recovery  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_recovery_f00.png | 84 | 84 | 149 | +0 | 5 |  |  |  |
| pursuer_recovery_f01.png | 115 | 115 | 115 | +0 | 6 |  |  |  |
| pursuer_recovery_f02.png | 139 | 139 | 129 | +1 | 5 |  |  |  |
| pursuer_recovery_f03.png | 109 | 109 | 128 | +0 | 5 |  |  |  |
| **median** | **112** | **112** | | | | | | |

## ranged_aim  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_aim_f00.png | 288 | 288 | 169 | +0 | 1 |  |  |  |
| ranged_aim_f01.png | 288 | 288 | 202 | +0 | 1 |  |  |  |
| ranged_aim_f02.png | 288 | 288 | 212 | +0 | 1 |  |  |  |
| ranged_aim_f03.png | 288 | 288 | 218 | +0 | 4 |  |  |  |
| ranged_aim_f04.png | 288 | 288 | 218 | +0 | 7 |  |  |  |
| ranged_aim_f05.png | 288 | 288 | 254 | +0 | 4 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_death  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_death_f00.png | 288 | 288 | 147 | +0 | 1 |  |  |  |
| ranged_death_f01.png | 288 | 288 | 172 | +0 | 1 |  |  |  |
| ranged_death_f02.png | 288 | 288 | 171 | +0 | 1 |  |  |  |
| ranged_death_f03.png | 288 | 288 | 165 | +0 | 2 |  |  |  |
| ranged_death_f04.png | 288 | 288 | 171 | +0 | 1 |  |  |  |
| ranged_death_f05.png | 288 | 288 | 172 | +0 | 11 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_fire  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_fire_f00.png | 288 | 288 | 170 | +0 | 8 |  |  |  |
| ranged_fire_f01.png | 288 | 288 | 118 | +0 | 10 |  |  |  |
| ranged_fire_f02.png | 288 | 288 | 117 | +0 | 1 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_hurt  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_hurt_f00.png | 288 | 288 | 255 | +0 | 3 |  |  |  |
| ranged_hurt_f01.png | 288 | 288 | 191 | +0 | 1 |  |  |  |
| ranged_hurt_f02.png | 288 | 288 | 176 | +0 | 3 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_idle  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_idle_f00.png | 288 | 288 | 131 | +0 | 1 |  |  |  |
| ranged_idle_f01.png | 288 | 288 | 137 | +0 | 1 |  |  |  |
| ranged_idle_f02.png | 288 | 288 | 144 | +0 | 3 |  |  |  |
| ranged_idle_f03.png | 288 | 288 | 161 | +0 | 1 |  |  |  |
| ranged_idle_f04.png | 288 | 288 | 148 | +0 | 1 |  |  |  |
| ranged_idle_f05.png | 288 | 288 | 143 | +0 | 1 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_recover  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_recover_f00.png | 288 | 288 | 256 | +0 | 2 |  |  |  |
| ranged_recover_f01.png | 288 | 288 | 256 | +0 | 3 |  |  |  |
| ranged_recover_f02.png | 288 | 288 | 256 | +0 | 2 |  |  |  |
| ranged_recover_f03.png | 288 | 288 | 256 | +0 | 1 |  |  |  |
| ranged_recover_f04.png | 288 | 288 | 256 | +0 | 3 |  |  |  |
| ranged_recover_f05.png | 288 | 288 | 256 | +0 | 2 |  |  |  |
| ranged_recover_f06.png | 288 | 288 | 256 | +0 | 1 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## swooper_cruise  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_cruise_f00.png | 182 | 182 | 165 | -91 | 2 |  |  |  |
| swooper_cruise_f01.png | 180 | 180 | 173 | -90 | 1 |  |  |  |
| swooper_cruise_f02.png | 132 | 132 | 180 | -65 | 1 |  |  |  |
| swooper_cruise_f03.png | 136 | 136 | 164 | -68 | 2 |  |  |  |
| swooper_cruise_f04.png | 157 | 157 | 187 | -78 | 1 |  |  |  |
| swooper_cruise_f05.png | 169 | 169 | 168 | -84 | 1 |  |  |  |
| swooper_cruise_f06.png | 169 | 169 | 183 | -84 | 1 |  |  |  |
| swooper_cruise_f07.png | 173 | 173 | 183 | -86 | 1 |  |  |  |
| **median** | **169** | **169** | | | | | | |

## swooper_death_fall  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_death_fall_f00.png | 240 | 240 | 227 | -120 | 1 |  |  |  |
| swooper_death_fall_f01.png | 170 | 170 | 191 | -85 | 1 |  |  |  |
| swooper_death_fall_f02.png | 177 | 177 | 178 | -89 | 1 |  |  |  |
| swooper_death_fall_f03.png | 164 | 164 | 176 | -82 | 12 |  |  |  |
| swooper_death_fall_f04.png | 80 | 80 | 269 | -40 | 3 |  |  |  |
| **median** | **170** | **170** | | | | | | |

## swooper_dive  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_dive_f00.png | 165 | 165 | 164 | -82 | 1 |  |  |  |
| swooper_dive_f01.png | 155 | 155 | 145 | -77 | 1 |  |  |  |
| swooper_dive_f02.png | 174 | 174 | 221 | -87 | 1 |  |  |  |
| swooper_dive_f03.png | 174 | 174 | 222 | -88 | 2 |  |  |  |
| **median** | **170** | **170** | | | | | | |

## swooper_dive_telegraph  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_dive_telegraph_f00.png | 235 | 235 | 133 | -118 | 1 |  |  |  |
| swooper_dive_telegraph_f01.png | 199 | 198 | 87 | -100 | 4 |  |  |  |
| swooper_dive_telegraph_f02.png | 141 | 141 | 86 | -70 | 3 |  |  |  |
| swooper_dive_telegraph_f03.png | 108 | 108 | 109 | -54 | 1 |  |  |  |
| **median** | **170** | **170** | | | | | | |

## swooper_hurt  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_hurt_f00.png | 184 | 184 | 188 | -92 | 3 |  |  |  |
| swooper_hurt_f01.png | 170 | 170 | 145 | -85 | 1 |  |  |  |
| swooper_hurt_f02.png | 128 | 128 | 181 | -64 | 1 |  |  |  |
| **median** | **170** | **170** | | | | | | |

## swooper_perch_idle  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_perch_idle_f00.png | 168 | 168 | 150 | -84 | 1 |  |  |  |
| swooper_perch_idle_f01.png | 168 | 168 | 143 | -84 | 1 |  |  |  |
| swooper_perch_idle_f02.png | 168 | 168 | 149 | -84 | 1 |  |  |  |
| swooper_perch_idle_f03.png | 173 | 173 | 154 | -87 | 1 |  |  |  |
| swooper_perch_idle_f04.png | 173 | 173 | 153 | -86 | 1 |  |  |  |
| swooper_perch_idle_f05.png | 170 | 170 | 156 | -84 | 1 |  |  |  |
| **median** | **169** | **169** | | | | | | |

## swooper_recovery_climb  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_recovery_climb_f00.png | 175 | 175 | 143 | -87 | 2 |  |  |  |
| swooper_recovery_climb_f01.png | 135 | 135 | 177 | -68 | 1 |  |  |  |
| swooper_recovery_climb_f02.png | 125 | 125 | 165 | -62 | 4 |  |  |  |
| swooper_recovery_climb_f03.png | 167 | 167 | 164 | -83 | 1 |  |  |  |
| swooper_recovery_climb_f04.png | 171 | 171 | 143 | -85 | 1 |  |  |  |
| swooper_recovery_climb_f05.png | 172 | 172 | 152 | -86 | 5 |  |  |  |
| **median** | **169** | **169** | | | | | | |

## vfx_checkpoint_activate  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_checkpoint_activate_f00.png | 97 | 29 | 46 | -49 | 2 |  |  |  |
| vfx_checkpoint_activate_f01.png | 256 | 135 | 118 | -128 | 14 |  |  |  |
| vfx_checkpoint_activate_f02.png | 256 | 183 | 81 | -128 | 9 |  |  |  |
| vfx_checkpoint_activate_f03.png | 256 | 256 | 167 | -128 | 5 |  |  |  |
| vfx_checkpoint_activate_f04.png | 256 | 256 | 167 | -128 | 5 |  |  |  |
| vfx_checkpoint_activate_f05.png | 256 | 256 | 155 | -128 | 4 |  |  |  |
| vfx_checkpoint_activate_f06.png | 256 | 256 | 116 | -128 | 5 |  |  |  |
| vfx_checkpoint_activate_f07.png | 256 | 256 | 114 | -128 | 1 |  |  |  |
| **median** | **256** | **256** | | | | | | |

## vfx_damage_indicator  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_damage_indicator_f00.png | 217 | 217 | 200 | -109 | 17 |  |  |  |
| vfx_damage_indicator_f01.png | 220 | 220 | 217 | -111 | 21 |  |  |  |
| **median** | **218** | **218** | | | | | | |

## vfx_enemy_defeat  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_enemy_defeat_f00.png | 256 | 256 | 256 | -128 | 1 |  |  |  |
| vfx_enemy_defeat_f01.png | 256 | 256 | 256 | -128 | 2 |  |  |  |
| vfx_enemy_defeat_f02.png | 256 | 256 | 256 | -128 | 9 |  |  |  |
| vfx_enemy_defeat_f03.png | 256 | 256 | 256 | -128 | 27 |  |  |  |
| vfx_enemy_defeat_f04.png | 256 | 256 | 256 | -128 | 5 |  |  |  |
| vfx_enemy_defeat_f05.png | 256 | 256 | 256 | -128 | 23 |  |  |  |
| vfx_enemy_defeat_f06.png | 246 | 86 | 63 | -110 | 49 |  |  |  |
| vfx_enemy_defeat_f07.png | 251 | 32 | 20 | -2 | 32 |  |  |  |
| **median** | **256** | **256** | | | | | | |

## vfx_hazard_eruption  (actor=vfx, canvas=[320, 192], pivot=[160, 176])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_hazard_eruption_f00.png | 101 | 67 | 119 | -16 | 21 |  |  |  |
| vfx_hazard_eruption_f01.png | 192 | 192 | 222 | -16 | 20 |  |  |  |
| vfx_hazard_eruption_f02.png | 192 | 192 | 312 | -16 | 6 |  |  |  |
| vfx_hazard_eruption_f03.png | 192 | 192 | 320 | -16 | 1 |  |  |  |
| vfx_hazard_eruption_f04.png | 192 | 80 | 170 | +96 | 57 |  |  |  |
| vfx_hazard_eruption_f05.png | 97 | 82 | 310 | -16 | 8 |  |  |  |
| **median** | **192** | **137** | | | | | | |

## vfx_hazard_telegraph  (actor=vfx, canvas=[320, 192], pivot=[160, 176])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_hazard_telegraph_f00.png | 77 | 77 | 320 | +99 | 1 |  |  |  |
| vfx_hazard_telegraph_f01.png | 75 | 75 | 320 | +101 | 1 |  |  |  |
| vfx_hazard_telegraph_f02.png | 79 | 79 | 320 | +97 | 1 |  |  |  |
| vfx_hazard_telegraph_f03.png | 80 | 80 | 320 | +96 | 1 |  |  |  |
| **median** | **78** | **78** | | | | | | |

## vfx_whip_impact  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_whip_impact_f00.png | 215 | 76 | 102 | -8 | 59 |  |  |  |
| vfx_whip_impact_f01.png | 256 | 198 | 256 | -70 | 46 |  |  |  |
| vfx_whip_impact_f02.png | 256 | 256 | 256 | -128 | 43 |  |  |  |
| vfx_whip_impact_f03.png | 256 | 111 | 69 | +10 | 60 |  |  |  |
| vfx_whip_impact_f04.png | 218 | 63 | 25 | +34 | 33 |  |  |  |
| vfx_whip_impact_f05.png | 18 | 2 | 6 | -17 | 2 |  |  |  |
| **median** | **237** | **94** | | | | | | |

## whip_attack_air  (actor=whip, canvas=[768, 512], pivot=[276, 308])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| whip_attack_air_f00.png | 169 | 169 | 251 | -19 | 1 | 276 | 308 | 527 |
| whip_attack_air_f01.png | 174 | 174 | 308 | -18 | 1 | 276 | 308 | 584 |
| whip_attack_air_f02.png | 253 | 252 | 324 | -106 | 2 | 276 | 308 | 600 |
| whip_attack_air_f03.png | 232 | 232 | 344 | -84 | 1 | 276 | 308 | 620 |
| whip_attack_air_f04.png | 233 | 233 | 303 | -65 | 1 | 276 | 307 | 579 |
| whip_attack_air_f05.png | 230 | 230 | 290 | -62 | 1 | 276 | 307 | 566 |
| whip_attack_air_f06.png | 185 | 185 | 297 | -19 | 1 | 276 | 308 | 573 |
| whip_attack_air_f07.png | 188 | 188 | 310 | -28 | 2 | 276 | 308 | 586 |
| **median** | **209** | **209** | | | | | | |

## whip_attack_crouch  (actor=whip, canvas=[768, 512], pivot=[276, 308])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| whip_attack_crouch_f00.png | 240 | 240 | 304 | -27 | 1 | 276 | 309 | 580 |
| whip_attack_crouch_f01.png | 249 | 249 | 328 | -30 | 1 | 276 | 310 | 604 |
| whip_attack_crouch_f02.png | 270 | 270 | 329 | -30 | 1 | 276 | 309 | 605 |
| whip_attack_crouch_f03.png | 191 | 191 | 344 | -27 | 1 | 276 | 308 | 620 |
| whip_attack_crouch_f04.png | 245 | 245 | 311 | -19 | 1 | 276 | 308 | 587 |
| whip_attack_crouch_f05.png | 251 | 251 | 317 | -21 | 1 | 276 | 308 | 593 |
| whip_attack_crouch_f06.png | 244 | 244 | 301 | -20 | 1 | 276 | 308 | 577 |
| whip_attack_crouch_f07.png | 225 | 225 | 306 | -19 | 1 | 276 | 308 | 582 |
| **median** | **244** | **244** | | | | | | |

## whip_attack_ground  (actor=whip, canvas=[768, 512], pivot=[276, 308])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| whip_attack_ground_f00.png | 281 | 281 | 233 | -21 | 1 | 276 | 308 | 509 |
| whip_attack_ground_f01.png | 257 | 257 | 293 | -29 | 1 | 276 | 309 | 569 |
| whip_attack_ground_f02.png | 233 | 233 | 318 | -26 | 1 | 276 | 308 | 594 |
| whip_attack_ground_f03.png | 151 | 151 | 344 | -21 | 1 | 276 | 308 | 620 |
| whip_attack_ground_f04.png | 220 | 220 | 292 | -20 | 1 | 276 | 308 | 568 |
| whip_attack_ground_f05.png | 232 | 232 | 303 | -33 | 1 | 276 | 308 | 579 |
| whip_attack_ground_f06.png | 199 | 199 | 314 | -21 | 1 | 276 | 308 | 590 |
| whip_attack_ground_f07.png | 183 | 183 | 288 | -21 | 1 | 276 | 308 | 564 |
| **median** | **226** | **226** | | | | | | |

