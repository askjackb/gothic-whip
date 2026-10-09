# Whip-in-hand fix — metrics (2026-10-09)

User report: the whip roll/unroll motion is fine, "but it is not holding
or attached correctly to the player — it doesn't look like he is holding
a whip; the whip when rolled is the same size as the player."

Re-rendered by `tools/fix_whip_in_hand.py` (modes: bank/debug/render/
metrics/strips/archive). Pose progression, timing
[75,75,50,50,62.5,62.5,62.5,62.5] ms, canvases (whip 768×512 pivot
(276,308), body 512×512 pivot (256,448)), 0.5 sprite scale, hitboxes
unchanged.

## Hand-anchor approach

For each of the 24 attack body frames, the whip-hand (fist centre, body
canvas px) was read off coordinate-grid zoom crops of the painted frame,
plus the forearm direction (elbow→fist unit vector). First-pass anchors
were off by up to ~59 px — every frame was re-read on 4× crops before
rendering. The fix script draws: (1) a wrapped grip, 32 px long / ~11 px
thick, centred on the fist along the forearm axis; (2) the thong from
the grip's front end along the (unchanged) pose path, stamped from the
original painted braid re-sliced to taper 9 → 2.5 px; (3) rolled frames
spiral compactly at the fist. Anchors are stored in the fix script and
in `whip_hands.json` (audit contract). Body→whip canvas mapping:
whip_pt = body_pt + (20, −140) (pivot difference).

Anchors (body px): ground f0–f7 (242,238)(242,238)(367,300)(352,284)
(212,296)(294,267)(249,337)(249,337); air (209,245)(210,244)(232,296)
(356,257)(376,283)(338,331)(334,360)(337,358); crouch (206,330)(206,330)
(317,356)(322,354)(216,375)(190,336)(189,354)(203,386).

## Measured table (final render, alpha > 30)

attach = fist→nearest whip pixel (px); gripCtr = centroid of whip alpha
within r=12 of the fist; thongMax = max thong cross-section beyond
r=26 of the fist; reach = sprite right edge → game units from pivot.

| clip | f | attach | gripCtr | bbox (src px) | thongMax | reach (u) |
|---|---|---|---|---|---|---|
| ground | 0 | 0.0 | 3.7 | 99×81 (coil) | 10.0 | – |
| ground | 1 | 0.0 | 3.7 | 110×82 (coil+tail) | 8.9 | – |
| ground | 2 | 0.0 | 2.7 | 234×85 | 10.0 | 168.5 |
| ground | 3 | 0.0 | 3.0 | 257×20 | 10.0 | 173.0 |
| ground | 4 | 0.0 | 3.3 | 240×83 | 10.0 | – |
| ground | 5 | 0.0 | 3.9 | 169×39 | 8.0 | – |
| ground | 6 | 0.0 | 3.0 | 83×83 (coil) | 8.2 | – |
| ground | 7 | 0.0 | 1.3 | 82×85 (coil) | 8.2 | – |
| air | 0 | 0.0 | 3.7 | 79×70 (coil) | 8.9 | – |
| air | 1 | 0.0 | 2.2 | 81×66 (coil) | 10.0 | – |
| air | 2 | 0.0 | 4.0 | 216×97 | 8.9 | – |
| air | 3 | 0.0 | 3.0 | 251×17 | 10.0 | 172.0 |
| air | 4 | 0.0 | 2.8 | 175×107 | 8.9 | – |
| air | 5 | 0.0 | 2.7 | 179×57 | 8.9 | – |
| air | 6 | 0.0 | 2.7 | 77×81 (coil) | 8.2 | – |
| air | 7 | 0.0 | 1.8 | 78×83 (coil) | 8.2 | – |
| crouch | 0 | 0.0 | 2.4 | 81×72 (coil) | 8.9 | – |
| crouch | 1 | 0.0 | 2.5 | 81×74 (coil) | 8.9 | – |
| crouch | 2 | 0.0 | 2.8 | 233×54 | 8.9 | 143.0* |
| crouch | 3 | 0.0 | 2.8 | 286×16 | 10.0 | 172.5 |
| crouch | 4 | 0.0 | 3.3 | 238×74 | 8.9 | – |
| crouch | 5 | 0.0 | 3.3 | 162×47 | 8.0 | – |
| crouch | 6 | 0.0 | 2.8 | 78×80 (coil) | 8.9 | – |
| crouch | 7 | 0.0 | 1.3 | 78×76 (coil) | 8.5 | – |

*Crouch f2 is mid-unfurl (the crack is f3); the audit's ≥168 u rule
applies to the max over active frames 2–3 (172.5 u here).

Rolled coil size vs the 224 px standing height: 77–110 px (34–49%) —
before the fix the coil reached 257 px (115%). Max thong thickness
10.0 px (design 9 px + antialiasing) — before: ~28 px baton.

## Verification

- Audit (`tools/audit_sequences.py`, new hand-anchor whip contract):
  **0 defects**, 6 pre-existing cloth warnings unchanged.
- `tests/sequence_engine_check.gd`: **SEQUENCE ENGINE RESULT: PASS**.
- `tests/smoke_test.gd`: **SMOKE RESULT: PASS**.
- Composite evidence: `tests/shots/fix2_composite_whip_attack_*.png`
  (body+whip, anchor-cross debug renders reviewed by eye beforehand).
- Engine crack capture: `tests/shots/fix2_whip_strike_engine.png`.
- Web build in Chromium: `tests/shots/fix2_whip_strike.png`
  (`tools/web_check2.js`), 0 console errors.
