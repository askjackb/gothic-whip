extends Node2D
class_name Checkpoint
## Checkpoint (STAGE_DESIGN S6): overlap activates it and moves the respawn
## point here (GAMEPLAY_RULES S7). Production prop art, two states.

var activated := false
var _sprite: Sprite2D
var _tex_off: Texture2D
var _tex_on: Texture2D


func _ready() -> void:
	_tex_off = load("res://art/props/prop_checkpoint_off.png")
	_tex_on = load("res://art/props/prop_checkpoint_on.png")
	_sprite = Sprite2D.new()
	_sprite.texture = _tex_off
	_sprite.centered = false
	_sprite.scale = Vector2(0.5, 0.5)
	_sprite.position = Vector2(-48, -144) # canvas 192x320, pivot (96,288)
	add_child(_sprite)


func set_activated() -> void:
	activated = true
	if _sprite != null:
		_sprite.texture = _tex_on


func reset_prop() -> void:
	activated = false
	if _sprite != null:
		_sprite.texture = _tex_off
