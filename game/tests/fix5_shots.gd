extends SceneTree
## Native-res screenshot for the round-5 crouch/boss repair: the boss
## standing in the arena on the regenerated full-body idle. The hunter is
## placed inside confrontation range (<160 u) and the capture happens
## before the boss's first strike decision, so he is standing on
## boss_idle. Saves to res://tests/shots/fix5/.
##   xvfb-run ~/workspace/bin/godot --path . --script tests/fix5_shots.gd

var _main: Node


func _shot(name: String) -> void:
	var img := root.get_texture().get_image()
	img.save_png("res://tests/shots/fix5/" + name + ".png")
	print("SHOT: ", name, " ", img.get_size())


func _run() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	_main = packed.instantiate()
	root.add_child(_main)
	await create_timer(1.0).timeout
	var h = _main.get("hunter")
	var boss = _main.get("boss")
	# inside confrontation range: the arena gate auto-starts the fight and
	# the boss stands on boss_idle before his first decision (0.4-1.0 s)
	h.global_position = Vector2(6088, 512)
	h.velocity = Vector2.ZERO
	await create_timer(1.2).timeout  # let the camera settle on the arena
	# then poll for a confrontation-idle window (boss standing on boss_idle)
	var waited := 0.0
	var got := false
	while waited < 20.0:
		await create_timer(0.05).timeout
		waited += 0.05
		if boss.get("state") == "idle":
			await create_timer(0.12).timeout
			print("BOSS STATE AT SHOT: ", boss.get("state"))
			_shot("fix5_boss_standing")
			got = true
			break
	if not got:
		print("BOSS IDLE NOT SEEN in 20 s (last state: ", boss.get("state"), ")")
	await create_timer(0.3).timeout
	print("FIX5 SHOTS DONE")
	quit(0)


func _initialize() -> void:
	_run()
