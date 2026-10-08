extends Node2D
class_name RangedThreat
## Stationary ranged threat - 2 HP (GAMEPLAY_RULES S8.3, values [P1 proposal]).
## Rooted: 900 ms tracked aim with visible charge cue, one projectile,
## 700 ms recovery. Projectile hits are non-displacing (hurt_recoil);
## body contact is displacing. Stationary is not static: idle sways, aim
## tracks, hurt interrupts aim. Visuals: production frames via Anim.

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

var _visual: Node2D
var _body: AnimatedSprite2D
var _vis_clip := ""
var _vis_t := 0.0


func _ready() -> void:
	home_pos = global_position
	_visual = Node2D.new()
	add_child(_visual)
	_body = Anim.make_sprite(load("res://art/spriteframes/enemy_frames.tres"), "ranged_idle")
	_visual.add_child(_body)


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
	_update_visuals(delta)


func _fire() -> void:
	if game != null and game.has_method("spawn_projectile"):
		# Band y -70..-95 relative to this actor's own ground surface
		# (GAMEPLAY_RULES S8.3); from the B4 ground route it passes overhead.
		game.spawn_projectile(global_position + Vector2(facing * 30, -82), facing)


func _set_state(s: String) -> void:
	state = s
	state_t = 0.0
	if s == "aim" and game != null and game.has_method("play_sfx"):
		game.play_sfx("sfx_enemy_tell", 0.8)


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
		if game != null and game.has_method("spawn_vfx"):
			game.spawn_vfx("vfx_enemy_defeat", global_position + Vector2(0, -40))
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

func _update_visuals(delta: float) -> void:
	if _body == null:
		return
	_visual.scale.x = facing
	# recover opens with the 200 ms fire clip (ASSET_BRIEFS S6), then recover
	var clip := "ranged_idle"
	var t := state_t
	match state:
		"idle":
			clip = "ranged_idle"
		"aim":
			clip = "ranged_aim"
			t = aim_t
		"recover":
			if state_t < 0.2:
				clip = "ranged_fire"
			else:
				clip = "ranged_recover"
				t = state_t - 0.2
		"hurt":
			clip = "ranged_hurt"
		"dead":
			clip = "ranged_death"
	if clip != _vis_clip:
		_vis_clip = clip
		_vis_t = t
	Anim.apply(_body, clip, t)
