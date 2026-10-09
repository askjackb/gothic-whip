# Scale audit — BEFORE (pre-fix, as shipped 2026-10-08; audited 2026-10-09)

Method: final normalized frames on disk, alpha > 40; full alpha bbox and
largest-connected-component (LCC = the figure) bbox per frame; foot_off =
pivot.y − LCC bbox bottom.

## Findings (measured)

- Only the five anchor clips sit at their design heights: hero_idle 224
  (target 224), pursuer_idle 111 (112), swooper_cruise 169 (170),
  boss_idle 351 (352). Ranged measures 288 everywhere — not its 300
  production reference: the 300 px figure placed on a 288 px pivot is
  clipped 12 px at the canvas top in every frame.
- Every non-anchor clip carries its own generation scale (LCC medians,
  final px): hero walk 192 (−14% vs idle), crouch_idle 252 (crouch
  TALLER than standing — the user-visible bug), attack_ground 210,
  attack_air 194, hurt_recoil ~418, start/stop/turn ~340–363, fall
  ~430, jump_rise ~364, knockback ~400, land ~388.
- A second defect class: detached generation debris inflates full
  bboxes — thin full-height vertical line artifacts (hero_fall measures
  448 = the whole canvas height in all 4 frames; the visible figure is
  407–434), specks below the feet that set the bbox bottom during
  production placement (hero_attack_ground), and multi-component debris
  fields (boss_turn up to 14 components, again 448 in every frame).
  Pursuer hurt/alert read a uniform clipped 160 (= canvas room above
  the pivot) — the figure is drawn oversize and sliced at the canvas
  top; boss turn/hurt/hazard_execute read a uniform clipped 448.
- Diagnosis: the shipped "one uniform anchor scale per actor" claim in
  art/manifest.json was wrong in effect. Sheets were generated per clip
  at mutually inconsistent figure sizes, and the single anchor scale
  (plus bbox-based measurement and placement) propagated each clip's
  drift. Fix record: SCALE_AUDIT_AFTER.md + manifest scale_fix_2026_10_09.

---

Alpha threshold > 40. `h` = full alpha-bbox height; `lcc_h` = largest-connected-component (the figure) bbox height; `foot_off` = pivot.y − LCC bbox bottom (0 = figure's lowest point exactly on the pivot; negative = figure extends below pivot); `ncomp` = component count (>1 means detached debris/satellites present). Whip rows add grip/tip stats vs pivot.
## Summary (per clip)

| clip | actor | n | full_h min/med/max | lcc_h min/med/max |
|---|---|---|---|---|
| boss_death | boss | 12 | 164/259/293 | 113/186/293 |
| boss_hazard_execute | boss | 4 | 432/448/448 | 432/448/448 |
| boss_hazard_recover | boss | 6 | 419/425/425 | 281/404/417 |
| boss_hazard_windup | boss | 8 | 346/350/358 | 345/350/358 |
| boss_hurt | boss | 3 | 448/448/448 | 448/448/448 |
| boss_idle | boss | 8 | 329/351/358 | 329/351/358 |
| boss_strike_execute | boss | 4 | 343/408/448 | 343/408/448 |
| boss_strike_recover | boss | 6 | 424/425/425 | 317/399/425 |
| boss_strike_windup | boss | 7 | 346/353/362 | 346/353/362 |
| boss_turn | boss | 4 | 448/448/448 | 448/448/448 |
| boss_walk | boss | 8 | 326/343/360 | 326/343/360 |
| hero_attack_air | hero | 8 | 184/200/240 | 181/194/201 |
| hero_attack_crouch | hero | 8 | 204/213/217 | 204/213/217 |
| hero_attack_ground | hero | 8 | 197/218/235 | 194/210/235 |
| hero_crouch_enter | hero | 4 | 332/391/448 | 332/391/448 |
| hero_crouch_exit | hero | 4 | 332/391/448 | 332/391/448 |
| hero_crouch_idle | hero | 6 | 242/252/260 | 242/252/260 |
| hero_death | hero | 10 | 171/192/207 | 37/160/204 |
| hero_fall | hero | 4 | 448/448/448 | 407/430/434 |
| hero_get_up | hero | 6 | 180/212/335 | 180/212/335 |
| hero_hurt_recoil | hero | 4 | 397/418/448 | 381/418/448 |
| hero_idle | hero | 8 | 222/224/226 | 222/224/226 |
| hero_jump_apex | hero | 3 | 266/283/336 | 266/283/336 |
| hero_jump_rise | hero | 4 | 302/364/389 | 302/364/389 |
| hero_jump_takeoff | hero | 3 | 261/352/356 | 261/352/356 |
| hero_knockback | hero | 4 | 349/400/423 | 349/400/423 |
| hero_knockdown | hero | 6 | 180/212/335 | 180/212/335 |
| hero_land | hero | 4 | 294/388/448 | 294/388/448 |
| hero_start_move | hero | 3 | 334/342/365 | 334/342/365 |
| hero_stop_move | hero | 3 | 339/340/366 | 339/340/366 |
| hero_turn | hero | 3 | 343/363/364 | 343/363/364 |
| hero_walk | hero | 10 | 184/196/207 | 184/192/197 |
| projectile_grave_shot | projectile | 3 | 64/64/64 | 64/64/64 |
| pursuer_alert | pursuer | 4 | 110/160/160 | 110/160/160 |
| pursuer_approach_walk | pursuer | 8 | 78/90/100 | 78/90/100 |
| pursuer_death | pursuer | 6 | 77/137/160 | 53/106/160 |
| pursuer_hurt | pursuer | 3 | 160/160/160 | 160/160/160 |
| pursuer_idle | pursuer | 6 | 109/111/148 | 109/111/148 |
| pursuer_lunge | pursuer | 3 | 88/160/160 | 88/113/160 |
| pursuer_lunge_windup | pursuer | 4 | 159/159/159 | 159/159/159 |
| pursuer_patrol_walk | pursuer | 8 | 94/98/109 | 94/98/109 |
| pursuer_recovery | pursuer | 4 | 121/157/160 | 121/157/160 |
| ranged_aim | ranged | 6 | 288/288/288 | 288/288/288 |
| ranged_death | ranged | 6 | 288/288/288 | 288/288/288 |
| ranged_fire | ranged | 3 | 288/288/288 | 288/288/288 |
| ranged_hurt | ranged | 3 | 288/288/288 | 288/288/288 |
| ranged_idle | ranged | 6 | 288/288/288 | 288/288/288 |
| ranged_recover | ranged | 7 | 278/278/278 | 269/269/269 |
| swooper_cruise | swooper | 8 | 132/169/182 | 132/169/182 |
| swooper_death_fall | swooper | 5 | 92/163/212 | 71/150/212 |
| swooper_dive | swooper | 4 | 178/194/200 | 178/194/200 |
| swooper_dive_telegraph | swooper | 4 | 160/232/256 | 160/232/256 |
| swooper_hurt | swooper | 3 | 191/254/256 | 191/254/256 |
| swooper_perch_idle | swooper | 6 | 168/169/173 | 168/169/173 |
| swooper_recovery_climb | swooper | 6 | 148/200/207 | 148/200/207 |
| vfx_checkpoint_activate | vfx | 8 | 97/256/256 | 29/256/256 |
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
| boss_death_f00.png | 293 | 293 | 150 | +0 | 3 |  |  |  |
| boss_death_f01.png | 272 | 272 | 181 | +0 | 1 |  |  |  |
| boss_death_f02.png | 254 | 254 | 191 | +0 | 1 |  |  |  |
| boss_death_f03.png | 225 | 225 | 207 | +0 | 2 |  |  |  |
| boss_death_f04.png | 287 | 213 | 227 | +0 | 4 |  |  |  |
| boss_death_f05.png | 284 | 189 | 240 | +0 | 4 |  |  |  |
| boss_death_f06.png | 281 | 183 | 261 | +0 | 17 |  |  |  |
| boss_death_f07.png | 264 | 169 | 281 | +0 | 12 |  |  |  |
| boss_death_f08.png | 164 | 164 | 298 | +0 | 3 |  |  |  |
| boss_death_f09.png | 247 | 136 | 298 | +0 | 19 |  |  |  |
| boss_death_f10.png | 254 | 139 | 298 | +0 | 25 |  |  |  |
| boss_death_f11.png | 248 | 113 | 298 | +1 | 12 |  |  |  |
| **median** | **259** | **186** | | | | | | |

## boss_hazard_execute  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_execute_f00.png | 448 | 448 | 236 | +0 | 9 |  |  |  |
| boss_hazard_execute_f01.png | 432 | 432 | 415 | +0 | 11 |  |  |  |
| boss_hazard_execute_f02.png | 448 | 448 | 423 | +0 | 10 |  |  |  |
| boss_hazard_execute_f03.png | 448 | 448 | 170 | +0 | 2 |  |  |  |
| **median** | **448** | **448** | | | | | | |

## boss_hazard_recover  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_recover_f00.png | 425 | 281 | 311 | +58 | 2 |  |  |  |
| boss_hazard_recover_f01.png | 424 | 292 | 301 | +58 | 13 |  |  |  |
| boss_hazard_recover_f02.png | 419 | 408 | 311 | +12 | 3 |  |  |  |
| boss_hazard_recover_f03.png | 425 | 413 | 267 | +7 | 5 |  |  |  |
| boss_hazard_recover_f04.png | 425 | 417 | 277 | +3 | 10 |  |  |  |
| boss_hazard_recover_f05.png | 425 | 401 | 279 | +11 | 2 |  |  |  |
| **median** | **425** | **404** | | | | | | |

## boss_hazard_windup  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_windup_f00.png | 347 | 347 | 158 | +0 | 1 |  |  |  |
| boss_hazard_windup_f01.png | 346 | 345 | 221 | +0 | 3 |  |  |  |
| boss_hazard_windup_f02.png | 350 | 350 | 283 | +0 | 5 |  |  |  |
| boss_hazard_windup_f03.png | 350 | 350 | 311 | +0 | 4 |  |  |  |
| boss_hazard_windup_f04.png | 353 | 353 | 317 | +0 | 3 |  |  |  |
| boss_hazard_windup_f05.png | 350 | 350 | 324 | +0 | 13 |  |  |  |
| boss_hazard_windup_f06.png | 358 | 358 | 334 | +0 | 6 |  |  |  |
| boss_hazard_windup_f07.png | 358 | 358 | 348 | +0 | 6 |  |  |  |
| **median** | **350** | **350** | | | | | | |

## boss_hurt  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hurt_f00.png | 448 | 448 | 431 | +0 | 9 |  |  |  |
| boss_hurt_f01.png | 448 | 448 | 416 | +0 | 4 |  |  |  |
| boss_hurt_f02.png | 448 | 448 | 355 | +0 | 1 |  |  |  |
| **median** | **448** | **448** | | | | | | |

## boss_idle  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_idle_f00.png | 351 | 351 | 157 | +0 | 1 |  |  |  |
| boss_idle_f01.png | 351 | 351 | 272 | +0 | 4 |  |  |  |
| boss_idle_f02.png | 353 | 353 | 302 | +0 | 4 |  |  |  |
| boss_idle_f03.png | 329 | 329 | 323 | +0 | 3 |  |  |  |
| boss_idle_f04.png | 358 | 358 | 170 | +0 | 3 |  |  |  |
| boss_idle_f05.png | 347 | 347 | 290 | +0 | 4 |  |  |  |
| boss_idle_f06.png | 335 | 335 | 329 | +0 | 5 |  |  |  |
| boss_idle_f07.png | 353 | 353 | 158 | +0 | 1 |  |  |  |
| **median** | **351** | **351** | | | | | | |

## boss_strike_execute  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_execute_f00.png | 448 | 448 | 303 | +0 | 3 |  |  |  |
| boss_strike_execute_f01.png | 448 | 448 | 400 | +0 | 1 |  |  |  |
| boss_strike_execute_f02.png | 367 | 367 | 427 | +0 | 2 |  |  |  |
| boss_strike_execute_f03.png | 343 | 343 | 419 | +0 | 1 |  |  |  |
| **median** | **408** | **408** | | | | | | |

## boss_strike_recover  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_recover_f00.png | 425 | 317 | 381 | +44 | 2 |  |  |  |
| boss_strike_recover_f01.png | 424 | 321 | 366 | +43 | 4 |  |  |  |
| boss_strike_recover_f02.png | 425 | 387 | 300 | +30 | 4 |  |  |  |
| boss_strike_recover_f03.png | 425 | 411 | 215 | +4 | 4 |  |  |  |
| boss_strike_recover_f04.png | 424 | 420 | 389 | +0 | 5 |  |  |  |
| boss_strike_recover_f05.png | 425 | 425 | 389 | +0 | 2 |  |  |  |
| **median** | **425** | **399** | | | | | | |

## boss_strike_windup  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_windup_f00.png | 361 | 361 | 152 | +0 | 1 |  |  |  |
| boss_strike_windup_f01.png | 346 | 346 | 230 | +0 | 4 |  |  |  |
| boss_strike_windup_f02.png | 352 | 352 | 269 | +0 | 6 |  |  |  |
| boss_strike_windup_f03.png | 348 | 348 | 305 | +0 | 2 |  |  |  |
| boss_strike_windup_f04.png | 353 | 353 | 264 | +0 | 5 |  |  |  |
| boss_strike_windup_f05.png | 355 | 355 | 303 | +0 | 2 |  |  |  |
| boss_strike_windup_f06.png | 362 | 362 | 327 | +0 | 4 |  |  |  |
| **median** | **353** | **353** | | | | | | |

## boss_turn  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_turn_f00.png | 448 | 448 | 421 | +0 | 1 |  |  |  |
| boss_turn_f01.png | 448 | 448 | 410 | +0 | 8 |  |  |  |
| boss_turn_f02.png | 448 | 448 | 381 | +0 | 14 |  |  |  |
| boss_turn_f03.png | 448 | 448 | 427 | +0 | 6 |  |  |  |
| **median** | **448** | **448** | | | | | | |

## boss_walk  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_walk_f00.png | 360 | 360 | 221 | +0 | 5 |  |  |  |
| boss_walk_f01.png | 354 | 354 | 260 | +0 | 4 |  |  |  |
| boss_walk_f02.png | 344 | 344 | 292 | +0 | 3 |  |  |  |
| boss_walk_f03.png | 343 | 343 | 331 | +0 | 1 |  |  |  |
| boss_walk_f04.png | 328 | 327 | 298 | +0 | 4 |  |  |  |
| boss_walk_f05.png | 343 | 343 | 311 | +0 | 4 |  |  |  |
| boss_walk_f06.png | 338 | 338 | 336 | +0 | 1 |  |  |  |
| boss_walk_f07.png | 326 | 326 | 316 | +0 | 7 |  |  |  |
| **median** | **343** | **343** | | | | | | |

## hero_attack_air  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_air_f00.png | 240 | 197 | 187 | +24 | 19 |  |  |  |
| hero_attack_air_f01.png | 199 | 199 | 188 | +21 | 1 |  |  |  |
| hero_attack_air_f02.png | 192 | 192 | 208 | +13 | 1 |  |  |  |
| hero_attack_air_f03.png | 240 | 181 | 237 | +28 | 4 |  |  |  |
| hero_attack_air_f04.png | 232 | 182 | 230 | +22 | 18 |  |  |  |
| hero_attack_air_f05.png | 184 | 184 | 176 | +23 | 3 |  |  |  |
| hero_attack_air_f06.png | 198 | 198 | 155 | +22 | 1 |  |  |  |
| hero_attack_air_f07.png | 201 | 201 | 159 | +23 | 1 |  |  |  |
| **median** | **200** | **194** | | | | | | |

## hero_attack_crouch  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_crouch_f00.png | 213 | 213 | 186 | +0 | 1 |  |  |  |
| hero_attack_crouch_f01.png | 213 | 213 | 186 | +0 | 1 |  |  |  |
| hero_attack_crouch_f02.png | 204 | 204 | 233 | +0 | 1 |  |  |  |
| hero_attack_crouch_f03.png | 208 | 208 | 234 | +0 | 1 |  |  |  |
| hero_attack_crouch_f04.png | 213 | 213 | 205 | +0 | 1 |  |  |  |
| hero_attack_crouch_f05.png | 213 | 213 | 206 | +0 | 1 |  |  |  |
| hero_attack_crouch_f06.png | 213 | 213 | 206 | +0 | 1 |  |  |  |
| hero_attack_crouch_f07.png | 217 | 217 | 201 | +0 | 1 |  |  |  |
| **median** | **213** | **213** | | | | | | |

## hero_attack_ground  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_ground_f00.png | 218 | 218 | 168 | +0 | 2 |  |  |  |
| hero_attack_ground_f01.png | 219 | 219 | 168 | +0 | 1 |  |  |  |
| hero_attack_ground_f02.png | 219 | 203 | 209 | +16 | 3 |  |  |  |
| hero_attack_ground_f03.png | 217 | 194 | 236 | +23 | 2 |  |  |  |
| hero_attack_ground_f04.png | 197 | 197 | 198 | +0 | 1 |  |  |  |
| hero_attack_ground_f05.png | 202 | 202 | 181 | +0 | 1 |  |  |  |
| hero_attack_ground_f06.png | 235 | 235 | 68 | +0 | 1 |  |  |  |
| hero_attack_ground_f07.png | 235 | 235 | 68 | +0 | 1 |  |  |  |
| **median** | **218** | **210** | | | | | | |

## hero_crouch_enter  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_enter_f00.png | 448 | 448 | 140 | +0 | 2 |  |  |  |
| hero_crouch_enter_f01.png | 436 | 436 | 196 | +0 | 3 |  |  |  |
| hero_crouch_enter_f02.png | 346 | 346 | 222 | +0 | 4 |  |  |  |
| hero_crouch_enter_f03.png | 332 | 332 | 226 | +0 | 3 |  |  |  |
| **median** | **391** | **391** | | | | | | |

## hero_crouch_exit  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_exit_f00.png | 332 | 332 | 226 | +0 | 3 |  |  |  |
| hero_crouch_exit_f01.png | 346 | 346 | 222 | +0 | 4 |  |  |  |
| hero_crouch_exit_f02.png | 436 | 436 | 196 | +0 | 3 |  |  |  |
| hero_crouch_exit_f03.png | 448 | 448 | 140 | +0 | 2 |  |  |  |
| **median** | **391** | **391** | | | | | | |

## hero_crouch_idle  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_idle_f00.png | 260 | 260 | 207 | +0 | 1 |  |  |  |
| hero_crouch_idle_f01.png | 250 | 250 | 214 | +0 | 1 |  |  |  |
| hero_crouch_idle_f02.png | 242 | 242 | 216 | +0 | 1 |  |  |  |
| hero_crouch_idle_f03.png | 252 | 252 | 215 | +0 | 1 |  |  |  |
| hero_crouch_idle_f04.png | 252 | 252 | 215 | +0 | 1 |  |  |  |
| hero_crouch_idle_f05.png | 253 | 253 | 215 | +0 | 1 |  |  |  |
| **median** | **252** | **252** | | | | | | |

## hero_death  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_death_f00.png | 204 | 204 | 106 | +0 | 1 |  |  |  |
| hero_death_f01.png | 195 | 195 | 117 | +0 | 1 |  |  |  |
| hero_death_f02.png | 191 | 191 | 163 | +0 | 1 |  |  |  |
| hero_death_f03.png | 174 | 174 | 146 | +0 | 1 |  |  |  |
| hero_death_f04.png | 171 | 171 | 183 | +0 | 1 |  |  |  |
| hero_death_f05.png | 207 | 149 | 185 | +0 | 2 |  |  |  |
| hero_death_f06.png | 195 | 116 | 163 | +0 | 3 |  |  |  |
| hero_death_f07.png | 192 | 78 | 213 | +0 | 2 |  |  |  |
| hero_death_f08.png | 186 | 37 | 129 | +6 | 3 |  |  |  |
| hero_death_f09.png | 185 | 69 | 210 | +0 | 3 |  |  |  |
| **median** | **192** | **160** | | | | | | |

## hero_fall  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_fall_f00.png | 448 | 407 | 212 | +38 | 3 |  |  |  |
| hero_fall_f01.png | 448 | 428 | 235 | +20 | 2 |  |  |  |
| hero_fall_f02.png | 448 | 431 | 235 | +17 | 2 |  |  |  |
| hero_fall_f03.png | 448 | 434 | 227 | +14 | 2 |  |  |  |
| **median** | **448** | **430** | | | | | | |

## hero_get_up  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_get_up_f00.png | 180 | 180 | 195 | +0 | 2 |  |  |  |
| hero_get_up_f01.png | 199 | 199 | 177 | +0 | 5 |  |  |  |
| hero_get_up_f02.png | 190 | 187 | 195 | +0 | 5 |  |  |  |
| hero_get_up_f03.png | 225 | 225 | 196 | +0 | 3 |  |  |  |
| hero_get_up_f04.png | 321 | 321 | 188 | +0 | 7 |  |  |  |
| hero_get_up_f05.png | 335 | 335 | 189 | +0 | 2 |  |  |  |
| **median** | **212** | **212** | | | | | | |

## hero_hurt_recoil  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_hurt_recoil_f00.png | 448 | 448 | 143 | +0 | 9 |  |  |  |
| hero_hurt_recoil_f01.png | 425 | 425 | 228 | +0 | 5 |  |  |  |
| hero_hurt_recoil_f02.png | 397 | 381 | 241 | +16 | 4 |  |  |  |
| hero_hurt_recoil_f03.png | 410 | 410 | 233 | +0 | 2 |  |  |  |
| **median** | **418** | **418** | | | | | | |

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
| hero_jump_apex_f00.png | 336 | 336 | 264 | +0 | 1 |  |  |  |
| hero_jump_apex_f01.png | 266 | 266 | 327 | +0 | 1 |  |  |  |
| hero_jump_apex_f02.png | 283 | 283 | 282 | +0 | 3 |  |  |  |
| **median** | **283** | **283** | | | | | | |

## hero_jump_rise  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_rise_f00.png | 302 | 302 | 237 | +0 | 1 |  |  |  |
| hero_jump_rise_f01.png | 389 | 389 | 231 | +0 | 5 |  |  |  |
| hero_jump_rise_f02.png | 367 | 367 | 241 | +0 | 2 |  |  |  |
| hero_jump_rise_f03.png | 362 | 362 | 239 | +0 | 2 |  |  |  |
| **median** | **364** | **364** | | | | | | |

## hero_jump_takeoff  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_takeoff_f00.png | 261 | 261 | 270 | +0 | 4 |  |  |  |
| hero_jump_takeoff_f01.png | 356 | 356 | 260 | +0 | 4 |  |  |  |
| hero_jump_takeoff_f02.png | 352 | 352 | 292 | +0 | 3 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## hero_knockback  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_knockback_f00.png | 423 | 423 | 232 | +0 | 2 |  |  |  |
| hero_knockback_f01.png | 416 | 416 | 232 | +0 | 2 |  |  |  |
| hero_knockback_f02.png | 349 | 349 | 226 | +0 | 3 |  |  |  |
| hero_knockback_f03.png | 385 | 385 | 221 | +0 | 2 |  |  |  |
| **median** | **400** | **400** | | | | | | |

## hero_knockdown  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_knockdown_f00.png | 335 | 335 | 189 | +0 | 2 |  |  |  |
| hero_knockdown_f01.png | 321 | 321 | 188 | +0 | 7 |  |  |  |
| hero_knockdown_f02.png | 225 | 225 | 196 | +0 | 3 |  |  |  |
| hero_knockdown_f03.png | 190 | 187 | 195 | +0 | 5 |  |  |  |
| hero_knockdown_f04.png | 199 | 199 | 177 | +0 | 5 |  |  |  |
| hero_knockdown_f05.png | 180 | 180 | 195 | +0 | 2 |  |  |  |
| **median** | **212** | **212** | | | | | | |

## hero_land  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_land_f00.png | 415 | 415 | 209 | +0 | 3 |  |  |  |
| hero_land_f01.png | 362 | 362 | 217 | +0 | 3 |  |  |  |
| hero_land_f02.png | 294 | 294 | 241 | +0 | 2 |  |  |  |
| hero_land_f03.png | 448 | 448 | 142 | +0 | 4 |  |  |  |
| **median** | **388** | **388** | | | | | | |

## hero_start_move  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_start_move_f00.png | 365 | 365 | 122 | +0 | 1 |  |  |  |
| hero_start_move_f01.png | 334 | 334 | 269 | +0 | 1 |  |  |  |
| hero_start_move_f02.png | 342 | 342 | 263 | +0 | 1 |  |  |  |
| **median** | **342** | **342** | | | | | | |

## hero_stop_move  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_stop_move_f00.png | 339 | 339 | 312 | +0 | 2 |  |  |  |
| hero_stop_move_f01.png | 340 | 340 | 308 | +0 | 1 |  |  |  |
| hero_stop_move_f02.png | 366 | 366 | 130 | +0 | 1 |  |  |  |
| **median** | **340** | **340** | | | | | | |

## hero_turn  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_turn_f00.png | 364 | 364 | 136 | +0 | 1 |  |  |  |
| hero_turn_f01.png | 343 | 343 | 301 | +0 | 1 |  |  |  |
| hero_turn_f02.png | 363 | 363 | 143 | +0 | 2 |  |  |  |
| **median** | **363** | **363** | | | | | | |

## hero_walk  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_walk_f00.png | 196 | 196 | 105 | +0 | 2 |  |  |  |
| hero_walk_f01.png | 197 | 197 | 115 | +9 | 3 |  |  |  |
| hero_walk_f02.png | 193 | 193 | 130 | +10 | 2 |  |  |  |
| hero_walk_f03.png | 184 | 184 | 138 | +12 | 2 |  |  |  |
| hero_walk_f04.png | 187 | 187 | 138 | +8 | 1 |  |  |  |
| hero_walk_f05.png | 191 | 191 | 124 | +0 | 5 |  |  |  |
| hero_walk_f06.png | 207 | 195 | 130 | +6 | 4 |  |  |  |
| hero_walk_f07.png | 207 | 192 | 131 | +6 | 2 |  |  |  |
| hero_walk_f08.png | 204 | 192 | 128 | +6 | 2 |  |  |  |
| hero_walk_f09.png | 203 | 190 | 131 | +10 | 4 |  |  |  |
| **median** | **196** | **192** | | | | | | |

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
| pursuer_alert_f00.png | 110 | 110 | 202 | +1 | 3 |  |  |  |
| pursuer_alert_f01.png | 160 | 160 | 210 | +0 | 2 |  |  |  |
| pursuer_alert_f02.png | 160 | 160 | 174 | +0 | 4 |  |  |  |
| pursuer_alert_f03.png | 160 | 160 | 107 | +0 | 2 |  |  |  |
| **median** | **160** | **160** | | | | | | |

## pursuer_approach_walk  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_approach_walk_f00.png | 78 | 78 | 149 | +1 | 2 |  |  |  |
| pursuer_approach_walk_f01.png | 85 | 85 | 145 | +1 | 11 |  |  |  |
| pursuer_approach_walk_f02.png | 100 | 100 | 142 | +0 | 12 |  |  |  |
| pursuer_approach_walk_f03.png | 93 | 93 | 143 | +1 | 7 |  |  |  |
| pursuer_approach_walk_f04.png | 87 | 87 | 150 | +1 | 7 |  |  |  |
| pursuer_approach_walk_f05.png | 90 | 90 | 146 | +1 | 7 |  |  |  |
| pursuer_approach_walk_f06.png | 90 | 90 | 145 | +1 | 8 |  |  |  |
| pursuer_approach_walk_f07.png | 90 | 90 | 147 | +1 | 4 |  |  |  |
| **median** | **90** | **90** | | | | | | |

## pursuer_death  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_death_f00.png | 160 | 160 | 165 | +0 | 2 |  |  |  |
| pursuer_death_f01.png | 157 | 125 | 148 | +0 | 11 |  |  |  |
| pursuer_death_f02.png | 123 | 123 | 150 | +0 | 3 |  |  |  |
| pursuer_death_f03.png | 151 | 88 | 160 | +3 | 8 |  |  |  |
| pursuer_death_f04.png | 77 | 53 | 162 | +0 | 12 |  |  |  |
| pursuer_death_f05.png | 80 | 53 | 161 | +0 | 12 |  |  |  |
| **median** | **137** | **106** | | | | | | |

## pursuer_hurt  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_hurt_f00.png | 160 | 160 | 240 | +0 | 1 |  |  |  |
| pursuer_hurt_f01.png | 160 | 160 | 199 | +0 | 5 |  |  |  |
| pursuer_hurt_f02.png | 160 | 160 | 219 | +0 | 1 |  |  |  |
| **median** | **160** | **160** | | | | | | |

## pursuer_idle  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_idle_f00.png | 111 | 111 | 156 | +1 | 2 |  |  |  |
| pursuer_idle_f01.png | 148 | 148 | 163 | +1 | 2 |  |  |  |
| pursuer_idle_f02.png | 111 | 111 | 155 | +1 | 2 |  |  |  |
| pursuer_idle_f03.png | 110 | 110 | 159 | +1 | 3 |  |  |  |
| pursuer_idle_f04.png | 140 | 140 | 162 | +1 | 3 |  |  |  |
| pursuer_idle_f05.png | 109 | 109 | 159 | +1 | 2 |  |  |  |
| **median** | **111** | **111** | | | | | | |

## pursuer_lunge  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_lunge_f00.png | 160 | 160 | 235 | +0 | 7 |  |  |  |
| pursuer_lunge_f01.png | 160 | 113 | 222 | +3 | 14 |  |  |  |
| pursuer_lunge_f02.png | 88 | 88 | 239 | +0 | 2 |  |  |  |
| **median** | **160** | **113** | | | | | | |

## pursuer_lunge_windup  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_lunge_windup_f00.png | 159 | 159 | 111 | +1 | 3 |  |  |  |
| pursuer_lunge_windup_f01.png | 159 | 159 | 118 | +1 | 1 |  |  |  |
| pursuer_lunge_windup_f02.png | 159 | 159 | 145 | +1 | 1 |  |  |  |
| pursuer_lunge_windup_f03.png | 159 | 159 | 136 | +1 | 1 |  |  |  |
| **median** | **159** | **159** | | | | | | |

## pursuer_patrol_walk  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_patrol_walk_f00.png | 102 | 102 | 147 | +1 | 5 |  |  |  |
| pursuer_patrol_walk_f01.png | 109 | 109 | 137 | +0 | 5 |  |  |  |
| pursuer_patrol_walk_f02.png | 108 | 108 | 144 | +1 | 8 |  |  |  |
| pursuer_patrol_walk_f03.png | 99 | 99 | 143 | +1 | 2 |  |  |  |
| pursuer_patrol_walk_f04.png | 95 | 95 | 147 | +0 | 1 |  |  |  |
| pursuer_patrol_walk_f05.png | 96 | 95 | 145 | +2 | 3 |  |  |  |
| pursuer_patrol_walk_f06.png | 97 | 97 | 145 | +1 | 7 |  |  |  |
| pursuer_patrol_walk_f07.png | 94 | 94 | 145 | +1 | 2 |  |  |  |
| **median** | **98** | **98** | | | | | | |

## pursuer_recovery  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_recovery_f00.png | 121 | 121 | 213 | +0 | 2 |  |  |  |
| pursuer_recovery_f01.png | 159 | 159 | 164 | +1 | 6 |  |  |  |
| pursuer_recovery_f02.png | 160 | 160 | 184 | +0 | 5 |  |  |  |
| pursuer_recovery_f03.png | 155 | 155 | 183 | +0 | 1 |  |  |  |
| **median** | **157** | **157** | | | | | | |

## ranged_aim  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_aim_f00.png | 288 | 288 | 174 | +0 | 1 |  |  |  |
| ranged_aim_f01.png | 288 | 288 | 209 | +0 | 1 |  |  |  |
| ranged_aim_f02.png | 288 | 288 | 219 | +0 | 4 |  |  |  |
| ranged_aim_f03.png | 288 | 288 | 225 | +0 | 8 |  |  |  |
| ranged_aim_f04.png | 288 | 288 | 238 | +0 | 11 |  |  |  |
| ranged_aim_f05.png | 288 | 288 | 256 | +0 | 10 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_death  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_death_f00.png | 288 | 288 | 148 | +0 | 1 |  |  |  |
| ranged_death_f01.png | 288 | 288 | 173 | +0 | 1 |  |  |  |
| ranged_death_f02.png | 288 | 288 | 172 | +0 | 1 |  |  |  |
| ranged_death_f03.png | 288 | 288 | 166 | +0 | 2 |  |  |  |
| ranged_death_f04.png | 288 | 288 | 171 | +0 | 20 |  |  |  |
| ranged_death_f05.png | 288 | 288 | 172 | +0 | 45 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_fire  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_fire_f00.png | 288 | 288 | 91 | +0 | 25 |  |  |  |
| ranged_fire_f01.png | 288 | 288 | 170 | +0 | 10 |  |  |  |
| ranged_fire_f02.png | 288 | 288 | 168 | +0 | 4 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_hurt  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_hurt_f00.png | 288 | 288 | 256 | +0 | 2 |  |  |  |
| ranged_hurt_f01.png | 288 | 288 | 256 | +0 | 1 |  |  |  |
| ranged_hurt_f02.png | 288 | 288 | 254 | +0 | 1 |  |  |  |
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
| ranged_recover_f00.png | 278 | 269 | 256 | +0 | 4 |  |  |  |
| ranged_recover_f01.png | 278 | 269 | 256 | +0 | 3 |  |  |  |
| ranged_recover_f02.png | 278 | 269 | 256 | +0 | 3 |  |  |  |
| ranged_recover_f03.png | 278 | 269 | 256 | +0 | 2 |  |  |  |
| ranged_recover_f04.png | 278 | 269 | 256 | +0 | 3 |  |  |  |
| ranged_recover_f05.png | 278 | 269 | 256 | +0 | 3 |  |  |  |
| ranged_recover_f06.png | 278 | 269 | 256 | +0 | 2 |  |  |  |
| **median** | **278** | **269** | | | | | | |

## swooper_cruise  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_cruise_f00.png | 182 | 182 | 165 | -90 | 2 |  |  |  |
| swooper_cruise_f01.png | 180 | 180 | 173 | -90 | 1 |  |  |  |
| swooper_cruise_f02.png | 132 | 132 | 180 | -66 | 1 |  |  |  |
| swooper_cruise_f03.png | 136 | 136 | 164 | -68 | 2 |  |  |  |
| swooper_cruise_f04.png | 157 | 157 | 187 | -78 | 1 |  |  |  |
| swooper_cruise_f05.png | 169 | 169 | 168 | -84 | 1 |  |  |  |
| swooper_cruise_f06.png | 169 | 169 | 183 | -84 | 1 |  |  |  |
| swooper_cruise_f07.png | 173 | 173 | 183 | -86 | 1 |  |  |  |
| **median** | **169** | **169** | | | | | | |

## swooper_death_fall  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_death_fall_f00.png | 212 | 212 | 201 | -106 | 2 |  |  |  |
| swooper_death_fall_f01.png | 164 | 150 | 169 | -68 | 6 |  |  |  |
| swooper_death_fall_f02.png | 163 | 157 | 158 | -75 | 6 |  |  |  |
| swooper_death_fall_f03.png | 151 | 144 | 156 | -75 | 30 |  |  |  |
| swooper_death_fall_f04.png | 92 | 71 | 238 | -46 | 16 |  |  |  |
| **median** | **163** | **150** | | | | | | |

## swooper_dive  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_dive_f00.png | 190 | 190 | 188 | -95 | 1 |  |  |  |
| swooper_dive_f01.png | 178 | 178 | 167 | -89 | 1 |  |  |  |
| swooper_dive_f02.png | 199 | 199 | 253 | -99 | 2 |  |  |  |
| swooper_dive_f03.png | 200 | 200 | 255 | -101 | 3 |  |  |  |
| **median** | **194** | **194** | | | | | | |

## swooper_dive_telegraph  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_dive_telegraph_f00.png | 256 | 256 | 197 | -128 | 1 |  |  |  |
| swooper_dive_telegraph_f01.png | 256 | 256 | 129 | -128 | 3 |  |  |  |
| swooper_dive_telegraph_f02.png | 209 | 209 | 129 | -105 | 3 |  |  |  |
| swooper_dive_telegraph_f03.png | 160 | 160 | 160 | -80 | 1 |  |  |  |
| **median** | **232** | **232** | | | | | | |

## swooper_hurt  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_hurt_f00.png | 256 | 256 | 280 | -128 | 2 |  |  |  |
| swooper_hurt_f01.png | 254 | 254 | 217 | -127 | 1 |  |  |  |
| swooper_hurt_f02.png | 191 | 191 | 269 | -95 | 1 |  |  |  |
| **median** | **254** | **254** | | | | | | |

## swooper_perch_idle  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_perch_idle_f00.png | 168 | 168 | 150 | -84 | 1 |  |  |  |
| swooper_perch_idle_f01.png | 168 | 168 | 143 | -84 | 1 |  |  |  |
| swooper_perch_idle_f02.png | 168 | 168 | 149 | -84 | 1 |  |  |  |
| swooper_perch_idle_f03.png | 173 | 173 | 154 | -87 | 1 |  |  |  |
| swooper_perch_idle_f04.png | 173 | 173 | 153 | -87 | 1 |  |  |  |
| swooper_perch_idle_f05.png | 170 | 170 | 156 | -84 | 1 |  |  |  |
| **median** | **169** | **169** | | | | | | |

## swooper_recovery_climb  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_recovery_climb_f00.png | 207 | 207 | 169 | -103 | 1 |  |  |  |
| swooper_recovery_climb_f01.png | 159 | 159 | 210 | -79 | 5 |  |  |  |
| swooper_recovery_climb_f02.png | 148 | 148 | 195 | -74 | 3 |  |  |  |
| swooper_recovery_climb_f03.png | 197 | 197 | 194 | -98 | 1 |  |  |  |
| swooper_recovery_climb_f04.png | 203 | 203 | 169 | -101 | 2 |  |  |  |
| swooper_recovery_climb_f05.png | 204 | 204 | 180 | -102 | 3 |  |  |  |
| **median** | **200** | **200** | | | | | | |

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

## vfx_damage_indicator

ALL FRAMES EMPTY

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
| whip_attack_ground_f02.png | 233 | 233 | 318 | -26 | 2 | 276 | 308 | 594 |
| whip_attack_ground_f03.png | 151 | 151 | 344 | -21 | 1 | 276 | 308 | 620 |
| whip_attack_ground_f04.png | 220 | 220 | 292 | -20 | 1 | 276 | 308 | 568 |
| whip_attack_ground_f05.png | 232 | 232 | 303 | -33 | 1 | 276 | 308 | 579 |
| whip_attack_ground_f06.png | 199 | 199 | 314 | -21 | 2 | 276 | 308 | 590 |
| whip_attack_ground_f07.png | 183 | 183 | 288 | -21 | 1 | 276 | 308 | 564 |
| **median** | **226** | **226** | | | | | | |

