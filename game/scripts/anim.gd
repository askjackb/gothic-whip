class_name Anim
## Runtime animation helper. The state machines stay the single source of
## truth for timing (GAMEPLAY_RULES); this helper only maps (clip, elapsed
## seconds) -> frame index using the per-frame durations in res://art/clips.json
## (generated from the ASSET_BRIEFS tables) and pushes that frame onto an
## AnimatedSprite2D. Sprites never auto-play; frames are state-driven.

static var _data: Dictionary = {}
static var _loaded := false


static func _ensure() -> void:
	if _loaded:
		return
	_loaded = true
	var path := "res://art/clips.json"
	if not FileAccess.file_exists(path):
		push_warning("Anim: clips.json missing")
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if parsed is Dictionary:
		_data = parsed


static func has_clip(clip: String) -> bool:
	_ensure()
	return _data.has(clip)


static func clip_len(clip: String) -> float:
	_ensure()
	var total := 0.0
	for d in durations(clip):
		total += float(d)
	return total


static func durations(clip: String) -> Array:
	_ensure()
	var info: Dictionary = _data.get(clip, {})
	return info.get("durations", info.get("durations_s", []))


static func is_loop(clip: String) -> bool:
	_ensure()
	var info: Dictionary = _data.get(clip, {})
	return bool(info.get("loop", false))


static func pivot_of(clip: String) -> Vector2:
	_ensure()
	var info: Dictionary = _data.get(clip, {})
	var p: Array = info.get("pivot", [0, 0])
	return Vector2(float(p[0]), float(p[1])) if p.size() == 2 else Vector2.ZERO


static func frame_at(clip: String, time: float) -> int:
	var ds := durations(clip)
	if ds.is_empty():
		return 0
	var total := 0.0
	for d in ds:
		total += float(d)
	if total <= 0.0:
		return 0
	var t := time
	if is_loop(clip):
		t = fmod(t, total)
	else:
		t = minf(t, total - 0.0001)
	var acc := 0.0
	for i in ds.size():
		acc += float(ds[i])
		if t < acc:
			return i
	return ds.size() - 1


## Set the sprite to the frame for (clip, time). Returns false if the sprite
## has no such animation (greybox fallback path stays visible to tests).
## Trimmed atlas frames are re-placed exactly via the per-frame trim offset.
static func apply(sprite: AnimatedSprite2D, clip: String, time: float) -> bool:
	if sprite == null or sprite.sprite_frames == null:
		return false
	if not sprite.sprite_frames.has_animation(clip):
		return false
	if sprite.animation != clip:
		sprite.animation = clip
	var idx := frame_at(clip, time)
	sprite.frame = idx
	var info: Dictionary = _data.get(clip, {})
	var trims: Array = info.get("trims", [])
	if idx < trims.size():
		var tr: Array = trims[idx]
		var piv := pivot_of(clip)
		sprite.offset = Vector2(float(tr[0]) - piv.x, float(tr[1]) - piv.y)
	return true


## Make an AnimatedSprite2D for a clip canvas: centered=false, pivot placed
## at the node origin by `apply` via trim offsets, 0.5 display scale
## (2 source px per game unit).
static func make_sprite(frames: SpriteFrames, clip: String) -> AnimatedSprite2D:
	var s := AnimatedSprite2D.new()
	s.sprite_frames = frames
	s.centered = false
	s.scale = Vector2(0.5, 0.5)
	s.position = Vector2.ZERO
	if frames != null and frames.has_animation(clip):
		s.animation = clip
	apply(s, clip, 0.0)
	return s
