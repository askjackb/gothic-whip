extends CharacterBody2D
class_name Boss
## Boss - 8 HP, two attacks (GAMEPLAY_RULES S8.4, values [P1 proposal]).
## Close-range strike: 150 u trigger, 700 ms tell, threatens 100 u in front,
## HEAVY hit -> knockdown; 1100 ms recovery. Ground hazard: 1200 ms marked
## 160 u zone at the hunter's position, 400 ms eruption (<=46 u tall),
## ordinary knockback hit. Dormant until Main starts the fight.
## Visuals: production frames (style_lock_r01) via Anim; hazard VFX by Main.

const GRAVITY := 1600.0
const ADVANCE_SPEED := 70.0
const STRIKE_TRIGGER := 150.0
const WINDUP_TIME := 0.700
const STRIKE_FLASH_TIME := 0.120
const STRIKE_RECOVER_TIME := 1.100
const HAZARD_CAST_TIME := 1.200
const HAZARD_ERUPT_TIME := 0.400
const HAZARD_RECOVER_TIME := 0.900
const HAZARD_COOLDOWN := 2.5
const TURN_TIME := 0.350
const HURT_TIME := 0.200
const MAX_HP := 8

var hunter: Hunter
var game: Node

var hp := MAX_HP
var state := "dormant"
var state_t := 0.0
var facing := -1
var hazard_cooldown := 0.0
var zone_x := 0.0
var last_hit_id := -1
var home_pos := Vector2.ZERO

var _visual: Node2D
var _body: AnimatedSprite2D
var _vis_clip := ""
var _vis_t := 0.0

const STATE_TO_CLIP := {
	"dormant": "boss_idle", "idle": "boss_idle", "advance": "boss_walk",
	"turn": "boss_turn", "strike_windup": "boss_strike_windup",
	"strike": "boss_strike_execute", "strike_recover": "boss_strike_recover",
	"hazard_cast": "boss_hazard_windup", "hazard_erupt": "boss_hazard_execute",
	"hazard_recover": "boss_hazard_recover", "hurt": "boss_hurt",
	"dead": "boss_death",
}


func _ready() -> void:
	collision_layer = 4
	collision_mask = 1
	floor_snap_length = 6.0
	var shape := CollisionShape2D.new()
	var rs := RectangleShape2D.new()
	rs.size = Vector2(76, 128)
	shape.shape = rs
	shape.position = Vector2(0, -64)
	add_child(shape)
	home_pos = global_position
	_visual = Node2D.new()
	add_child(_visual)
	_body = Anim.make_sprite(load("res://art/spriteframes/boss_frames.tres"), "boss_idle")
	_visual.add_child(_body)


func start_fight() -> void:
	if state == "dormant":
		_set_state("idle")


func erupting() -> bool:
	return state == "hazard_erupt"


func zone_rect() -> Rect2:
	return Rect2(Vector2(zone_x - 80, global_position.y - 46), Vector2(160, 46))


func strike_rect() -> Rect2:
	var x0 := global_position.x + facing * 38.0
	var x1 := x0 + facing * 100.0
	return Rect2(Vector2(minf(x0, x1), global_position.y - 140), Vector2(100, 140))


func _dist_x() -> float:
	return absf(hunter.global_position.x - global_position.x) if hunter != null else 99999.0


func _same_level() -> bool:
	return hunter != null and absf(hunter.global_position.y - global_position.y) < 60.0


func _physics_process(delta: float) -> void:
	state_t += delta
	if hazard_cooldown > 0.0:
		hazard_cooldown -= delta
	if state == "dead":
		velocity.x = 0.0
		if not is_on_floor():
			velocity.y += GRAVITY * delta
		move_and_slide()
		_update_visuals(delta)
		return

	match state:
		"dormant":
			velocity.x = 0.0
		"idle":
			velocity.x = 0.0
			if state_t >= 0.350 and hunter != null and not hunter.is_dead():
				if _dist_x() <= STRIKE_TRIGGER and _same_level():
					_set_state("strike_windup")
				elif hazard_cooldown <= 0.0 and _dist_x() > 170.0:
					zone_x = hunter.global_position.x
					_set_state("hazard_cast")
				else:
					_set_state("advance")
		"advance":
			if hunter == null or hunter.is_dead():
				velocity.x = 0.0
				_set_state("idle")
			else:
				var dir := 1 if hunter.global_position.x > global_position.x else -1
				if dir != facing:
					_set_state("turn")
				else:
					velocity.x = facing * ADVANCE_SPEED
					if _dist_x() <= STRIKE_TRIGGER and _same_level():
						_set_state("strike_windup")
		"turn":
			velocity.x = 0.0
			if state_t >= TURN_TIME:
				facing = -facing
				_set_state("advance")
		"strike_windup":
			velocity.x = 0.0
			if state_t >= WINDUP_TIME:
				_do_strike()
				_set_state("strike")
		"strike":
			velocity.x = 0.0
			if state_t >= STRIKE_FLASH_TIME:
				_set_state("strike_recover")
		"strike_recover":
			velocity.x = 0.0
			if state_t >= STRIKE_RECOVER_TIME:
				_set_state("idle")
		"hazard_cast":
			velocity.x = 0.0
			if state_t >= HAZARD_CAST_TIME:
				_set_state("hazard_erupt")
		"hazard_erupt":
			velocity.x = 0.0
			if state_t >= HAZARD_ERUPT_TIME:
				hazard_cooldown = HAZARD_COOLDOWN
				_set_state("hazard_recover")
		"hazard_recover":
			velocity.x = 0.0
			if state_t >= HAZARD_RECOVER_TIME:
				_set_state("idle")
		"hurt":
			velocity.x = 0.0
			if state_t >= HURT_TIME:
				_set_state("idle")

	if not is_on_floor():
		velocity.y += GRAVITY * delta
	elif velocity.y > 0.0:
		velocity.y = 0.0
	move_and_slide()
	_update_visuals(delta)


func _do_strike() -> void:
	if hunter != null and not hunter.is_dead():
		if hunter.body_rect().intersects(strike_rect()):
			hunter.take_damage("heavy", global_position.x)


func _set_state(s: String) -> void:
	state = s
	state_t = 0.0
	if game != null:
		if (s == "strike_windup" or s == "hazard_cast") and game.has_method("play_sfx"):
			game.play_sfx("sfx_boss_tell")
		if game.has_method("spawn_vfx"):
			if s == "hazard_cast":
				game.spawn_vfx("vfx_hazard_telegraph", Vector2(zone_x, global_position.y - 8.0))
			elif s == "hazard_erupt":
				game.spawn_vfx("vfx_hazard_eruption", Vector2(zone_x, global_position.y - 8.0))


# ------------------------------------------------------------- interfaces

func hurt_rect() -> Rect2:
	if state == "dead":
		return Rect2()
	return Rect2(global_position + Vector2(-38, -128), Vector2(76, 128))


func contact_rect() -> Rect2:
	return hurt_rect()


func contact_active() -> bool:
	return state != "dead" and state != "dormant"


func contact_kind() -> String:
	return "contact"


func apply_whip_hit(attack_id_: int, _from_x: float) -> void:
	if state == "dead" or state == "dormant" or attack_id_ == last_hit_id:
		return
	last_hit_id = attack_id_
	hp -= 1
	if hp <= 0:
		_set_state("dead")
		if game != null and game.has_method("spawn_vfx"):
			game.spawn_vfx("vfx_enemy_defeat", global_position + Vector2(0, -70))
		if game != null and game.has_method("on_boss_defeated"):
			game.on_boss_defeated()
	elif state != "strike":
		# hurt interrupts anticipation; a live strike is not interrupted (S5)
		_set_state("hurt")


func reset_actor() -> void:
	global_position = home_pos
	velocity = Vector2.ZERO
	hp = MAX_HP
	last_hit_id = -1
	facing = -1
	hazard_cooldown = 0.0
	visible = true
	modulate = Color.WHITE
	_set_state("dormant")


# ---------------------------------------------------------------- visuals

func _update_visuals(delta: float) -> void:
	if _body == null:
		return
	_visual.scale.x = facing
	var clip: String = STATE_TO_CLIP.get(state, "boss_idle")
	if clip != _vis_clip:
		_vis_clip = clip
		_vis_t = 0.0
	else:
		_vis_t += delta
	# dormant: hold the first idle frame (a still warden, GAMEPLAY_RULES S8.4)
	Anim.apply(_body, clip, 0.0 if state == "dormant" else _vis_t)
