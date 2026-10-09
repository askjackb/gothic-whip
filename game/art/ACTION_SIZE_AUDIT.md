# Scale audit — post-integrity-fix

Alpha threshold > 40. `h` = full alpha-bbox height; `lcc_h` = largest-connected-component (the figure) bbox height; `foot_off` = pivot.y − LCC bbox bottom (0 = figure's lowest point exactly on the pivot; negative = figure extends below pivot); `ncomp` = component count (>1 means detached debris/satellites present). Whip rows add grip/tip stats vs pivot.
## Summary (per clip)

| clip | actor | n | full_h min/med/max | lcc_h min/med/max |
|---|---|---|---|---|
| boss_death | boss | 12 | 160/241/365 | 160/240/364 |
| boss_hazard_execute | boss | 4 | 304/330/351 | 304/330/351 |
| boss_hazard_recover | boss | 6 | 252/351/352 | 252/350/352 |
| boss_hazard_windup | boss | 8 | 351/352/352 | 351/352/352 |
| boss_hurt | boss | 3 | 352/352/352 | 352/352/352 |
| boss_idle | boss | 8 | 350/352/353 | 350/352/353 |
| boss_strike_execute | boss | 4 | 293/359/424 | 293/359/424 |
| boss_strike_recover | boss | 6 | 317/352/358 | 263/350/352 |
| boss_strike_windup | boss | 7 | 350/352/352 | 350/352/352 |
| boss_turn | boss | 4 | 352/352/352 | 352/352/352 |
| boss_walk | boss | 8 | 350/351/352 | 350/351/352 |
| hero_attack_air | hero | 8 | 198/224/246 | 198/223/224 |
| hero_attack_crouch | hero | 8 | 139/142/144 | 139/142/144 |
| hero_attack_ground | hero | 8 | 203/224/224 | 203/224/224 |
| hero_crouch_enter | hero | 4 | 142/163/211 | 142/163/211 |
| hero_crouch_exit | hero | 4 | 142/163/211 | 142/163/211 |
| hero_crouch_idle | hero | 6 | 135/140/146 | 135/140/146 |
| hero_death | hero | 10 | 91/160/238 | 91/160/238 |
| hero_fall | hero | 4 | 197/221/230 | 197/221/230 |
| hero_get_up | hero | 6 | 123/160/208 | 123/160/208 |
| hero_hurt_recoil | hero | 4 | 209/224/224 | 209/224/224 |
| hero_idle | hero | 8 | 224/224/224 | 224/224/224 |
| hero_jump_apex | hero | 3 | 178/200/224 | 178/200/224 |
| hero_jump_rise | hero | 4 | 181/224/224 | 181/224/224 |
| hero_jump_takeoff | hero | 3 | 171/223/224 | 171/223/224 |
| hero_knockback | hero | 4 | 190/214/224 | 190/214/224 |
| hero_knockdown | hero | 6 | 123/160/208 | 123/160/208 |
| hero_land | hero | 4 | 174/224/224 | 174/224/224 |
| hero_start_move | hero | 3 | 224/224/224 | 224/224/224 |
| hero_stop_move | hero | 3 | 224/224/224 | 224/224/224 |
| hero_turn | hero | 3 | 224/224/224 | 224/224/224 |
| hero_walk | hero | 10 | 223/224/242 | 223/224/224 |
| projectile_grave_shot | projectile | 3 | 64/64/64 | 64/64/64 |
| pursuer_alert | pursuer | 4 | 111/196/245 | 111/196/245 |
| pursuer_approach_walk | pursuer | 8 | 99/111/124 | 99/111/124 |
| pursuer_death | pursuer | 6 | 50/88/126 | 48/86/126 |
| pursuer_hurt | pursuer | 3 | 94/112/132 | 93/112/132 |
| pursuer_idle | pursuer | 6 | 109/110/148 | 109/110/148 |
| pursuer_lunge | pursuer | 3 | 50/61/95 | 50/61/95 |
| pursuer_lunge_windup | pursuer | 4 | 112/133/171 | 111/133/170 |
| pursuer_patrol_walk | pursuer | 8 | 106/110/122 | 105/110/122 |
| pursuer_recovery | pursuer | 4 | 88/110/140 | 87/110/140 |
| ranged_aim | ranged | 6 | 279/288/288 | 279/288/288 |
| ranged_death | ranged | 6 | 284/288/288 | 284/288/288 |
| ranged_fire | ranged | 3 | 272/288/288 | 272/288/288 |
| ranged_hurt | ranged | 3 | 270/288/288 | 270/288/288 |
| ranged_idle | ranged | 6 | 279/288/288 | 279/288/288 |
| ranged_recover | ranged | 7 | 269/288/288 | 269/288/288 |
| swooper_cruise | swooper | 8 | 138/169/180 | 138/169/180 |
| swooper_death_fall | swooper | 5 | 89/170/213 | 89/170/212 |
| swooper_dive | swooper | 4 | 156/168/188 | 156/168/188 |
| swooper_dive_telegraph | swooper | 4 | 127/182/200 | 127/182/200 |
| swooper_hurt | swooper | 3 | 128/170/180 | 128/170/180 |
| swooper_perch_idle | swooper | 6 | 166/171/174 | 166/171/174 |
| swooper_recovery_climb | swooper | 6 | 126/163/171 | 126/162/171 |
| vfx_checkpoint_activate | vfx | 8 | 126/226/254 | 38/207/254 |
| vfx_damage_indicator | vfx | 2 | 217/218/220 | 217/218/220 |
| vfx_enemy_defeat | vfx | 8 | 128/188/220 | 17/154/217 |
| vfx_hazard_eruption | vfx | 6 | 97/192/192 | 67/136/192 |
| vfx_hazard_telegraph | vfx | 4 | 75/78/80 | 75/78/80 |
| vfx_whip_impact | vfx | 6 | 58/128/204 | 58/128/204 |
| whip_attack_air | whip | 8 | 17/76/107 | 17/76/107 |
| whip_attack_crouch | whip | 8 | 16/73/80 | 16/73/80 |
| whip_attack_ground | whip | 8 | 20/82/85 | 20/82/85 |


## boss_death  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_death_f00.png | 365 | 364 | 188 | +0 | 4 |  |  |  |
| boss_death_f01.png | 336 | 336 | 223 | +0 | 2 |  |  |  |
| boss_death_f02.png | 309 | 309 | 231 | +0 | 2 |  |  |  |
| boss_death_f03.png | 283 | 283 | 259 | +1 | 1 |  |  |  |
| boss_death_f04.png | 276 | 276 | 293 | +0 | 1 |  |  |  |
| boss_death_f05.png | 249 | 249 | 318 | +0 | 1 |  |  |  |
| boss_death_f06.png | 233 | 230 | 332 | +0 | 4 |  |  |  |
| boss_death_f07.png | 202 | 202 | 338 | +0 | 3 |  |  |  |
| boss_death_f08.png | 192 | 192 | 341 | +0 | 4 |  |  |  |
| boss_death_f09.png | 169 | 168 | 361 | +1 | 3 |  |  |  |
| boss_death_f10.png | 167 | 167 | 352 | +0 | 6 |  |  |  |
| boss_death_f11.png | 160 | 160 | 386 | +0 | 7 |  |  |  |
| **median** | **241** | **240** | | | | | | |

## boss_hazard_execute  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_execute_f00.png | 351 | 351 | 201 | +0 | 14 |  |  |  |
| boss_hazard_execute_f01.png | 310 | 310 | 343 | +0 | 11 |  |  |  |
| boss_hazard_execute_f02.png | 304 | 304 | 324 | +0 | 8 |  |  |  |
| boss_hazard_execute_f03.png | 351 | 351 | 116 | +0 | 2 |  |  |  |
| **median** | **330** | **330** | | | | | | |

## boss_hazard_recover  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_recover_f00.png | 252 | 252 | 292 | +0 | 1 |  |  |  |
| boss_hazard_recover_f01.png | 261 | 261 | 274 | +0 | 2 |  |  |  |
| boss_hazard_recover_f02.png | 350 | 350 | 268 | +0 | 2 |  |  |  |
| boss_hazard_recover_f03.png | 352 | 352 | 227 | +0 | 1 |  |  |  |
| boss_hazard_recover_f04.png | 352 | 352 | 234 | +0 | 4 |  |  |  |
| boss_hazard_recover_f05.png | 352 | 351 | 245 | +0 | 2 |  |  |  |
| **median** | **351** | **350** | | | | | | |

## boss_hazard_windup  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hazard_windup_f00.png | 352 | 352 | 158 | +0 | 2 |  |  |  |
| boss_hazard_windup_f01.png | 352 | 352 | 226 | +0 | 3 |  |  |  |
| boss_hazard_windup_f02.png | 351 | 351 | 285 | +0 | 5 |  |  |  |
| boss_hazard_windup_f03.png | 352 | 352 | 313 | +0 | 1 |  |  |  |
| boss_hazard_windup_f04.png | 351 | 351 | 313 | +1 | 5 |  |  |  |
| boss_hazard_windup_f05.png | 352 | 352 | 326 | +0 | 12 |  |  |  |
| boss_hazard_windup_f06.png | 351 | 351 | 327 | +1 | 3 |  |  |  |
| boss_hazard_windup_f07.png | 352 | 352 | 342 | +0 | 4 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_hurt  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_hurt_f00.png | 352 | 352 | 353 | +0 | 4 |  |  |  |
| boss_hurt_f01.png | 352 | 352 | 311 | +0 | 4 |  |  |  |
| boss_hurt_f02.png | 352 | 352 | 225 | +0 | 2 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_idle  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_idle_f00.png | 351 | 351 | 157 | +0 | 1 |  |  |  |
| boss_idle_f01.png | 351 | 351 | 272 | +0 | 4 |  |  |  |
| boss_idle_f02.png | 353 | 353 | 302 | +0 | 4 |  |  |  |
| boss_idle_f03.png | 352 | 352 | 343 | +0 | 4 |  |  |  |
| boss_idle_f04.png | 350 | 350 | 167 | +1 | 2 |  |  |  |
| boss_idle_f05.png | 352 | 352 | 293 | +0 | 3 |  |  |  |
| boss_idle_f06.png | 352 | 352 | 345 | +0 | 3 |  |  |  |
| boss_idle_f07.png | 353 | 353 | 158 | +0 | 1 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_strike_execute  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_execute_f00.png | 424 | 424 | 244 | +0 | 1 |  |  |  |
| boss_strike_execute_f01.png | 404 | 404 | 353 | +0 | 1 |  |  |  |
| boss_strike_execute_f02.png | 314 | 314 | 378 | +0 | 5 |  |  |  |
| boss_strike_execute_f03.png | 293 | 293 | 372 | +0 | 1 |  |  |  |
| **median** | **359** | **359** | | | | | | |

## boss_strike_recover  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_recover_f00.png | 317 | 263 | 333 | +1 | 15 |  |  |  |
| boss_strike_recover_f01.png | 327 | 274 | 320 | +0 | 11 |  |  |  |
| boss_strike_recover_f02.png | 358 | 350 | 272 | +1 | 3 |  |  |  |
| boss_strike_recover_f03.png | 352 | 352 | 184 | +0 | 2 |  |  |  |
| boss_strike_recover_f04.png | 352 | 351 | 346 | +0 | 2 |  |  |  |
| boss_strike_recover_f05.png | 352 | 352 | 342 | +0 | 1 |  |  |  |
| **median** | **352** | **350** | | | | | | |

## boss_strike_windup  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_strike_windup_f00.png | 352 | 352 | 149 | +0 | 1 |  |  |  |
| boss_strike_windup_f01.png | 352 | 352 | 235 | +0 | 2 |  |  |  |
| boss_strike_windup_f02.png | 351 | 351 | 268 | +0 | 4 |  |  |  |
| boss_strike_windup_f03.png | 351 | 351 | 307 | +1 | 1 |  |  |  |
| boss_strike_windup_f04.png | 352 | 352 | 263 | +0 | 5 |  |  |  |
| boss_strike_windup_f05.png | 352 | 352 | 300 | +0 | 1 |  |  |  |
| boss_strike_windup_f06.png | 350 | 350 | 317 | +1 | 2 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_turn  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_turn_f00.png | 352 | 352 | 348 | +0 | 2 |  |  |  |
| boss_turn_f01.png | 352 | 352 | 326 | +0 | 2 |  |  |  |
| boss_turn_f02.png | 352 | 352 | 290 | +0 | 6 |  |  |  |
| boss_turn_f03.png | 352 | 352 | 350 | +0 | 3 |  |  |  |
| **median** | **352** | **352** | | | | | | |

## boss_walk  (actor=boss, canvas=[512, 512], pivot=[176, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| boss_walk_f00.png | 350 | 350 | 215 | +1 | 2 |  |  |  |
| boss_walk_f01.png | 351 | 351 | 256 | +0 | 2 |  |  |  |
| boss_walk_f02.png | 352 | 352 | 298 | +0 | 3 |  |  |  |
| boss_walk_f03.png | 352 | 352 | 339 | +0 | 2 |  |  |  |
| boss_walk_f04.png | 350 | 350 | 318 | +0 | 3 |  |  |  |
| boss_walk_f05.png | 351 | 351 | 318 | +0 | 2 |  |  |  |
| boss_walk_f06.png | 352 | 352 | 351 | +0 | 2 |  |  |  |
| boss_walk_f07.png | 351 | 350 | 339 | +0 | 3 |  |  |  |
| **median** | **351** | **351** | | | | | | |

## hero_attack_air  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_air_f00.png | 246 | 224 | 212 | +0 | 2 |  |  |  |
| hero_attack_air_f01.png | 223 | 223 | 210 | +1 | 1 |  |  |  |
| hero_attack_air_f02.png | 214 | 214 | 232 | +0 | 1 |  |  |  |
| hero_attack_air_f03.png | 229 | 198 | 259 | +1 | 3 |  |  |  |
| hero_attack_air_f04.png | 198 | 198 | 252 | +1 | 1 |  |  |  |
| hero_attack_air_f05.png | 224 | 224 | 214 | +0 | 1 |  |  |  |
| hero_attack_air_f06.png | 224 | 224 | 176 | +0 | 1 |  |  |  |
| hero_attack_air_f07.png | 223 | 223 | 178 | +1 | 1 |  |  |  |
| **median** | **224** | **223** | | | | | | |

## hero_attack_crouch  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_crouch_f00.png | 144 | 144 | 126 | +0 | 1 |  |  |  |
| hero_attack_crouch_f01.png | 144 | 144 | 126 | +0 | 1 |  |  |  |
| hero_attack_crouch_f02.png | 141 | 141 | 159 | +0 | 1 |  |  |  |
| hero_attack_crouch_f03.png | 143 | 143 | 161 | +0 | 1 |  |  |  |
| hero_attack_crouch_f04.png | 139 | 139 | 134 | +0 | 1 |  |  |  |
| hero_attack_crouch_f05.png | 140 | 140 | 136 | +0 | 1 |  |  |  |
| hero_attack_crouch_f06.png | 139 | 139 | 134 | +0 | 1 |  |  |  |
| hero_attack_crouch_f07.png | 142 | 142 | 131 | +0 | 1 |  |  |  |
| **median** | **142** | **142** | | | | | | |

## hero_attack_ground  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_attack_ground_f00.png | 224 | 224 | 173 | +0 | 1 |  |  |  |
| hero_attack_ground_f01.png | 224 | 224 | 173 | +0 | 1 |  |  |  |
| hero_attack_ground_f02.png | 223 | 223 | 230 | +0 | 1 |  |  |  |
| hero_attack_ground_f03.png | 203 | 203 | 246 | +0 | 1 |  |  |  |
| hero_attack_ground_f04.png | 224 | 224 | 226 | +0 | 1 |  |  |  |
| hero_attack_ground_f05.png | 224 | 224 | 200 | +0 | 1 |  |  |  |
| hero_attack_ground_f06.png | 224 | 224 | 65 | +0 | 1 |  |  |  |
| hero_attack_ground_f07.png | 224 | 224 | 65 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_crouch_enter  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_enter_f00.png | 211 | 211 | 66 | +0 | 1 |  |  |  |
| hero_crouch_enter_f01.png | 180 | 180 | 81 | +0 | 1 |  |  |  |
| hero_crouch_enter_f02.png | 146 | 146 | 94 | +0 | 1 |  |  |  |
| hero_crouch_enter_f03.png | 142 | 142 | 96 | +0 | 1 |  |  |  |
| **median** | **163** | **163** | | | | | | |

## hero_crouch_exit  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_exit_f00.png | 142 | 142 | 96 | +0 | 1 |  |  |  |
| hero_crouch_exit_f01.png | 146 | 146 | 94 | +0 | 1 |  |  |  |
| hero_crouch_exit_f02.png | 180 | 180 | 81 | +0 | 1 |  |  |  |
| hero_crouch_exit_f03.png | 211 | 211 | 66 | +0 | 1 |  |  |  |
| **median** | **163** | **163** | | | | | | |

## hero_crouch_idle  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_crouch_idle_f00.png | 146 | 146 | 116 | +0 | 1 |  |  |  |
| hero_crouch_idle_f01.png | 139 | 139 | 119 | +0 | 1 |  |  |  |
| hero_crouch_idle_f02.png | 135 | 135 | 120 | +0 | 1 |  |  |  |
| hero_crouch_idle_f03.png | 140 | 140 | 119 | +0 | 1 |  |  |  |
| hero_crouch_idle_f04.png | 140 | 140 | 119 | +0 | 1 |  |  |  |
| hero_crouch_idle_f05.png | 140 | 140 | 119 | +0 | 1 |  |  |  |
| **median** | **140** | **140** | | | | | | |

## hero_death  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_death_f00.png | 238 | 238 | 124 | +0 | 1 |  |  |  |
| hero_death_f01.png | 219 | 219 | 132 | +0 | 1 |  |  |  |
| hero_death_f02.png | 190 | 190 | 162 | +0 | 1 |  |  |  |
| hero_death_f03.png | 181 | 181 | 152 | +0 | 1 |  |  |  |
| hero_death_f04.png | 167 | 167 | 180 | +0 | 1 |  |  |  |
| hero_death_f05.png | 153 | 153 | 191 | +0 | 1 |  |  |  |
| hero_death_f06.png | 132 | 132 | 186 | +0 | 1 |  |  |  |
| hero_death_f07.png | 95 | 95 | 261 | +0 | 1 |  |  |  |
| hero_death_f08.png | 95 | 95 | 294 | +0 | 1 |  |  |  |
| hero_death_f09.png | 91 | 91 | 277 | +0 | 1 |  |  |  |
| **median** | **160** | **160** | | | | | | |

## hero_fall  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_fall_f00.png | 197 | 197 | 103 | +0 | 2 |  |  |  |
| hero_fall_f01.png | 218 | 218 | 120 | +0 | 3 |  |  |  |
| hero_fall_f02.png | 230 | 230 | 122 | +0 | 3 |  |  |  |
| hero_fall_f03.png | 224 | 224 | 113 | +0 | 1 |  |  |  |
| **median** | **221** | **221** | | | | | | |

## hero_get_up  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_get_up_f00.png | 123 | 123 | 134 | +0 | 1 |  |  |  |
| hero_get_up_f01.png | 156 | 156 | 139 | +1 | 2 |  |  |  |
| hero_get_up_f02.png | 145 | 142 | 144 | +0 | 5 |  |  |  |
| hero_get_up_f03.png | 164 | 164 | 144 | +1 | 3 |  |  |  |
| hero_get_up_f04.png | 208 | 208 | 121 | +0 | 1 |  |  |  |
| hero_get_up_f05.png | 205 | 205 | 115 | +0 | 1 |  |  |  |
| **median** | **160** | **160** | | | | | | |

## hero_hurt_recoil  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_hurt_recoil_f00.png | 224 | 224 | 70 | +0 | 1 |  |  |  |
| hero_hurt_recoil_f01.png | 224 | 224 | 120 | +0 | 1 |  |  |  |
| hero_hurt_recoil_f02.png | 209 | 209 | 132 | +0 | 1 |  |  |  |
| hero_hurt_recoil_f03.png | 224 | 224 | 127 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_idle  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_idle_f00.png | 224 | 224 | 84 | +0 | 4 |  |  |  |
| hero_idle_f01.png | 224 | 224 | 84 | +0 | 4 |  |  |  |
| hero_idle_f02.png | 224 | 224 | 84 | +0 | 8 |  |  |  |
| hero_idle_f03.png | 224 | 224 | 83 | +0 | 8 |  |  |  |
| hero_idle_f04.png | 224 | 224 | 83 | +0 | 8 |  |  |  |
| hero_idle_f05.png | 224 | 224 | 83 | +0 | 8 |  |  |  |
| hero_idle_f06.png | 224 | 224 | 84 | +0 | 8 |  |  |  |
| hero_idle_f07.png | 224 | 224 | 84 | +0 | 4 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_jump_apex  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_apex_f00.png | 224 | 224 | 176 | +0 | 1 |  |  |  |
| hero_jump_apex_f01.png | 178 | 178 | 218 | +0 | 2 |  |  |  |
| hero_jump_apex_f02.png | 200 | 200 | 198 | +0 | 2 |  |  |  |
| **median** | **200** | **200** | | | | | | |

## hero_jump_rise  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_rise_f00.png | 181 | 181 | 142 | +0 | 1 |  |  |  |
| hero_jump_rise_f01.png | 224 | 224 | 133 | +0 | 2 |  |  |  |
| hero_jump_rise_f02.png | 224 | 224 | 148 | +0 | 4 |  |  |  |
| hero_jump_rise_f03.png | 223 | 223 | 149 | +1 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_jump_takeoff  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_jump_takeoff_f00.png | 171 | 171 | 178 | +0 | 1 |  |  |  |
| hero_jump_takeoff_f01.png | 224 | 224 | 164 | +0 | 1 |  |  |  |
| hero_jump_takeoff_f02.png | 223 | 223 | 184 | +0 | 1 |  |  |  |
| **median** | **223** | **223** | | | | | | |

## hero_knockback  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_knockback_f00.png | 224 | 224 | 123 | +0 | 1 |  |  |  |
| hero_knockback_f01.png | 224 | 224 | 125 | +0 | 1 |  |  |  |
| hero_knockback_f02.png | 190 | 190 | 123 | +0 | 1 |  |  |  |
| hero_knockback_f03.png | 204 | 204 | 117 | +0 | 1 |  |  |  |
| **median** | **214** | **214** | | | | | | |

## hero_knockdown  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_knockdown_f00.png | 205 | 205 | 115 | +0 | 1 |  |  |  |
| hero_knockdown_f01.png | 208 | 208 | 121 | +0 | 1 |  |  |  |
| hero_knockdown_f02.png | 164 | 164 | 144 | +1 | 3 |  |  |  |
| hero_knockdown_f03.png | 145 | 142 | 144 | +0 | 5 |  |  |  |
| hero_knockdown_f04.png | 156 | 156 | 139 | +1 | 2 |  |  |  |
| hero_knockdown_f05.png | 123 | 123 | 134 | +0 | 1 |  |  |  |
| **median** | **160** | **160** | | | | | | |

## hero_land  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_land_f00.png | 223 | 223 | 112 | +0 | 1 |  |  |  |
| hero_land_f01.png | 224 | 224 | 135 | +0 | 2 |  |  |  |
| hero_land_f02.png | 174 | 174 | 143 | +0 | 1 |  |  |  |
| hero_land_f03.png | 224 | 224 | 71 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_start_move  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_start_move_f00.png | 224 | 224 | 75 | +0 | 1 |  |  |  |
| hero_start_move_f01.png | 224 | 224 | 180 | +0 | 1 |  |  |  |
| hero_start_move_f02.png | 224 | 224 | 172 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_stop_move  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_stop_move_f00.png | 224 | 224 | 206 | +0 | 1 |  |  |  |
| hero_stop_move_f01.png | 224 | 224 | 203 | +0 | 1 |  |  |  |
| hero_stop_move_f02.png | 224 | 224 | 79 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_turn  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_turn_f00.png | 224 | 224 | 84 | +0 | 1 |  |  |  |
| hero_turn_f01.png | 224 | 224 | 197 | +0 | 2 |  |  |  |
| hero_turn_f02.png | 224 | 224 | 88 | +0 | 1 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## hero_walk  (actor=hero, canvas=[512, 512], pivot=[256, 448])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| hero_walk_f00.png | 224 | 224 | 118 | +0 | 1 |  |  |  |
| hero_walk_f01.png | 223 | 223 | 130 | +0 | 5 |  |  |  |
| hero_walk_f02.png | 223 | 223 | 150 | +0 | 2 |  |  |  |
| hero_walk_f03.png | 223 | 223 | 169 | +0 | 3 |  |  |  |
| hero_walk_f04.png | 224 | 224 | 164 | +0 | 1 |  |  |  |
| hero_walk_f05.png | 223 | 223 | 145 | +0 | 3 |  |  |  |
| hero_walk_f06.png | 237 | 224 | 149 | +0 | 4 |  |  |  |
| hero_walk_f07.png | 242 | 224 | 152 | +0 | 2 |  |  |  |
| hero_walk_f08.png | 224 | 224 | 150 | +0 | 1 |  |  |  |
| hero_walk_f09.png | 224 | 224 | 156 | +0 | 3 |  |  |  |
| **median** | **224** | **224** | | | | | | |

## projectile_grave_shot  (actor=projectile, canvas=[64, 64], pivot=[32, 32])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| projectile_grave_shot_f00.png | 64 | 64 | 64 | -32 | 1 |  |  |  |
| projectile_grave_shot_f01.png | 64 | 64 | 64 | -32 | 1 |  |  |  |
| projectile_grave_shot_f02.png | 64 | 64 | 64 | -32 | 1 |  |  |  |
| **median** | **64** | **64** | | | | | | |

## pursuer_alert  (actor=pursuer, canvas=[320, 288], pivot=[128, 256])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_alert_f00.png | 111 | 111 | 203 | +1 | 2 |  |  |  |
| pursuer_alert_f01.png | 185 | 185 | 188 | +0 | 2 |  |  |  |
| pursuer_alert_f02.png | 207 | 207 | 179 | +0 | 3 |  |  |  |
| pursuer_alert_f03.png | 245 | 245 | 166 | +0 | 4 |  |  |  |
| **median** | **196** | **196** | | | | | | |

## pursuer_approach_walk  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_approach_walk_f00.png | 99 | 99 | 188 | +0 | 1 |  |  |  |
| pursuer_approach_walk_f01.png | 102 | 102 | 180 | +1 | 9 |  |  |  |
| pursuer_approach_walk_f02.png | 124 | 124 | 175 | +0 | 16 |  |  |  |
| pursuer_approach_walk_f03.png | 113 | 113 | 173 | +1 | 10 |  |  |  |
| pursuer_approach_walk_f04.png | 109 | 109 | 188 | +0 | 4 |  |  |  |
| pursuer_approach_walk_f05.png | 111 | 111 | 179 | +1 | 3 |  |  |  |
| pursuer_approach_walk_f06.png | 111 | 111 | 179 | +1 | 5 |  |  |  |
| pursuer_approach_walk_f07.png | 111 | 111 | 180 | +0 | 15 |  |  |  |
| **median** | **111** | **111** | | | | | | |

## pursuer_death  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_death_f00.png | 126 | 126 | 130 | +0 | 4 |  |  |  |
| pursuer_death_f01.png | 96 | 96 | 114 | +1 | 16 |  |  |  |
| pursuer_death_f02.png | 96 | 95 | 113 | +0 | 15 |  |  |  |
| pursuer_death_f03.png | 80 | 78 | 141 | +0 | 3 |  |  |  |
| pursuer_death_f04.png | 50 | 48 | 149 | +0 | 3 |  |  |  |
| pursuer_death_f05.png | 52 | 48 | 149 | +0 | 7 |  |  |  |
| **median** | **88** | **86** | | | | | | |

## pursuer_hurt  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_hurt_f00.png | 132 | 132 | 134 | +0 | 5 |  |  |  |
| pursuer_hurt_f01.png | 94 | 93 | 114 | +1 | 2 |  |  |  |
| pursuer_hurt_f02.png | 112 | 112 | 124 | +1 | 5 |  |  |  |
| **median** | **112** | **112** | | | | | | |

## pursuer_idle  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_idle_f00.png | 109 | 109 | 154 | +0 | 1 |  |  |  |
| pursuer_idle_f01.png | 148 | 148 | 163 | +1 | 3 |  |  |  |
| pursuer_idle_f02.png | 109 | 109 | 153 | +0 | 1 |  |  |  |
| pursuer_idle_f03.png | 111 | 111 | 158 | +0 | 9 |  |  |  |
| pursuer_idle_f04.png | 140 | 140 | 163 | +1 | 8 |  |  |  |
| pursuer_idle_f05.png | 110 | 110 | 158 | +0 | 9 |  |  |  |
| **median** | **110** | **110** | | | | | | |

## pursuer_lunge  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_lunge_f00.png | 95 | 95 | 102 | +0 | 8 |  |  |  |
| pursuer_lunge_f01.png | 61 | 61 | 119 | -1 | 5 |  |  |  |
| pursuer_lunge_f02.png | 50 | 50 | 134 | +0 | 10 |  |  |  |
| **median** | **61** | **61** | | | | | | |

## pursuer_lunge_windup  (actor=pursuer, canvas=[320, 288], pivot=[128, 256])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_lunge_windup_f00.png | 171 | 170 | 91 | +1 | 6 |  |  |  |
| pursuer_lunge_windup_f01.png | 150 | 150 | 83 | +1 | 4 |  |  |  |
| pursuer_lunge_windup_f02.png | 112 | 111 | 93 | +1 | 6 |  |  |  |
| pursuer_lunge_windup_f03.png | 116 | 116 | 88 | +0 | 1 |  |  |  |
| **median** | **133** | **133** | | | | | | |

## pursuer_patrol_walk  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_patrol_walk_f00.png | 121 | 121 | 174 | +0 | 4 |  |  |  |
| pursuer_patrol_walk_f01.png | 121 | 121 | 152 | +1 | 8 |  |  |  |
| pursuer_patrol_walk_f02.png | 122 | 122 | 162 | +1 | 3 |  |  |  |
| pursuer_patrol_walk_f03.png | 112 | 112 | 161 | +1 | 3 |  |  |  |
| pursuer_patrol_walk_f04.png | 108 | 108 | 169 | +1 | 2 |  |  |  |
| pursuer_patrol_walk_f05.png | 108 | 108 | 163 | +1 | 2 |  |  |  |
| pursuer_patrol_walk_f06.png | 107 | 105 | 163 | +3 | 11 |  |  |  |
| pursuer_patrol_walk_f07.png | 106 | 106 | 163 | +1 | 3 |  |  |  |
| **median** | **110** | **110** | | | | | | |

## pursuer_recovery  (actor=pursuer, canvas=[320, 192], pivot=[128, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| pursuer_recovery_f00.png | 88 | 87 | 158 | +2 | 10 |  |  |  |
| pursuer_recovery_f01.png | 111 | 111 | 112 | +1 | 12 |  |  |  |
| pursuer_recovery_f02.png | 140 | 140 | 126 | +0 | 8 |  |  |  |
| pursuer_recovery_f03.png | 109 | 109 | 128 | +0 | 5 |  |  |  |
| **median** | **110** | **110** | | | | | | |

## ranged_aim  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_aim_f00.png | 288 | 288 | 173 | +0 | 1 |  |  |  |
| ranged_aim_f01.png | 288 | 288 | 204 | +0 | 2 |  |  |  |
| ranged_aim_f02.png | 288 | 288 | 212 | +0 | 3 |  |  |  |
| ranged_aim_f03.png | 288 | 288 | 218 | +0 | 4 |  |  |  |
| ranged_aim_f04.png | 286 | 286 | 185 | +0 | 16 |  |  |  |
| ranged_aim_f05.png | 279 | 279 | 174 | +0 | 8 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_death  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_death_f00.png | 288 | 288 | 150 | +0 | 1 |  |  |  |
| ranged_death_f01.png | 288 | 288 | 172 | +0 | 1 |  |  |  |
| ranged_death_f02.png | 287 | 287 | 170 | +0 | 2 |  |  |  |
| ranged_death_f03.png | 288 | 288 | 165 | +0 | 2 |  |  |  |
| ranged_death_f04.png | 288 | 288 | 171 | +0 | 1 |  |  |  |
| ranged_death_f05.png | 284 | 284 | 169 | +0 | 14 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_fire  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_fire_f00.png | 272 | 272 | 160 | +0 | 8 |  |  |  |
| ranged_fire_f01.png | 288 | 288 | 118 | +0 | 10 |  |  |  |
| ranged_fire_f02.png | 288 | 288 | 117 | +0 | 3 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_hurt  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_hurt_f00.png | 270 | 270 | 239 | +0 | 3 |  |  |  |
| ranged_hurt_f01.png | 288 | 288 | 191 | +0 | 1 |  |  |  |
| ranged_hurt_f02.png | 288 | 288 | 180 | +0 | 4 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_idle  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_idle_f00.png | 288 | 288 | 132 | +0 | 1 |  |  |  |
| ranged_idle_f01.png | 288 | 288 | 138 | +0 | 1 |  |  |  |
| ranged_idle_f02.png | 288 | 288 | 144 | +0 | 3 |  |  |  |
| ranged_idle_f03.png | 279 | 279 | 155 | +0 | 1 |  |  |  |
| ranged_idle_f04.png | 288 | 288 | 148 | +0 | 1 |  |  |  |
| ranged_idle_f05.png | 288 | 288 | 143 | +0 | 1 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## ranged_recover  (actor=ranged, canvas=[256, 320], pivot=[128, 288])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| ranged_recover_f00.png | 269 | 269 | 239 | +0 | 3 |  |  |  |
| ranged_recover_f01.png | 288 | 288 | 256 | +0 | 3 |  |  |  |
| ranged_recover_f02.png | 288 | 288 | 256 | +0 | 2 |  |  |  |
| ranged_recover_f03.png | 288 | 288 | 256 | +0 | 1 |  |  |  |
| ranged_recover_f04.png | 288 | 288 | 256 | +0 | 1 |  |  |  |
| ranged_recover_f05.png | 288 | 288 | 256 | +0 | 2 |  |  |  |
| ranged_recover_f06.png | 288 | 288 | 256 | +0 | 1 |  |  |  |
| **median** | **288** | **288** | | | | | | |

## swooper_cruise  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_cruise_f00.png | 179 | 179 | 162 | -89 | 3 |  |  |  |
| swooper_cruise_f01.png | 180 | 180 | 173 | -90 | 1 |  |  |  |
| swooper_cruise_f02.png | 138 | 138 | 188 | -69 | 2 |  |  |  |
| swooper_cruise_f03.png | 142 | 142 | 171 | -71 | 1 |  |  |  |
| swooper_cruise_f04.png | 163 | 163 | 195 | -81 | 1 |  |  |  |
| swooper_cruise_f05.png | 171 | 171 | 171 | -85 | 2 |  |  |  |
| swooper_cruise_f06.png | 169 | 169 | 183 | -84 | 1 |  |  |  |
| swooper_cruise_f07.png | 169 | 169 | 179 | -84 | 2 |  |  |  |
| **median** | **169** | **169** | | | | | | |

## swooper_death_fall  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_death_fall_f00.png | 213 | 212 | 201 | -107 | 2 |  |  |  |
| swooper_death_fall_f01.png | 170 | 170 | 191 | -85 | 1 |  |  |  |
| swooper_death_fall_f02.png | 188 | 188 | 189 | -94 | 1 |  |  |  |
| swooper_death_fall_f03.png | 162 | 162 | 174 | -81 | 10 |  |  |  |
| swooper_death_fall_f04.png | 89 | 89 | 305 | -45 | 2 |  |  |  |
| **median** | **170** | **170** | | | | | | |

## swooper_dive  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_dive_f00.png | 156 | 156 | 156 | -78 | 1 |  |  |  |
| swooper_dive_f01.png | 161 | 161 | 152 | -81 | 1 |  |  |  |
| swooper_dive_f02.png | 174 | 174 | 221 | -87 | 1 |  |  |  |
| swooper_dive_f03.png | 188 | 188 | 240 | -94 | 1 |  |  |  |
| **median** | **168** | **168** | | | | | | |

## swooper_dive_telegraph  (actor=swooper, canvas=[512, 320], pivot=[256, 160])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_dive_telegraph_f00.png | 200 | 200 | 113 | -100 | 2 |  |  |  |
| swooper_dive_telegraph_f01.png | 199 | 198 | 87 | -100 | 3 |  |  |  |
| swooper_dive_telegraph_f02.png | 166 | 166 | 102 | -83 | 1 |  |  |  |
| swooper_dive_telegraph_f03.png | 127 | 127 | 128 | -63 | 1 |  |  |  |
| **median** | **182** | **182** | | | | | | |

## swooper_hurt  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_hurt_f00.png | 180 | 180 | 184 | -90 | 1 |  |  |  |
| swooper_hurt_f01.png | 170 | 170 | 145 | -85 | 1 |  |  |  |
| swooper_hurt_f02.png | 128 | 128 | 181 | -64 | 1 |  |  |  |
| **median** | **170** | **170** | | | | | | |

## swooper_perch_idle  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_perch_idle_f00.png | 174 | 174 | 156 | -87 | 1 |  |  |  |
| swooper_perch_idle_f01.png | 172 | 172 | 147 | -85 | 1 |  |  |  |
| swooper_perch_idle_f02.png | 168 | 168 | 149 | -84 | 1 |  |  |  |
| swooper_perch_idle_f03.png | 173 | 173 | 154 | -87 | 1 |  |  |  |
| swooper_perch_idle_f04.png | 166 | 166 | 148 | -82 | 1 |  |  |  |
| swooper_perch_idle_f05.png | 170 | 170 | 156 | -84 | 1 |  |  |  |
| **median** | **171** | **171** | | | | | | |

## swooper_recovery_climb  (actor=swooper, canvas=[384, 256], pivot=[192, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| swooper_recovery_climb_f00.png | 161 | 161 | 131 | -80 | 3 |  |  |  |
| swooper_recovery_climb_f01.png | 139 | 139 | 182 | -70 | 3 |  |  |  |
| swooper_recovery_climb_f02.png | 126 | 126 | 167 | -63 | 3 |  |  |  |
| swooper_recovery_climb_f03.png | 167 | 167 | 164 | -83 | 1 |  |  |  |
| swooper_recovery_climb_f04.png | 171 | 171 | 143 | -85 | 1 |  |  |  |
| swooper_recovery_climb_f05.png | 165 | 164 | 146 | -82 | 3 |  |  |  |
| **median** | **163** | **162** | | | | | | |

## vfx_checkpoint_activate  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_checkpoint_activate_f00.png | 126 | 38 | 61 | -126 | 2 |  |  |  |
| vfx_checkpoint_activate_f01.png | 236 | 124 | 110 | -126 | 13 |  |  |  |
| vfx_checkpoint_activate_f02.png | 254 | 182 | 150 | -126 | 9 |  |  |  |
| vfx_checkpoint_activate_f03.png | 217 | 217 | 142 | -126 | 5 |  |  |  |
| vfx_checkpoint_activate_f04.png | 209 | 209 | 137 | -126 | 5 |  |  |  |
| vfx_checkpoint_activate_f05.png | 205 | 205 | 123 | -126 | 4 |  |  |  |
| vfx_checkpoint_activate_f06.png | 254 | 254 | 122 | -126 | 3 |  |  |  |
| vfx_checkpoint_activate_f07.png | 249 | 249 | 111 | -126 | 2 |  |  |  |
| **median** | **226** | **207** | | | | | | |

## vfx_damage_indicator  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_damage_indicator_f00.png | 217 | 217 | 200 | -109 | 17 |  |  |  |
| vfx_damage_indicator_f01.png | 220 | 220 | 217 | -111 | 21 |  |  |  |
| **median** | **218** | **218** | | | | | | |

## vfx_enemy_defeat  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_enemy_defeat_f00.png | 128 | 128 | 128 | -64 | 1 |  |  |  |
| vfx_enemy_defeat_f01.png | 174 | 174 | 174 | -86 | 2 |  |  |  |
| vfx_enemy_defeat_f02.png | 217 | 217 | 217 | -108 | 4 |  |  |  |
| vfx_enemy_defeat_f03.png | 220 | 135 | 174 | -112 | 25 |  |  |  |
| vfx_enemy_defeat_f04.png | 214 | 214 | 223 | -112 | 2 |  |  |  |
| vfx_enemy_defeat_f05.png | 202 | 202 | 195 | -106 | 13 |  |  |  |
| vfx_enemy_defeat_f06.png | 168 | 29 | 13 | +29 | 44 |  |  |  |
| vfx_enemy_defeat_f07.png | 136 | 17 | 12 | +0 | 16 |  |  |  |
| **median** | **188** | **154** | | | | | | |

## vfx_hazard_eruption  (actor=vfx, canvas=[320, 192], pivot=[160, 176])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_hazard_eruption_f00.png | 101 | 67 | 119 | -16 | 21 |  |  |  |
| vfx_hazard_eruption_f01.png | 192 | 192 | 222 | -16 | 20 |  |  |  |
| vfx_hazard_eruption_f02.png | 192 | 192 | 312 | -16 | 6 |  |  |  |
| vfx_hazard_eruption_f03.png | 192 | 192 | 320 | -16 | 1 |  |  |  |
| vfx_hazard_eruption_f04.png | 192 | 80 | 200 | +96 | 53 |  |  |  |
| vfx_hazard_eruption_f05.png | 97 | 75 | 204 | -16 | 9 |  |  |  |
| **median** | **192** | **136** | | | | | | |

## vfx_hazard_telegraph  (actor=vfx, canvas=[320, 192], pivot=[160, 176])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_hazard_telegraph_f00.png | 77 | 77 | 320 | -9 | 1 |  |  |  |
| vfx_hazard_telegraph_f01.png | 75 | 75 | 320 | -7 | 1 |  |  |  |
| vfx_hazard_telegraph_f02.png | 79 | 79 | 320 | -11 | 1 |  |  |  |
| vfx_hazard_telegraph_f03.png | 80 | 80 | 320 | -12 | 1 |  |  |  |
| **median** | **78** | **78** | | | | | | |

## vfx_whip_impact  (actor=vfx, canvas=[256, 256], pivot=[128, 128])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| vfx_whip_impact_f00.png | 86 | 86 | 86 | -43 | 26 |  |  |  |
| vfx_whip_impact_f01.png | 148 | 148 | 148 | -74 | 39 |  |  |  |
| vfx_whip_impact_f02.png | 204 | 204 | 204 | -102 | 43 |  |  |  |
| vfx_whip_impact_f03.png | 162 | 162 | 162 | -81 | 35 |  |  |  |
| vfx_whip_impact_f04.png | 108 | 108 | 108 | -54 | 30 |  |  |  |
| vfx_whip_impact_f05.png | 58 | 58 | 58 | -29 | 32 |  |  |  |
| **median** | **128** | **128** | | | | | | |

## whip_attack_air  (actor=whip, canvas=[768, 512], pivot=[276, 308])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| whip_attack_air_f00.png | 70 | 70 | 79 | +181 | 1 | 202 | 92 | 281 |
| whip_attack_air_f01.png | 66 | 66 | 81 | +189 | 1 | 204 | 90 | 285 |
| whip_attack_air_f02.png | 97 | 97 | 216 | +147 | 1 | 228 | 130 | 444 |
| whip_attack_air_f03.png | 17 | 17 | 251 | +185 | 1 | 369 | 116 | 620 |
| whip_attack_air_f04.png | 107 | 107 | 175 | +64 | 1 | 389 | 142 | 564 |
| whip_attack_air_f05.png | 57 | 57 | 179 | +104 | 1 | 350 | 191 | 529 |
| whip_attack_air_f06.png | 81 | 81 | 77 | +66 | 1 | 341 | 205 | 418 |
| whip_attack_air_f07.png | 83 | 83 | 78 | +68 | 1 | 344 | 202 | 422 |
| **median** | **76** | **76** | | | | | | |

## whip_attack_crouch  (actor=whip, canvas=[768, 512], pivot=[276, 308])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| whip_attack_crouch_f00.png | 72 | 72 | 81 | +110 | 1 | 197 | 168 | 278 |
| whip_attack_crouch_f01.png | 74 | 74 | 81 | +110 | 1 | 198 | 167 | 279 |
| whip_attack_crouch_f02.png | 53 | 53 | 233 | +85 | 1 | 329 | 216 | 562 |
| whip_attack_crouch_f03.png | 16 | 16 | 286 | +87 | 1 | 335 | 214 | 621 |
| whip_attack_crouch_f04.png | 74 | 74 | 238 | +8 | 1 | 219 | 243 | 457 |
| whip_attack_crouch_f05.png | 47 | 47 | 162 | +102 | 1 | 186 | 195 | 348 |
| whip_attack_crouch_f06.png | 80 | 80 | 78 | +83 | 1 | 177 | 190 | 255 |
| whip_attack_crouch_f07.png | 76 | 76 | 78 | +40 | 1 | 202 | 234 | 280 |
| **median** | **73** | **73** | | | | | | |

## whip_attack_ground  (actor=whip, canvas=[768, 512], pivot=[276, 308])

| frame | h_full | lcc_h | lcc_w | foot_off | ncomp | grip_x | grip_y | tip_x |
|---|---|---|---|---|---|---|---|---|
| whip_attack_ground_f00.png | 81 | 81 | 99 | +186 | 1 | 168 | 79 | 267 |
| whip_attack_ground_f01.png | 82 | 82 | 110 | +191 | 1 | 170 | 74 | 280 |
| whip_attack_ground_f02.png | 85 | 85 | 234 | +141 | 1 | 379 | 160 | 613 |
| whip_attack_ground_f03.png | 20 | 20 | 257 | +157 | 1 | 365 | 143 | 622 |
| whip_attack_ground_f04.png | 83 | 83 | 240 | +77 | 1 | 219 | 164 | 459 |
| whip_attack_ground_f05.png | 39 | 39 | 169 | +166 | 1 | 300 | 116 | 469 |
| whip_attack_ground_f06.png | 83 | 83 | 83 | +89 | 1 | 251 | 183 | 334 |
| whip_attack_ground_f07.png | 85 | 85 | 82 | +89 | 1 | 250 | 182 | 332 |
| **median** | **82** | **82** | | | | | | |

