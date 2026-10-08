# Asset generation instructions for a future asset worker

This is an instruction template, not authorization to start generating assets during specification work. D05/D06 lock no visible pixels and primarily Castlevania. The identity is Simon Belmont in Castlevania’s world; choose the exact incarnation/costume reference and approve a canonical style pack first.

## Workflow

1. Read the approved style-lock reference, ASSET_SPEC.md, and the individual asset brief. List missing inputs. Do not start a production batch when canvas, pivot, identity, or state/timing is unresolved.
2. Establish a reference pose at exact intended relative scale. Generate small candidates for art-direction review; label them concepts rather than runtime assets.
3. Once the reference is accepted, use reference-based editing/conditioning to derive a small number of key poses. Preserve costume, anatomy, perspective, palette, and light. Generate animation clips separately, using neighboring poses as references when supported.
4. Review silhouettes and key poses before in-betweens. Request specific corrections instead of regenerating a complete sheet repeatedly. If the generator cannot maintain temporal consistency, propose a separately authorized manual cleanup or rigged workflow; do not call inconsistent frames production-ready.
5. Assemble and normalize deliveries with deterministic tools after generation. Validate dimensions and actual alpha. Record every crop, padding, resize, and pivot adjustment. Avoid resampling repeatedly. A painted checkerboard is not transparency.
6. Produce timed animation playback, contact sheets, socket/pivot overlays, and a scene mockup at logical and phone display sizes. Compare against the acceptance checklist.
7. Write a manifest and verdict. Keep rejected candidates traceable. Promote only reviewed assets and preserve the exact prompt/references used.

## Master visual prompt

> Create a production candidate for {asset_id}, revision {revision}, following {approved_style_lock} and {canonical_character_or_environment_reference}. The project is a detailed gothic horror side-view platformer. Use the approved non-pixel painted treatment; maintain the locked silhouette, anatomy, costume construction, materials, palette, and broad upper-left form lighting. The gameplay view is 1280×720 logical units. This asset occupies {logical_width}×{logical_height} units at 2 source pixels per unit unless its approved brief overrides density. Render {specific_pose_or_state_and_action_phase} facing right, side-on, with {camera_and_perspective}. Deliver {canvas_width}×{canvas_height} source pixels, with the ground/foot origin at {pivot_x},{pivot_y}. Preserve the canonical scale; leave room for extremities. {alpha_or_background_requirement}. Keep important shapes legible at phone gameplay size. The exact deliverable is {single_frame_or_small_pose_set}; no collage or presentation layout.
>
> Do not add labels, lettering, borders, watermarks, floor shadows, extra props, duplicate limbs, new armor, altered hair/costume, perspective rotation, unrequested gore, blur, or lighting that obscures the silhouette. Do not bake collision/debug guides into the image. {asset_specific_exclusions}.

Prompted dimensions and anchors are targets, not proof the generator complied. Verify and repair through the documented workflow.

## Hero attack key-pose example

> Use the approved Simon design reference and style lock; if either is missing, stop and report it. Create the body-only full-extension key pose for hero_attack_ground, active phase. Painted gothic horror 2D, no visible pixel grid. Side view facing right, planted rear foot, believable shoulder/hip rotation, striking hand extended, empty hand socket ready for a separate whip layer. Maintain 224-source-pixel standing height and fixed 512×512 RGBA canvas with foot origin (256,448). Actual transparent background. No whip, no ground plane, no text, no camera zoom or changed outfit. This is one pose, not a full animation sheet.

Follow with a separate whip-layer request tied to the accepted hand socket and matched pose. The arm and whip must meet in the composite. Review intended reach against the active hitbox before approving.

## Terrain prompt extension

> Create {tile_id} from the same material kit. Orthographic side view, 128×128 source pixels representing one 64×64 module. The walkable top is exactly at the declared top edge. Match the adjoining edges of {neighbor_ids}. Keep ornaments separate from solid terrain. Deliver the named tile only, with no scene lighting gradients that create repeated seams.

## Review prompt

> Review {candidate_revision} against its brief, canonical reference, ASSET_SPEC.md, ANIMATION_SPEC.md, and SPEC.md. Report PASS/FAIL/NOT-TESTED for actual dimensions/alpha, proportions, identity, pivot drift, hand-to-whip connection, timing, clipping, edge halos, tiling where relevant, collision readability, and phone-size readability. Name the failing frames and concrete corrections. Do not claim engine/mobile validation without evidence. Return the smallest correction request that can resolve each failure.

## Batch stop conditions

Stop if two correction rounds still drift in anatomy/pivot or if one complete attack cannot be made coherent. Diagnose the pipeline before expanding the roster or animation inventory. A larger batch multiplies defects; it does not validate the style.
