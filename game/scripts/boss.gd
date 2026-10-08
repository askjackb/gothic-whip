extends CharacterBody2D
class_name Boss
## Boss - 8 HP, two attacks (GAMEPLAY_RULES S8.4, values [P1 proposal]).
## Close-range strike: 150 u trigger, 700 ms tell, threatens 100 u in front,
## HEAVY hit -> knockdown; 1100 ms recovery. Ground hazard: 1200 ms marked
## 160 u zone at the hunter's position, 400 ms eruption (<=46 u tall),
## ordinary knockback hit. Dormant until Main starts the fight.
## GREYBOX visuals only.

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
		queue_redraw()
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
	queue_redraw()


func _do_strike() -> void:
	if hunter != null and not hunter.is_dead():
		if hunter.body_rect().intersects(strike_rect()):
			hunter.take_damage("heavy", global_position.x)


func _set_state(s: String) -> void:
	state = s
	state_t = 0.0


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

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(facing, 1))
	var body := Color(0.23, 0.18, 0.25)
	var accent := Color(0.43, 0.14, 0.2)
	var bone := Color(0.85, 0.78, 0.66)
	if state == "dead":
		draw_rect(Rect2(-52, -16, 104, 16), body.darkened(0.4))
		draw_circle(Vector2(46, -10), 11, body.darkened(0.3))
		return
	# hazard zone marker (world-anchored, drawn in local space)
	if state == "hazard_cast" or state == "hazard_erupt":
		var zx := zone_x - global_position.x - 80.0
		var a := 0.55 if state == "hazard_erupt" else 0.28
		var h := 46.0 if state == "hazard_erupt" else 8.0
		draw_rect(Rect2(zx, -h, 160, h), Color(0.9, 0.25, 0.2, a))
	draw_rect(Rect2(-30, -52, 16, 52), body.darkened(0.2)) # legs
	draw_rect(Rect2(14, -52, 16, 52), body.darkened(0.2))
	draw_rect(Rect2(-38, -118, 76, 70), body) # torso
	draw_rect(Rect2(-38, -118, 76, 12), accent) # chest band
	draw_colored_polygon(PackedVector2Array([Vector2(-30, -118), Vector2(-44, -134), Vector2(-24, -126)]), bone) # horn L
	draw_colored_polygon(PackedVector2Array([Vector2(30, -118), Vector2(44, -134), Vector2(24, -126)]), bone) # horn R
	draw_circle(Vector2(4, -106), 11, body.lightened(0.15)) # head
	if state == "strike_windup":
		draw_rect(Rect2(24, -150, 14, 52), body) # raised arm (tell)
		draw_rect(Rect2(-4, -162, 5, 18), Color(1.0, 0.8, 0.3))
		draw_circle(Vector2(-1.5, -138), 3.5, Color(1.0, 0.8, 0.3))
	elif state == "strike":
		draw_rect(Rect2(30, -104, 60, 16), body) # swung arm
		draw_rect(Rect2(38, -140, 100, 140), Color(0.9, 0.3, 0.25, 0.18)) # strike flash
	elif state == "hazard_cast":
		draw_rect(Rect2(20, -140, 12, 44), body) # raised casting arm
	else:
		draw_rect(Rect2(26, -100, 13, 48), body) # resting arm
