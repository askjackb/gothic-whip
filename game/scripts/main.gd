extends Node2D
## Gothic Whip - greybox slice (game gate 2). Builds the STAGE_DESIGN P4
## blockout as collision + flat-color greybox terrain, wires the actors,
## routes hazard damage, and owns camera / checkpoint / boss-gate / exit /
## restart flow (GAMEPLAY_RULES S7). No production art anywhere in here.

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


func _ready() -> void:
	input_state = InputState.new()
	add_child(input_state)
	input_state.pause_toggled.connect(toggle_pause)

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


# ------------------------------------------------------------ greybox art
# Flat-color terrain + distant silhouettes. NOT production art.

func _draw() -> void:
	draw_rect(Rect2(-200, -400, STAGE_RIGHT + 400, 1250), Color(0.07, 0.07, 0.11))
	# distant gothic silhouettes (flat)
	var sil := Color(0.1, 0.1, 0.15)
	for i in range(0, int(STAGE_RIGHT), 640):
		draw_rect(Rect2(i + 60, 180, 90, 332), sil)
		draw_colored_polygon(PackedVector2Array([
			Vector2(i + 55, 180), Vector2(i + 105, 110), Vector2(i + 155, 180)]), sil)
	var top_edge := Color(0.42, 0.45, 0.52)
	var fill := Color(0.2, 0.21, 0.26)
	for entry in TERRAIN:
		var rect: Rect2 = entry[0]
		draw_rect(rect, fill)
		draw_rect(Rect2(rect.position, Vector2(rect.size.x, 5)), top_edge)
	if fight_active:
		var bar := Color(0.5, 0.52, 0.58)
		draw_rect(Rect2(5568, 192, 64, 320), Color(0.16, 0.16, 0.2))
		draw_rect(Rect2(6528, 192, 64, 320), Color(0.16, 0.16, 0.2))
		for x in [5584.0, 5608.0, 6544.0, 6568.0]:
			draw_rect(Rect2(x, 192, 7, 320), bar)
