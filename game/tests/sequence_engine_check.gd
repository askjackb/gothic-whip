extends SceneTree
## Engine-side sequence audit (companion to tools/audit_sequences.py).
## Loads every actor SpriteFrames resource, asserts every clip in
## res://art/clips.json exists with the manifest frame count, steps through
## each clip frame-by-frame via Anim.apply at each frame's midpoint, and
## asserts the AtlasTexture region matches art/atlases/atlas_regions.json
## and reconstructs inside the contract canvas via the trim offset.
## Run: godot --headless --path . --script tests/sequence_engine_check.gd
## Prints "SEQUENCE ENGINE RESULT: PASS" + exit 0 on success.

var _failures: Array[String] = []
var _checked_frames := 0
var _checked_clips := 0


func _fail(msg: String) -> void:
	_failures.append(msg)
	print("SEQ FAIL: ", msg)


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		_fail("missing " + path)
		return {}
	var v: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return v if v is Dictionary else {}


func _resource_for(clip: String) -> String:
	if clip.begins_with("hero_"):
		return "hero_frames.tres"
	if clip.begins_with("whip_"):
		return "whip_frames.tres"
	if clip.begins_with("boss_"):
		return "boss_frames.tres"
	if clip.begins_with("vfx_"):
		return "fx_frames.tres"
	return "enemy_frames.tres" # pursuer_/swooper_/ranged_/projectile_


func _initialize() -> void:
	var clips: Dictionary = _load_json("res://art/clips.json")
	var regions: Dictionary = _load_json("res://art/atlases/atlas_regions.json")
	if clips.is_empty() or regions.is_empty():
		_finish()
		return
	var resources: Dictionary = {}
	for res_name in ["hero_frames.tres", "whip_frames.tres", "enemy_frames.tres",
			"boss_frames.tres", "fx_frames.tres"]:
		var sf: SpriteFrames = load("res://art/spriteframes/" + res_name)
		if sf == null:
			_fail(res_name + " failed to load")
		resources[res_name] = sf

	var sprite := AnimatedSprite2D.new()
	sprite.centered = false
	root.add_child(sprite)

	var actor_clips: Dictionary = {}
	for clip in clips:
		var info: Dictionary = clips[clip]
		var actor: String = clip.split("_")[0]
		actor_clips[actor] = int(actor_clips.get(actor, 0)) + 1
		var res_name := _resource_for(clip)
		var sf: SpriteFrames = resources.get(res_name)
		if sf == null:
			continue
		if not sf.has_animation(clip):
			_fail("%s missing from %s" % [clip, res_name])
			continue
		var durations: Array = info.get("durations_s", [])
		var count := sf.get_frame_count(clip)
		if count != durations.size():
			_fail("%s frame count %d != clips.json %d" % [clip, count, durations.size()])
			continue
		if bool(info.get("loop", false)) != sf.get_animation_loop(clip):
			_fail("%s loop flag mismatch (clips.json=%s)" % [clip, str(info.get("loop"))])
		var canvas: Array = info.get("canvas", [])
		var pivot: Array = info.get("pivot", [])
		var trims: Array = info.get("trims", [])
		sprite.sprite_frames = sf
		# step through the clip one frame at a time at each frame midpoint
		var t := 0.0
		for i in count:
			var d := float(durations[i])
			if not Anim.apply(sprite, clip, t + d * 0.5):
				_fail("%s f%d: Anim.apply returned false" % [clip, i])
				break
			if sprite.frame != i:
				_fail("%s f%d: Anim.apply selected frame %d" % [clip, i, sprite.frame])
			var tex: Texture2D = sf.get_frame_texture(clip, i)
			if tex == null:
				_fail("%s f%d: null frame texture" % [clip, i])
				continue
			var key := "%s#%d" % [clip, i]
			if not regions.has(key):
				_fail("%s: no atlas region" % key)
				continue
			var reg: Dictionary = regions[key]
			var want := Vector2(float(reg["w"]), float(reg["h"]))
			if tex.get_size() != want:
				_fail("%s: region size %s != atlas_regions %s" % [key, str(tex.get_size()), str(want)])
			# trim offset must reconstruct the frame inside the contract canvas
			if i < trims.size() and canvas.size() == 2 and pivot.size() == 2:
				var tr: Array = trims[i]
				var off := Vector2(float(tr[0]) - float(pivot[0]), float(tr[1]) - float(pivot[1]))
				if sprite.offset != off:
					_fail("%s: sprite offset %s != trim-pivot %s" % [key, str(sprite.offset), str(off)])
				if float(tr[0]) < 0.0 or float(tr[1]) < 0.0 \
						or float(tr[0]) + want.x > float(canvas[0]) \
						or float(tr[1]) + want.y > float(canvas[1]):
					_fail("%s: trimmed region escapes contract canvas %s" % [key, str(canvas)])
			t += d
			_checked_frames += 1
		_checked_clips += 1

	for actor in actor_clips:
		print("SEQ: actor %s — %d clips checked" % [actor, int(actor_clips[actor])])
	print("SEQ: %d clips, %d frames stepped" % [_checked_clips, _checked_frames])
	_finish()


func _finish() -> void:
	if _failures.is_empty():
		print("SEQUENCE ENGINE RESULT: PASS")
		quit(0)
	else:
		print("SEQUENCE ENGINE RESULT: FAIL (%d failures)" % _failures.size())
		quit(1)
