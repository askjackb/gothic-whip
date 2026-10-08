extends Node2D
class_name RangedThreat
## Stationary ranged threat - 2 HP (GAMEPLAY_RULES S8.3, values [P1 proposal]).
## Rooted: 900 ms tracked aim with visible charge cue, one projectile,
## 700 ms recovery. Projectile hits are non-displacing (hurt_recoil);
## body contact is displacing. Stationary is not static: idle sways, aim
## tracks, hurt interrupts aim. GREYBOX visuals only.

const AIM_TIME := 0.900
const RECOVER_TIME := 0.700
const HURT_TIME := 0.200
const RANGE_X := 720.0
const MAX_HP := 2

var hunter: Hunter
var game: Node

var hp := MAX_HP
var state := "idle"
var state_t := 0.0
var aim_t := 0.0
var facing := -1
var last_hit_id := -1
var home_pos := Vector2.ZERO


func _ready() -> void:
	home_pos = global_position


func _in_range() -> bool:
	if hunter == null or hunter.is_dead():
		return false
	return absf(hunter.global_position.x - global_position.x) <= RANGE_X \
		and hunter.global_position.y > global_position.y - 320.0


func _physics_process(delta: float) -> void:
	state_t += delta
	if state == "dead":
		return
	# face the hunter while it can be engaged
	if hunter != null and _in_range():
		facing = 1 if hunter.global_position.x > global_position.x else -1
	match state:
		"idle":
			aim_t = 0.0
			if _in_range():
				_set_state("aim")
		"aim":
			if not _in_range():
				_set_state("idle")
			else:
				aim_t += delta
				if aim_t >= AIM_TIME:
					_fire()
					_set_state("recover")
		"recover":
			if state_t >= RECOVER_TIME:
				aim_t = 0.0
				_set_state("aim" if _in_range() else "idle")
		"hurt":
			if state_t >= HURT_TIME:
				aim_t = 0.0
				_set_state("aim" if _in_range() else "idle")
	queue_redraw()


func _fire() -> void:
	if game != null and game.has_method("spawn_projectile"):
		# Band y -70..-95 relative to this actor's own ground surface
		# (GAMEPLAY_RULES S8.3); from the B4 ground route it passes overhead.
		game.spawn_projectile(global_position + Vector2(facing * 30, -82), facing)


func _set_state(s: String) -> void:
	state = s
	state_t = 0.0


# ------------------------------------------------------------- interfaces

func hurt_rect() -> Rect2:
	if state == "dead":
		return Rect2()
	return Rect2(global_position + Vector2(-20, -64), Vector2(40, 64))


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
		aim_t = 0.0
		_set_state("hurt") # interrupts aim (GAMEPLAY_RULES S5)


func reset_actor() -> void:
	global_position = home_pos
	hp = MAX_HP
	last_hit_id = -1
	aim_t = 0.0
	facing = -1
	visible = true
	modulate = Color.WHITE
	_set_state("idle")


# ---------------------------------------------------------------- visuals

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(facing, 1))
	var teal := Color(0.25, 0.42, 0.37)
	var bone := Color(0.85, 0.78, 0.66)
	if state == "dead":
		draw_rect(Rect2(-20, -10, 40, 10), teal.darkened(0.4))
		draw_circle(Vector2(10, -6), 9, teal.darkened(0.4))
		return
	draw_rect(Rect2(-20, -14, 40, 14), Color(0.3, 0.3, 0.33)) # rooted base
	draw_rect(Rect2(-7, -50, 14, 36), teal) # pillar
	draw_circle(Vector2(0, -58), 12, teal) # turret head
	draw_rect(Rect2(6, -62, 26, 7), teal.darkened(0.15)) # barrel
	draw_circle(Vector2(2, -58), 4, bone) # eye lens
	if state == "aim":
		var charge := 3.0 + 8.0 * clampf(aim_t / AIM_TIME, 0.0, 1.0)
		draw_circle(Vector2(36, -58), charge, Color(0.95, 0.55, 0.25, 0.8))
