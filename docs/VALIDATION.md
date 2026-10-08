# Acceptance and review plan

No game or assets exist in this repository. All production tests below are **PENDING**. Document consistency checks can run now; playtest/performance evidence cannot.

| Gate | Evidence required | Pass criterion |
|---|---|---|
| V0: specification | Cross-document review, decision ledger, valid examples and links | Confirmed/proposed/open states distinguished; shared coordinates/timing agree; no accidental implementation |
| V1: art calibration | Style pack, identity reference, logical-scale and phone-size scene review | One consistent treatment; hero/threats/terrain readable; no visible pixels; primarily Castlevania direction preserved |
| V2: sprite technical | Automated dimensions/alpha/frame inventory plus inspection | Exact declared canvases/pivots; real alpha; no missing frames or clipped extremities |
| V3: animation | Timed playback, contact sheet, pivot/socket/hitbox overlays | All ANIMATION_SPEC states/transitions covered; no static-slide substitutes; no identity drift; grounded drift ≤2 source px; attached whip; correct active windows |
| V4: terrain | Repeated patch and representative platforms with collision overlay | No seams; decorative features do not misrepresent collision; top edges align |
| V5: touch controls | Screen recording and observation on agreed Android hardware | Move+jump+whip works; controls recover from cancellation/focus loss; targets meet size requirement |
| V6: feel | At least three unfamiliar players, same short onboarding | At least two complete first mixed jump/whip encounter within three attempts without control confusion; record failures rather than rounding up |
| V7: stage | Complete playthrough, checkpoint/death/retry/boss/exit checks | No impossible mandatory jumps, off-screen unavoidable hits, stuck states, or inaccessible exit |
| V8: browser/performance | Exact device/browser/build IDs, network trace, frame samples | Meets agreed targets from technical spec; cold-load and warm-run evidence both supplied |
| V9: future APK | Later debug APK install and touch/resume test on device | Same bounded slice behavior; build prerequisites and version recorded |

V6 is an early diagnostic with a small sample, not statistical proof of broad usability. If it fails, adjust movement/encounter geometry before adding content.

## Review adversarially

- If all detail is dark, can the player still distinguish an enemy from masonry at phone size?
- Does the art imply a safe platform where collision is absent?
- Does a stationary target get hit only once per attack, including across multiple active frames?
- Are an enemy's vulnerable regions reachable without agile jumps or stomp kills?
- Does a left-facing whip retain its correct origin, socket alignment, and reach?
- Can a player combine movement, jumping, and whipping with two thumbs, and separately crouch+whip? If the proposed button layout cannot support the combinations comfortably, revise layout/input semantics before adding gestures.
- Does a camera movement hide a landing or introduce a blind required jump?
- Does the visual contract fit the atlas/memory budget once every animation is counted?
- Does every supported state have meaningful authored animation, including crouch/stand, takeoff/apex/fall/landing, knockback/knockdown/get-up, and complete death?
- Do death, restart, focus loss, touch cancellation, and resize clear input and combat state?

## Handoff evidence format

Record gate ID, revision/build, method, device/tool details, expected result, observed result, evidence path, verdict (PASS/FAIL/NOT-TESTED), and corrective action. Never replace missing measurements with “should work.”
