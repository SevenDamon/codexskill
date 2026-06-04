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

Each segment should inherit these assets and repeat an explicit consistency lock.

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
