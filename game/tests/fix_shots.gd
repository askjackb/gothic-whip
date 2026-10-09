extends SceneTree
## Screenshot evidence for the 2026-10-09 whip/VFX fix. Runs the real
## scene under a display (xvfb) and captures: the whip crack frame on the
## effigy, an enemy defeat burst, crouch + air whip poses, and the boss
## hazard telegraph on the ground. Saves to res://tests/shots/fix_*.png.
##   xvfb-run ~/workspace/bin/godot --path . --script tests/fix_shots.gd

var _main: Node


func _shot(name: String) -> void:
	var img := root.get_texture().get_image()
	img.save_png("res://tests/shots/" + name + ".png")
	print("SHOT: ", name, " ", img.get_size())


func _find_pursuer(node: Node) -> Node:
	if node is Pursuer:
		return node
	for c in node.get_children():
		var r := _find_pursuer(c)
		if r:
			return r
	return null


func _run() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	_main = packed.instantiate()
	root.add_child(_main)
	await create_timer(1.0).timeout
	var h = _main.get("hunter")
	var inp = _main.get("input_state")

	# 1) ground whip crack on the effigy (crack frame spans 150-200 ms)
	h.global_position = Vector2(300, 512)
	h.velocity = Vector2.ZERO
	await create_timer(0.4).timeout
	inp.call("debug_press", "whip")
	while h.attack_t < 0.21:
		await create_timer(0.01).timeout
	_shot("fix_whip_strike")
	await create_timer(0.8).timeout

	# 2) crouch whip (settle fully into crouch first; capture on state entry
	#    + a fixed offset - xvfb timer polls overshoot the attack clock)
	inp.call("debug_set_held", "crouch", true)
	await create_timer(0.5).timeout
	inp.call("debug_press", "whip")
	var guard := 0
	while h.state != "attack_crouch" and guard < 300:
		await create_timer(0.01).timeout
		guard += 1
	await create_timer(0.10).timeout
	_shot("fix_whip_crouch")
	inp.call("debug_set_held", "crouch", false)
	await create_timer(0.8).timeout

	# 3) air whip
	inp.call("debug_press", "jump")
	await create_timer(0.28).timeout
	inp.call("debug_press", "whip")
	guard = 0
	while h.state != "attack_air" and guard < 300:
		await create_timer(0.01).timeout
		guard += 1
	await create_timer(0.17).timeout
	_shot("fix_whip_air")
	await create_timer(1.0).timeout

	# 4) enemy defeat burst (pursuer has 1 HP; hit lands in active window)
	var p = _find_pursuer(_main)
	if p:
		h.global_position = p.global_position + Vector2(-120, 0)
		h.velocity = Vector2.ZERO
		await create_timer(0.5).timeout
		inp.call("debug_press", "whip")
		await create_timer(0.45).timeout
		_shot("fix_enemy_defeat")
	else:
		print("NO PURSUER FOUND")
	await create_timer(0.8).timeout

	# 5) boss hazard telegraph (wake the boss, stand off >170 u so it casts)
	var boss = _main.get("boss")
	h.global_position = Vector2(5940, 512)
	h.velocity = Vector2.ZERO
	await create_timer(0.4).timeout
	if boss:
		boss.call("start_fight")
	var waited := 0.0
	var got := false
	while waited < 20.0:
		await create_timer(0.25).timeout
		waited += 0.25
		for c in _main.get_children():
			if c is VfxPlayer and c.clip == "vfx_hazard_telegraph":
				_shot("fix_boss_telegraph")
				got = true
				break
		if got:
			break
	if not got:
		print("TELEGRAPH NOT SEEN in 20 s")
	print("FIX SHOTS DONE")
	quit(0)


func _initialize() -> void:
	_run()
