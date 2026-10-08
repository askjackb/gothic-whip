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
				_finish()


func _finish() -> void:
	if _failures.is_empty():
		print("SMOKE RESULT: PASS")
		quit(0)
	else:
		print("SMOKE RESULT: FAIL (%d failures)" % _failures.size())
		quit(1)
