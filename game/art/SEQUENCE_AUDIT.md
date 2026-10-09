# Sequence audit — every clip, every frame (2026-10-09)

Method: PIL/scipy measurement of `game/art/frames/<clip>/` (alpha > 40; LCC = largest connected component = the figure). Pivot drift tolerance ≤ 2 px; adjacent-frame LCC height pop threshold > 4.0%. One contact strip per clip in `game/tests/shots/seq_<actor>_<clip>.png` (red = contract pivot, green = actor design height).

Clips audited: 64. Defects: 0. Warnings: 6. Waived: 7. Intended transitions noted: 136.

## Per-clip verdicts

| clip | actor | frames (files/spec) | total ms | loop | LCC h min/med/max | max |drift| px | wrap % | states | verdict |
|---|---|---|---|---|---|---|---|---|---|
| hero_idle | hero | 8/8 | 1000 | True | 223/224/224 | 1 | 0.0 | hero.idle | PASS |
| hero_walk | hero | 10/10 | 800 | True | 223/224/224 | 1 | 0.0 | hero.walk | PASS |
| hero_start_move | hero | 3/3 | 150 | False | 224/224/224 | 0.5 | - | hero.start_move | PASS |
| hero_stop_move | hero | 3/3 | 150 | False | 224/224/224 | 1 | - | hero.stop_move | PASS |
| hero_turn | hero | 3/3 | 150 | False | 224/224/224 | 0.5 | - | hero.turn | PASS |
| hero_crouch_enter | hero | 4/4 | 200 | False | 142/163/211 | 0.5 | - | hero.crouch_enter | CHECK |
| hero_crouch_idle | hero | 6/6 | 900 | True | 135/140/146 | 0.5 | 4.3 | hero.crouch_idle | CHECK |
| hero_jump_takeoff | hero | 3/3 | 120 | False | 171/223/224 | 0 | - | hero.jump_takeoff | CHECK |
| hero_jump_rise | hero | 4/4 | 240 | False | 181/223/224 | 1 | - | hero.jump_rise | CHECK |
| hero_jump_apex | hero | 3/3 | 150 | False | 178/200/224 | 1 | - | hero.jump_apex | CHECK |
| hero_fall | hero | 4/4 | 400 | True | 197/221/230 | 0.5 | -12.1 | hero.fall | CHECK |
| hero_land | hero | 4/4 | 160 | False | 174/223/224 | 0.5 | - | hero.land | CHECK |
| hero_attack_ground | hero | 8/8 | 500 | False | 203/224/224 | 0.5 | - | hero.attack_ground | CHECK |
| hero_attack_air | hero | 8/8 | 500 | False | 198/223/224 | 1 | - | hero.attack_air | CHECK |
| hero_attack_crouch | hero | 8/8 | 500 | False | 139/141/144 | 1 | - | hero.attack_crouch | PASS |
| hero_hurt_recoil | hero | 4/4 | 200 | False | 209/224/224 | 0.5 | - | hero.hurt_recoil | CHECK |
| hero_knockback | hero | 4/4 | 300 | False | 190/214/224 | 0.5 | - | hero.knockback | CHECK |
| hero_knockdown | hero | 6/6 | 360 | False | 123/160/208 | 2 | - | hero.knockdown | CHECK |
| hero_death | hero | 10/10 | 800 | False | 48/160/238 | 7 | - | hero.death | CHECK |
| whip_attack_ground | whip | 8/8 | 500 | False | 20/82/85 | 0 | - | whip.attack_ground | CHECK |
| whip_attack_air | whip | 8/8 | 500 | False | 17/75/107 | 0 | - | whip.attack_air | CHECK |
| whip_attack_crouch | whip | 8/8 | 500 | False | 16/73/80 | 0 | - | whip.attack_crouch | CHECK |
| pursuer_idle | pursuer | 6/6 | 900 | True | 109/110/148 | 1 | -0.9 | — | WAIVED |
| pursuer_patrol_walk | pursuer | 8/8 | 720 | True | 105/110/122 | 3 | 14.2 | pursuer.patrol | CHECK |
| pursuer_alert | pursuer | 4/4 | 300 | False | 111/156/160 | 20 | - | pursuer.alert | CHECK |
| pursuer_approach_walk | pursuer | 8/8 | 560 | True | 99/111/124 | 1 | -10.8 | pursuer.chase | CHECK |
| pursuer_lunge_windup | pursuer | 4/4 | 350 | False | 111/133/160 | 1 | - | pursuer.windup | CHECK |
| pursuer_lunge | pursuer | 3/3 | 240 | False | 50/61/95 | 2 | - | pursuer.lunge | CHECK |
| pursuer_recovery | pursuer | 4/4 | 600 | False | 87/110/140 | 2 | - | pursuer.recover | CHECK |
| pursuer_hurt | pursuer | 3/3 | 180 | False | 93/112/132 | 1 | - | pursuer.hurt | CHECK |
| pursuer_death | pursuer | 6/6 | 480 | False | 48/86/126 | 2.5 | - | pursuer.dead | CHECK |
| swooper_perch_idle | swooper | 6/6 | 900 | True | 166/171/174 | 1 | 2.4 | — | WAIVED |
| swooper_cruise | swooper | 8/8 | 720 | True | 138/169/180 | 1 | 5.9 | swooper.cruise, swooper.recover | CHECK |
| swooper_dive_telegraph | swooper | 4/4 | 600 | False | 127/182/210 | 1 | - | swooper.telegraph | CHECK |
| swooper_dive | swooper | 4/4 | 240 | False | 156/167/188 | 0.5 | - | swooper.dive | CHECK |
| swooper_recovery_climb | swooper | 6/6 | 900 | False | 126/162/171 | 0.5 | - | swooper.climb | CHECK |
| swooper_hurt | swooper | 3/3 | 180 | False | 128/170/180 | 0.5 | - | swooper.hurt | CHECK |
| swooper_death_fall | swooper | 5/5 | 350 | False | 89/170/212 | 1 | - | swooper.dead | CHECK |
| ranged_idle | ranged | 6/6 | 900 | True | 279/288/288 | 1 | 0.0 | ranged.idle | PASS |
| ranged_aim | ranged | 6/6 | 900 | False | 279/288/288 | 36 | - | ranged.aim | PASS |
| ranged_fire | ranged | 3/3 | 200 | False | 272/288/288 | 0.5 | - | ranged.fire | CHECK |
| ranged_recover | ranged | 7/7 | 700 | False | 269/288/288 | 0.5 | - | ranged.recover | CHECK |
| ranged_hurt | ranged | 3/3 | 180 | False | 270/288/288 | 0.5 | - | ranged.hurt | CHECK |
| ranged_death | ranged | 6/6 | 480 | False | 284/288/288 | 0.5 | - | ranged.dead | PASS |
| projectile_grave_shot | projectile | 3/3 | 240 | True | 64/64/64 | 0 | 0.0 | projectile.flight | PASS |
| boss_idle | boss | 8/8 | 1000 | True | 350/352/353 | 1.5 | -0.6 | boss.dormant, boss.idle | PASS |
| boss_walk | boss | 8/8 | 640 | True | 350/351/352 | 1.5 | 0.0 | boss.advance | PASS |
| boss_turn | boss | 4/4 | 300 | False | 352/352/352 | 1 | - | boss.turn | PASS |
| boss_strike_windup | boss | 7/7 | 700 | False | 350/352/352 | 1 | - | boss.strike_windup | PASS |
| boss_strike_execute | boss | 4/4 | 200 | False | 293/359/424 | 13 | - | boss.strike | CHECK |
| boss_strike_recover | boss | 6/6 | 1100 | False | 263/350/352 | 36 | - | boss.strike_recover | CHECK |
| boss_hazard_windup | boss | 8/8 | 1200 | False | 351/352/352 | 1.5 | - | boss.hazard_cast | PASS |
| boss_hazard_execute | boss | 4/4 | 400 | False | 304/330/351 | 1 | - | boss.hazard_erupt | CHECK |
| boss_hazard_recover | boss | 6/6 | 900 | False | 252/350/352 | 52 | - | boss.hazard_recover | CHECK |
| boss_hurt | boss | 3/3 | 200 | False | 352/352/352 | 0.5 | - | boss.hurt | PASS |
| boss_death | boss | 12/12 | 1080 | False | 160/239/364 | 17 | - | boss.dead | CHECK |
| vfx_whip_impact | vfx | 6/6 | 280 | False | 58/128/204 | 0 | - | vfx.whip_hit | CHECK |
| vfx_damage_indicator | vfx | 2/2 | 300 | False | 217/218/220 | 2.5 | - | vfx.damage_flash | PASS |
| vfx_enemy_defeat | vfx | 8/8 | 560 | False | 17/154/217 | 64.5 | - | vfx.enemy_defeat | CHECK |
| vfx_checkpoint_activate | vfx | 8/8 | 720 | False | 38/207/254 | 107 | - | vfx.checkpoint | CHECK |
| vfx_hazard_telegraph | vfxhaz | 4/4 | 1200 | False | 75/78/80 | 30.5 | - | vfx.hazard_cast | CHECK |
| vfx_hazard_eruption | vfxhaz | 6/6 | 400 | False | 67/136/192 | 136 | - | vfx.hazard_erupt | CHECK |
| hero_crouch_exit | hero | 4/4 | 200 | False | 142/163/211 | 0.5 | - | hero.crouch_exit | CHECK |
| hero_get_up | hero | 6/6 | 450 | False | 123/160/208 | 2 | - | hero.get_up | CHECK |

## Defects

- none

## Warnings

- hero_death: f8 cloth/satellite extends 7 px below foot line
- boss_strike_recover: f0 cloth/satellite extends 36 px below foot line
- boss_strike_recover: f2 cloth/satellite extends 27 px below foot line
- boss_strike_recover: f3 cloth/satellite extends 4 px below foot line
- boss_hazard_recover: f0 cloth/satellite extends 52 px below foot line
- boss_hazard_recover: f2 cloth/satellite extends 11 px below foot line

Warnings disposition: the six warnings are painted cloth/ash extending below the foot line (boss cloak hems pooling in the two recover opening poses, hero_death ash settle). The feet themselves sit on the pivot in every case (see strips); cloth pooling is a pose property, not pivot or scale drift. Accepted as-is.


## Waived (explicit, with reason)

- **pursuer_idle**: No runtime state maps to it and its frames 1/4 rear up inside an 'idle' loop. The pursuer's shipped behavior has no stationary state (patrol is its locomotion; the rear-up tell lives in pursuer_alert), so the clip is not user-visible. Retained for ASSET_BRIEFS inventory; wiring it in would change gameplay, which this art fix must not do.
- **swooper_perch_idle**: No runtime state maps to it: the swooper spawns already cruising and has no perch behavior in GAMEPLAY_RULES S8.2's shipped state set. Retained for inventory; not user-visible.
- (finding) pursuer_idle: height pop f0->f1: 109->148 (+35.8%)
- (finding) pursuer_idle: height pop f1->f2: 148->109 (-26.4%)
- (finding) pursuer_idle: height pop f3->f4: 111->140 (+26.1%)
- (finding) pursuer_idle: height pop f4->f5: 140->110 (-21.4%)
- (finding) swooper_perch_idle: height pop f3->f4: 173->166 (-4.0%)
- (finding) pursuer_idle: no runtime state maps to this clip (orphan)
- (finding) swooper_perch_idle: no runtime state maps to this clip (orphan)

## Intended pose transitions (>4% height change, by design)

- hero_crouch_enter: height pop f0->f1: 211->180 (-14.7%) [reviewed cyclic/intended pose]
- hero_crouch_enter: height pop f1->f2: 180->146 (-18.9%) [reviewed cyclic/intended pose]
- hero_crouch_idle: height pop f0->f1: 146->139 (-4.8%) [reviewed cyclic/intended pose]
- hero_crouch_idle: loop wrap f5->f0 height 140->146 (+4.3%) [reviewed cyclic pose]
- hero_jump_takeoff: height pop f0->f1: 171->224 (+31.0%) [reviewed cyclic/intended pose]
- hero_jump_rise: height pop f0->f1: 181->224 (+23.8%) [reviewed cyclic/intended pose]
- hero_jump_apex: height pop f0->f1: 224->178 (-20.5%) [reviewed cyclic/intended pose]
- hero_jump_apex: height pop f1->f2: 178->200 (+12.4%) [reviewed cyclic/intended pose]
- hero_fall: height pop f0->f1: 197->218 (+10.7%) [reviewed cyclic/intended pose]
- hero_fall: height pop f1->f2: 218->230 (+5.5%) [reviewed cyclic/intended pose]
- hero_fall: loop wrap f3->f0 height 224->197 (-12.1%) [reviewed cyclic pose]
- hero_land: height pop f1->f2: 224->174 (-22.3%) [reviewed cyclic/intended pose]
- hero_land: height pop f2->f3: 174->224 (+28.7%) [reviewed cyclic/intended pose]
- hero_attack_ground: height pop f2->f3: 223->203 (-9.0%) [reviewed cyclic/intended pose]
- hero_attack_ground: height pop f3->f4: 203->224 (+10.3%) [reviewed cyclic/intended pose]
- hero_attack_air: height pop f1->f2: 223->214 (-4.0%) [reviewed cyclic/intended pose]
- hero_attack_air: height pop f2->f3: 214->198 (-7.5%) [reviewed cyclic/intended pose]
- hero_attack_air: height pop f4->f5: 198->224 (+13.1%) [reviewed cyclic/intended pose]
- hero_hurt_recoil: height pop f1->f2: 224->209 (-6.7%)
- hero_hurt_recoil: height pop f2->f3: 209->224 (+7.2%)
- hero_knockback: height pop f1->f2: 224->190 (-15.2%) [reviewed cyclic/intended pose]
- hero_knockback: height pop f2->f3: 190->204 (+7.4%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f1->f2: 208->164 (-21.2%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f2->f3: 164->142 (-13.4%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f3->f4: 142->156 (+9.9%) [reviewed cyclic/intended pose]
- hero_knockdown: height pop f4->f5: 156->123 (-21.2%) [reviewed cyclic/intended pose]
- hero_death: height pop f0->f1: 238->219 (-8.0%) [reviewed cyclic/intended pose]
- hero_death: height pop f1->f2: 219->190 (-13.2%) [reviewed cyclic/intended pose]
- hero_death: height pop f2->f3: 190->181 (-4.7%) [reviewed cyclic/intended pose]
- hero_death: height pop f3->f4: 181->167 (-7.7%) [reviewed cyclic/intended pose]
- hero_death: height pop f4->f5: 167->153 (-8.4%) [reviewed cyclic/intended pose]
- hero_death: height pop f5->f6: 153->132 (-13.7%) [reviewed cyclic/intended pose]
- hero_death: height pop f6->f7: 132->95 (-28.0%) [reviewed cyclic/intended pose]
- hero_death: height pop f7->f8: 95->48 (-49.5%) [reviewed cyclic/intended pose]
- hero_death: height pop f8->f9: 48->91 (+89.6%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f2->f3: 85->20 (-76.5%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f3->f4: 20->83 (+315.0%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f4->f5: 83->39 (-53.0%) [reviewed cyclic/intended pose]
- whip_attack_ground: height pop f5->f6: 39->83 (+112.8%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f0->f1: 70->66 (-5.7%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f1->f2: 66->97 (+47.0%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f2->f3: 97->17 (-82.5%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f3->f4: 17->107 (+529.4%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f4->f5: 107->57 (-46.7%) [reviewed cyclic/intended pose]
- whip_attack_air: height pop f5->f6: 57->81 (+42.1%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f1->f2: 74->53 (-28.4%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f2->f3: 53->16 (-69.8%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f3->f4: 16->74 (+362.5%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f4->f5: 74->47 (-36.5%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f5->f6: 47->80 (+70.2%) [reviewed cyclic/intended pose]
- whip_attack_crouch: height pop f6->f7: 80->76 (-5.0%) [reviewed cyclic/intended pose]
- pursuer_patrol_walk: height pop f2->f3: 122->112 (-8.2%) [reviewed cyclic/intended pose]
- pursuer_patrol_walk: loop wrap f7->f0 height 106->121 (+14.2%) [reviewed cyclic pose]
- pursuer_alert: height pop f0->f1: 111->152 (+36.9%)
- pursuer_alert: height pop f1->f2: 152->160 (+5.3%)
- pursuer_approach_walk: height pop f1->f2: 102->124 (+21.6%) [reviewed cyclic/intended pose]
- pursuer_approach_walk: height pop f2->f3: 124->113 (-8.9%) [reviewed cyclic/intended pose]
- pursuer_approach_walk: loop wrap f7->f0 height 111->99 (-10.8%) [reviewed cyclic pose]
- pursuer_lunge_windup: height pop f0->f1: 160->150 (-6.2%)
- pursuer_lunge_windup: height pop f1->f2: 150->111 (-26.0%)
- pursuer_lunge_windup: height pop f2->f3: 111->116 (+4.5%)
- pursuer_lunge: height pop f0->f1: 95->61 (-35.8%) [reviewed cyclic/intended pose]
- pursuer_lunge: height pop f1->f2: 61->50 (-18.0%) [reviewed cyclic/intended pose]
- pursuer_recovery: height pop f0->f1: 87->111 (+27.6%)
- pursuer_recovery: height pop f1->f2: 111->140 (+26.1%)
- pursuer_recovery: height pop f2->f3: 140->109 (-22.1%)
- pursuer_hurt: height pop f0->f1: 132->93 (-29.5%)
- pursuer_hurt: height pop f1->f2: 93->112 (+20.4%)
- pursuer_death: height pop f0->f1: 126->96 (-23.8%) [reviewed cyclic/intended pose]
- pursuer_death: height pop f2->f3: 95->78 (-17.9%) [reviewed cyclic/intended pose]
- pursuer_death: height pop f3->f4: 78->48 (-38.5%) [reviewed cyclic/intended pose]
- swooper_cruise: height pop f1->f2: 180->138 (-23.3%) [reviewed cyclic/intended pose]
- swooper_cruise: height pop f3->f4: 142->163 (+14.8%) [reviewed cyclic/intended pose]
- swooper_cruise: height pop f4->f5: 163->171 (+4.9%) [reviewed cyclic/intended pose]
- swooper_cruise: loop wrap f7->f0 height 169->179 (+5.9%) [reviewed cyclic pose]
- swooper_dive_telegraph: height pop f0->f1: 210->198 (-5.7%)
- swooper_dive_telegraph: height pop f1->f2: 198->166 (-16.2%)
- swooper_dive_telegraph: height pop f2->f3: 166->127 (-23.5%)
- swooper_dive: height pop f1->f2: 161->174 (+8.1%)
- swooper_dive: height pop f2->f3: 174->188 (+8.0%)
- swooper_recovery_climb: height pop f0->f1: 161->139 (-13.7%)
- swooper_recovery_climb: height pop f1->f2: 139->126 (-9.4%)
- swooper_recovery_climb: height pop f2->f3: 126->167 (+32.5%)
- swooper_recovery_climb: height pop f4->f5: 171->164 (-4.1%)
- swooper_hurt: height pop f0->f1: 180->170 (-5.6%)
- swooper_hurt: height pop f1->f2: 170->128 (-24.7%)
- swooper_death_fall: height pop f0->f1: 212->170 (-19.8%) [reviewed cyclic/intended pose]
- swooper_death_fall: height pop f1->f2: 170->188 (+10.6%) [reviewed cyclic/intended pose]
- swooper_death_fall: height pop f2->f3: 188->162 (-13.8%) [reviewed cyclic/intended pose]
- swooper_death_fall: height pop f3->f4: 162->89 (-45.1%) [reviewed cyclic/intended pose]
- ranged_fire: height pop f0->f1: 272->288 (+5.9%)
- ranged_recover: height pop f0->f1: 269->288 (+7.1%)
- ranged_hurt: height pop f0->f1: 270->288 (+6.7%)
- boss_strike_execute: height pop f0->f1: 424->404 (-4.7%) [reviewed cyclic/intended pose]
- boss_strike_execute: height pop f1->f2: 404->314 (-22.3%) [reviewed cyclic/intended pose]
- boss_strike_execute: height pop f2->f3: 314->293 (-6.7%) [reviewed cyclic/intended pose]
- boss_strike_recover: height pop f0->f1: 263->274 (+4.2%)
- boss_strike_recover: height pop f1->f2: 274->350 (+27.7%)
- boss_hazard_execute: height pop f0->f1: 351->310 (-11.7%)
- boss_hazard_execute: height pop f2->f3: 304->351 (+15.5%)
- boss_hazard_recover: height pop f1->f2: 261->350 (+34.1%)
- boss_death: height pop f0->f1: 364->336 (-7.7%) [reviewed cyclic/intended pose]
- boss_death: height pop f1->f2: 336->309 (-8.0%) [reviewed cyclic/intended pose]
- boss_death: height pop f2->f3: 309->283 (-8.4%) [reviewed cyclic/intended pose]
- boss_death: height pop f4->f5: 276->249 (-9.8%) [reviewed cyclic/intended pose]
- boss_death: height pop f5->f6: 249->230 (-7.6%) [reviewed cyclic/intended pose]
- boss_death: height pop f6->f7: 230->202 (-12.2%) [reviewed cyclic/intended pose]
- boss_death: height pop f7->f8: 202->192 (-5.0%) [reviewed cyclic/intended pose]
- boss_death: height pop f8->f9: 192->168 (-12.5%) [reviewed cyclic/intended pose]
- boss_death: height pop f10->f11: 167->160 (-4.2%) [reviewed cyclic/intended pose]
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
- hero_crouch_exit: height pop f1->f2: 146->180 (+23.3%) [reviewed cyclic/intended pose]
- hero_crouch_exit: height pop f2->f3: 180->211 (+17.2%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f0->f1: 123->156 (+26.8%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f1->f2: 156->142 (-9.0%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f2->f3: 142->164 (+15.5%) [reviewed cyclic/intended pose]
- hero_get_up: height pop f3->f4: 164->208 (+26.8%) [reviewed cyclic/intended pose]

## Coverage

State→clip maps were read from `game/scripts/*.gd` (STATE_TO_CLIP in hunter/pursuer/swooper/boss, STATE_TO_WHIP in hunter, spawn sites for projectile/VFX). Every GAMEPLAY_RULES §4 hero state, §8.1–§8.4 enemy/boss behavior state, the three whip attack states, the projectile and all six VFX clips resolve to an existing clip (asserted by this audit and by `game/tests/sequence_engine_check.gd` in Godot).

