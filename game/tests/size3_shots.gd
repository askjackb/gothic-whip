extends SceneTree
## Screenshot evidence for the 2026-10-09 per-frame scale fix: the hunter
## standing, mid-whip-attack and mid-jump in the same spawn area, to prove
## the in-action figure matches the standing figure. Run under xvfb:
##   xvfb-run ~/workspace/bin/godot --path . --script tests/size3_shots.gd

var _main: Node

func _shot(name: String) -> void:
	var img := root.get_texture().get_image()
	img.save_png("res://tests/shots/" + name + ".png")
	print("SHOT: ", name, " ", img.get_size())

func _initialize() -> void:
	_run()

func _run() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	_main = packed.instantiate()
	root.add_child(_main)
	await create_timer(1.2).timeout
	_shot("size3_a_stand")
	var h = _main.get("hunter")
	var inp = _main.get("input_state")
	# mid ground attack (frame ~200 ms into the 500 ms swing)
	inp.call("debug_press", "whip")
	await create_timer(0.21).timeout
	_shot("size3_b_attack")
	await create_timer(0.6).timeout
	# mid jump: rise phase
	inp.call("debug_press", "jump")
	await create_timer(0.20).timeout
	_shot("size3_c_jump")
	await create_timer(0.8).timeout
	print("SIZE3 SHOTS DONE")
	quit(0)
