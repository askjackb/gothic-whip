extends Node2D
class_name Checkpoint
## Checkpoint (STAGE_DESIGN S6): overlap activates it and moves the respawn
## point here (GAMEPLAY_RULES S7). GREYBOX visual only.

var activated := false


func set_activated() -> void:
	activated = true
	queue_redraw()


func reset_prop() -> void:
	activated = false
	queue_redraw()


func _draw() -> void:
	var stone := Color(0.32, 0.34, 0.4)
	draw_rect(Rect2(-6, -72, 12, 72), stone)
	draw_rect(Rect2(-14, -6, 28, 6), stone) # base
	if activated:
		draw_circle(Vector2(0, -82), 10, Color(0.95, 0.55, 0.25, 0.25)) # ember glow
		draw_circle(Vector2(0, -82), 6, Color(0.95, 0.6, 0.3))
	else:
		draw_circle(Vector2(0, -82), 6, Color(0.45, 0.46, 0.5))
