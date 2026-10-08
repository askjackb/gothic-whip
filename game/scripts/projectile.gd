extends Node2D
class_name Projectile
## Ranged-threat projectile (GAMEPLAY_RULES S8.3): 280 u/s, fixed height band,
## dissipates after 640 u of travel. GREYBOX: drawn ember orb.

const SPEED := 280.0
const RANGE := 640.0

var dir := 1
var active := true
var _traveled := 0.0


func setup(p: Vector2, d: int) -> void:
	global_position = p
	dir = d


func _ready() -> void:
	add_to_group("projectiles")


func _physics_process(delta: float) -> void:
	if not active:
		return
	var step := dir * SPEED * delta
	global_position.x += step
	_traveled += absf(step)
	if _traveled >= RANGE:
		despawn()


func rect() -> Rect2:
	return Rect2(global_position + Vector2(-9, -6), Vector2(18, 12))


func despawn() -> void:
	active = false
	queue_free()


func _draw() -> void:
	draw_circle(Vector2.ZERO, 7, Color(0.95, 0.55, 0.25))
	draw_circle(Vector2.ZERO, 3.5, Color(1.0, 0.85, 0.55))
