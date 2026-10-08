extends CanvasLayer
class_name HUD
## Presentation layer (TECHNICAL_SPEC S2): health pips, boss bar, touch
## buttons (>=64 px logical; SPEC S6 asks 64 initially), pause/victory/
## rotate overlays, death fade, damage indicator. All text is live UI text
## (ASSET_SPEC S5). Pips and damage frame use production art; the rest is
## code-drawn UI as permitted by the briefs.

var game: Node
var input_state: InputState

var _pips: Array = []
var _pip_full: Texture2D
var _pip_empty: Texture2D
var _damage_flash: TextureRect
var _damage_t := 0.0
var _last_hp := 5
var _boss_bar_root: Control
var _boss_fill: ColorRect
var _message_label: Label
var _message_t := 0.0
var _pause_overlay: Control
var _victory_overlay: Control
var _rotate_overlay: Control
var _fade: ColorRect
var _rotate_pausing := false


func _ready() -> void:
	layer = 5
	process_mode = Node.PROCESS_MODE_ALWAYS
	_pip_full = load("res://art/ui/ui_health_full.png")
	_pip_empty = load("res://art/ui/ui_health_empty.png")
	_build_pips()
	_build_boss_bar()
	_build_labels()
	_build_touch_controls()
	_build_overlays()
	_build_damage_flash()


func _build_damage_flash() -> void:
	# SPEC S5: steady, non-strobing damage indicator at the screen edge.
	_damage_flash = TextureRect.new()
	_damage_flash.size = Vector2(1280, 720)
	_damage_flash.stretch_mode = TextureRect.STRETCH_SCALE
	_damage_flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var frames: SpriteFrames = load("res://art/spriteframes/fx_frames.tres")
	if frames != null and frames.has_animation("vfx_damage_indicator"):
		_damage_flash.texture = frames.get_frame_texture("vfx_damage_indicator", 0)
	_damage_flash.modulate = Color(1, 1, 1, 0)
	add_child(_damage_flash)


func _mk_label(text: String, pos: Vector2, size: Vector2, font_size: int, align := HORIZONTAL_ALIGNMENT_LEFT) -> Label:
	var l := Label.new()
	l.text = text
	l.position = pos
	l.size = size
	l.horizontal_alignment = align
	l.add_theme_font_size_override("font_size", font_size)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(l)
	return l


func _mk_button(text: String, pos: Vector2, size: Vector2) -> Button:
	var b := Button.new()
	b.text = text
	b.position = pos
	b.size = size
	b.focus_mode = Control.FOCUS_NONE
	b.add_theme_font_size_override("font_size", 26)
	b.modulate = Color(1, 1, 1, 0.85)
	add_child(b)
	return b


func _build_pips() -> void:
	var box := HBoxContainer.new()
	box.position = Vector2(16, 16)
	box.add_theme_constant_override("separation", 4)
	add_child(box)
	for i in 5:
		var pip := TextureRect.new()
		pip.custom_minimum_size = Vector2(26, 26)
		pip.texture = _pip_full
		pip.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		pip.mouse_filter = Control.MOUSE_FILTER_IGNORE
		box.add_child(pip)
		_pips.append(pip)
	_mk_label("HP", Vector2(16, 48), Vector2(60, 20), 16)


func _build_boss_bar() -> void:
	_boss_bar_root = Control.new()
	_boss_bar_root.position = Vector2(440, 656)
	_boss_bar_root.size = Vector2(400, 40)
	add_child(_boss_bar_root)
	var bg := ColorRect.new()
	bg.position = Vector2(0, 18)
	bg.size = Vector2(400, 16)
	bg.color = Color(0.15, 0.12, 0.18)
	_boss_bar_root.add_child(bg)
	_boss_fill = ColorRect.new()
	_boss_fill.position = Vector2(0, 18)
	_boss_fill.size = Vector2(400, 16)
	_boss_fill.color = Color(0.62, 0.2, 0.28)
	_boss_bar_root.add_child(_boss_fill)
	var l := Label.new()
	l.text = "BOSS"
	l.size = Vector2(400, 18)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size", 15)
	_boss_bar_root.add_child(l)
	_boss_bar_root.visible = false


func _build_labels() -> void:
	_message_label = _mk_label("", Vector2(0, 84), Vector2(1280, 44), 30, HORIZONTAL_ALIGNMENT_CENTER)
	_message_label.visible = false
	_fade = ColorRect.new()
	_fade.size = Vector2(1280, 720)
	_fade.color = Color(0, 0, 0, 0)
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_fade)


func _build_touch_controls() -> void:
	var pause_btn := _mk_button("II", Vector2(1184, 16), Vector2(80, 64))
	pause_btn.pressed.connect(func() -> void: input_state.touch_set("pause", true))
	if DisplayServer.is_touchscreen_available():
		_bind_touch(_mk_button("<", Vector2(24, 592), Vector2(104, 104)), "move_left")
		_bind_touch(_mk_button(">", Vector2(144, 592), Vector2(104, 104)), "move_right")
		_bind_touch(_mk_button("CROUCH", Vector2(856, 592), Vector2(104, 104)), "crouch")
		_bind_touch(_mk_button("JUMP", Vector2(976, 592), Vector2(104, 104)), "jump")
		_bind_touch(_mk_button("WHIP", Vector2(1096, 592), Vector2(160, 104)), "whip")
	else:
		_mk_label("Arrows/A-D move - Space jump - J whip - S/Down crouch - Esc pause",
			Vector2(0, 690), Vector2(1280, 24), 16, HORIZONTAL_ALIGNMENT_CENTER)


func _bind_touch(b: Button, action: String) -> void:
	b.button_down.connect(func() -> void: input_state.touch_set(action, true))
	b.button_up.connect(func() -> void: input_state.touch_set(action, false))


func _build_overlays() -> void:
	_pause_overlay = _mk_overlay("PAUSED")
	var resume := _mk_overlay_button(_pause_overlay, "RESUME", Vector2(540, 330))
	resume.pressed.connect(func() -> void: game.toggle_pause())
	var retry := _mk_overlay_button(_pause_overlay, "RETRY", Vector2(540, 410))
	retry.pressed.connect(func() -> void: game.on_pause_retry())
	_pause_overlay.visible = false

	_victory_overlay = _mk_overlay("STAGE CLEAR")
	var again := _mk_overlay_button(_victory_overlay, "PLAY AGAIN", Vector2(515, 350))
	again.pressed.connect(func() -> void: game.on_victory_retry())
	_victory_overlay.visible = false


func _mk_overlay_button(parent: Control, text: String, pos: Vector2) -> Button:
	var b := Button.new()
	b.text = text
	b.position = pos
	b.size = Vector2(200, 60)
	b.focus_mode = Control.FOCUS_NONE
	b.add_theme_font_size_override("font_size", 24)
	parent.add_child(b)
	return b

	_rotate_overlay = _mk_overlay("ROTATE DEVICE - LANDSCAPE REQUIRED")
	_rotate_overlay.visible = false


func _mk_overlay(title: String) -> Control:
	var root := Control.new()
	root.size = Vector2(1280, 720)
	add_child(root)
	var dim := ColorRect.new()
	dim.size = Vector2(1280, 720)
	dim.color = Color(0, 0, 0, 0.62)
	root.add_child(dim)
	var l := Label.new()
	l.text = title
	l.position = Vector2(0, 240)
	l.size = Vector2(1280, 60)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size", 40)
	root.add_child(l)
	return root


# ------------------------------------------------------------- public API

func set_pause_visible(b: bool) -> void:
	_pause_overlay.visible = b


func show_victory() -> void:
	_victory_overlay.visible = true


func hide_victory() -> void:
	_victory_overlay.visible = false


func set_message(text: String) -> void:
	_message_label.text = text
	_message_label.visible = true
	_message_t = 2.2


func _process(delta: float) -> void:
	if game == null:
		return
	var hunter: Hunter = game.hunter
	if hunter != null:
		for i in _pips.size():
			_pips[i].texture = _pip_full if i < hunter.hp else _pip_empty
		if hunter.hp < _last_hp:
			_damage_t = 0.3 # steady indicator, not a strobe (SPEC S5)
		_last_hp = hunter.hp
		if _damage_t > 0.0:
			_damage_t -= delta
		if _damage_flash != null:
			_damage_flash.modulate.a = 0.55 if _damage_t > 0.0 else 0.0
		var target := 0.85 if hunter.state == "death" else 0.0
		var c := _fade.color
		c.a = move_toward(c.a, target, delta * 1.8)
		_fade.color = c
	if game.boss != null:
		var show: bool = bool(game.fight_active) and game.boss.state != "dead"
		_boss_bar_root.visible = show
		if show:
			_boss_fill.size.x = 400.0 * clampf(float(game.boss.hp) / 8.0, 0.0, 1.0)
	if _message_t > 0.0:
		_message_t -= delta
		if _message_t <= 0.0:
			_message_label.visible = false
	# Portrait -> rotate prompt over a paused game (SPEC S6). The prompt
	# pauses/resumes itself; a manual pause underneath is left alone.
	var win := DisplayServer.window_get_size()
	var portrait := win.x > 0 and win.y > win.x
	if portrait and not _rotate_pausing:
		_rotate_pausing = true
		_rotate_overlay.visible = true
		game.set_rotate_paused(true)
	elif not portrait and _rotate_pausing:
		_rotate_pausing = false
		_rotate_overlay.visible = false
		game.set_rotate_paused(false)
