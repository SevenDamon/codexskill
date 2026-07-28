# Story Video Director

`story-video-director` turns lesson texts, stories, plot passages, and short film concepts into staged materials for AI image and video generation.

It is not a one-step final prompt generator. Its main value is forcing the work through reviewable stages so a story becomes controllable 8-15 second visual events.

## What It Produces

- Video feasibility diagnosis
- Narrative skeleton
- Character, object, scene, and visual-style consistency cards
- Reference image prompt plans for recurring characters, objects, scenes, and style
- 8-15 second visual-event segment tables
- Director-note input cards
- GPT Image 2 director-note image prompts
- Seedance text prompts
- Revision guidance from generated-video feedback

## Recommended Workflow

```text
Story or lesson text
-> feasibility diagnosis
-> narrative skeleton
-> generation mode and duration limit
-> consistency asset cards
-> reference image prompts
-> visual-event segment breakdown
-> selected segment director-note cards
-> director-note image prompts
-> Seedance prompts
-> feedback-based revision
```

## Why Reference Assets Matter

When generating multiple video segments, models often drift: faces change, clothing changes, props morph, scene direction flips, and color style shifts.

Before generating per-segment video prompts, create shared reference assets:

- Character reference images to lock age band, body shape, clothing color, silhouette, and fixed props
- Object reference images to lock shape, scale, material, color, and allowed state changes
- Scene reference images to lock geography, entrances, windows, major objects, and camera axis
- Unified style reference images to lock palette, lighting, lens feel, and texture
- A completed master audio track or voice consistency card to lock voice, delivery, pacing, and emotional baseline

Each segment should inherit these assets and repeat an explicit consistency lock.

Pose continuity is also locked as structured state. Every recurring character gets an initial support/foot/torso/hand/gaze/contact state; each segment lists only its allowed pose changes and required end state. Unlisted changes stay forbidden, and models must not invent chairs, stools, walls, tables, vehicles, props, or other supports to justify a pose.

The full continuity state stays in the internal director-note card. The visible director-note page is intentionally lighter: six content zones, one execution strip, one key shot by default, and at most five highest-priority restrictions. Seedance prompts are concise and describe only the inherited start, speaker/listener, one action change, camera behavior, and a compact negative sentence.

Before generating prompts for a named or identifiable real person, the skill asks whether the person belongs to a sensitive real-person category. When confirmed, downstream image and video prompts use stable neutral role aliases rather than real names. This is prompt hygiene, not a guarantee that a target platform will permit a recognizable likeness.

Only a story, dialogue, plot passage, or character-and-scene description is required to begin. Character images, scene images, audio, stable tail frames, and previous director-note pages are conditional assets. Description-only input enters a setup stage that creates character, scene, voice, and segment cards before any director-note prompt.

Seedance timing is mode-aware: Agent mode with uploaded audio has a 13-second hard audio-file limit; video generation with model-generated sound has a 15-second hard video limit. Over-limit audio is split at semantic pauses by default and is never silently truncated.

Every boundary is classified as either a same-shot continuation or a motivated cut. Same-shot continuation inherits a stable end frame plus framing, camera position and motion state, pose, gaze, background crop, and light. Motivated cuts preserve screen direction, world-space pose, and continuous master audio. Large visual jumps are regenerated rather than hidden with decorative transitions.

## Example Invocation

```text
Use $story-video-director to process this story for a 4-part AI video.

Purpose: cinematic short fragment
Style: restrained suspense, low saturation, handheld tension
Fidelity: basically faithful, light visual translation allowed
Audience and limits: adult short film, no graphic violence
Need: consistency asset cards, reference image prompts, segment table, then director-note cards

Story:
...
```

## Key Rule

Do not generate all final Seedance prompts before the segment split and consistency assets are reviewed. For multi-segment stories, reference assets come before per-segment director-note images.
