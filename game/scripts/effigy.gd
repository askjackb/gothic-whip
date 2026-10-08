extends Node2D
class_name Effigy
## Training effigy (STAGE_DESIGN S3, E0): non-hostile first-strike target at
## whip height. Counts whip hits; never deals damage. GREYBOX visual only.

var hit_count := 0
var last_hit_id := -1
var _flash_t := 0.0


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
		queue_redraw()


func _draw() -> void:
	var wood := Color(0.42, 0.32, 0.22)
	draw_rect(Rect2(-4, -100, 8, 100), wood) # post
	draw_rect(Rect2(-18, -8, 36, 8), wood) # foot brace
	draw_circle(Vector2(0, -68), 26, Color(0.72, 0.56, 0.34)) # ochre target
	draw_circle(Vector2(0, -68), 17, Color(0.3, 0.26, 0.22))
	draw_circle(Vector2(0, -68), 9, Color(0.72, 0.56, 0.34))
	if _flash_t > 0.0:
		draw_circle(Vector2(0, -68), 26, Color(1, 1, 1, 0.45))
