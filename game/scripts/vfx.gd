extends AnimatedSprite2D
class_name VfxPlayer
## One-shot world VFX (ASSET_BRIEFS S11): plays a clip once, driven by the
## same duration table as the actors, then frees itself. Spawned by Main via
## spawn_vfx(); never touches gameplay state.

var clip := ""
var _t := 0.0


func setup(frames: SpriteFrames, clip_name: String, world_pos: Vector2, scl := 0.5) -> void:
	clip = clip_name
	sprite_frames = frames
	centered = false
	scale = Vector2(scl, scl)
	position = Vector2.ZERO
	global_position = world_pos
	if frames != null and frames.has_animation(clip):
		animation = clip
		frame = 0
	Anim.apply(self, clip, 0.0)


func _process(delta: float) -> void:
	_t += delta
	if clip == "" or sprite_frames == null:
		queue_free()
		return
	Anim.apply(self, clip, _t)
	if _t >= Anim.clip_len(clip):
		queue_free()
