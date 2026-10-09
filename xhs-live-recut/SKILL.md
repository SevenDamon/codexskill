---
name: xhs-live-recut
description: Turn Chinese education, STEM, AI course livestream replays, screen recordings, or SRT transcripts into Xiaohongshu-style short promo videos, source-frame covers, and HyperFrames compositions. Use when the user asks to mine independent topics, preserve original picture and voice, render clips, or make publishable covers from a livestream or screen recording.
---

# XHS Live Recut

Turn long Chinese education livestreams into short, platform-native videos. Default to a **source recut**: preserve the original picture and synchronized original voice, remove repetition and dead air with sentence-level cuts, then add restrained titles, captions, zooms, and callouts. Use rewritten narration only when the user explicitly chooses remake mode.

## Non-negotiable decisions

- Name likely failure points first: weak topic, thin insight, unsupported rewrite, unreadable screen capture, robotic voice, or pasted-on CTA.
- Prefer an adjacent SRT for sources longer than 20 minutes. Before running expensive transcription, state the expected cost/time and obtain approval.
- Default full-screen PPT, browser, code, and software demos to horizontal 16:9. Use 9:16 only when requested and redesign the layout with pan/zoom, split panels, or recreated UI; never crop blindly.
- Give one concrete, useful idea in every promo. Reveal a framework or key judgment while reserving the full implementation for the replay/product.
- Preserve provenance. Mark every material claim as source-derived, compressed, combined, or newly written.
- Treat `source-recut` and `remake` as separate modes. Default to `source-recut`; never replace usable original speech with TTS merely because a voice engine is available.
- In `source-recut`, keep picture and voice from the same intervals. Never mute the source, reorder unrelated screen moments under new narration, or turn the livestream into a motion-graphics explainer unless explicitly requested.
- Never render before the required content approvals. After the pilot and project profile are approved, automate within the frozen profile instead of asking repetitive questions.

## Inputs

Required:
- `video_path`: local livestream replay or screen recording.

Optional:
- `srt_path`: SRT exported from Jianying/CapCut or another tool.
- `reference_images`: cover, caption, or channel-style screenshots.
- `style`: a content style from `references/style_catalog.md`.
- `aspect`: `horizontal` by default; `vertical` only when requested.
- `cover_aspect`: independent of video aspect. For Xiaohongshu feed covers, start with a designed 3:4 portrait canvas (for example 1080×1440) and verify the actual crop in the user's publishing UI; keep a separate 16:9 cover when needed for a horizontal-video destination.
- `voice`: preferred TTS voice or `human-script-only`.
- `mode`: `source-recut` (default) or `remake`.
- `product_context`: buyer, promise, linked product/replay, and disclosure boundary.
- `target_count`: default to 3–5 topic briefs and one pilot render.
- `project_profile`: an approved reusable profile from a prior video in the same series.

## Workflow

### 1. Verify source

- Confirm the source exists; probe duration, resolution, frame rate, and audio.
- Look for an adjacent same-basename SRT.
- Create a new output folder without overwriting prior work.

### 1.5 Cache transcript and build a coarse segment index

- Transcribe the full source at most once. Reuse the adjacent SRT or cached transcript on every later run.
- For sources longer than 20 minutes, generate a 3–8 minute coarse index before topic mining. Run `scripts/srt_chunk_indexer.py` for a mechanical index, then name chapters with editorial judgment.
- Do not physically split the entire video and transcribe every file. That repeats model startup, weakens cross-boundary context, and creates unnecessary media files.
- After topic selection, extract only its 30–120 second source neighborhood as a lightweight working proxy. Perform sentence cuts, captions, screenshots, and A/V validation against that proxy.
- Cache original timecodes, proxy-local timecodes, selected sentences, and rejected gaps so revisions do not rescan the full replay.

### 2. Mine topics — approval gate 1

- Parse the SRT and identify 3–5 remake-worthy topics. Use `scripts/srt_topic_miner.py` only for rough candidate windows; apply editorial judgment.
- For each candidate provide: source range, viewer pain, hook, dry-good point, withheld portion, visual evidence, CTA angle, and likely failure.
- Reject topics that are clever but not useful, depend heavily on missing context, or lack readable screen evidence.
- Stop and obtain the user's topic selection before developing a full script.

### 3. Build sourced structure — approval gate 2

- Produce a concise structure: title, audience, core problem, hook, claims, example/screens, partial reveal, and CTA.
- Create `source-map.md` using `references/workflow_artifacts.md`. Map each claim and visual to source timecodes and label its transformation.
- Flag semantic risks explicitly: strengthened claims, combined distant passages, missing transitions, stale UI states, or narration that the source does not support.
- Stop and obtain approval of both structure and factual boundary. Do not write final narration or create the composition before approval.
- In `source-recut`, propose a cut structure made from verbatim source sentences and state the expected duration after removing pauses and repetition. Do not rewrite narration at this gate.

### 4. Establish content and visual style

- Read `references/style_catalog.md` when style is missing or alternatives are requested. Offer at most two content directions.
- When reference screenshots are provided, infer a candidate visual system rather than claiming exact identification. Extract approximate palette, typography class, hierarchy, caption placement, cover layout, and screenshot treatment.
- Require explicit values for caption/cover font size. Resolve a real installed or supplied font file and note licensing uncertainty; do not silently substitute fonts.
- Create or update `project-profile.yaml` using `references/workflow_artifacts.md`.
- For a new series, stop for visual approval before rendering. For an approved existing profile, reuse it without asking again unless the source makes it unreadable.

### 5. Write the short video

- For `source-recut`, target 40–60 seconds unless the source supports a clean shorter cut. Select verbatim source spans, preserve their order by default, and cut only at phrase or sentence boundaries. Use the original voice as narration.
- For `remake`, target 30–45 seconds and use: hook → problem reframe → concrete framework/example → partial reveal → product-link CTA.
- Keep newly written narration conversational Chinese and avoid dense written prose.
- Avoid stiff lines such as “我不在这条讲完” or “想了解更多请点击链接.” Prefer a specific, native CTA such as “照着做的完整过程，放在下面的课程回放里.”
- Never present newly written copy as a verbatim source quote.
- In `source-recut`, keep editorial overlays separate from spoken captions. Do not fabricate a spoken CTA; display it as an overlay if needed.

### 6. Build and render

- Use HyperFrames and its CLI for composition and rendering.
- In `source-recut`, extract and concatenate matching source A/V intervals together. Feed the recut video muted plus the same recut file as a separate audio element so HyperFrames owns playback while picture and original voice stay synchronized.
- For multiple jump cuts, encode only the selected sentence parts with timestamps reset to zero, then join them with the concat demuxer. Do not concatenate raw seek inputs in one filter graph when it produces non-monotonic audio timestamps.
- Normalize original audio conservatively; do not clone, replace, or change the speaker's voice.
- In `remake`, use separate narration audio.
- Prefer full-width screen captures in 16:9. Add concise callouts without covering important UI.
- For 9:16, use designed containers, staged pan/zoom, or recreated panels; keep text and controls legible at delivery size.
- Only in `remake`, prefer Edge neural voices for Chinese when available: `zh-CN-XiaoxiaoNeural`, `zh-CN-YunxiNeural`, or `zh-CN-XiaoyiNeural`. Avoid `zf_xiaobei` unless requested.
- If synthetic voice is unsuitable, deliver a human-recording script and wait for audio before the final voiced render.
- Apply captions last so overlays cannot hide them.

### 7. Validate pilot — approval gate 3

- Run relevant HyperFrames lint, validate, and draft-render checks.
- Inspect hook, main evidence, CTA, first/last two seconds, and every significant screenshot transition.
- Verify audio presence, duration, aspect ratio, caption safe area, font rendering, source-screen readability, and factual consistency with `source-map.md`.
- For every `source-recut` jump cut, re-transcribe or audition the assembled proxy to check sentence order, missing syllables, duplicated words, and A/V duration agreement. FFmpeg timestamp warnings are not proof of corruption, but must trigger this check.
- Present one pilot first. Stop for approval before batch production.

### 7.5 Make a publishable cover when requested

- Choose a source frame that actually shows the video's topic. Treat the cover title as an editorial claim that must be supported by the clip.
- Keep video aspect and cover aspect separate. A 16:9 source-recut video can have a 3:4 portrait cover, but the cover does not turn the video itself vertical. Recompose the title, source evidence, and optional speaker bubble on the portrait canvas; never just crop the finished horizontal cover.
- When the user supplies cover examples or requests varied styles, read [references/cover_style_guide.md](references/cover_style_guide.md). Optional private inspiration screenshots may be installed separately; the guide remains usable without them. Treat any reference images as visual cues, never assets to paste into output. Select a style by topic evidence and available image quality, and keep the cover title readable at mobile thumbnail size. Do not force one palette onto every clip when the user asks for variety.
- For text-heavy lesson screens, first try one clear headline, one meaningful source-screen fragment, and intentional empty space. Remove duplicate headings, keyword lists, captions, and decorative labels before merely shrinking them. This is a tested preference for the user's current series, not a universal template; change composition when the source or user preference warrants it.
- For 16:9 screen recordings, keep the topic-bearing UI inside a framed panel and put a short, readable title outside it. Remove browser chrome and taskbar with an explicit source-pixel crop; use opaque redaction rectangles for visible private paths, accounts, or names. Do not claim that cropping replaces a full privacy review.
- Use [scripts/make_screen_cover.py](scripts/make_screen_cover.py) for the existing 16:9 layout. For a simple 3:4 layout with a headline and one evidence panel, use [scripts/make_portrait_cover.py](scripts/make_portrait_cover.py) and the manifest guidance in [references/cover_style_guide.md](references/cover_style_guide.md). Both scripts use source-pixel crops/redactions and refuse to overwrite without `--overwrite`. Use a custom composition when the source cannot fit the preset legibly.
- Keep raw frame grabs separate from final covers. Review every final cover at full size and as a 270×360 mobile thumbnail; inspect the screenshot region for unmasked private or stale product details before publishing. Present a pilot before applying the cover style across the series.

### 8. Freeze and batch

- After pilot approval, set `profile_status: frozen` in `project-profile.yaml`.
- Reuse approved video aspect, font files, caption layout, voice, CTA policy, and disclosure boundary across the series. Track cover aspect separately from video aspect.
- Reuse approved cover hierarchy and series marker, but allow per-video palette and arrangement when the user has asked for varied covers. Do not turn one successful cover into a universal template. Keep per-video changes grounded in topic, evidence, screenshot framing, and legibility.
- Reopen approval when a requested change alters the frozen brand/content policy or when the source cannot work within the preset.

## Outputs

For topic mining, return a table containing source time, title, style, hook, dry-good point, visual plan, CTA, and failure risk.

For each developed video, preserve:

```text
<output>/
├── structure.md
├── source-map.md
├── project-profile.yaml
├── script.md
├── preview.mp4
├── final.mp4
└── covers/
```

For a pilot or final render, report file path, duration/aspect, voice, profile status, source-map risks, validation performed, and the next required decision.
