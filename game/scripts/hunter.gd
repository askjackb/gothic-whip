extends CharacterBody2D
class_name Hunter
## The hunter. Origin at the foot pivot (ASSET_SPEC S2). Implements the
## GAMEPLAY_RULES S4 state table, S2 interruption priority, S5 damage rules,
## S6 crouch-clearance cases. All constants from GAMEPLAY_RULES S1 / SPEC S4-S5.
## GREYBOX: visuals are flat-color polygons drawn in _draw(); the logical
## state machine is what the future animation clips will observe.

# --- spec constants (GAMEPLAY_RULES S1) ---
const SPEED := 240.0
const GRAVITY := 1600.0
const JUMP_VELOCITY := -640.0
const COYOTE_TIME := 0.100
const BUFFER_TIME := 0.100
const AIR_ACCEL := 600.0 # [P1 proposal]
const WHIP_ANTICIPATION := 0.150
const WHIP_ACTIVE_END := 0.250
const WHIP_TOTAL := 0.500
const MAX_HP := 5
const INVULN_TIME := 1.0
const KNOCKBACK_SPEED := 160.0 # [P1 proposal] ~48 u over the clip
const KNOCKBACK_TIME := 0.300
const HURT_RECOIL_TIME := 0.200
const KNOCKDOWN_TIME := 0.360
const GET_UP_TIME := 0.450
const LAND_TIME := 0.160
const TURN_TIME := 0.150
const CROUCH_ENTER_TIME := 0.200
const CROUCH_EXIT_TIME := 0.200
const TAKEOFF_TIME := 0.120

const STAND_SIZE := Vector2(40, 104)
const STAND_CENTER := Vector2(0, -52)
const CROUCH_SIZE := Vector2(40, 60)
const CROUCH_CENTER := Vector2(0, -30)

const ATTACK_STATES: Array[String] = ["attack_ground", "attack_air", "attack_crouch"]
const AIR_STATES: Array[String] = ["jump_takeoff", "jump_rise", "jump_apex", "fall", "attack_air"]
const LEDGE_STATES: Array[String] = [
	"idle", "start_move", "walk", "stop_move", "turn", "land",
	"crouch_enter", "crouch_idle", "hurt_recoil", "knockdown", "get_up",
]

var input: InputState
var game: Node # Main (restart callbacks)

var hp := MAX_HP
var state := "idle"
var state_t := 0.0
var facing := 1
var grounded := false

var invuln_t := 0.0
var time_since_grounded := 99.0
var jump_buffer := 0.0

var attack_t := 0.0
var attack_id := 0
var knockback_dir := 1
var knockdown_pending := false
var turn_from := 1
var _turn_flipped := false
var air_from_jump := false
var crouched_body := false

var death_t := 0.0
var death_in_pit := false
var death_reported := false

var _stand_shape: CollisionShape2D
var _crouch_shape: CollisionShape2D
var _clearance_shape: RectangleShape2D


func _ready() -> void:
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 6.0
	_stand_shape = CollisionShape2D.new()
	var rs := RectangleShape2D.new()
	rs.size = STAND_SIZE
	_stand_shape.shape = rs
	_stand_shape.position = STAND_CENTER
	add_child(_stand_shape)
	_crouch_shape = CollisionShape2D.new()
	var cs := RectangleShape2D.new()
	cs.size = CROUCH_SIZE
	_crouch_shape.shape = cs
	_crouch_shape.position = CROUCH_CENTER
	_crouch_shape.disabled = true
	add_child(_crouch_shape)
	_clearance_shape = RectangleShape2D.new()
	_clearance_shape.size = Vector2(36, 100)


# ---------------------------------------------------------------- queries

func is_dead() -> bool:
	return state == "death"


func body_rect() -> Rect2:
	if crouched_body:
		return Rect2(global_position + Vector2(-20, -60), Vector2(40, 60))
	return Rect2(global_position + Vector2(-20, -104), Vector2(40, 104))


func _whip_rect_local() -> Rect2:
	var top := -82.0
	var height := 36.0
	if state == "attack_crouch":
		top = -48.0
		height = 28.0
	var x := 40.0 if facing > 0 else -168.0
	return Rect2(Vector2(x, top), Vector2(128, height))


func whip_rect() -> Rect2:
	var r := _whip_rect_local()
	r.position += global_position
	return r


func is_whip_active() -> bool:
	return state in ATTACK_STATES and attack_t >= WHIP_ANTICIPATION and attack_t < WHIP_ACTIVE_END


func get_state() -> String:
	return state


# ---------------------------------------------------------------- helpers

func _change_state(s: String) -> void:
	if s != state:
		state = s
		state_t = 0.0


func set_crouched_body(on: bool) -> void:
	crouched_body = on
	_stand_shape.set_deferred("disabled", on)
	_crouch_shape.set_deferred("disabled", not on)


func _input_dir() -> int:
	if input == null:
		return 0
	var l := input.is_held("move_left")
	var r := input.is_held("move_right")
	if l and not r:
		return -1
	if r and not l:
		return 1
	return 0 # opposing inputs resolve to neutral (SPEC S4)


func _crouch_held() -> bool:
	return input != null and input.is_held("crouch")


func _has_standing_clearance() -> bool:
	var query := PhysicsShapeQueryParameters2D.new()
	query.shape = _clearance_shape
	query.transform = Transform2D(0.0, global_position + Vector2(0, -54))
	query.collision_mask = 1
	query.exclude = [get_rid()]
	return get_world_2d().direct_space_state.intersect_shape(query).is_empty()


func _try_jump() -> bool:
	if jump_buffer > 0.0 and (grounded or time_since_grounded <= COYOTE_TIME):
		jump_buffer = 0.0
		velocity.y = JUMP_VELOCITY
		air_from_jump = true
		_change_state("jump_takeoff")
		return true
	return false


func _try_crouch_jump() -> bool:
	# GAMEPLAY_RULES S6 case 3: jump from crouch only with standing clearance.
	if jump_buffer > 0.0 and grounded and _has_standing_clearance():
		set_crouched_body(false)
		return _try_jump()
	return false


func _start_attack(kind_state: String) -> void:
	attack_id += 1
	attack_t = 0.0
	_change_state(kind_state)


func _air_region_state() -> String:
	if velocity.y < -160.0:
		return "jump_rise"
	if velocity.y <= 160.0:
		return "jump_apex" if air_from_jump else "fall"
	return "fall"


func _to_ground_rest(dir: int) -> void:
	if _crouch_held():
		_change_state("crouch_idle" if crouched_body else "crouch_enter")
	elif crouched_body:
		_change_state("crouch_exit" if _has_standing_clearance() else "crouch_idle")
	elif dir != 0:
		facing = dir
		_change_state("start_move")
	else:
		_change_state("idle")


# ---------------------------------------------------------------- damage

## kind: "projectile" (non-displacing), "contact"/"hazard" (displacing),
## "heavy" (knockdown). Routing per GAMEPLAY_RULES S5.
func take_damage(kind: String, source_x: float) -> void:
	if state == "death" or invuln_t > 0.0:
		return
	if game != null and game.has_method("is_completed") and game.is_completed():
		return
	hp -= 1
	invuln_t = INVULN_TIME
	attack_t = 0.0 # damage cancels any attack; hitbox dies this step (SPEC S4)
	if hp <= 0:
		death_in_pit = false
		death_t = 0.0
		_change_state("death")
		return
	var dir_away := -facing
	if global_position.x < source_x:
		dir_away = -1
	elif global_position.x > source_x:
		dir_away = 1
	if kind == "heavy":
		if grounded:
			_change_state("knockdown")
		else:
			knockdown_pending = true
			knockback_dir = dir_away
			_change_state("knockback")
	elif kind == "projectile" and grounded:
		_change_state("hurt_recoil")
	else:
		knockback_dir = dir_away
		_change_state("knockback")


func start_pit_death() -> void:
	if state == "death":
		return
	attack_t = 0.0
	death_in_pit = true
	death_t = 0.0
	_change_state("death")


func reset_to(pos: Vector2) -> void:
	global_position = pos
	velocity = Vector2.ZERO
	hp = MAX_HP
	invuln_t = 0.0
	jump_buffer = 0.0
	attack_t = 0.0
	knockdown_pending = false
	facing = 1
	grounded = false
	time_since_grounded = 99.0
	death_in_pit = false
	death_reported = false
	death_t = 0.0
	set_crouched_body(false)
	_change_state("idle")
	state_t = 0.0


# ---------------------------------------------------------------- physics

func _physics_process(delta: float) -> void:
	state_t += delta
	if state in ATTACK_STATES:
		attack_t += delta
	if invuln_t > 0.0:
		invuln_t = maxf(0.0, invuln_t - delta)
	if jump_buffer > 0.0:
		jump_buffer = maxf(0.0, jump_buffer - delta)
	time_since_grounded += delta

	var whip_pressed := false
	if input != null:
		if input.consume_pressed("jump"):
			jump_buffer = BUFFER_TIME
		whip_pressed = input.consume_pressed("whip")

	var dir := _input_dir()
	_state_logic(delta, dir, whip_pressed)

	if not grounded:
		velocity.y += GRAVITY * delta
	elif velocity.y > 0.0:
		velocity.y = 0.0

	move_and_slide()
	_post_move(delta)

	if is_whip_active():
		_apply_whip_hits()
	_update_visual_state()
	queue_redraw()


func _state_logic(delta: float, dir: int, whip_pressed: bool) -> void:
	match state:
		"idle", "start_move", "walk", "stop_move", "land":
			_ground_locomotion(delta, dir, whip_pressed)
		"turn":
			if state_t >= TURN_TIME * 0.5 and not _turn_flipped:
				_turn_flipped = true
				facing = -turn_from
			velocity.x = turn_from * SPEED if state_t < TURN_TIME * 0.5 else facing * SPEED
			if whip_pressed:
				_start_attack("attack_ground")
			elif _try_jump():
				pass
			elif state_t >= TURN_TIME:
				_change_state("walk" if dir != 0 else "idle")
		"crouch_enter":
			velocity.x = 0.0
			if whip_pressed:
				_start_attack("attack_crouch")
			elif _try_crouch_jump():
				pass
			elif not _crouch_held():
				_change_state("crouch_exit" if _has_standing_clearance() else "crouch_idle")
			elif state_t >= CROUCH_ENTER_TIME:
				_change_state("crouch_idle")
		"crouch_idle":
			velocity.x = 0.0
			if whip_pressed:
				_start_attack("attack_crouch")
			elif _try_crouch_jump():
				pass
			elif not _crouch_held() and _has_standing_clearance():
				_change_state("crouch_exit")
		"crouch_exit":
			velocity.x = 0.0
			if state_t >= CROUCH_EXIT_TIME:
				set_crouched_body(false)
				if dir != 0:
					facing = dir
					_change_state("start_move")
				else:
					_change_state("idle")
		"jump_takeoff", "jump_rise", "jump_apex", "fall":
			_air_control(delta, dir)
			if whip_pressed:
				_start_attack("attack_air")
			elif state == "jump_takeoff":
				if state_t >= TAKEOFF_TIME:
					_change_state(_air_region_state())
			else:
				_change_state(_air_region_state())
		"attack_ground", "attack_crouch":
			velocity.x = 0.0 # grounded strikes stop horizontal movement (SPEC S4)
			if attack_t >= WHIP_TOTAL:
				_end_attack_ground(dir)
		"attack_air":
			_air_control(delta, dir) # trajectory preserved; no extra jump height
			if attack_t >= WHIP_TOTAL:
				_change_state(_air_region_state())
		"hurt_recoil":
			velocity.x = 0.0
			if state_t >= HURT_RECOIL_TIME:
				_to_ground_rest(dir)
		"knockback":
			velocity.x = knockback_dir * KNOCKBACK_SPEED
			if state_t >= KNOCKBACK_TIME:
				if grounded:
					_to_ground_rest(dir)
				else:
					air_from_jump = false
					_change_state("fall")
		"knockdown":
			velocity.x = move_toward(velocity.x, 0.0, 900.0 * delta)
			if state_t >= KNOCKDOWN_TIME:
				_change_state("get_up")
		"get_up":
			velocity.x = 0.0
			if state_t >= GET_UP_TIME:
				_to_ground_rest(dir)
		"death":
			velocity.x = move_toward(velocity.x, 0.0, 900.0 * delta)


func _ground_locomotion(_delta: float, dir: int, whip_pressed: bool) -> void:
	if whip_pressed:
		_start_attack("attack_ground")
		return
	if _try_jump():
		return
	if state == "land":
		if _crouch_held():
			velocity.x = move_toward(velocity.x, 0.0, 2400.0 * _delta)
			if state_t >= LAND_TIME:
				_change_state("crouch_enter")
		elif dir != 0:
			facing = dir
			velocity.x = dir * SPEED
			_change_state("start_move")
		else:
			velocity.x = move_toward(velocity.x, 0.0, 2400.0 * _delta)
			if state_t >= LAND_TIME:
				_change_state("idle")
		return
	if _crouch_held():
		velocity.x = 0.0
		_change_state("crouch_enter")
		return
	if dir != 0:
		if state == "walk" and dir != facing:
			turn_from = facing
			_turn_flipped = false
			_change_state("turn")
			velocity.x = turn_from * SPEED
			return
		facing = dir
		velocity.x = dir * SPEED
		if state == "idle" or state == "stop_move":
			_change_state("start_move")
		elif state == "start_move" and state_t >= 0.150:
			_change_state("walk")
	else:
		velocity.x = move_toward(velocity.x, 0.0, 2400.0 * _delta)
		if state == "walk" or state == "start_move":
			_change_state("stop_move")
		elif state == "stop_move" and state_t >= 0.150:
			_change_state("idle")
		elif state == "idle":
			velocity.x = 0.0


func _air_control(delta: float, dir: int) -> void:
	# Limited air correction [P1 proposal]: 600 u/s^2 toward input x top speed.
	velocity.x = move_toward(velocity.x, dir * SPEED, AIR_ACCEL * delta)


func _end_attack_ground(dir: int) -> void:
	if state == "attack_crouch":
		if _crouch_held():
			_change_state("crouch_idle")
		elif _has_standing_clearance():
			_change_state("crouch_exit")
		else:
			_change_state("crouch_idle")
	elif dir != 0 and dir != facing:
		turn_from = facing
		_turn_flipped = false
		_change_state("turn")
	elif dir != 0:
		_change_state("walk")
	else:
		_change_state("idle")


func _post_move(delta: float) -> void:
	var was_grounded := grounded
	grounded = is_on_floor()
	if grounded:
		time_since_grounded = 0.0
		if velocity.y > 0.0:
			velocity.y = 0.0
	if is_on_ceiling() and velocity.y < 0.0:
		velocity.y = 0.0

	if grounded and not was_grounded:
		if state == "attack_air":
			# Landing continues the same attack: elapsed time and hit ID carry
			# over, only the grounded pose changes (GAMEPLAY_RULES S2).
			if _crouch_held():
				set_crouched_body(true)
				_change_state("attack_crouch")
			else:
				_change_state("attack_ground")
			velocity.x = 0.0
		elif state == "knockback" and knockdown_pending:
			knockdown_pending = false
			_change_state("knockdown")
		elif state in AIR_STATES:
			_change_state("land")

	if not grounded and was_grounded and velocity.y >= 0.0 and state in LEDGE_STATES:
		air_from_jump = false
		_change_state("fall")

	if state == "death":
		if death_in_pit or grounded:
			death_t += delta
			var limit := 0.9 if death_in_pit else 1.3
			if death_t >= limit and not death_reported:
				death_reported = true
				if game != null and game.has_method("on_hunter_restart"):
					game.on_hunter_restart()


func _apply_whip_hits() -> void:
	var rect := whip_rect()
	for t in get_tree().get_nodes_in_group("targets"):
		if t.has_method("hurt_rect") and t.has_method("apply_whip_hit"):
			var hr: Rect2 = t.hurt_rect()
			if hr.size != Vector2.ZERO and rect.intersects(hr):
				t.apply_whip_hit(attack_id, global_position.x)


# ---------------------------------------------------------------- visuals
# GREYBOX ONLY: flat-color polygons. These are NOT animation frames; the
# state machine above is the deliverable the animation contract observes.

func _update_visual_state() -> void:
	if state == "death":
		modulate = Color(0.55, 0.55, 0.6)
	elif state in ["hurt_recoil", "knockback", "knockdown"]:
		modulate = Color(1.0, 0.55, 0.5)
	elif invuln_t > 0.0:
		modulate = Color(1, 1, 1, 0.55) # non-strobing tint (SPEC S5)
	else:
		modulate = Color.WHITE


func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(facing, 1))
	var slate := Color(0.29, 0.35, 0.42)
	var dark := Color(0.16, 0.19, 0.24)
	var skin := Color(0.85, 0.74, 0.6)
	var hair := Color(0.4, 0.27, 0.15)
	var ochre := Color(0.72, 0.56, 0.34)
	if state == "death":
		draw_rect(Rect2(-42, -14, 84, 14), slate)
		draw_circle(Vector2(38, -8), 8, skin)
		return
	if crouched_body:
		draw_rect(Rect2(-16, -26, 32, 26), dark) # folded legs
		draw_rect(Rect2(-17, -56, 34, 32), slate) # torso
		draw_rect(Rect2(-17, -34, 34, 5), ochre) # belt
		draw_circle(Vector2(5, -62), 8, hair)
		draw_circle(Vector2(7, -60), 7, skin)
	else:
		var airborne := state in AIR_STATES
		if airborne:
			draw_rect(Rect2(-13, -36, 26, 36), dark) # tucked legs
		else:
			draw_rect(Rect2(-13, -46, 10, 46), dark)
			draw_rect(Rect2(3, -46, 10, 46), dark)
		draw_rect(Rect2(-16, -88, 32, 46), slate)
		draw_rect(Rect2(-16, -52, 32, 6), ochre)
		draw_circle(Vector2(2, -101), 9, hair)
		draw_circle(Vector2(4, -98), 8, skin)
		draw_rect(Rect2(10, -80, 16, 7), slate) # whip arm
	if state in ATTACK_STATES:
		var hand := Vector2(16, -42) if state == "attack_crouch" else Vector2(16, -70)
		var tip_x := 46.0
		if attack_t < WHIP_ANTICIPATION:
			tip_x = 46.0 + 30.0 * (attack_t / WHIP_ANTICIPATION)
		elif attack_t < WHIP_ACTIVE_END:
			tip_x = 168.0
		else:
			tip_x = 168.0 - 100.0 * ((attack_t - WHIP_ACTIVE_END) / (WHIP_TOTAL - WHIP_ACTIVE_END))
		var mid := Vector2(hand.x + (tip_x - hand.x) * 0.5, hand.y - 7)
		var tip := Vector2(tip_x, hand.y + 5)
		draw_polyline(PackedVector2Array([hand, mid, tip]), Color(0.88, 0.82, 0.7), 4.0)
		if is_whip_active():
			draw_rect(_whip_rect_local(), Color(1.0, 0.85, 0.5, 0.15))
