extends Node2D
class_name ExitDoor
## Exit door (SPEC S5): locked until the boss is defeated; touching it after
## the unlock completes the stage (GAMEPLAY_RULES S7). GREYBOX visual only.

var unlocked := false


func set_unlocked() -> void:
	unlocked = true
	queue_redraw()


func set_locked() -> void:
	unlocked = false
	queue_redraw()


func _draw() -> void:
	var stone := Color(0.3, 0.31, 0.38)
	draw_rect(Rect2(-30, -128, 60, 128), stone) # frame
	if unlocked:
		draw_rect(Rect2(-20, -118, 40, 118), Color(0.98, 0.75, 0.45)) # lit opening
		draw_rect(Rect2(-20, -118, 40, 10), Color(1.0, 0.9, 0.65))
	else:
		draw_rect(Rect2(-20, -118, 40, 118), Color(0.12, 0.12, 0.16))
		var bar := Color(0.55, 0.57, 0.62)
		draw_rect(Rect2(-16, -118, 6, 118), bar)
		draw_rect(Rect2(-3, -118, 6, 118), bar)
		draw_rect(Rect2(10, -118, 6, 118), bar)
