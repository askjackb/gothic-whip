extends Node
class_name InputState
## Single input layer (TECHNICAL_SPEC S2): keyboard (InputMap actions) and
## on-screen touch buttons both feed this state. Gameplay reads only this.
## Opposing directions resolve to neutral in the consumer (Hunter._input_dir).
## Focus loss / pause clears everything (SPEC S4, GAMEPLAY_RULES S3).

signal pause_toggled

const ACTIONS: Array[String] = ["move_left", "move_right", "jump", "whip", "crouch", "pause"]
const KEYMAP := {
	"move_left": [KEY_A, KEY_LEFT],
	"move_right": [KEY_D, KEY_RIGHT],
	"jump": [KEY_SPACE],
	"whip": [KEY_J],
	"crouch": [KEY_S, KEY_DOWN],
	"pause": [KEY_ESCAPE],
}

var held: Dictionary = {}
var _pressed: Dictionary = {}


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_ensure_input_map()
	clear_all()


## The actions are declared in project.godot; this only repairs a missing
## binding so the game (and the headless smoke test) can never boot inputless.
func _ensure_input_map() -> void:
	for action in ACTIONS:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for key in KEYMAP[action]:
			var exists := false
			for ev in InputMap.action_get_events(action):
				if ev is InputEventKey and ev.physical_keycode == key:
					exists = true
			if not exists:
				var ev := InputEventKey.new()
				ev.physical_keycode = key
				InputMap.action_add_event(action, ev)


func _input(event: InputEvent) -> void:
	for action in ACTIONS:
		if event.is_action_pressed(action):
			held[action] = true
			_pressed[action] = true
			if action == "pause":
				pause_toggled.emit()
		elif event.is_action_released(action):
			held[action] = false


## Called by HUD touch buttons (button_down / button_up).
func touch_set(action: String, down: bool) -> void:
	if not ACTIONS.has(action):
		return
	held[action] = down
	if down:
		_pressed[action] = true
		if action == "pause":
			pause_toggled.emit()


func is_held(action: String) -> bool:
	return bool(held.get(action, false))


func consume_pressed(action: String) -> bool:
	var v := bool(_pressed.get(action, false))
	_pressed[action] = false
	return v


func clear_all() -> void:
	for action in ACTIONS:
		held[action] = false
		_pressed[action] = false


# --- test helpers (headless smoke test drives input through these) ---

func debug_press(action: String) -> void:
	_pressed[action] = true


func debug_set_held(action: String, down: bool) -> void:
	held[action] = down
