# ACTION SIZE AUDIT — per-frame scale drift (user playtest round 3, 2026-10-09)

User report: "When the player stands still, its size doesn't match when he is in action... list all actions of one character and make sure their size won't drift. Cover enemy and boss too."

## Why the previous fixes were not enough

Fix #1 (per-clip uniform scale) anchored each clip's reference statistic (median/max/first-two/last/min LCC height) to the actor design height. A median over mutually inconsistent frames lands on the anchor while individual frames straddle it: e.g. hero_land shipped heights 239/209/169/260 (median 224 = anchor, scale 1.000) — the 260 px 'standing back up' frame stood 16% taller than idle in game. The drift was WITHIN clips, so only a per-frame correction can remove it.

## Method

- **Standing-class frames** of feet-anchored bipeds (hero, boss) are corrected by **height**: factor = design_H / frame_H. An upright figure's perceived size is its height; idle = 224 (hero) / 352 (boss) is the contract (crouch family 140).
- **All other frames** (poses, transitions, quadruped pursuer, canvas-clipped ranged, flying swooper) are corrected by **SA = sqrt(alpha area)**: factor = clip_median_SA / frame_SA. Under a pure scale change SA scales exactly linearly; pose changes mostly redistribute the same ink (hero_land SA spread 4.9% across a 169..260 px height swing).
- Standing class = H/design in [0.92, 1.25] and W/H <= 1.05, with an overhead guard: a frame >12% over design height whose SA already matches the clip median (e.g. boss weapon raised) is pose, not scale.
- **SQ = sqrt(H x W) is reported but NOT used for correction**: for narrow side-profile standing frames SQ collapses (hero_attack_ground f6: SQ 134 vs clip ~204 at identical drawn scale); SQ-driven scaling would have blown that standing recovery frame from 250 px to ~295 px tall — 32% larger than idle, i.e. it would CREATE the reported bug. SQ residuals >4% are listed with the named pose instead.
- Factors clamp to [0.85, 1.18]; rescale pivots on the contract foot point (LCC bottom-centre -> pivot; swooper: LCC centre -> pivot). Trims recomputed by pack_atlases.py (5 pages, 80 MiB, mips off).
- **Exempt (contract-locked)**: whip_attack_* (in-hand fix geometry), vfx_*, projectile_grave_shot — verified byte-identical to the pre-fix archive (61/61 md5 matches), only sanity-checked.
- **Frames regenerated: 0.** The only frames needing a factor outside the clamp are 8 ink-poor collapse/fold poses (death heaps, pursuer alert apex, folded-wing telegraph) — clamp-corrected and pose-named below; no standing-class frame needed more than the clamp, so there was no misdrawn standing frame to regenerate.

## Per-actor summary (LCC height, src px)

| actor | clip | before H | after H | note |
|---|---|---|---|---|
| boss | boss_death (12f) | 141..364 | 160..364 |  |
| boss | boss_hazard_execute (4f) | 310..373 | 304..351 |  |
| boss | boss_hazard_recover (6f) | 245..361 | 252..352 |  |
| boss | boss_hazard_windup (8f) | 346..359 | 351..352 |  |
| boss | boss_hurt (3f) | 339..352 | 352..352 |  |
| boss | boss_idle (8f) | 329..358 | 350..353 |  |
| boss | boss_strike_execute (4f) | 276..424 | 293..424 |  |
| boss | boss_strike_recover (6f) | 280..374 | 263..352 |  |
| boss | boss_strike_windup (7f) | 345..361 | 350..352 |  |
| boss | boss_turn (4f) | 347..355 | 352..352 |  |
| boss | boss_walk (8f) | 335..369 | 350..352 |  |
| hero | hero_attack_air (8f) | 205..227 | 198..224 |  |
| hero | hero_attack_crouch (8f) | 135..143 | 139..144 |  |
| hero | hero_attack_ground (8f) | 207..250 | 203..224 |  |
| hero | hero_crouch_enter (4f) | 140..190 | 142..211 |  |
| hero | hero_crouch_exit (4f) | 140..190 | 142..211 |  |
| hero | hero_crouch_idle (6f) | 135..145 | 135..146 |  |
| hero | hero_death (10f) | 42..229 | 48..238 |  |
| hero | hero_fall (4f) | 203..224 | 197..230 |  |
| hero | hero_get_up (6f) | 123..229 | 123..208 |  |
| hero | hero_hurt_recoil (4f) | 205..243 | 209..224 |  |
| hero | hero_idle (8f) | 222..226 | 223..224 |  |
| hero | hero_jump_apex (3f) | 178..224 | 178..224 |  |
| hero | hero_jump_rise (4f) | 174..224 | 181..224 |  |
| hero | hero_jump_takeoff (3f) | 164..223 | 171..224 |  |
| hero | hero_knockback (4f) | 185..224 | 190..224 |  |
| hero | hero_knockdown (6f) | 123..229 | 123..208 |  |
| hero | hero_land (4f) | 169..260 | 174..224 |  |
| hero | hero_start_move (3f) | 219..239 | 224..224 |  |
| hero | hero_stop_move (3f) | 223..241 | 224..224 |  |
| hero | hero_turn (3f) | 212..225 | 224..224 |  |
| hero | hero_walk (10f) | 215..231 | 223..224 |  |
| projectile | projectile_grave_shot (3f) | 64..64 | 64..64 | exempt (verified unchanged) |
| pursuer | pursuer_alert (4f) | 111..160 | 111..160 |  |
| pursuer | pursuer_approach_walk (8f) | 96..123 | 99..124 |  |
| pursuer | pursuer_death (6f) | 41..126 | 48..126 |  |
| pursuer | pursuer_hurt (3f) | 93..135 | 93..132 |  |
| pursuer | pursuer_idle (6f) | 109..148 | 109..148 |  |
| pursuer | pursuer_lunge (3f) | 47..112 | 50..95 |  |
| pursuer | pursuer_lunge_windup (4f) | 111..159 | 111..160 |  |
| pursuer | pursuer_patrol_walk (8f) | 106..124 | 105..122 |  |
| pursuer | pursuer_recovery (4f) | 84..139 | 87..140 |  |
| ranged | ranged_aim (6f) | 288..288 | 279..288 |  |
| ranged | ranged_death (6f) | 288..288 | 284..288 |  |
| ranged | ranged_fire (3f) | 288..288 | 272..288 |  |
| ranged | ranged_hurt (3f) | 288..288 | 270..288 |  |
| ranged | ranged_idle (6f) | 288..288 | 279..288 |  |
| ranged | ranged_recover (7f) | 288..288 | 269..288 |  |
| swooper | swooper_cruise (8f) | 132..182 | 138..180 |  |
| swooper | swooper_death_fall (5f) | 80..240 | 89..212 |  |
| swooper | swooper_dive (4f) | 155..174 | 156..188 |  |
| swooper | swooper_dive_telegraph (4f) | 108..235 | 127..210 |  |
| swooper | swooper_hurt (3f) | 128..184 | 128..180 |  |
| swooper | swooper_perch_idle (6f) | 168..173 | 166..174 |  |
| swooper | swooper_recovery_climb (6f) | 125..175 | 126..171 |  |
| vfx | vfx_checkpoint_activate (8f) | 38..254 | 38..254 | exempt (verified unchanged) |
| vfx | vfx_damage_indicator (2f) | 217..220 | 217..220 | exempt (verified unchanged) |
| vfx | vfx_enemy_defeat (8f) | 17..217 | 17..217 | exempt (verified unchanged) |
| vfx | vfx_hazard_eruption (6f) | 67..192 | 67..192 | exempt (verified unchanged) |
| vfx | vfx_hazard_telegraph (4f) | 75..80 | 75..80 | exempt (verified unchanged) |
| vfx | vfx_whip_impact (6f) | 58..204 | 58..204 | exempt (verified unchanged) |
| whip | whip_attack_air (8f) | 17..107 | 17..107 | exempt (verified unchanged) |
| whip | whip_attack_crouch (8f) | 16..80 | 16..80 | exempt (verified unchanged) |
| whip | whip_attack_ground (8f) | 20..85 | 20..85 | exempt (verified unchanged) |

## Action inventory — every clip, every frame (before -> after)

Columns: HxW = LCC bbox px; SA = sqrt(alpha area); SQ = sqrt(HxW); factor/rule = applied correction (H = height-anchored standing frame, SA = ink-anchored); verdict flags SQ residuals > 4% from the clip median with the named pose.

### boss_death — 12 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 364x188 (207, 262) | - | 364x188 (207, 262) | OK |
| 1 | 339x227 (208, 277) | 0.994/SA | 336x223 (206, 274) | OK |
| 2 | 316x240 (212, 275) | 0.977/SA | 309x231 (206, 267) | OK |
| 3 | 280x257 (204, 268) | 1.014/SA | 283x259 (206, 271) | OK |
| 4 | 266x285 (199, 275) | 1.039/SA | 276x293 (206, 284) | SQ residual +6.4% — collapse (pose) |
| 5 | 235x299 (194, 265) | 1.066/SA | 249x318 (206, 281) | SQ residual +5.3% — collapse (pose) |
| 6 | 228x325 (201, 272) | 1.028/SA | 230x332 (204, 276) | OK |
| 7 | 210x352 (214, 272) | 0.965/SA | 202x338 (204, 261) | OK |
| 8 | 205x361 (219, 272) | 0.944/SA | 192x341 (203, 256) | SQ residual -4.2% — collapse (pose) |
| 9 | 168x361 (206, 246) | 1.004/SA | 168x361 (206, 246) | SQ residual -7.8% — collapse (pose) |
| 10 | 173x361 (211, 250) | 0.979/SA | 167x352 (203, 242) | SQ residual -9.2% — collapse (pose) |
| 11 | 141x361 (178, 226) | 1.163/SA | 160x386 (195, 248) | SQ residual -7.0% — collapse (pose) |

### boss_hazard_execute — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 373x214 (193, 282) | 0.944/H | 351x201 (181, 266) | SQ residual -15.4% — pose redistribution; SA-anchored |
| 1 | 310x343 (206, 326) | - | 310x343 (206, 326) | OK |
| 2 | 332x354 (224, 343) | 0.918/SA | 304x324 (204, 314) | OK |
| 3 | 372x123 (167, 214) | 0.946/H | 351x116 (157, 202) | SQ residual -35.7% — pose redistribution; SA-anchored |

### boss_hazard_recover — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 245x284 (195, 264) | 1.032/SA | 252x292 (200, 271) | SQ residual -5.5% — pose redistribution; SA-anchored |
| 1 | 254x267 (195, 260) | 1.031/SA | 261x274 (200, 267) | SQ residual -6.8% — pose redistribution; SA-anchored |
| 2 | 354x270 (208, 309) | 0.994/H | 350x268 (206, 306) | SQ residual +6.7% — pose redistribution; SA-anchored |
| 3 | 359x232 (193, 289) | 0.981/H | 352x227 (188, 283) | OK |
| 4 | 361x241 (201, 295) | 0.975/H | 352x234 (195, 287) | OK |
| 5 | 348x242 (219, 290) | 1.011/H | 351x245 (221, 293) | OK |

### boss_hazard_windup — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 348x158 (195, 234) | 1.011/H | 352x158 (197, 236) | SQ residual -29.0% — pose redistribution; SA-anchored |
| 1 | 346x222 (214, 277) | 1.017/H | 352x226 (216, 282) | SQ residual -15.0% — pose redistribution; SA-anchored |
| 2 | 351x285 (229, 316) | - | 351x285 (229, 316) | SQ residual -4.7% — pose redistribution; SA-anchored |
| 3 | 352x313 (239, 332) | - | 352x313 (239, 332) | OK |
| 4 | 355x318 (236, 336) | 0.992/H | 351x313 (233, 332) | OK |
| 5 | 352x326 (240, 339) | - | 352x326 (240, 339) | OK |
| 6 | 359x336 (249, 347) | 0.981/H | 351x327 (242, 339) | OK |
| 7 | 359x349 (256, 354) | 0.981/H | 352x342 (249, 347) | SQ residual +4.5% — pose redistribution; SA-anchored |

### boss_hurt — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 352x353 (223, 352) | - | 352x353 (223, 352) | SQ residual +6.5% — pose redistribution; SA-anchored |
| 1 | 339x300 (214, 319) | 1.038/H | 352x311 (221, 331) | OK |
| 2 | 352x225 (195, 281) | - | 352x225 (195, 281) | SQ residual -15.0% — pose redistribution; SA-anchored |

### boss_idle — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 351x157 (194, 235) | - | 351x157 (194, 235) | SQ residual -26.9% — pose redistribution; SA-anchored |
| 1 | 351x272 (212, 309) | - | 351x272 (212, 309) | OK |
| 2 | 353x302 (232, 326) | - | 353x302 (232, 326) | OK |
| 3 | 329x323 (220, 326) | 1.070/H | 352x343 (234, 348) | SQ residual +8.2% — pose redistribution; SA-anchored |
| 4 | 358x170 (201, 247) | 0.983/H | 350x167 (197, 242) | SQ residual -24.7% — pose redistribution; SA-anchored |
| 5 | 347x289 (227, 317) | 1.014/H | 352x293 (230, 321) | OK |
| 6 | 335x329 (224, 332) | 1.051/H | 352x345 (235, 348) | SQ residual +8.5% — pose redistribution; SA-anchored |
| 7 | 353x158 (195, 236) | - | 353x158 (195, 236) | SQ residual -26.4% — pose redistribution; SA-anchored |

### boss_strike_execute — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 424x244 (261, 322) | - | 424x244 (261, 322) | SQ residual -6.6% — overhead slam (raised-weapon pose; ink on-scale) |
| 1 | 408x356 (263, 381) | 0.991/SA | 404x353 (260, 378) | SQ residual +9.6% — overhead slam (raised-weapon pose; ink on-scale) |
| 2 | 295x378 (245, 334) | 1.066/SA | 314x378 (257, 344) | OK |
| 3 | 276x370 (245, 320) | 1.062/SA | 293x372 (254, 330) | SQ residual -4.2% — overhead slam (raised-weapon pose; ink on-scale) |

### boss_strike_recover — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 280x353 (227, 314) | 0.946/SA | 263x333 (214, 296) | SQ residual -4.1% — pose redistribution; SA-anchored |
| 1 | 283x330 (221, 306) | 0.972/SA | 274x320 (213, 296) | SQ residual -4.0% — pose redistribution; SA-anchored |
| 2 | 341x263 (213, 300) | 1.032/H | 350x272 (219, 308) | OK |
| 3 | 361x190 (201, 262) | 0.975/H | 352x184 (195, 254) | SQ residual -17.5% — pose redistribution; SA-anchored |
| 4 | 369x363 (199, 366) | 0.954/H | 351x346 (189, 348) | SQ residual +13.0% — pose redistribution; SA-anchored |
| 5 | 374x363 (215, 368) | 0.941/H | 352x342 (201, 347) | SQ residual +12.5% — pose redistribution; SA-anchored |

### boss_strike_windup — 7 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 360x152 (182, 234) | 0.978/H | 352x149 (178, 229) | SQ residual -25.3% — pose redistribution; SA-anchored |
| 1 | 345x230 (202, 282) | 1.020/H | 352x235 (206, 288) | SQ residual -6.2% — pose redistribution; SA-anchored |
| 2 | 351x268 (207, 307) | - | 351x268 (207, 307) | OK |
| 3 | 347x305 (213, 325) | 1.014/H | 351x307 (215, 328) | SQ residual +7.0% — pose redistribution; SA-anchored |
| 4 | 352x263 (207, 304) | - | 352x263 (207, 304) | OK |
| 5 | 354x304 (215, 328) | 0.994/H | 352x300 (213, 325) | SQ residual +6.0% — pose redistribution; SA-anchored |
| 6 | 361x326 (221, 343) | 0.975/H | 350x317 (215, 333) | SQ residual +8.6% — pose redistribution; SA-anchored |

### boss_turn — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 347x344 (242, 346) | 1.014/H | 352x348 (245, 350) | OK |
| 1 | 355x330 (250, 342) | 0.992/H | 352x326 (247, 339) | OK |
| 2 | 350x289 (233, 318) | 1.006/H | 352x290 (234, 320) | SQ residual -8.7% — pose redistribution; SA-anchored |
| 3 | 354x352 (240, 353) | 0.994/H | 352x350 (238, 351) | OK |

### boss_walk — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 369x227 (190, 289) | 0.954/H | 350x215 (181, 274) | SQ residual -17.9% — pose redistribution; SA-anchored |
| 1 | 363x266 (195, 311) | 0.970/H | 351x256 (188, 300) | SQ residual -10.3% — pose redistribution; SA-anchored |
| 2 | 352x298 (211, 324) | - | 352x298 (211, 324) | OK |
| 3 | 352x339 (216, 345) | - | 352x339 (216, 345) | OK |
| 4 | 337x305 (218, 321) | 1.045/H | 350x318 (227, 334) | OK |
| 5 | 351x318 (214, 334) | - | 351x318 (214, 334) | OK |
| 6 | 345x345 (221, 345) | 1.020/H | 352x351 (225, 352) | SQ residual +5.2% — pose redistribution; SA-anchored |
| 7 | 335x324 (214, 330) | 1.051/H | 350x339 (224, 344) | OK |

### hero_attack_air — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 222x211 (148, 216) | 1.009/H | 224x212 (148, 218) | OK |
| 1 | 226x213 (148, 219) | 0.991/H | 223x210 (146, 216) | OK |
| 2 | 216x235 (149, 225) | 0.992/SA | 214x232 (147, 223) | OK |
| 3 | 205x267 (153, 234) | 0.969/SA | 198x259 (147, 226) | OK |
| 4 | 206x260 (153, 231) | 0.968/SA | 198x252 (147, 223) | OK |
| 5 | 208x199 (144, 204) | 1.077/H | 224x214 (154, 219) | OK |
| 6 | 223x175 (145, 198) | 1.004/H | 224x176 (145, 199) | SQ residual -9.3% — airborne lunge/tuck poses |
| 7 | 227x181 (144, 203) | 0.987/H | 223x178 (142, 199) | SQ residual -9.0% — airborne lunge/tuck poses |

### hero_attack_crouch — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 140x122 (101, 131) | 1.031/SA | 144x126 (104, 135) | OK |
| 1 | 140x123 (101, 131) | 1.030/SA | 144x126 (104, 135) | OK |
| 2 | 135x153 (100, 144) | 1.042/SA | 141x159 (104, 150) | SQ residual +9.7% — pose redistribution; SA-anchored |
| 3 | 137x154 (100, 145) | 1.046/SA | 143x161 (104, 152) | SQ residual +11.1% — pose redistribution; SA-anchored |
| 4 | 140x135 (105, 138) | 0.992/SA | 139x134 (104, 136) | OK |
| 5 | 140x136 (104, 138) | - | 140x136 (104, 138) | OK |
| 6 | 140x135 (105, 138) | 0.994/SA | 139x134 (103, 136) | OK |
| 7 | 143x132 (105, 137) | 0.994/SA | 142x131 (103, 136) | OK |

### hero_attack_ground — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 232x179 (139, 204) | 0.966/H | 224x173 (134, 197) | SQ residual -7.0% — lunge + side-profile poses (width collapses in profile; standing frames height-anchored to 224) |
| 1 | 232x179 (139, 204) | 0.966/H | 224x173 (134, 197) | SQ residual -7.0% — lunge + side-profile poses (width collapses in profile; standing frames height-anchored to 224) |
| 2 | 216x222 (136, 219) | 1.037/H | 223x230 (141, 226) | SQ residual +7.0% — lunge + side-profile poses (width collapses in profile; standing frames height-anchored to 224) |
| 3 | 207x250 (139, 228) | 0.985/SA | 203x246 (136, 224) | SQ residual +5.6% — lunge + side-profile poses (width collapses in profile; standing frames height-anchored to 224) |
| 4 | 209x211 (136, 210) | 1.072/H | 224x226 (145, 225) | SQ residual +6.3% — lunge + side-profile poses (width collapses in profile; standing frames height-anchored to 224) |
| 5 | 215x192 (132, 203) | 1.042/H | 224x200 (137, 212) | OK |
| 6 | 250x72 (112, 134) | 0.896/H | 224x65 (100, 121) | SQ residual -43.0% — lunge + side-profile poses (width collapses in profile; standing frames height-anchored to 224) |
| 7 | 250x72 (113, 134) | 0.896/H | 224x65 (101, 121) | SQ residual -43.0% — lunge + side-profile poses (width collapses in profile; standing frames height-anchored to 224) |

### hero_crouch_enter — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 190x59 (83, 106) | 1.112/SA | 211x66 (92, 118) | OK |
| 1 | 184x83 (95, 124) | 0.980/SA | 180x81 (92, 121) | OK |
| 2 | 146x94 (93, 117) | - | 146x94 (93, 117) | OK |
| 3 | 140x95 (91, 115) | 1.015/SA | 142x96 (92, 117) | OK |

### hero_crouch_exit — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 140x95 (91, 115) | 1.015/SA | 142x96 (92, 117) | OK |
| 1 | 146x94 (93, 117) | - | 146x94 (93, 117) | OK |
| 2 | 184x83 (95, 124) | 0.980/SA | 180x81 (92, 121) | OK |
| 3 | 190x59 (83, 106) | 1.112/SA | 211x66 (92, 118) | OK |

### hero_crouch_idle — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 145x115 (96, 129) | 1.005/SA | 146x116 (97, 130) | OK |
| 1 | 139x119 (97, 129) | - | 139x119 (97, 129) | OK |
| 2 | 135x120 (97, 127) | - | 135x120 (97, 127) | OK |
| 3 | 140x119 (97, 129) | - | 140x119 (97, 129) | OK |
| 4 | 140x119 (97, 129) | - | 140x119 (97, 129) | OK |
| 5 | 140x119 (97, 129) | - | 140x119 (97, 129) | OK |

### hero_death — 10 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 229x119 (134, 165) | 1.041/SA | 238x124 (138, 172) | OK |
| 1 | 219x132 (139, 170) | - | 219x132 (139, 170) | OK |
| 2 | 214x183 (156, 198) | 0.890/SA | 190x162 (139, 175) | OK |
| 3 | 194x164 (149, 178) | 0.935/SA | 181x152 (138, 166) | OK |
| 4 | 192x205 (159, 198) | 0.877/SA | 167x180 (139, 173) | OK |
| 5 | 166x208 (151, 186) | 0.921/SA | 153x191 (139, 171) | OK |
| 6 | 130x183 (137, 154) | 1.019/SA | 132x186 (139, 157) | SQ residual -7.8% — death collapse to lying corpse (pose); final heap frames are ink-poor by pose |
| 7 | 88x239 (128, 145) | 1.090/SA | 95x261 (139, 158) | SQ residual -7.4% — death collapse to lying corpse (pose); final heap frames are ink-poor by pose |
| 8 | 42x145 (91, 78) | 1.180/SA | 48x171 (107, 91) | SQ residual -46.7% — death collapse to lying corpse (pose); final heap frames are ink-poor by pose |
| 9 | 78x235 (113, 135) | 1.180/SA | 91x277 (132, 159) | SQ residual -6.6% — death collapse to lying corpse (pose); final heap frames are ink-poor by pose |

### hero_fall — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 203x106 (104, 147) | 0.973/SA | 197x103 (100, 142) | SQ residual -11.9% — airborne tuck (pose) |
| 1 | 215x118 (99, 159) | 1.013/SA | 218x120 (100, 162) | OK |
| 2 | 222x118 (97, 162) | 1.037/SA | 230x122 (99, 168) | OK |
| 3 | 224x113 (101, 159) | - | 224x113 (101, 159) | OK |

### hero_get_up — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 123x134 (104, 128) | - | 123x134 (104, 128) | SQ residual -16.4% — rise-from-ground (pose, reverse of knockdown) |
| 1 | 136x121 (90, 128) | 1.151/SA | 156x139 (103, 147) | SQ residual -4.0% — rise-from-ground (pose, reverse of knockdown) |
| 2 | 128x133 (93, 130) | 1.113/SA | 142x144 (103, 143) | SQ residual -6.8% — rise-from-ground (pose, reverse of knockdown) |
| 3 | 153x134 (97, 143) | 1.076/SA | 164x144 (103, 154) | OK |
| 4 | 219x128 (110, 167) | 0.948/SA | 208x121 (103, 159) | OK |
| 5 | 229x129 (116, 172) | 0.895/SA | 205x115 (103, 154) | OK |

### hero_hurt_recoil — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 243x77 (109, 137) | 0.922/H | 224x70 (100, 125) | SQ residual -24.6% — pose redistribution; SA-anchored |
| 1 | 228x122 (123, 167) | 0.982/H | 224x120 (120, 164) | OK |
| 2 | 205x129 (117, 163) | 1.022/SA | 209x132 (119, 166) | OK |
| 3 | 220x125 (120, 166) | 1.018/H | 224x127 (121, 169) | OK |

### hero_idle — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 223x133 (137, 172) | 1.004/H | 224x133 (137, 173) | SQ residual -6.1% — pose redistribution; SA-anchored |
| 1 | 224x139 (139, 176) | - | 224x139 (139, 176) | SQ residual -4.0% — pose redistribution; SA-anchored |
| 2 | 225x142 (140, 179) | 0.996/H | 224x140 (138, 177) | OK |
| 3 | 222x146 (138, 180) | 1.009/H | 224x146 (139, 181) | OK |
| 4 | 226x182 (142, 203) | 0.991/H | 223x179 (140, 200) | SQ residual +8.6% — pose redistribution; SA-anchored |
| 5 | 224x151 (140, 184) | - | 224x151 (140, 184) | OK |
| 6 | 224x178 (142, 200) | - | 224x178 (142, 200) | SQ residual +8.6% — pose redistribution; SA-anchored |
| 7 | 223x152 (140, 184) | 1.004/H | 224x152 (140, 184) | OK |

### hero_jump_apex — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 224x176 (149, 199) | - | 224x176 (149, 199) | OK |
| 1 | 178x218 (147, 197) | - | 178x218 (147, 197) | OK |
| 2 | 189x188 (139, 188) | 1.059/SA | 200x198 (146, 199) | OK |

### hero_jump_rise — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 174x136 (113, 154) | 1.042/SA | 181x142 (117, 160) | SQ residual -12.0% — airborne extension/tuck (pose) |
| 1 | 224x133 (122, 173) | - | 224x133 (122, 173) | SQ residual -5.2% — airborne extension/tuck (pose) |
| 2 | 211x139 (118, 171) | 1.062/H | 224x148 (124, 182) | OK |
| 3 | 208x138 (117, 169) | 1.077/H | 223x149 (125, 182) | OK |

### hero_jump_takeoff — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 164x170 (126, 167) | 1.045/SA | 171x178 (131, 174) | SQ residual -9.0% — takeoff crouch then extension (pose) |
| 1 | 223x163 (132, 191) | 1.004/H | 224x164 (132, 192) | OK |
| 2 | 221x183 (132, 201) | 1.014/H | 223x184 (132, 203) | SQ residual +5.7% — takeoff crouch then extension (pose) |

### hero_knockback — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 224x123 (116, 166) | - | 224x123 (116, 166) | OK |
| 1 | 220x123 (105, 164) | 1.018/H | 224x125 (106, 167) | OK |
| 2 | 185x120 (104, 149) | 1.029/SA | 190x123 (106, 153) | SQ residual -7.9% — pose redistribution; SA-anchored |
| 3 | 204x117 (107, 154) | - | 204x117 (107, 154) | SQ residual -6.9% — pose redistribution; SA-anchored |

### hero_knockdown — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 229x129 (116, 172) | 0.895/SA | 205x115 (103, 154) | OK |
| 1 | 219x128 (110, 167) | 0.948/SA | 208x121 (103, 159) | OK |
| 2 | 153x134 (97, 143) | 1.076/SA | 164x144 (103, 154) | OK |
| 3 | 128x133 (93, 130) | 1.113/SA | 142x144 (103, 143) | SQ residual -6.8% — fall-to-ground collapse (pose) |
| 4 | 136x121 (90, 128) | 1.151/SA | 156x139 (103, 147) | SQ residual -4.0% — fall-to-ground collapse (pose) |
| 5 | 123x134 (104, 128) | - | 123x134 (104, 128) | SQ residual -16.4% — fall-to-ground collapse (pose) |

### hero_land — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 239x121 (121, 170) | 0.937/H | 223x112 (112, 158) | OK |
| 1 | 209x126 (122, 162) | 1.072/H | 224x135 (130, 174) | SQ residual +10.1% — landing squash (pose; height residual intended, clamp-corrected only) |
| 2 | 169x139 (117, 153) | 1.029/SA | 174x143 (120, 158) | OK |
| 3 | 260x82 (116, 146) | 0.862/H | 224x71 (100, 126) | SQ residual -20.2% — landing squash (pose; height residual intended, clamp-corrected only) |

### hero_start_move — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 239x80 (109, 138) | 0.937/H | 224x75 (101, 130) | SQ residual -34.0% — side-profile start frame (width collapse; height anchored) |
| 1 | 219x176 (138, 196) | 1.023/H | 224x180 (140, 201) | OK |
| 2 | 224x172 (133, 196) | - | 224x172 (133, 196) | OK |

### hero_stop_move — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 223x206 (137, 214) | 1.004/H | 224x206 (137, 215) | OK |
| 1 | 224x203 (131, 213) | - | 224x203 (131, 213) | OK |
| 2 | 241x85 (112, 143) | 0.929/H | 224x79 (103, 133) | SQ residual -37.6% — side-profile stop frame (width collapse; height anchored) |

### hero_turn — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 225x84 (108, 138) | 0.996/H | 224x84 (107, 137) | OK |
| 1 | 212x186 (128, 199) | 1.057/H | 224x197 (135, 210) | SQ residual +49.6% — mid-turn coat spread (width pose; height anchored) |
| 2 | 224x88 (108, 140) | - | 224x88 (108, 140) | OK |

### hero_walk — 10 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 229x122 (118, 167) | 0.978/H | 224x118 (114, 163) | SQ residual -11.3% — pose redistribution; SA-anchored |
| 1 | 231x135 (118, 177) | 0.970/H | 223x130 (113, 170) | SQ residual -7.1% — pose redistribution; SA-anchored |
| 2 | 227x152 (125, 186) | 0.987/H | 223x150 (123, 183) | OK |
| 3 | 215x162 (123, 187) | 1.042/H | 223x169 (127, 194) | SQ residual +5.9% — pose redistribution; SA-anchored |
| 4 | 219x161 (124, 188) | 1.023/H | 224x164 (126, 192) | SQ residual +4.6% — pose redistribution; SA-anchored |
| 5 | 223x144 (121, 179) | 1.004/H | 223x145 (121, 180) | OK |
| 6 | 227x152 (123, 186) | 0.987/H | 224x149 (120, 183) | OK |
| 7 | 224x152 (123, 184) | - | 224x152 (123, 184) | OK |
| 8 | 224x150 (123, 183) | - | 224x150 (123, 183) | OK |
| 9 | 220x153 (119, 184) | 1.018/H | 224x156 (121, 187) | OK |

### projectile_grave_shot — 3 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 64x64 (62, 64) | - | 64x64 (62, 64) | unchanged (md5-verified) |
| 1 | 64x64 (64, 64) | - | 64x64 (64, 64) | unchanged (md5-verified) |
| 2 | 64x64 (62, 64) | - | 64x64 (62, 64) | unchanged (md5-verified) |

### pursuer_alert — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 111x203 (100, 150) | - | 111x203 (100, 150) | SQ residual -4.4% — rear-up tell (pose apex) |
| 1 | 160x211 (105, 184) | 0.953/SA | 152x201 (98, 175) | SQ residual +11.3% — rear-up tell (pose apex) |
| 2 | 160x175 (90, 167) | 1.111/SA | 160x154 (92, 157) | OK |
| 3 | 160x108 (78, 132) | 1.180/SA | 160x94 (81, 123) | SQ residual -21.9% — rear-up tell (pose apex) |

### pursuer_approach_walk — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 96x183 (85, 132) | 1.026/SA | 99x188 (86, 136) | OK |
| 1 | 104x179 (87, 136) | 1.004/SA | 102x180 (85, 136) | OK |
| 2 | 123x174 (86, 146) | 1.008/SA | 124x175 (85, 147) | SQ residual +4.5% — pose redistribution; SA-anchored |
| 3 | 115x175 (88, 142) | 0.989/SA | 113x173 (86, 140) | OK |
| 4 | 107x184 (85, 140) | 1.021/SA | 109x188 (86, 143) | OK |
| 5 | 111x179 (87, 141) | - | 111x179 (87, 141) | OK |
| 6 | 111x179 (87, 141) | - | 111x179 (87, 141) | OK |
| 7 | 111x181 (87, 142) | 0.996/SA | 111x180 (86, 141) | OK |

### pursuer_death — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 126x130 (69, 128) | - | 126x130 (69, 128) | SQ residual +22.4% — collapse to corpse (pose) |
| 1 | 98x117 (69, 107) | 0.990/SA | 96x114 (67, 105) | OK |
| 2 | 96x118 (69, 106) | 0.992/SA | 95x113 (67, 104) | OK |
| 3 | 69x126 (61, 93) | 1.125/SA | 78x141 (68, 105) | OK |
| 4 | 41x127 (55, 72) | 1.180/SA | 48x149 (64, 85) | SQ residual -19.1% — collapse to corpse (pose) |
| 5 | 41x127 (55, 72) | 1.180/SA | 48x149 (64, 85) | SQ residual -19.1% — collapse to corpse (pose) |

### pursuer_hurt — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 135x137 (74, 136) | 0.979/SA | 132x134 (72, 133) | SQ residual +12.9% — pose redistribution; SA-anchored |
| 1 | 93x114 (73, 103) | - | 93x114 (73, 103) | SQ residual -12.6% — pose redistribution; SA-anchored |
| 2 | 112x124 (72, 118) | 1.011/SA | 112x124 (72, 118) | OK |

### pursuer_idle — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 111x156 (92, 132) | 0.990/SA | 109x154 (89, 130) | OK |
| 1 | 148x163 (91, 155) | - | 148x163 (91, 155) | SQ residual +17.3% — pose redistribution; SA-anchored |
| 2 | 111x155 (92, 131) | 0.984/SA | 109x153 (89, 129) | OK |
| 3 | 110x159 (90, 132) | 1.007/SA | 111x158 (90, 132) | OK |
| 4 | 140x162 (90, 151) | 1.008/SA | 140x163 (89, 151) | SQ residual +14.1% — pose redistribution; SA-anchored |
| 5 | 109x159 (90, 132) | 1.007/SA | 110x158 (90, 132) | OK |

### pursuer_lunge — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 112x122 (69, 117) | 0.850/SA | 95x102 (57, 98) | SQ residual +15.5% — flattened leap (pose) |
| 1 | 61x119 (54, 85) | - | 61x119 (54, 85) | OK |
| 2 | 47x126 (51, 77) | 1.068/SA | 50x134 (53, 82) | OK |

### pursuer_lunge_windup — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 159x93 (71, 122) | 1.013/SA | 160x94 (71, 123) | SQ residual +9.9% — rear-up/crouch before lunge (pose) |
| 1 | 150x83 (72, 112) | - | 150x83 (72, 112) | OK |
| 2 | 111x93 (72, 102) | - | 111x93 (72, 102) | SQ residual -9.0% — rear-up/crouch before lunge (pose) |
| 3 | 115x87 (72, 100) | 1.008/SA | 116x88 (71, 101) | SQ residual -9.5% — rear-up/crouch before lunge (pose) |

### pursuer_patrol_walk — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 115x166 (79, 138) | 1.049/SA | 121x174 (83, 145) | SQ residual +7.4% — pose redistribution; SA-anchored |
| 1 | 124x154 (85, 138) | 0.986/SA | 121x152 (82, 136) | OK |
| 2 | 122x162 (83, 141) | - | 122x162 (83, 141) | SQ residual +4.1% — pose redistribution; SA-anchored |
| 3 | 112x161 (83, 134) | - | 112x161 (83, 134) | OK |
| 4 | 107x166 (82, 133) | 1.021/SA | 108x169 (82, 135) | OK |
| 5 | 108x163 (84, 133) | - | 108x163 (84, 133) | OK |
| 6 | 110x164 (84, 134) | 0.995/SA | 105x163 (82, 131) | OK |
| 7 | 106x163 (83, 131) | - | 106x163 (83, 131) | OK |

### pursuer_recovery — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 84x149 (74, 112) | 1.063/SA | 87x158 (77, 117) | OK |
| 1 | 115x115 (80, 115) | 0.976/SA | 111x112 (77, 112) | SQ residual -5.6% — pose redistribution; SA-anchored |
| 2 | 139x129 (78, 134) | 1.008/SA | 140x126 (77, 133) | SQ residual +12.4% — pose redistribution; SA-anchored |
| 3 | 109x128 (78, 118) | - | 109x128 (78, 118) | OK |

### ranged_aim — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 288x169 (165, 221) | 1.028/SA | 288x173 (168, 223) | SQ residual -7.9% — pose redistribution; SA-anchored |
| 1 | 288x202 (168, 241) | 1.013/SA | 288x204 (169, 242) | OK |
| 2 | 288x212 (169, 247) | 1.005/SA | 288x212 (169, 247) | OK |
| 3 | 288x218 (170, 251) | - | 288x218 (170, 251) | OK |
| 4 | 288x218 (171, 251) | 0.994/SA | 286x185 (167, 230) | SQ residual -5.1% — pose redistribution; SA-anchored |
| 5 | 288x254 (175, 270) | 0.968/SA | 279x174 (166, 220) | SQ residual -9.1% — pose redistribution; SA-anchored |

### ranged_death — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 288x147 (153, 206) | 1.023/SA | 288x150 (155, 208) | SQ residual -5.9% — pose redistribution; SA-anchored |
| 1 | 288x172 (157, 223) | - | 288x172 (157, 223) | OK |
| 2 | 288x171 (158, 222) | 0.996/SA | 287x170 (156, 221) | OK |
| 3 | 288x165 (157, 218) | - | 288x165 (157, 218) | OK |
| 4 | 288x171 (157, 222) | - | 288x171 (157, 222) | OK |
| 5 | 288x172 (159, 223) | 0.988/SA | 284x169 (155, 219) | OK |

### ranged_fire — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 288x170 (136, 221) | 0.943/SA | 272x160 (127, 209) | SQ residual +13.2% — pose redistribution; SA-anchored |
| 1 | 288x118 (129, 184) | - | 288x118 (129, 184) | OK |
| 2 | 288x117 (127, 184) | 1.010/SA | 288x117 (127, 184) | OK |

### ranged_hurt — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 288x255 (174, 271) | 0.939/SA | 270x239 (162, 254) | SQ residual +8.3% — pose redistribution; SA-anchored |
| 1 | 288x191 (163, 234) | - | 288x191 (163, 234) | OK |
| 2 | 288x176 (159, 225) | 1.023/SA | 288x180 (162, 228) | OK |

### ranged_idle — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 288x131 (151, 194) | 1.017/SA | 288x132 (152, 195) | SQ residual -4.2% — pose redistribution; SA-anchored |
| 1 | 288x137 (152, 199) | 1.005/SA | 288x138 (153, 199) | OK |
| 2 | 288x144 (153, 204) | - | 288x144 (153, 204) | OK |
| 3 | 288x161 (158, 215) | 0.968/SA | 279x155 (153, 208) | OK |
| 4 | 288x148 (154, 206) | - | 288x148 (154, 206) | OK |
| 5 | 288x143 (153, 203) | 1.004/SA | 288x143 (152, 203) | OK |

### ranged_recover — 7 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 288x256 (169, 272) | 0.935/SA | 269x239 (157, 254) | SQ residual -6.6% — pose redistribution; SA-anchored |
| 1 | 288x256 (156, 272) | 1.017/SA | 288x256 (157, 272) | OK |
| 2 | 288x256 (158, 272) | - | 288x256 (158, 272) | OK |
| 3 | 288x256 (156, 272) | 1.018/SA | 288x256 (157, 272) | OK |
| 4 | 288x256 (156, 272) | 1.015/SA | 288x256 (157, 272) | OK |
| 5 | 288x256 (158, 272) | - | 288x256 (158, 272) | OK |
| 6 | 288x256 (158, 272) | - | 288x256 (158, 272) | OK |

### swooper_cruise — 8 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 182x165 (119, 173) | 0.990/SA | 179x162 (117, 170) | OK |
| 1 | 180x173 (118, 176) | - | 180x173 (118, 176) | OK |
| 2 | 132x180 (113, 154) | 1.048/SA | 138x188 (118, 161) | SQ residual -7.4% — pose redistribution; SA-anchored |
| 3 | 136x164 (114, 149) | 1.042/SA | 142x171 (118, 156) | SQ residual -10.4% — pose redistribution; SA-anchored |
| 4 | 157x187 (113, 171) | 1.044/SA | 163x195 (117, 178) | OK |
| 5 | 169x168 (116, 168) | 1.017/SA | 171x171 (118, 171) | OK |
| 6 | 169x183 (119, 176) | - | 169x183 (119, 176) | OK |
| 7 | 173x183 (120, 178) | 0.984/SA | 169x179 (117, 174) | OK |

### swooper_death_fall — 5 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 240x227 (143, 233) | 0.886/SA | 212x201 (126, 206) | SQ residual +14.5% — tumbling fall (pose) |
| 1 | 170x191 (127, 180) | - | 170x191 (127, 180) | OK |
| 2 | 177x178 (119, 178) | 1.063/SA | 188x189 (126, 188) | SQ residual +4.6% — tumbling fall (pose) |
| 3 | 164x176 (128, 170) | 0.989/SA | 162x174 (125, 168) | SQ residual -6.8% — tumbling fall (pose) |
| 4 | 80x269 (112, 147) | 1.137/SA | 89x305 (126, 165) | SQ residual -8.5% — tumbling fall (pose) |

### swooper_dive — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 165x164 (122, 164) | 0.953/SA | 156x156 (115, 156) | SQ residual -20.4% — dive fold (pose) |
| 1 | 155x145 (111, 150) | 1.047/SA | 161x152 (116, 156) | SQ residual -20.2% — dive fold (pose) |
| 2 | 174x221 (116, 196) | - | 174x221 (116, 196) | OK |
| 3 | 174x222 (108, 196) | 1.080/SA | 188x240 (116, 212) | SQ residual +8.3% — dive fold (pose) |

### swooper_dive_telegraph — 4 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 235x133 (119, 177) | 0.895/SA | 210x119 (106, 158) | SQ residual +20.5% — wings folding to dart (pose) |
| 1 | 198x87 (107, 131) | - | 198x87 (107, 131) | OK |
| 2 | 141x86 (78, 110) | 1.180/SA | 166x102 (91, 130) | OK |
| 3 | 108x109 (62, 108) | 1.180/SA | 127x128 (72, 128) | OK |

### swooper_hurt — 3 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 184x188 (112, 186) | 0.977/SA | 180x184 (109, 182) | SQ residual +15.9% — pose redistribution; SA-anchored |
| 1 | 170x145 (109, 157) | - | 170x145 (109, 157) | OK |
| 2 | 128x181 (109, 152) | - | 128x181 (109, 152) | OK |

### swooper_perch_idle — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 168x150 (118, 159) | 1.039/SA | 174x156 (122, 165) | OK |
| 1 | 168x143 (119, 155) | 1.031/SA | 172x147 (122, 159) | OK |
| 2 | 168x149 (122, 158) | - | 168x149 (122, 158) | OK |
| 3 | 173x154 (123, 163) | - | 173x154 (123, 163) | OK |
| 4 | 173x153 (127, 163) | 0.966/SA | 166x148 (122, 157) | OK |
| 5 | 170x156 (123, 163) | - | 170x156 (123, 163) | OK |

### swooper_recovery_climb — 6 frames
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 175x143 (111, 158) | 0.921/SA | 161x131 (101, 145) | SQ residual -7.2% — pose redistribution; SA-anchored |
| 1 | 135x177 (99, 155) | 1.026/SA | 139x182 (101, 159) | OK |
| 2 | 125x165 (101, 144) | 1.010/SA | 126x167 (101, 145) | SQ residual -7.2% — pose redistribution; SA-anchored |
| 3 | 167x164 (102, 166) | - | 167x164 (102, 166) | SQ residual +5.8% — pose redistribution; SA-anchored |
| 4 | 171x143 (102, 156) | - | 171x143 (102, 156) | OK |
| 5 | 172x152 (106, 162) | 0.958/SA | 164x146 (101, 155) | OK |

### vfx_checkpoint_activate — 8 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 38x61 (35, 48) | - | 38x61 (35, 48) | unchanged (md5-verified) |
| 1 | 124x110 (77, 117) | - | 124x110 (77, 117) | unchanged (md5-verified) |
| 2 | 182x150 (133, 165) | - | 182x150 (133, 165) | unchanged (md5-verified) |
| 3 | 217x142 (165, 176) | - | 217x142 (165, 176) | unchanged (md5-verified) |
| 4 | 209x137 (158, 169) | - | 209x137 (158, 169) | unchanged (md5-verified) |
| 5 | 205x123 (150, 159) | - | 205x123 (150, 159) | unchanged (md5-verified) |
| 6 | 254x122 (143, 176) | - | 254x122 (143, 176) | unchanged (md5-verified) |
| 7 | 249x111 (137, 166) | - | 249x111 (137, 166) | unchanged (md5-verified) |

### vfx_damage_indicator — 2 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 217x200 (113, 208) | - | 217x200 (113, 208) | unchanged (md5-verified) |
| 1 | 220x217 (141, 218) | - | 220x217 (141, 218) | unchanged (md5-verified) |

### vfx_enemy_defeat — 8 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 128x128 (128, 128) | - | 128x128 (128, 128) | unchanged (md5-verified) |
| 1 | 174x174 (169, 174) | - | 174x174 (169, 174) | unchanged (md5-verified) |
| 2 | 217x217 (188, 217) | - | 217x217 (188, 217) | unchanged (md5-verified) |
| 3 | 135x174 (124, 153) | - | 135x174 (124, 153) | unchanged (md5-verified) |
| 4 | 214x223 (187, 218) | - | 214x223 (187, 218) | unchanged (md5-verified) |
| 5 | 202x195 (136, 198) | - | 202x195 (136, 198) | unchanged (md5-verified) |
| 6 | 29x13 (31, 19) | - | 29x13 (31, 19) | unchanged (md5-verified) |
| 7 | 17x12 (15, 14) | - | 17x12 (15, 14) | unchanged (md5-verified) |

### vfx_hazard_eruption — 6 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 67x119 (70, 89) | - | 67x119 (70, 89) | unchanged (md5-verified) |
| 1 | 192x222 (163, 206) | - | 192x222 (163, 206) | unchanged (md5-verified) |
| 2 | 192x312 (230, 245) | - | 192x312 (230, 245) | unchanged (md5-verified) |
| 3 | 192x320 (246, 248) | - | 192x320 (246, 248) | unchanged (md5-verified) |
| 4 | 80x200 (132, 126) | - | 80x200 (132, 126) | unchanged (md5-verified) |
| 5 | 75x204 (81, 124) | - | 75x204 (81, 124) | unchanged (md5-verified) |

### vfx_hazard_telegraph — 4 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 77x320 (156, 157) | - | 77x320 (156, 157) | unchanged (md5-verified) |
| 1 | 75x320 (155, 155) | - | 75x320 (155, 155) | unchanged (md5-verified) |
| 2 | 79x320 (159, 159) | - | 79x320 (159, 159) | unchanged (md5-verified) |
| 3 | 80x320 (160, 160) | - | 80x320 (160, 160) | unchanged (md5-verified) |

### vfx_whip_impact — 6 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 86x86 (65, 86) | - | 86x86 (65, 86) | unchanged (md5-verified) |
| 1 | 148x148 (111, 148) | - | 148x148 (111, 148) | unchanged (md5-verified) |
| 2 | 204x204 (152, 204) | - | 204x204 (152, 204) | unchanged (md5-verified) |
| 3 | 162x162 (120, 162) | - | 162x162 (120, 162) | unchanged (md5-verified) |
| 4 | 108x108 (79, 108) | - | 108x108 (79, 108) | unchanged (md5-verified) |
| 5 | 58x58 (40, 58) | - | 58x58 (40, 58) | unchanged (md5-verified) |

### whip_attack_air — 8 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 70x79 (42, 74) | - | 70x79 (42, 74) | unchanged (md5-verified) |
| 1 | 66x81 (42, 73) | - | 66x81 (42, 73) | unchanged (md5-verified) |
| 2 | 97x216 (44, 145) | - | 97x216 (44, 145) | unchanged (md5-verified) |
| 3 | 17x251 (40, 65) | - | 17x251 (40, 65) | unchanged (md5-verified) |
| 4 | 107x175 (36, 137) | - | 107x175 (36, 137) | unchanged (md5-verified) |
| 5 | 57x179 (37, 101) | - | 57x179 (37, 101) | unchanged (md5-verified) |
| 6 | 81x77 (40, 79) | - | 81x77 (40, 79) | unchanged (md5-verified) |
| 7 | 83x78 (42, 80) | - | 83x78 (42, 80) | unchanged (md5-verified) |

### whip_attack_crouch — 8 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 72x81 (44, 76) | - | 72x81 (44, 76) | unchanged (md5-verified) |
| 1 | 74x81 (44, 77) | - | 74x81 (44, 77) | unchanged (md5-verified) |
| 2 | 53x233 (41, 111) | - | 53x233 (41, 111) | unchanged (md5-verified) |
| 3 | 16x286 (42, 68) | - | 16x286 (42, 68) | unchanged (md5-verified) |
| 4 | 74x238 (41, 133) | - | 74x238 (41, 133) | unchanged (md5-verified) |
| 5 | 47x162 (36, 87) | - | 47x162 (36, 87) | unchanged (md5-verified) |
| 6 | 80x78 (42, 79) | - | 80x78 (42, 79) | unchanged (md5-verified) |
| 7 | 76x78 (42, 77) | - | 76x78 (42, 77) | unchanged (md5-verified) |

### whip_attack_ground — 8 frames (EXEMPT — unchanged)
| f | before HxW (SA, SQ) | factor/rule | after HxW (SA, SQ) | verdict |
|---|---|---|---|---|
| 0 | 81x99 (46, 90) | - | 81x99 (46, 90) | unchanged (md5-verified) |
| 1 | 82x110 (49, 95) | - | 82x110 (49, 95) | unchanged (md5-verified) |
| 2 | 85x234 (44, 141) | - | 85x234 (44, 141) | unchanged (md5-verified) |
| 3 | 20x257 (40, 72) | - | 20x257 (40, 72) | unchanged (md5-verified) |
| 4 | 83x240 (41, 141) | - | 83x240 (41, 141) | unchanged (md5-verified) |
| 5 | 39x169 (36, 81) | - | 39x169 (36, 81) | unchanged (md5-verified) |
| 6 | 83x83 (42, 83) | - | 83x83 (42, 83) | unchanged (md5-verified) |
| 7 | 85x82 (44, 84) | - | 85x82 (44, 84) | unchanged (md5-verified) |

