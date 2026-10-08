# Copy-paste handoff prompt

You are continuing a specification project in this repository. Your current job is to make the scope and asset contracts implementation-ready, not to build a game or generate production assets.

Read AGENTS.md, README.md, SPEC.md, docs/DECISIONS.md, docs/ART_DIRECTION.md, docs/ASSET_SPEC.md, docs/ANIMATION_SPEC.md, docs/TECHNICAL_CONSTRAINTS.md, and docs/VALIDATION.md.

The confirmed intent is a 2D Godot gothic horror platformer for mobile browser play, with a later Android APK. The protagonist is an original hunter in an original gothic world (user decision 2026-10-08; see the DECISIONS.md amendments, which supersede the interview-era Simon Belmont identity). He uses a whip, and jumping is restrained. Preserve the final direction: Castlevania as the primary design reference for tone and mechanics, dark detailed horror, no visible pixels, and fully animated supported actions including crouch, jump, knockback, recovery, and death. Do not revive the earlier all-franchise/Mario scope, do not substitute franchise characters or world elements, and do not reopen the resolved pixel-art choice. Resolve only the remaining reference-design and implementation details in the ledger; the original hunter design reference itself is a P2 (art bible) deliverable.

First deliver a concise gap/contradiction audit. Pick one bounded package from docs/WORK_PACKAGES.md. Improve its documents, using clearly marked proposed defaults for missing routine details and asking only the unresolved questions that change fundamental direction. Do not attribute your recommendations to the user.

For asset work, define a repeatable reference → brief → candidate → temporal/technical review → manifest → approval process. No mass sprite generation before scale, identity, art treatment, animation timing, and asset acceptance criteria are settled. Provide filled brief examples and reference requirements, not fake image outputs.

For gameplay work, keep the initial slice bounded and prove on paper that enemy behaviors and level geometry are compatible with the proposed movement and whip windows. Future physical/device testing must be recorded as pending, never invented.

Finish with changed files, decisions resolved/proposed, cross-document consistency checks actually performed, blockers and dependencies, and the next bounded task. Do not initialize a Godot project, publish a build, add a campaign, or silently change a confirmed requirement. A later explicit implementation assignment is needed to enter production.
