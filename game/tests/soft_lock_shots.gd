extends SceneTree
## Screenshot evidence for the 2026-10-09 crouch soft-lock fix. Runs the
## real scene under a display (xvfb) at the exact reported wedge spot
## (B3 re-ascent tread, street x=3550, a 12 u one-way slab 52 u overhead):
## shot 1 = hunter crouched beneath the tread; shot 2 = crouch released,
## hunter standing and walking out from under it.
##   xvfb-run ~/workspace/bin/godot --path . --script tests/soft_lock_shots.gd

var _main: Node


func _shot(name: String) -> void:
	var img := root.get_texture().get_image()
	img.save_png("res://tests/shots/" + name + ".png")
	print("SHOT: ", name, " ", img.get_size())


func _run() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	_main = packed.instantiate()
	root.add_child(_main)
	await create_timer(1.0).timeout
	var h = _main.get("hunter")
	var inp = _main.get("input_state")
	# Freeze enemies so the evidence is deterministic (same as smoke test).
	for e in _main.get("enemies"):
		e.set_physics_process(false)
		e.set_process(false)
	h.global_position = Vector2(3550, 512)
	h.velocity = Vector2.ZERO
	await create_timer(0.5).timeout
	inp.call("debug_set_held", "crouch", true)
	await create_timer(0.5).timeout
	_shot("fix_soft_lock_crouched")
	inp.call("debug_set_held", "crouch", false)
	inp.call("debug_set_held", "move_right", true)
	await create_timer(0.6).timeout
	_shot("fix_soft_lock_walkout")
	inp.call("debug_set_held", "move_right", false)
	print(" hunter state=", h.state, " pos=", h.global_position)
	print("SOFT LOCK SHOTS DONE")
	quit(0)


func _initialize() -> void:
	_run()
