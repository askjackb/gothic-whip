extends Node2D
class_name Projectile
## Ranged-threat projectile (GAMEPLAY_RULES S8.3): 280 u/s, fixed height band,
## dissipates after 640 u of travel. Visual: Grave Phosphor diamond (ART_BIBLE S4).

const SPEED := 280.0
const RANGE := 640.0

var dir := 1
var active := true
var _traveled := 0.0
var _t := 0.0
var _sprite: AnimatedSprite2D


func setup(p: Vector2, d: int) -> void:
	global_position = p
	dir = d


func _ready() -> void:
	add_to_group("projectiles")
	_sprite = Anim.make_sprite(load("res://art/spriteframes/enemy_frames.tres"), "projectile_grave_shot")
	add_child(_sprite)


func _physics_process(delta: float) -> void:
	if not active:
		return
	_t += delta
	if _sprite != null:
		Anim.apply(_sprite, "projectile_grave_shot", _t)
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


