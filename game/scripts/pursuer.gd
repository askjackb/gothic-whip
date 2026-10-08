extends CharacterBody2D
class_name Pursuer
## Ground pursuer - basic, 1 HP (GAMEPLAY_RULES S8.1, all values [P1 proposal]).
## Patrol 60 u/s; alert 300 ms; approach 100 u/s; wind-up 350 ms inside
## 120 u; lunge 260 u/s; recovery 600 ms. Contact is a displacing hit.
## Visuals: production frames (style_lock_r01) via Anim; state machine rules.

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

var _visual: Node2D
var _body: AnimatedSprite2D
var _vis_clip := ""
var _vis_t := 0.0

const STATE_TO_CLIP := {
	"patrol": "pursuer_patrol_walk", "alert": "pursuer_alert",
	"chase": "pursuer_approach_walk", "windup": "pursuer_lunge_windup",
	"lunge": "pursuer_lunge", "recover": "pursuer_recovery",
	"hurt": "pursuer_hurt", "dead": "pursuer_death",
}


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
	_visual = Node2D.new()
	add_child(_visual)
	_body = Anim.make_sprite(load("res://art/spriteframes/enemy_frames.tres"), "pursuer_patrol_walk")
	_visual.add_child(_body)


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
		_update_visuals(delta)
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
	_update_visuals(delta)


func _set_state(s: String) -> void:
	state = s
	state_t = 0.0
	if s == "alert" and game != null and game.has_method("play_sfx"):
		game.play_sfx("sfx_enemy_tell")


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
		if game != null and game.has_method("spawn_vfx"):
			game.spawn_vfx("vfx_enemy_defeat", global_position + Vector2(0, -28))
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

func _update_visuals(delta: float) -> void:
	if _body == null:
		return
	_visual.scale.x = facing
	var clip: String = STATE_TO_CLIP.get(state, "pursuer_patrol_walk")
	if clip != _vis_clip:
		_vis_clip = clip
		_vis_t = 0.0
	else:
		_vis_t += delta
	Anim.apply(_body, clip, _vis_t)
