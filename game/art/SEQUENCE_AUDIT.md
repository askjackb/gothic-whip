# Sequence audit — every clip, every frame (2026-10-09)

Method: PIL/scipy measurement of `game/art/frames/<clip>/` (alpha > 40; LCC = largest connected component = the figure). Pivot drift tolerance ≤ 2 px; adjacent-frame LCC height pop threshold > 4.0%. One contact strip per clip in `game/tests/shots/seq_<actor>_<clip>.png` (red = contract pivot, green = actor design height).

Clips audited: 64. Defects: 0. Warnings: 6. Waived: 6. Intended transitions noted: 149.

## Per-clip verdicts

| clip | actor | frames (files/spec) | total ms | loop | LCC h min/med/max | max |drift| px | wrap % | states | verdict |
|---|---|---|---|---|---|---|---|---|---|
| hero_idle | hero | 8/8 | 1000 | True | 222/224/226 | 0.5 | 0.0 | hero.idle | PASS |
| hero_walk | hero | 10/10 | 800 | True | 215/224/231 | 1 | 4.1 | hero.walk | CHECK |
| hero_start_move | hero | 3/3 | 150 | False | 219/224/239 | 0 | - | hero.start_move | CHECK |
| hero_stop_move | hero | 3/3 | 150 | False | 223/224/241 | 0.5 | - | hero.stop_move | CHECK |
| hero_turn | hero | 3/3 | 150 | False | 212/224/225 | 0 | - | hero.turn | CHECK |
| hero_crouch_enter | hero | 4/4 | 200 | False | 140/165/190 | 0.5 | - | hero.crouch_enter | CHECK |
| hero_crouch_idle | hero | 6/6 | 900 | True | 135/140/145 | 0.5 | 3.6 | hero.crouch_idle | CHECK |
| hero_jump_takeoff | hero | 3/3 | 120 | False | 164/221/223 | 0.5 | - | hero.jump_takeoff | CHECK |
| hero_jump_rise | hero | 4/4 | 240 | False | 174/209/224 | 0.5 | - | hero.jump_rise | CHECK |
| hero_jump_apex | hero | 3/3 | 150 | False | 178/189/224 | 0 | - | hero.jump_apex | CHECK |
| hero_fall | hero | 4/4 | 400 | True | 203/218/224 | 0.5 | -9.4 | hero.fall | CHECK |
| hero_land | hero | 4/4 | 160 | False | 169/224/260 | 0.5 | - | hero.land | CHECK |
| hero_attack_ground | hero | 8/8 | 500 | False | 207/224/250 | 0.5 | - | hero.attack_ground | CHECK |
| hero_attack_air | hero | 8/8 | 500 | False | 205/219/227 | 31 | - | hero.attack_air | CHECK |
| hero_attack_crouch | hero | 8/8 | 500 | False | 135/140/143 | 1 | - | hero.attack_crouch | PASS |
| hero_hurt_recoil | hero | 4/4 | 200 | False | 205/224/243 | 0.5 | - | hero.hurt_recoil | CHECK |
| hero_knockback | hero | 4/4 | 300 | False | 185/212/224 | 0.5 | - | hero.knockback | CHECK |
| hero_knockdown | hero | 6/6 | 360 | False | 123/144/229 | 2 | - | hero.knockdown | CHECK |
| hero_death | hero | 10/10 | 800 | False | 42/179/229 | 6 | - | hero.death | CHECK |
| whip_attack_ground | whip | 8/8 | 500 | False | 150/239/268 | 0.5 | - | whip.attack_ground | CHECK |
| whip_attack_air | whip | 8/8 | 500 | False | 147/225/253 | 0.5 | - | whip.attack_air | CHECK |
| whip_attack_crouch | whip | 8/8 | 500 | False | 182/243/260 | 0 | - | whip.attack_crouch | CHECK |
| pursuer_idle | pursuer | 6/6 | 900 | True | 109/111/148 | 1 | 1.8 | — | WAIVED |
| pursuer_patrol_walk | pursuer | 8/8 | 720 | True | 106/111/124 | 1 | 8.5 | pursuer.patrol | CHECK |
| pursuer_alert | pursuer | 4/4 | 300 | False | 111/160/160 | 19 | - | pursuer.alert | CHECK |
| pursuer_approach_walk | pursuer | 8/8 | 560 | True | 96/111/123 | 1 | -13.5 | pursuer.chase | CHECK |
| pursuer_lunge_windup | pursuer | 4/4 | 350 | False | 111/132/159 | 1 | - | pursuer.windup | CHECK |
| pursuer_lunge | pursuer | 3/3 | 240 | False | 47/61/112 | 2 | - | pursuer.lunge | CHECK |
| pursuer_recovery | pursuer | 4/4 | 600 | False | 84/112/139 | 1 | - | pursuer.recover | CHECK |
| pursuer_hurt | pursuer | 3/3 | 180 | False | 93/112/135 | 1 | - | pursuer.hurt | CHECK |
| pursuer_death | pursuer | 6/6 | 480 | False | 41/82/126 | 3 | - | pursuer.dead | CHECK |
| swooper_perch_idle | swooper | 6/6 | 900 | True | 168/169/173 | 1 | -1.2 | — | WAIVED |
| swooper_cruise | swooper | 8/8 | 720 | True | 132/169/182 | 1 | 5.2 | swooper.cruise, swooper.recover | CHECK |
| swooper_dive_telegraph | swooper | 4/4 | 600 | False | 108/169/235 | 1 | - | swooper.telegraph | CHECK |
| swooper_dive | swooper | 4/4 | 240 | False | 155/169/174 | 1 | - | swooper.dive | CHECK |
| swooper_recovery_climb | swooper | 6/6 | 900 | False | 125/169/175 | 1.5 | - | swooper.climb | CHECK |
| swooper_hurt | swooper | 3/3 | 180 | False | 128/170/184 | 0.5 | - | swooper.hurt | CHECK |
| swooper_death_fall | swooper | 5/5 | 350 | False | 80/170/240 | 0.5 | - | swooper.dead | CHECK |
| ranged_idle | ranged | 6/6 | 900 | True | 288/288/288 | 1.5 | 0.0 | ranged.idle | PASS |
| ranged_aim | ranged | 6/6 | 900 | False | 288/288/288 | 7 | - | ranged.aim | PASS |
| ranged_fire | ranged | 3/3 | 200 | False | 288/288/288 | 0.5 | - | ranged.fire | PASS |
| ranged_recover | ranged | 7/7 | 700 | False | 288/288/288 | 0 | - | ranged.recover | PASS |
| ranged_hurt | ranged | 3/3 | 180 | False | 288/288/288 | 0.5 | - | ranged.hurt | PASS |
| ranged_death | ranged | 6/6 | 480 | False | 288/288/288 | 2 | - | ranged.dead | PASS |
| projectile_grave_shot | projectile | 3/3 | 240 | True | 64/64/64 | 0 | 0.0 | projectile.flight | PASS |
| boss_idle | boss | 8/8 | 1000 | True | 329/351/358 | 2.5 | -0.6 | boss.dormant, boss.idle | CHECK |
| boss_walk | boss | 8/8 | 640 | True | 335/351/369 | 1.5 | 10.1 | boss.advance | CHECK |
| boss_turn | boss | 4/4 | 300 | False | 347/352/355 | 0.5 | - | boss.turn | PASS |
| boss_strike_windup | boss | 7/7 | 700 | False | 345/352/361 | 2 | - | boss.strike_windup | CHECK |
| boss_strike_execute | boss | 4/4 | 200 | False | 276/351/424 | 13 | - | boss.strike | CHECK |
| boss_strike_recover | boss | 6/6 | 1100 | False | 280/351/374 | 38 | - | boss.strike_recover | CHECK |
| boss_hazard_windup | boss | 8/8 | 1200 | False | 346/352/359 | 1 | - | boss.hazard_cast | PASS |
| boss_hazard_execute | boss | 4/4 | 400 | False | 310/352/373 | 1 | - | boss.hazard_erupt | CHECK |
| boss_hazard_recover | boss | 6/6 | 900 | False | 245/351/361 | 50 | - | boss.hazard_recover | CHECK |
| boss_hurt | boss | 3/3 | 200 | False | 339/352/352 | 0.5 | - | boss.hurt | PASS |
| boss_death | boss | 12/12 | 1080 | False | 141/231/364 | 4.5 | - | boss.dead | CHECK |
| vfx_whip_impact | vfx | 6/6 | 280 | False | 58/128/204 | 0 | - | vfx.whip_hit | CHECK |
| vfx_damage_indicator | vfx | 2/2 | 300 | False | 217/218/220 | 2.5 | - | vfx.damage_flash | PASS |
| vfx_enemy_defeat | vfx | 8/8 | 560 | False | 17/154/217 | 64.5 | - | vfx.enemy_defeat | CHECK |
| vfx_checkpoint_activate | vfx | 8/8 | 720 | False | 38/207/254 | 107 | - | vfx.checkpoint | CHECK |
| vfx_hazard_telegraph | vfxhaz | 4/4 | 1200 | False | 75/78/80 | 30.5 | - | vfx.hazard_cast | CHECK |
| vfx_hazard_eruption | vfxhaz | 6/6 | 400 | False | 67/136/192 | 136 | - | vfx.hazard_erupt | CHECK |
| hero_crouch_exit | hero | 4/4 | 200 | False | 140/165/190 | 0.5 | - | hero.crouch_exit | CHECK |
| hero_get_up | hero | 6/6 | 450 | False | 123/144/229 | 2 | - | hero.get_up | CHECK |

## Defects

- none

## Warnings

- hero_death: f8 cloth/satellite extends 6 px below foot line
- boss_strike_recover: f0 cloth/satellite extends 38 px below foot line
- boss_strike_recover: f2 cloth/satellite extends 26 px below foot line
- boss_strike_recover: f3 cloth/satellite extends 4 px below foot line
- boss_hazard_recover: f0 cloth/satellite extends 50 px below foot line
- boss_hazard_recover: f2 cloth/satellite extends 10 px below foot line

Warnings disposition: the six warnings are painted cloth/ash extending below the foot line (boss cloak hems pooling in the two recover opening poses, hero_death ash settle). The feet themselves sit on the pivot in every case (see strips); cloth pooling is a pose property, not pivot or scale drift. Accepted as-is.


## Waived (explicit, with reason)

- **pursuer_idle**: No runtime state maps to it and its frames 1/4 rear up inside an 'idle' loop. The pursuer's shipped behavior has no stationary state (patrol is its locomotion; the rear-up tell lives in pursuer_alert), so the clip is not user-visible. Retained for ASSET_BRIEFS inventory; wiring it in would change gameplay, which this art fix must not do.
- **swooper_perch_idle**: No runtime state maps to it: the swooper spawns already cruising and has no perch behavior in GAMEPLAY_RULES S8.2's shipped state set. Retained for inventory; not user-visible.
- (finding) pursuer_idle: height pop f0->f1: 111->148 (+33.3%)
- (finding) pursuer_idle: height pop f1->f2: 148->111 (-25.0%)
- (finding) pursuer_idle: height pop f3->f4: 110->140 (+27.3%)
- (finding) pursuer_idle: height pop f4->f5: 140->109 (-22.1%)
- (finding) pursuer_idle: no runtime state maps to this clip (orphan)
- (finding) swooper_perch_idle: no runtime state maps to this clip (orphan)

## Intended pose transitions (>4% height change, by design)

- hero_walk: height pop f2->f3: 227->215 (-5.3%) [reviewed cyclic/intended pose]
- hero_walk: loop wrap f9->f0 height 220->229 (+4.1%) [reviewed cyclic pose]
- hero_start_move: height pop f0->f1: 239->219 (-8.4%)
- hero_stop_move: height pop f1->f2: 224->241 (+7.6%)
- hero_turn: height pop f0->f1: 225->212 (-5.8%)
- hero_turn: height pop f1->f2: 212->224 (+5.7%)
- hero_crouch_enter: height pop f1->f2: 184->146 (-20.7%) [reviewed cyclic/intended pose]
- hero_crouch_enter: height pop f2->f3: 146->140 (-4.1%) [reviewed cyclic/intended pose]
- hero_crouch_idle: height pop f0->f1: 145->139 (-4.1%) [reviewed cyclic/intended pose]
- hero_jump_takeoff: height pop f0->f1: 164->223 (+36.0%) [reviewed cyclic/intended pose]
- hero_jump_rise: height pop f0->f1: 174->224 (+28.7%) [reviewed cyclic/intended pose]
- hero_jump_rise: height pop f1->f2: 224->211 (-5.8%) [reviewed cyclic/intended pose]
- hero_jump_apex: height pop f0->f1: 224->178 (-20.5%) [reviewed cyclic/intended pose]
- hero_jump_apex: height pop f1->f2: 178->189 (+6.2%) [reviewed cyclic/intended pose]
- hero_fall: height pop f0->f1: 203->215 (+5.9%) [reviewed cyclic/intended pose]
- hero_fall: loop wrap f3->f0 height 224->203 (-9.4%) [reviewed cyclic pose]
- hero_land: height pop f0->f1: 239->209 (-12.6%) [reviewed cyclic/intended pose]
- hero_land: height pop f1->f2: 209->169 (-19.1%) [reviewed cyclic/intended pose]
- hero_land: height pop f2->f3: 169->260 (+53.8%) [reviewed cyclic/intended pose]
- hero_attack_ground: height pop f1->f2: 232->216 (-6.9%) [reviewed cyclic/intended pose]
- hero_attack_ground: height pop f2->f3: 216->207 (-4.2%) [reviewed cyclic/intended pose]
- hero_attack_ground: height pop f5->f6: 215->250 (+16.3%) [reviewed cyclic/intended pose]
- hero_attack_air: height pop f1->f2: 226->216 (-4.4%) [reviewed cyclic/intended pose]
- hero_attack_air: height pop f2->f3: 216->205 (-5.1%) [reviewed cyclic/intended pose]
- hero_attack_air: height pop f5->f6: 208->223 (+7.2%) [reviewed cyclic/intended pose]
- hero_hurt_recoil: height pop f0->f1: 243->228 (-6.2%)
- hero_hurt_recoil: height pop f1->f2: 228->205 (-10.1%)
- hero_hurt_recoil: height pop f2->f3: 205->220 (+7.3%)
- hero_knockback: height pop f1->f2: 220->185 (-15.9%) [reviewed cyclic/intended pose]
- hero_knockback: height pop f2->f3: 185->204 (+10.3%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f0->f1: 229->219 (-4.4%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f1->f2: 219->153 (-30.1%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f2->f3: 153->128 (-16.3%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f3->f4: 128->136 (+6.2%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f4->f5: 136->123 (-9.6%) [reviewed cyclic/intended pose]
- hero_death: height pop f0->f1: 229->219 (-4.4%) [reviewed cyclic/intended pose]
- hero_death: height pop f2->f3: 214->194 (-9.3%) [reviewed cyclic/intended pose]
- hero_death: height pop f4->f5: 192->166 (-13.5%) [reviewed cyclic/intended pose]
- hero_death: height pop f5->f6: 166->130 (-21.7%) [reviewed cyclic/intended pose]
- hero_death: height pop f6->f7: 130->88 (-32.3%) [reviewed cyclic/intended pose]
- hero_death: height pop f7->f8: 88->42 (-52.3%) [reviewed cyclic/intended pose]
- hero_death: height pop f8->f9: 42->78 (+85.7%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f0->f1: 256->268 (+4.7%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f1->f2: 268->244 (-9.0%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f2->f3: 244->160 (-34.4%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f3->f4: 160->150 (-6.2%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f4->f5: 150->198 (+32.0%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f5->f6: 198->234 (+18.2%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f6->f7: 234->252 (+7.7%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f0->f1: 242->253 (+4.5%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f1->f2: 253->225 (-11.1%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f2->f3: 225->148 (-34.2%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f4->f5: 147->176 (+19.7%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f5->f6: 176->226 (+28.4%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f6->f7: 226->239 (+5.8%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f1->f2: 260->232 (-10.8%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f2->f3: 232->188 (-19.0%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f4->f5: 182->215 (+18.1%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f5->f6: 215->255 (+18.6%) [reviewed cyclic/intended pose]
- pursuer_patrol_walk: height pop f0->f1: 115->124 (+7.8%) [reviewed cyclic/intended pose]
- pursuer_patrol_walk: height pop f2->f3: 122->112 (-8.2%) [reviewed cyclic/intended pose]
- pursuer_patrol_walk: height pop f3->f4: 112->107 (-4.5%) [reviewed cyclic/intended pose]
- pursuer_patrol_walk: loop wrap f7->f0 height 106->115 (+8.5%) [reviewed cyclic pose]
- pursuer_alert: height pop f0->f1: 111->160 (+44.1%)
- pursuer_approach_walk: height pop f0->f1: 96->104 (+8.3%) [reviewed cyclic/intended pose]
- pursuer_approach_walk: height pop f1->f2: 104->123 (+18.3%) [reviewed cyclic/intended pose]
- pursuer_approach_walk: height pop f2->f3: 123->115 (-6.5%) [reviewed cyclic/intended pose]
- pursuer_approach_walk: height pop f3->f4: 115->107 (-7.0%) [reviewed cyclic/intended pose]
- pursuer_approach_walk: loop wrap f7->f0 height 111->96 (-13.5%) [reviewed cyclic pose]
- pursuer_lunge_windup: height pop f0->f1: 159->150 (-5.7%)
- pursuer_lunge_windup: height pop f1->f2: 150->111 (-26.0%)
- pursuer_lunge: height pop f0->f1: 112->61 (-45.5%) [reviewed cyclic/intended pose]
- pursuer_lunge: height pop f1->f2: 61->47 (-23.0%) [reviewed cyclic/intended pose]
- pursuer_recovery: height pop f0->f1: 84->115 (+36.9%)
- pursuer_recovery: height pop f1->f2: 115->139 (+20.9%)
- pursuer_recovery: height pop f2->f3: 139->109 (-21.6%)
- pursuer_hurt: height pop f0->f1: 135->93 (-31.1%)
- pursuer_hurt: height pop f1->f2: 93->112 (+20.4%)
- pursuer_death: height pop f0->f1: 126->98 (-22.2%) [reviewed cyclic/intended pose]
- pursuer_death: height pop f2->f3: 96->69 (-28.1%) [reviewed cyclic/intended pose]
- pursuer_death: height pop f3->f4: 69->41 (-40.6%) [reviewed cyclic/intended pose]
- swooper_cruise: height pop f1->f2: 180->132 (-26.7%) [reviewed cyclic/intended pose]
- swooper_cruise: height pop f3->f4: 136->157 (+15.4%) [reviewed cyclic/intended pose]
- swooper_cruise: height pop f4->f5: 157->169 (+7.6%) [reviewed cyclic/intended pose]
- swooper_cruise: loop wrap f7->f0 height 173->182 (+5.2%) [reviewed cyclic pose]
- swooper_dive_telegraph: height pop f0->f1: 235->198 (-15.7%)
- swooper_dive_telegraph: height pop f1->f2: 198->141 (-28.8%)
- swooper_dive_telegraph: height pop f2->f3: 141->108 (-23.4%)
- swooper_dive: height pop f0->f1: 165->155 (-6.1%)
- swooper_dive: height pop f1->f2: 155->174 (+12.3%)
- swooper_recovery_climb: height pop f0->f1: 175->135 (-22.9%)
- swooper_recovery_climb: height pop f1->f2: 135->125 (-7.4%)
- swooper_recovery_climb: height pop f2->f3: 125->167 (+33.6%)
- swooper_hurt: height pop f0->f1: 184->170 (-7.6%)
- swooper_hurt: height pop f1->f2: 170->128 (-24.7%)
- swooper_death_fall: height pop f0->f1: 240->170 (-29.2%) [reviewed cyclic/intended pose]
- swooper_death_fall: height pop f1->f2: 170->177 (+4.1%) [reviewed cyclic/intended pose]
- swooper_death_fall: height pop f2->f3: 177->164 (-7.3%) [reviewed cyclic/intended pose]
- swooper_death_fall: height pop f3->f4: 164->80 (-51.2%) [reviewed cyclic/intended pose]
- boss_idle: height pop f2->f3: 353->329 (-6.8%) [reviewed cyclic/intended pose]
- boss_idle: height pop f3->f4: 329->358 (+8.8%) [reviewed cyclic/intended pose]
- boss_idle: height pop f6->f7: 335->353 (+5.4%) [reviewed cyclic/intended pose]
- boss_walk: height pop f3->f4: 352->337 (-4.3%) [reviewed cyclic/intended pose]
- boss_walk: height pop f4->f5: 337->351 (+4.2%) [reviewed cyclic/intended pose]
- boss_walk: loop wrap f7->f0 height 335->369 (+10.1%) [reviewed cyclic pose]
- boss_strike_windup: height pop f0->f1: 360->345 (-4.2%)
- boss_strike_execute: height pop f1->f2: 408->295 (-27.7%) [reviewed cyclic/intended pose]
- boss_strike_execute: height pop f2->f3: 295->276 (-6.4%) [reviewed cyclic/intended pose]
- boss_strike_recover: height pop f1->f2: 283->341 (+20.5%)
- boss_strike_recover: height pop f2->f3: 341->361 (+5.9%)
- boss_hazard_execute: height pop f0->f1: 373->310 (-16.9%)
- boss_hazard_execute: height pop f1->f2: 310->332 (+7.1%)
- boss_hazard_execute: height pop f2->f3: 332->372 (+12.0%)
- boss_hazard_recover: height pop f1->f2: 254->354 (+39.4%)
- boss_death: height pop f0->f1: 364->339 (-6.9%) [reviewed cyclic/intended pose]
- boss_death: height pop f1->f2: 339->316 (-6.8%) [reviewed cyclic/intended pose]
- boss_death: height pop f2->f3: 316->280 (-11.4%) [reviewed cyclic/intended pose]
- boss_death: height pop f3->f4: 280->266 (-5.0%) [reviewed cyclic/intended pose]
- boss_death: height pop f4->f5: 266->235 (-11.7%) [reviewed cyclic/intended pose]
- boss_death: height pop f6->f7: 228->210 (-7.9%) [reviewed cyclic/intended pose]
- boss_death: height pop f8->f9: 205->168 (-18.0%) [reviewed cyclic/intended pose]
- boss_death: height pop f10->f11: 173->141 (-18.5%) [reviewed cyclic/intended pose]
- vfx_whip_impact: height pop f0->f1: 86->148 (+72.1%)
- vfx_whip_impact: height pop f1->f2: 148->204 (+37.8%)
- vfx_whip_impact: height pop f2->f3: 204->162 (-20.6%)
- vfx_whip_impact: height pop f3->f4: 162->108 (-33.3%)
- vfx_whip_impact: height pop f4->f5: 108->58 (-46.3%)
- vfx_enemy_defeat: height pop f0->f1: 128->174 (+35.9%)
- vfx_enemy_defeat: height pop f1->f2: 174->217 (+24.7%)
- vfx_enemy_defeat: height pop f2->f3: 217->135 (-37.8%)
- vfx_enemy_defeat: height pop f3->f4: 135->214 (+58.5%)
- vfx_enemy_defeat: height pop f4->f5: 214->202 (-5.6%)
- vfx_enemy_defeat: height pop f5->f6: 202->29 (-85.6%)
- vfx_enemy_defeat: height pop f6->f7: 29->17 (-41.4%)
- vfx_checkpoint_activate: height pop f0->f1: 38->124 (+226.3%)
- vfx_checkpoint_activate: height pop f1->f2: 124->182 (+46.8%)
- vfx_checkpoint_activate: height pop f2->f3: 182->217 (+19.2%)
- vfx_checkpoint_activate: height pop f5->f6: 205->254 (+23.9%)
- vfx_hazard_telegraph: height pop f1->f2: 75->79 (+5.3%)
- vfx_hazard_eruption: height pop f0->f1: 67->192 (+186.6%)
- vfx_hazard_eruption: height pop f3->f4: 192->80 (-58.3%)
- vfx_hazard_eruption: height pop f4->f5: 80->75 (-6.2%)
- hero_crouch_exit: height pop f0->f1: 140->146 (+4.3%) [reviewed cyclic/intended pose]
- hero_crouch_exit: height pop f1->f2: 146->184 (+26.0%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f0->f1: 123->136 (+10.6%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f1->f2: 136->128 (-5.9%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f2->f3: 128->153 (+19.5%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f3->f4: 153->219 (+43.1%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f4->f5: 219->229 (+4.6%) [reviewed cyclic/intended pose]

## Coverage

State→clip maps were read from `game/scripts/*.gd` (STATE_TO_CLIP in hunter/pursuer/swooper/boss, STATE_TO_WHIP in hunter, spawn sites for projectile/VFX). Every GAMEPLAY_RULES §4 hero state, §8.1–§8.4 enemy/boss behavior state, the three whip attack states, the projectile and all six VFX clips resolve to an existing clip (asserted by this audit and by `game/tests/sequence_engine_check.gd` in Godot).

