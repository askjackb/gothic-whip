extends Node2D
class_name ExitDoor
## Exit door (SPEC S5): locked until the boss is defeated; touching it after
## the unlock completes the stage (GAMEPLAY_RULES S7). Production prop art;
## locked state is a presentation darkening (ASSET_BRIEFS S9 tint overlay).

var unlocked := false
var _sprite: Sprite2D


func _ready() -> void:
	_sprite = Sprite2D.new()
	_sprite.texture = load("res://art/props/prop_exit.png")
	_sprite.centered = false
	_sprite.scale = Vector2(0.5, 0.5)
	_sprite.position = Vector2(-48, -144) # canvas 192x320, pivot (96,288)
	_sprite.modulate = Color(0.4, 0.42, 0.5)
	add_child(_sprite)


func set_unlocked() -> void:
	unlocked = true
	if _sprite != null:
		_sprite.modulate = Color.WHITE


func set_locked() -> void:
	unlocked = false
	if _sprite != null:
		_sprite.modulate = Color(0.4, 0.42, 0.5)
