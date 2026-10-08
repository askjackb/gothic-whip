extends Node2D
class_name Swooper
## Airborne swooper - basic, 1 HP (GAMEPLAY_RULES S8.2, values [P1 proposal]).
## Cruises 175-190 u over its ground lane; 600 ms telegraphed dive bottoming
## 46-82 u over the lane (inside the standing whip band); 900 ms recovery.
## Visuals: production frames (style_lock_r01) via Anim. Moved manually.

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

var _visual: Node2D
var _body: AnimatedSprite2D
var _vis_clip := ""
var _vis_t := 0.0

const STATE_TO_CLIP := {
	"cruise": "swooper_cruise", "telegraph": "swooper_dive_telegraph",
	"dive": "swooper_dive", "climb": "swooper_recovery_climb",
	"recover": "swooper_cruise", "hurt": "swooper_hurt",
	"dead": "swooper_death_fall",
}


func _ready() -> void:
	home_pos = global_position
	_visual = Node2D.new()
	add_child(_visual)
	_body = Anim.make_sprite(load("res://art/spriteframes/enemy_frames.tres"), "swooper_cruise")
	_visual.add_child(_body)


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
	_update_visuals(delta)


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
	if s == "telegraph" and game != null and game.has_method("play_sfx"):
		game.play_sfx("sfx_enemy_tell", 1.2)


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
		if game != null and game.has_method("spawn_vfx"):
			game.spawn_vfx("vfx_enemy_defeat", global_position)
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

func _update_visuals(delta: float) -> void:
	if _body == null:
		return
	_visual.scale.x = facing
	var clip: String = STATE_TO_CLIP.get(state, "swooper_cruise")
	if clip != _vis_clip:
		_vis_clip = clip
		_vis_t = 0.0
	else:
		_vis_t += delta
	Anim.apply(_body, clip, _vis_t)
