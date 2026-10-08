extends Node2D
class_name Swooper
## Airborne swooper - basic, 1 HP (GAMEPLAY_RULES S8.2, values [P1 proposal]).
## Cruises 175-190 u over its ground lane; 600 ms telegraphed dive bottoming
## 46-82 u over the lane (inside the standing whip band); 900 ms recovery.
## GREYBOX visuals only. Moved manually (no physics body).

const CRUISE_ALT := 182.0
const CRUISE_SPEED := 120.0
const DIVE_SPEED := 340.0
const TELEGRAPH_TIME := 0.600
const RECOVER_TIME := 0.900
const MAX_HP := 1

var hunter: Hunter
var game: Node

var hp := MAX_HP
var state := "cruise"
var state_t := 0.0
var facing := -1
var ground_y := 512.0 # lane surface this swooper dives over
var patrol_min_x := 0.0
var patrol_max_x := 0.0
var dive_target := Vector2.ZERO
var fall_vy := 0.0
var anim_t := 0.0
var last_hit_id := -1
var home_pos := Vector2.ZERO


func _ready() -> void:
	home_pos = global_position


func _cruise_y() -> float:
	return ground_y - CRUISE_ALT


func _physics_process(delta: float) -> void:
	state_t += delta
	anim_t += delta
	match state:
		"dead":
			fall_vy += 1600.0 * delta
			global_position.y = minf(global_position.y + fall_vy * delta, ground_y - 12.0)
		"cruise":
			global_position.x += facing * CRUISE_SPEED * delta
			global_position.y = move_toward(global_position.y, _cruise_y(), 120.0 * delta)
			if global_position.x <= patrol_min_x:
				facing = 1
			elif global_position.x >= patrol_max_x:
				facing = -1
			if _should_dive():
				_set_state("telegraph")
		"telegraph":
			if state_t >= TELEGRAPH_TIME:
				dive_target = Vector2(hunter.global_position.x, ground_y - 64.0)
				_set_state("dive")
		"dive":
			var to_target := dive_target - global_position
			if to_target.length() < 14.0 or global_position.y >= ground_y - 58.0:
				_set_state("climb")
			else:
				global_position += to_target.normalized() * DIVE_SPEED * delta
				facing = 1 if to_target.x >= 0.0 else -1
		"climb":
			global_position.y = move_toward(global_position.y, _cruise_y(), 230.0 * delta)
			global_position.x += facing * 90.0 * delta
			if global_position.y <= _cruise_y() + 2.0:
				_set_state("recover")
		"recover":
			global_position.x += facing * CRUISE_SPEED * 0.6 * delta
			if state_t >= RECOVER_TIME:
				_set_state("cruise")
		"hurt":
			if state_t >= 0.200:
				_set_state("climb")
	queue_redraw()


func _should_dive() -> bool:
	if hunter == null or hunter.is_dead():
		return false
	if absf(hunter.global_position.x - global_position.x) > 360.0:
		return false
	# hunter below us, near the lane surface (walkway or street under it)
	return hunter.global_position.y > global_position.y + 40.0 and absf(hunter.global_position.y - ground_y) < 220.0


func _set_state(s: String) -> void:
	state = s
	state_t = 0.0


# ------------------------------------------------------------- interfaces

func hurt_rect() -> Rect2:
	if state == "dead":
		return Rect2()
	return Rect2(global_position + Vector2(-28, -20), Vector2(56, 40))


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
		fall_vy = 0.0
		_set_state("dead")
	else:
		_set_state("hurt")


func reset_actor() -> void:
	global_position = home_pos
	hp = MAX_HP
	last_hit_id = -1
	facing = -1
	fall_vy = 0.0
	visible = true
	modulate = Color.WHITE
	_set_state("cruise")


# ---------------------------------------------------------------- visuals

func _draw() -> void:
	var body := Color(0.35, 0.29, 0.48)
	var wing := Color(0.48, 0.41, 0.66)
	if state == "dead":
		draw_colored_polygon(PackedVector2Array([Vector2(-16, 0), Vector2(0, -10), Vector2(16, 0), Vector2(0, 8)]), body.darkened(0.4))
		return
	if state == "telegraph":
		body = Color(0.62, 0.5, 0.85) # brightened tell
		if hunter != null:
			draw_line(Vector2.ZERO, hunter.global_position - global_position, Color(1, 0.4, 0.3, 0.3), 2.0)
		draw_rect(Rect2(-2, -44, 5, 18), Color(1.0, 0.8, 0.3))
		draw_circle(Vector2(0.5, -20), 3.5, Color(1.0, 0.8, 0.3))
	var flap := sin(anim_t * 10.0) * 10.0
	draw_colored_polygon(PackedVector2Array([Vector2(-6, -4), Vector2(-34, -16 - flap), Vector2(-30, 2), Vector2(-8, 4)]), wing)
	draw_colored_polygon(PackedVector2Array([Vector2(6, -4), Vector2(34, -16 - flap), Vector2(30, 2), Vector2(8, 4)]), wing)
	draw_colored_polygon(PackedVector2Array([Vector2(-14, -8), Vector2(0, -14), Vector2(14, -8), Vector2(10, 8), Vector2(-10, 8)]), body)
	draw_circle(Vector2(6 * facing, -8), 4, Color(0.9, 0.85, 0.7))
