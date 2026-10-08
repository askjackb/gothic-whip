extends CharacterBody2D
class_name Pursuer
## Ground pursuer - basic, 1 HP (GAMEPLAY_RULES S8.1, all values [P1 proposal]).
## Patrol 60 u/s; alert 300 ms; approach 100 u/s; wind-up 350 ms inside
## 120 u; lunge 260 u/s; recovery 600 ms. Contact is a displacing hit.
## GREYBOX visuals only.

const GRAVITY := 1600.0
const PATROL_SPEED := 60.0
const CHASE_SPEED := 100.0
const LUNGE_SPEED := 260.0
const DETECT_RANGE := 400.0
const KEEP_RANGE := 520.0
const LUNGE_TRIGGER := 120.0
const MAX_HP := 1

var hunter: Hunter
var game: Node

var hp := MAX_HP
var state := "patrol"
var state_t := 0.0
var facing := -1
var patrol_min_x := 0.0
var patrol_max_x := 0.0
var lunge_dir := -1
var last_hit_id := -1
var home_pos := Vector2.ZERO


func _ready() -> void:
	collision_layer = 4
	collision_mask = 1
	floor_snap_length = 6.0
	var shape := CollisionShape2D.new()
	var rs := RectangleShape2D.new()
	rs.size = Vector2(52, 56)
	shape.shape = rs
	shape.position = Vector2(0, -28)
	add_child(shape)
	home_pos = global_position


func _same_level() -> bool:
	return hunter != null and absf(hunter.global_position.y - global_position.y) < 40.0


func _dist_x() -> float:
	return absf(hunter.global_position.x - global_position.x) if hunter != null else 99999.0


func _can_see(range_: float) -> bool:
	return hunter != null and not hunter.is_dead() and _same_level() and _dist_x() <= range_


func _physics_process(delta: float) -> void:
	state_t += delta
	if state == "dead":
		velocity.x = 0.0
		if not is_on_floor():
			velocity.y += GRAVITY * delta
		move_and_slide()
		queue_redraw()
		return

	match state:
		"patrol":
			velocity.x = facing * PATROL_SPEED
			if global_position.x <= patrol_min_x:
				facing = 1
			elif global_position.x >= patrol_max_x:
				facing = -1
			if _can_see(DETECT_RANGE):
				_set_state("alert")
		"alert":
			velocity.x = 0.0
			if state_t >= 0.300:
				_set_state("chase")
		"chase":
			if not _can_see(KEEP_RANGE):
				_set_state("patrol")
			else:
				facing = 1 if hunter.global_position.x > global_position.x else -1
				velocity.x = facing * CHASE_SPEED
				if _dist_x() <= LUNGE_TRIGGER:
					_set_state("windup")
		"windup":
			velocity.x = 0.0
			if state_t >= 0.350:
				lunge_dir = facing
				_set_state("lunge")
		"lunge":
			velocity.x = lunge_dir * LUNGE_SPEED
			if state_t >= 0.450:
				_set_state("recover")
		"recover":
			velocity.x = 0.0
			if state_t >= 0.600:
				_set_state("chase" if _can_see(KEEP_RANGE) else "patrol")
		"hurt":
			velocity.x = 0.0
			if state_t >= 0.200:
				_set_state("chase" if _can_see(KEEP_RANGE) else "patrol")

	if not is_on_floor():
		velocity.y += GRAVITY * delta
	elif velocity.y > 0.0:
		velocity.y = 0.0
	move_and_slide()
	queue_redraw()


func _set_state(s: String) -> void:
	state = s
	state_t = 0.0


# ------------------------------------------------------------- interfaces

func hurt_rect() -> Rect2:
	if state == "dead":
		return Rect2()
	return Rect2(global_position + Vector2(-26, -56), Vector2(52, 56))


func contact_rect() -> Rect2:
	return hurt_rect()


func contact_active() -> bool:
	return state != "dead"


func contact_kind() -> String:
	return "contact"


func apply_whip_hit(attack_id_: int, _from_x: float) -> void:
	if state == "dead" or attack_id_ == last_hit_id:
		return
	last_hit_id = attack_id_
	hp -= 1
	if hp <= 0:
		_set_state("dead")
	else:
		_set_state("hurt") # interrupts anticipation (GAMEPLAY_RULES S5)


func reset_actor() -> void:
	global_position = home_pos
	velocity = Vector2.ZERO
	hp = MAX_HP
	last_hit_id = -1
	facing = -1
	visible = true
	modulate = Color.WHITE
	_set_state("patrol")


# ---------------------------------------------------------------- visuals

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(facing, 1))
	var body := Color(0.54, 0.23, 0.18)
	var belly := Color(0.79, 0.44, 0.29)
	if state == "dead":
		draw_rect(Rect2(-28, -12, 56, 12), body.darkened(0.4))
		return
	var crouch := 5.0 if state in ["windup", "alert"] else 0.0
	draw_rect(Rect2(-26, -14 + crouch, 7, 14), body.darkened(0.25))
	draw_rect(Rect2(-9, -14 + crouch, 7, 14), body.darkened(0.25))
	draw_rect(Rect2(6, -14 + crouch, 7, 14), body.darkened(0.25))
	draw_rect(Rect2(20, -14 + crouch, 7, 14), body.darkened(0.25))
	draw_rect(Rect2(-28, -46 + crouch, 56, 32), body)
	draw_rect(Rect2(-20, -30 + crouch, 40, 14), belly)
	draw_rect(Rect2(18, -50 + crouch, 22, 24), body) # head
	draw_rect(Rect2(34, -36 + crouch, 10, 6), belly) # snout
	draw_colored_polygon(PackedVector2Array([Vector2(-14, -46 + crouch), Vector2(-8, -58 + crouch), Vector2(-2, -46 + crouch)]), belly)
	draw_colored_polygon(PackedVector2Array([Vector2(0, -46 + crouch), Vector2(6, -58 + crouch), Vector2(12, -46 + crouch)]), belly)
	if state in ["alert", "windup"]:
		# geometric telegraph: readable tell, never a static substitute
		draw_rect(Rect2(-2, -86 + crouch, 5, 18), Color(1.0, 0.8, 0.3))
		draw_circle(Vector2(0.5, -62 + crouch), 3.5, Color(1.0, 0.8, 0.3))
