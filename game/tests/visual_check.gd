extends SceneTree
## Visual verification tool (not a test): runs the real scene under a
## display, plays scripted moments, and saves viewport screenshots to
## /tmp/shots/ for human/agent review. Run under xvfb:
##   xvfb-run ~/workspace/bin/godot --path . --script tests/visual_check.gd

var _main: Node


func _initialize() -> void:
	_run()


func _shot(name: String) -> void:
	var img := root.get_texture().get_image()
	img.save_png("/tmp/shots/" + name + ".png")
	print("SHOT: ", name, " ", img.get_size())


func _run() -> void:
	var dir := DirAccess.open("/tmp")
	if dir and not dir.dir_exists("shots"):
		dir.make_dir("shots")
	var packed: PackedScene = load("res://scenes/main.tscn")
	_main = packed.instantiate()
	root.add_child(_main)
	await create_timer(1.0).timeout
	_shot("a_spawn")
	var h = _main.get("hunter")
	var inp = _main.get("input_state")
	inp.call("debug_set_held", "move_right", true)
	await create_timer(1.2).timeout
	inp.call("debug_set_held", "move_right", false)
	# place near the effigy and attack it
	h.global_position = Vector2(300, 512)
	h.velocity = Vector2.ZERO
	await create_timer(0.3).timeout
	inp.call("debug_press", "whip")
	await create_timer(0.22).timeout
	_shot("b_whip_strike")
	await create_timer(1.0).timeout
	# checkpoint area + pursuer encounter
	h.global_position = Vector2(1100, 512)
	h.velocity = Vector2.ZERO
	await create_timer(1.2).timeout
	_shot("c_pursuer")
	# boss arena via the dev warp
	h.global_position = Vector2(5560, 512)
	h.velocity = Vector2.ZERO
	await create_timer(1.5).timeout
	_shot("d_boss_arena")
	# hazard telegraph moment: wait for the boss cycle to cast
	await create_timer(6.0).timeout
	_shot("e_boss_fight")
	print("VISUAL CHECK DONE")
	quit(0)
