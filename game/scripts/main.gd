extends Node2D
## Gothic Whip - full production slice. Builds the STAGE_DESIGN P4 blockout
## as collision + production terrain tiles, wires the actors, routes hazard
## damage, and owns camera / checkpoint / boss-gate / exit / restart flow
## (GAMEPLAY_RULES S7), plus parallax backgrounds, VFX, and audio playback.
## Gameplay numbers are the greybox-verified SPEC values, unchanged.

const GROUND_Y := 512.0 # row 0 top surface
const KILL_Y := 800.0 # stage kill plane (GAMEPLAY_RULES S7)
const STAGE_RIGHT := 6656.0 # 104 modules
const ARENA_LEFT := 5632.0 # module 88
const ARENA_RIGHT := 6528.0 # module 102
const GATE_X := 5632.0 # module 87/88 boundary: entering starts the fight

const SPAWN_POINT := Vector2(160, GROUND_Y)
const CHECKPOINT_POS := Vector2(4128, GROUND_Y) # module 64

# Terrain: [rect, one_way]. Solid blocks are ground masses; thin slabs and
# step treads are one-way surfaces (the spec's zero-thickness surface model:
# recovery routes pass underneath, steps land on top). Every mandatory
# gap <= 112 u, step <= 64 u, landing >= 128 u (STAGE_DESIGN S4).
const TERRAIN: Array = [
	[Rect2(0, 512, 512, 160), false], # B1 spawn ground m0-7
	[Rect2(512, 640, 384, 96), false], # B1 recovery floor m8-13 (row -2)
	[Rect2(576, 512, 320, 12), true], # B1 bridge m9-13
	[Rect2(896, 576, 64, 64), false], # B1 recovery step m14 (row -1)
	[Rect2(960, 512, 320, 160), false], # B1 first-enemy ground m15-19
	[Rect2(1280, 512, 896, 160), false], # B2 patrol court m20-33
	[Rect2(2240, 512, 320, 160), false], # B2 landing m35-39 (m34 is the pit)
	[Rect2(2560, 512, 320, 160), false], # B3 ground m40-44 (under the ascent)
	[Rect2(2624, 448, 128, 12), true], # B3 treads m41-42 (+1)
	[Rect2(2752, 384, 128, 12), true], # B3 treads m43-44 (+2)
	[Rect2(2880, 384, 192, 12), true], # B3 walkway W1 m45-47
	[Rect2(2880, 512, 768, 160), false], # B3 street m45-56 (recovery)
	[Rect2(3136, 384, 256, 12), true], # B3 walkway W2 m49-52
	[Rect2(3520, 448, 64, 12), true], # B3 re-ascent tread m55 (+1)
	[Rect2(3456, 384, 192, 12), true], # B3 walkway W3 m54-56
	[Rect2(3648, 512, 384, 160), false], # B3 descent + ground m57-62
	[Rect2(4032, 512, 1280, 160), false], # B4 ground m63-82
	[Rect2(4480, 448, 64, 12), true], # B4 R1 tread m70 (+1)
	[Rect2(4544, 384, 128, 12), true], # B4 R1 platform m71-72 (+2)
	[Rect2(4672, 448, 64, 12), true], # B4 R1 tread m73 (+1)
	[Rect2(5312, 512, 1344, 160), false], # B5 apron + arena + vestibule m83-103
	[Rect2(-64, -256, 64, 1024), false], # left boundary
	[Rect2(6656, -256, 64, 1024), false], # right boundary
]

var input_state: InputState
var hunter: Hunter
var hud: HUD
var camera: Camera2D
var boss: Boss
var checkpoint: Checkpoint
var exit_door: ExitDoor
var effigy: Effigy

var enemies: Array = []
var _gate_left: CollisionShape2D
var _gate_right: CollisionShape2D

var respawn_point := SPAWN_POINT
var fight_active := false
var boss_defeated := false
var _completed := false
var _rotate_paused := false

var _fx_frames: SpriteFrames
var _sfx: Dictionary = {}
var _sfx_players: Array[AudioStreamPlayer] = []
var _music_players: Array[AudioStreamPlayer] = []

const TILE_TEX := {
	"cap_left": "res://art/terrain/terrain_cap_left.png",
	"cap_mid": "res://art/terrain/terrain_cap_mid.png",
	"cap_right": "res://art/terrain/terrain_cap_right.png",
	"side_left": "res://art/terrain/terrain_side_left.png",
	"side_right": "res://art/terrain/terrain_side_right.png",
	"fill": "res://art/terrain/terrain_fill_center.png",
	"bottom_left": "res://art/terrain/terrain_bottom_left.png",
	"bottom_mid": "res://art/terrain/terrain_bottom_mid.png",
	"bottom_right": "res://art/terrain/terrain_bottom_right.png",
	"inner_left": "res://art/terrain/terrain_inner_left.png",
	"inner_right": "res://art/terrain/terrain_inner_right.png",
	"plat_left": "res://art/terrain/terrain_plat_end_left.png",
	"plat_mid": "res://art/terrain/terrain_plat_mid.png",
	"plat_right": "res://art/terrain/terrain_plat_end_right.png",
}
var _tiles: Dictionary = {}
var _gate_tex: Texture2D


func _ready() -> void:
	input_state = InputState.new()
	add_child(input_state)
	input_state.pause_toggled.connect(toggle_pause)

	_fx_frames = load("res://art/spriteframes/fx_frames.tres")
	for key in TILE_TEX:
		_tiles[key] = load(TILE_TEX[key])
	_gate_tex = load("res://art/props/prop_boss_gate.png")
	_build_parallax()
	_setup_audio()

	_build_terrain()
	_build_gates()

	hunter = Hunter.new()
	hunter.position = SPAWN_POINT
	add_child(hunter)
	hunter.input = input_state
	hunter.game = self

	effigy = Effigy.new()
	effigy.position = Vector2(416, GROUND_Y)
	add_child(effigy)
	effigy.add_to_group("targets")

	_make_pursuer(1120, 1024, 1216) # P1, B1
	_make_pursuer(1568, 1408, 1728) # P2, B2
	_make_pursuer(1952, 1792, 2112) # P3, B2
	_make_pursuer(2400, 2304, 2496) # P4, B2 landing
	_make_pursuer(4384, 4288, 4480) # P5, B4

	_make_swooper(Vector2(3392, 202), 384.0, 3136, 3648) # S1 over W2-W3
	_make_swooper(Vector2(4896, 330), 512.0, 4736, 5056) # S2, B4

	var ranged := RangedThreat.new()
	ranged.position = Vector2(4608, 384)
	add_child(ranged)
	_register_enemy(ranged)

	boss = Boss.new()
	boss.position = Vector2(6240, GROUND_Y) # module 97
	add_child(boss)
	_register_enemy(boss)

	checkpoint = Checkpoint.new()
	checkpoint.position = CHECKPOINT_POS
	add_child(checkpoint)

	exit_door = ExitDoor.new()
	exit_door.position = Vector2(6624, GROUND_Y) # module 103
	add_child(exit_door)

	camera = Camera2D.new()
	camera.position = Vector2(640, 360)
	add_child(camera)
	camera.make_current()

	hud = HUD.new()
	hud.game = self
	hud.input_state = input_state
	add_child(hud)


func _register_enemy(e: Node) -> void:
	e.hunter = hunter
	e.game = self
	e.add_to_group("enemies")
	e.add_to_group("targets")
	enemies.append(e)


func _make_pursuer(x: float, min_x: float, max_x: float) -> void:
	var p := Pursuer.new()
	p.position = Vector2(x, GROUND_Y)
	p.patrol_min_x = min_x
	p.patrol_max_x = max_x
	add_child(p)
	_register_enemy(p)


func _make_swooper(pos: Vector2, lane_y: float, min_x: float, max_x: float) -> void:
	var s := Swooper.new()
	s.position = pos
	s.ground_y = lane_y
	s.patrol_min_x = min_x
	s.patrol_max_x = max_x
	add_child(s)
	_register_enemy(s)


func _build_terrain() -> void:
	var body := StaticBody2D.new()
	body.name = "Terrain"
	body.collision_layer = 1
	body.collision_mask = 0
	add_child(body)
	for entry in TERRAIN:
		var rect: Rect2 = entry[0]
		var shape := CollisionShape2D.new()
		var rs := RectangleShape2D.new()
		rs.size = rect.size
		shape.shape = rs
		shape.position = rect.get_center()
		shape.one_way_collision = bool(entry[1])
		body.add_child(shape)


func _build_gates() -> void:
	var body := StaticBody2D.new()
	body.name = "BossGates"
	body.collision_layer = 1
	body.collision_mask = 0
	add_child(body)
	_gate_left = _make_gate(body, Rect2(5568, 192, 64, 320)) # module 87
	_gate_right = _make_gate(body, Rect2(6528, 192, 64, 320)) # module 102
	_set_gates(false)


func _make_gate(body: StaticBody2D, rect: Rect2) -> CollisionShape2D:
	var shape := CollisionShape2D.new()
	var rs := RectangleShape2D.new()
	rs.size = rect.size
	shape.shape = rs
	shape.position = rect.get_center()
	body.add_child(shape)
	return shape


func _set_gates(closed: bool) -> void:
	_gate_left.set_deferred("disabled", not closed)
	_gate_right.set_deferred("disabled", not closed)
	queue_redraw()


# ------------------------------------------------------------ game flow

func is_completed() -> bool:
	return _completed


func spawn_projectile(pos: Vector2, dir: int) -> void:
	var p := Projectile.new()
	add_child(p)
	p.setup(pos, dir)


func toggle_pause() -> void:
	if _completed:
		return
	var paused := not get_tree().paused
	get_tree().paused = paused
	input_state.clear_all() # pause clears held input (SPEC S4)
	hud.set_pause_visible(paused)


func set_rotate_paused(on: bool) -> void:
	# Portrait rotate prompt pauses the game; rotating back resumes only
	# if this prompt did the pausing.
	if on and not get_tree().paused:
		_rotate_paused = true
		get_tree().paused = true
		input_state.clear_all()
	elif not on and _rotate_paused:
		_rotate_paused = false
		get_tree().paused = false
		input_state.clear_all()


func on_pause_retry() -> void:
	get_tree().paused = false
	hud.set_pause_visible(false)
	restart_encounter(false)


func on_victory_retry() -> void:
	_completed = false
	hud.hide_victory()
	get_tree().paused = false
	restart_encounter(true)


func on_hunter_restart() -> void:
	restart_encounter(false)


func restart_encounter(full: bool) -> void:
	if full:
		checkpoint.reset_prop()
		respawn_point = SPAWN_POINT
	for e in enemies:
		e.reset_actor()
	for p in get_tree().get_nodes_in_group("projectiles"):
		p.queue_free()
	effigy.reset_actor()
	fight_active = false
	boss_defeated = false # a boss-unlocked exit re-locks (SPEC S5)
	_set_gates(false)
	exit_door.set_locked()
	hunter.reset_to(respawn_point)
	input_state.clear_all()


func on_boss_defeated() -> void:
	boss_defeated = true
	fight_active = false
	_set_gates(false)
	exit_door.set_unlocked()
	hud.set_message("THE GATE OPENS")


func _start_fight() -> void:
	fight_active = true
	_set_gates(true)
	boss.start_fight()
	hud.set_message("THE WARDEN WAKES") # greybox label only


func _complete_stage() -> void:
	_completed = true
	input_state.clear_all()
	hud.show_victory()
	get_tree().paused = true


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		# Pause on focus loss + clear held input (SPEC S4/S6).
		input_state.clear_all()
		if not _completed and not get_tree().paused:
			get_tree().paused = true
			hud.set_pause_visible(true)


# ------------------------------------------------------------ per-frame

func _physics_process(_delta: float) -> void:
	if hunter == null or _completed:
		return
	# DEV AID (not a gameplay feature): F9 warps to the boss arena approach
	# for screenshot/testing sessions. See README "Debug aid".
	if Input.is_physical_key_pressed(KEY_F9):
		hunter.global_position = Vector2(5560, GROUND_Y)
		hunter.velocity = Vector2.ZERO
	if hunter.state != "death" and hunter.global_position.y > KILL_Y:
		hunter.start_pit_death()
		return
	if not fight_active and not boss_defeated and hunter.global_position.x >= GATE_X:
		_start_fight()
	if not checkpoint.activated \
			and absf(hunter.global_position.x - CHECKPOINT_POS.x) < 36.0 \
			and absf(hunter.global_position.y - CHECKPOINT_POS.y) < 80.0:
		checkpoint.set_activated()
		respawn_point = CHECKPOINT_POS
		hud.set_message("CHECKPOINT")
		play_sfx("sfx_checkpoint")
		spawn_vfx("vfx_checkpoint_activate", CHECKPOINT_POS + Vector2(0, -6))
	if boss_defeated and hunter.global_position.x >= 6600.0:
		_complete_stage()
		return
	_route_hazards()


func _route_hazards() -> void:
	if hunter.state == "death":
		return
	var hb := hunter.body_rect()
	for e in get_tree().get_nodes_in_group("enemies"):
		if e.contact_active() and hb.intersects(e.contact_rect()):
			hunter.take_damage(e.contact_kind(), e.global_position.x)
			if hunter.state == "death":
				return
	if boss != null and boss.erupting() and hb.intersects(boss.zone_rect()):
		hunter.take_damage("hazard", boss.zone_x)
		return
	for p in get_tree().get_nodes_in_group("projectiles"):
		if p.active and hb.intersects(p.rect()):
			hunter.take_damage("projectile", p.global_position.x)
			p.despawn()
			return


func _process(delta: float) -> void:
	# Camera (SPEC S6): horizontal follow with bounded look-ahead, modest
	# smoothing, vertical lock per zone, hard lock to the arena in the fight.
	var target := Vector2(640, 360)
	if hunter != null:
		if fight_active:
			target = Vector2((ARENA_LEFT + ARENA_RIGHT) * 0.5, 360)
		else:
			var look := hunter.global_position.x + hunter.facing * 90.0
			target.x = clampf(look, 640.0, STAGE_RIGHT - 640.0)
			# walkway zone (STAGE_DESIGN S6): lock a little higher
			target.y = 330.0 if hunter.global_position.x >= 2880.0 and hunter.global_position.x <= 3840.0 else 360.0
	var k := 1.0 - exp(-6.0 * delta)
	camera.position = camera.position.lerp(target, k)


# ------------------------------------------------------- presentation
# Parallax depth stack (ART_BIBLE S2), production terrain tiles, VFX, audio.

func _build_parallax() -> void:
	var back := ParallaxBackground.new()
	back.layer = -100
	back.scroll_ignore_camera_zoom = true
	add_child(back)
	_add_parallax_layer(back, "res://art/bg_sky.png", Vector2.ZERO, Vector2(640, 360), Vector2(1.25, 0.7032), 0.0, true)
	_add_parallax_layer(back, "res://art/bg_distant_silhouette.png", Vector2(0.25, 0.1), Vector2(0, 60), Vector2(0.5714, 0.5714), 1280.0)
	_add_parallax_layer(back, "res://art/bg_midground_arch.png", Vector2(0.55, 0.25), Vector2(0, 20), Vector2(0.6116, 0.75), 1438.0)
	var front := ParallaxBackground.new()
	front.layer = 1
	front.scroll_ignore_camera_zoom = true
	add_child(front)
	_add_parallax_layer(front, "res://art/bg_foreground_frame_rgba.png", Vector2(1.15, 1.0), Vector2(0, -30), Vector2(0.6116, 0.75), 1438.0)


func _add_parallax_layer(pb: ParallaxBackground, tex_path: String, motion: Vector2, offset: Vector2, scl: Vector2, mirror_x: float, centered := false) -> void:
	var layer := ParallaxLayer.new()
	layer.motion_scale = motion
	if mirror_x > 0.0:
		layer.motion_mirroring = Vector2(mirror_x, 0)
	var spr := Sprite2D.new()
	spr.texture = load(tex_path)
	spr.centered = centered
	spr.position = offset
	spr.scale = scl
	layer.add_child(spr)
	pb.add_child(layer)


func spawn_vfx(clip: String, world_pos: Vector2) -> void:
	if _fx_frames == null:
		return
	var v := VfxPlayer.new()
	add_child(v)
	v.setup(_fx_frames, clip, world_pos)


func _setup_audio() -> void:
	for name in ["sfx_whip_swing", "sfx_whip_hit", "sfx_jump", "sfx_land",
			"sfx_hurt", "sfx_death", "sfx_enemy_tell", "sfx_checkpoint", "sfx_boss_tell"]:
		_sfx[name] = load("res://art/audio/%s.wav" % name)
	for i in 10:
		var pl := AudioStreamPlayer.new()
		pl.bus = "SFX"
		add_child(pl)
		_sfx_players.append(pl)
	for name in ["mus_ambience_loop", "mus_stage_loop"]:
		var pl := AudioStreamPlayer.new()
		pl.stream = load("res://art/audio/%s.wav" % name)
		pl.bus = "Music"
		pl.volume_db = -16.0 if name == "mus_stage_loop" else -20.0
		add_child(pl)
		_music_players.append(pl)
		pl.play()


func play_sfx(name: String, pitch := 1.0) -> void:
	var stream: AudioStream = _sfx.get(name)
	if stream == null:
		return
	for pl in _sfx_players:
		if not pl.playing:
			pl.stream = stream
			pl.pitch_scale = pitch
			pl.play()
			return


func _draw() -> void:
	# Production terrain: the 14-tile masonry kit (128 px source = 64 u).
	for entry in TERRAIN:
		_draw_terrain_rect(entry[0], bool(entry[1]))
	# Boss gates: prop art at the arena edges, solid only during the fight.
	if _gate_tex != null:
		var tint := Color(1, 1, 1, 0.95) if fight_active else Color(1, 1, 1, 0.25)
		draw_texture_rect_region(_gate_tex, Rect2(5568, 352, 64, 160), Rect2(0, 0, 128, 320), tint)
		draw_texture_rect_region(_gate_tex, Rect2(6528, 352, 64, 160), Rect2(0, 0, 128, 320), tint)


func _draw_terrain_rect(rect: Rect2, one_way: bool) -> void:
	var cols := int(ceil(rect.size.x / 64.0))
	var rows := int(ceil(rect.size.y / 64.0))
	for cx in cols:
		for cy in rows:
			var w := minf(64.0, rect.size.x - cx * 64.0)
			var h := minf(64.0, rect.size.y - cy * 64.0)
			var cell := Rect2(rect.position + Vector2(cx * 64.0, cy * 64.0), Vector2(w, h))
			var key := "fill"
			if cy == 0:
				if one_way:
					key = "plat_left" if cx == 0 else ("plat_right" if cx == cols - 1 else "plat_mid")
					if cols == 1:
						key = "plat_mid"
				else:
					key = "cap_left" if cx == 0 else ("cap_right" if cx == cols - 1 else "cap_mid")
					if cols == 1:
						key = "cap_mid"
			elif cy == rows - 1 and not one_way:
				key = "bottom_left" if cx == 0 else ("bottom_right" if cx == cols - 1 else "bottom_mid")
				if cols == 1:
					key = "bottom_mid"
			elif cx == 0:
				key = "side_left"
			elif cx == cols - 1:
				key = "side_right"
			var tex: Texture2D = _tiles.get(key)
			if tex != null:
				draw_texture_rect_region(tex, cell, Rect2(0, 0, w * 2.0, h * 2.0))
