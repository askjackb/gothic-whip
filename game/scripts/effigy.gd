extends Node2D
class_name Effigy
## Training effigy (STAGE_DESIGN S3, E0): non-hostile first-strike target at
## whip height. Counts whip hits; never deals damage. Production prop art.

var hit_count := 0
var last_hit_id := -1
var _flash_t := 0.0
var _sprite: Sprite2D


func _ready() -> void:
	_sprite = Sprite2D.new()
	_sprite.texture = load("res://art/props/prop_effigy.png")
	_sprite.centered = false
	_sprite.scale = Vector2(0.5, 0.5)
	_sprite.position = Vector2(-32, -112) # canvas 128x256, pivot (64,224)
	add_child(_sprite)


func hurt_rect() -> Rect2:
	return Rect2(global_position + Vector2(-16, -96), Vector2(32, 56))


func apply_whip_hit(attack_id_: int, _from_x: float) -> void:
	if attack_id_ == last_hit_id:
		return
	last_hit_id = attack_id_
	hit_count += 1
	_flash_t = 0.25


func reset_actor() -> void:
	hit_count = 0
	last_hit_id = -1
	_flash_t = 0.0


func _process(delta: float) -> void:
	if _flash_t > 0.0:
		_flash_t -= delta
	if _sprite != null:
		_sprite.modulate = Color(1.8, 1.7, 1.5) if _flash_t > 0.0 else Color.WHITE
