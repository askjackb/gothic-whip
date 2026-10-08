extends SceneTree
## Headless smoke test (no GUT): loads the main scene, drives the hunter
## through InputState, and asserts movement, the jump envelope, and the
## whip active window [150, 250) ms of the 500 ms timeline (SPEC S5).
## Run: godot --headless --path . --script tests/smoke_test.gd
## Exit code 0 + "SMOKE RESULT: PASS" on success; 1 with FAIL lines otherwise.

var _main: Node
var _frame := 0
var _phase := 0
var _failures: Array[String] = []

var _start_x := 0.0
var _jump_start_y := 0.0
var _apex_y := 0.0
var _whip_frame := 0


func _initialize() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	if ps == null:
		_fail("main scene failed to load")
		_finish()
		return
	_main = ps.instantiate()
	root.add_child(_main)
	physics_frame.connect(_on_physics_frame)
	print("SMOKE: main scene loaded")


func _fail(msg: String) -> void:
	_failures.append(msg)
	print("SMOKE FAIL: ", msg)


func _check(cond: bool, msg: String) -> void:
	if cond:
		print("SMOKE PASS: ", msg)
	else:
		_fail(msg)


func _hunter() -> Hunter:
	return _main.hunter


func _input() -> InputState:
	return _main.input_state


func _on_physics_frame() -> void:
	_frame += 1
	var h := _hunter()
	if h == null:
		if _frame > 30:
			_fail("hunter never appeared")
			_finish()
		return
	match _phase:
		0: # settle, check spawn state
			if _frame >= 10:
				_check(h.get_state() == "idle", "hunter idles at spawn (state=%s)" % h.get_state())
				_check(h.hp == 5, "hunter spawns with 5 HP")
				_start_x = h.global_position.x
				_input().debug_set_held("move_right", true)
				_phase = 1
		1: # walk right for 30 physics frames (~0.5 s at 240 u/s)
			if _frame >= 40:
				_input().debug_set_held("move_right", false)
				var dx := h.global_position.x - _start_x
				_check(dx > 60.0, "hunter walked right %.1f u in 0.5 s" % dx)
				_check(h.get_state() in ["walk", "start_move", "stop_move", "idle"],
					"hunter in a ground locomotion state after walking (state=%s)" % h.get_state())
				_jump_start_y = h.global_position.y
				_apex_y = _jump_start_y
				_input().debug_press("jump")
				_phase = 2
		2: # track jump apex for ~1.9 s
			_apex_y = minf(_apex_y, h.global_position.y)
			if _frame >= 155:
				var rise := _jump_start_y - _apex_y
				_check(rise > 95.0 and rise < 150.0,
					"jump rise %.1f u within envelope of 128 u (SPEC S4)" % rise)
				_check(h.get_state() == "idle", "hunter landed back to idle (state=%s)" % h.get_state())
				# reposition in front of the training effigy (module 6)
				h.global_position = Vector2(300, 512)
				h.velocity = Vector2.ZERO
				h.facing = 1
				_phase = 3
		3: # settle, then whip
			if _frame >= 170:
				_whip_frame = _frame
				_input().debug_press("whip")
				_phase = 4
		4: # whip timeline assertions; press consumed on tick _whip_frame,
			# so after k further ticks attack_t = k/60 s.
			var k := _frame - _whip_frame
			if k == 3:
				_check(h.get_state() == "attack_ground", "whip enters attack_ground")
			if k == 6: # ~100 ms: anticipation, hitbox must be OFF
				_check(not h.is_whip_active(), "whip inactive at ~100 ms (anticipation)")
				_check(_main.effigy.hit_count == 0, "effigy not hit during anticipation")
			if k == 12: # ~200 ms: inside [150, 250) ms window
				_check(h.is_whip_active(), "whip active at ~200 ms (active window)")
			if k == 18: # ~300 ms: recovery, hitbox OFF again
				_check(not h.is_whip_active(), "whip inactive at ~300 ms (recovery)")
				_check(_main.effigy.hit_count == 1, "effigy hit exactly once (count=%d)" % _main.effigy.hit_count)
			if k == 45:
				_check(_main.effigy.hit_count == 1, "no repeat hit from one attack (fresh press required)")
				# damage routing: contact -> knockback, projectile -> recoil
				h.take_damage("contact", h.global_position.x - 50.0)
				_check(h.hp == 4, "contact hit costs 1 HP (hp=%d)" % h.hp)
				_check(h.get_state() == "knockback", "contact hit routes to knockback (state=%s)" % h.get_state())
				_phase = 5
		5: # wait out knockback + i-frames (1 s), then lethal hit -> restart
			if _frame >= _whip_frame + 140:
				h.hp = 1
				h.take_damage("contact", h.global_position.x + 50.0)
				_check(h.get_state() == "death", "lethal hit routes to death (state=%s)" % h.get_state())
				_phase = 6
		6: # death (1.3 s) -> restart at respawn with full HP
			if _frame >= _whip_frame + 260:
				_check(h.hp == 5, "restart restores 5 HP (hp=%d)" % h.hp)
				_check(h.get_state() == "idle", "hunter idles after restart (state=%s)" % h.get_state())
				_check(h.global_position.distance_to(Vector2(160, 512)) < 2.0,
					"hunter back at stage-start respawn %s" % str(h.global_position))
				_phase = 7
		7: # production-art assertions (frames exist; live sprite follows state)
			_check_art_resources()
			h.global_position = Vector2(300, 512)
			h.velocity = Vector2.ZERO
			_input().debug_set_held("move_right", true)
			_phase = 8
		8:
			if _frame >= _whip_frame + 300:
				_input().debug_set_held("move_right", false)
				var spr: AnimatedSprite2D = h.get("_body")
				_check(spr != null and spr.sprite_frames != null, "hunter body sprite has SpriteFrames")
				if spr != null:
					_check(String(spr.animation).begins_with("hero_"),
						"hunter sprite playing a hero clip (anim=%s)" % spr.animation)
					var tex: Texture2D = spr.sprite_frames.get_frame_texture(spr.animation, spr.frame)
					_check(tex != null, "hunter sprite frame texture is non-null")
				_input().debug_press("whip")
				_phase = 9
		9:
			if h.get_state() in ["attack_ground", "attack_air", "attack_crouch"]:
				var wspr: AnimatedSprite2D = h.get("_whip_sprite")
				_check(wspr != null and wspr.visible, "whip sprite visible during attack")
				if wspr != null:
					_check(String(wspr.animation).begins_with("whip_attack"),
						"whip sprite playing a whip clip (anim=%s)" % wspr.animation)
				_finish()
			elif _frame > _whip_frame + 420:
				_fail("hunter never entered an attack state for art check")
				_finish()


func _check_art_resources() -> void:
	var required := {
		"hero_frames.tres": ["hero_idle", "hero_walk", "hero_attack_ground", "hero_attack_air",
			"hero_attack_crouch", "hero_crouch_idle", "hero_jump_rise", "hero_fall",
			"hero_knockdown", "hero_get_up", "hero_death"],
		"whip_frames.tres": ["whip_attack_ground", "whip_attack_air", "whip_attack_crouch"],
		"enemy_frames.tres": ["pursuer_patrol_walk", "pursuer_alert", "pursuer_lunge",
			"swooper_cruise", "swooper_dive", "ranged_idle", "ranged_aim", "projectile_grave_shot"],
		"boss_frames.tres": ["boss_idle", "boss_walk", "boss_strike_windup",
			"boss_hazard_windup", "boss_death"],
		"fx_frames.tres": ["vfx_whip_impact", "vfx_enemy_defeat", "vfx_checkpoint_activate",
			"vfx_hazard_telegraph", "vfx_hazard_eruption", "vfx_damage_indicator"],
	}
	for res_name in required:
		var frames: SpriteFrames = load("res://art/spriteframes/" + res_name)
		_check(frames != null, "%s loads" % res_name)
		if frames == null:
			continue
		for anim in required[res_name]:
			_check(frames.has_animation(anim) and frames.get_frame_count(anim) >= 2,
				"%s has clip %s (%d frames)" % [res_name, anim,
					frames.get_frame_count(anim) if frames.has_animation(anim) else 0])
	for wav in ["sfx_whip_swing", "sfx_whip_hit", "sfx_jump", "sfx_hurt",
			"sfx_death", "sfx_checkpoint", "sfx_boss_tell", "mus_stage_loop"]:
		_check(load("res://art/audio/%s.wav" % wav) != null, "audio %s loads" % wav)


func _finish() -> void:
	if _failures.is_empty():
		print("SMOKE RESULT: PASS")
		quit(0)
	else:
		print("SMOKE RESULT: FAIL (%d failures)" % _failures.size())
		quit(1)
