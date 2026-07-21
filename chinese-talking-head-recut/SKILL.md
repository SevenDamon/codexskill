---
name: chinese-talking-head-recut
description: Restructure long, unscripted Chinese talking-head recordings into one or more publishable vertical short videos. Use when a user provides a Chinese one-take monologue, interview, lesson, vlog, or rambling oral recording and wants transcript-led topic splitting, narrative reordering, removal of mistakes/fillers/ringtones, Chinese emphasized subtitles, reference-based covers, and verified final renders. Orchestrates video-use rather than replacing its transcription and production-correct rendering rules.
---

# Chinese Talking-Head Recut

Turn a loose Chinese oral recording into several independent stories. Use `video-use` for transcription, word-boundary cuts, audio fades, rendering, and timeline verification.

## Workflow

1. Read the `video-use` skill completely. Treat its hard rules as mandatory.
2. Inventory the source and reuse any cached word-level transcript. Never retranscribe an unchanged source.
3. Read the packed transcript once. Identify distinct claims or stories, not merely chronological chapters.
4. Propose the smallest defensible set of videos. For each, state:
   - one-sentence promise;
   - hook, evidence, conclusion, CTA;
   - estimated runtime;
   - overlap with other proposed videos;
   - missing evidence or title risk.
5. Audit counted promises before confirmation. If the title or speech promises N items, choices, steps, mistakes, or lessons, map all N to explicit beats. Do not count a later item used only as the hook as also fulfilled in the body unless the body clearly labels or restates it.
6. Get human confirmation of the split and the first structure before cutting. Confirmation such as “按推荐结构剪” authorizes execution.
7. Create one project subdirectory per output under `<source_dir>/edit/videoN/`. Keep the source immutable and share/copy only the cached transcript.
8. Build the EDL on word boundaries. Prefer 30–200 ms padding and silence gaps. Remove false starts, repetitions, unrelated branches, and detected sound events. Do not cut inside a word to hide a ringtone; start from the next grammatical word or rewrite the structure.
9. Render a cut-only draft. Inspect every boundary with `timeline_view.py`, plus the first and last two seconds.
10. Add subtitles only after the cut passes. Generate semantic Chinese chunks, normally 6–12 Han characters, allowing a longer chunk to preserve a complete keyword. Use native ASS when colored keyword emphasis is required.
11. Generate an independent cover from a strong source frame. Do not prepend the cover to the video unless requested.
12. Render the final at source aspect and requested/source frame rate. Normalize audio, verify duration/specs, and sample captions and keyword color. Repeat the counted-promise audit against the rendered timeline and subtitles.
13. Append decisions and outstanding risks to `<source_dir>/edit/project.md`.

## Editorial rules

- A video needs one promise. Split autobiography, tutorial, warning, and opinion into separate videos when each has enough evidence.
- Do not label a video “教程” or “方法” unless the source demonstrates concrete steps or tools.
- Lead with the strongest claim or contrast, then restore chronology only if needed for comprehension.
- Reuse a short CTA across outputs when it matches, but minimize repeated body material.
- Prefer three strong videos over four thin ones. Reject a proposed video if it depends mainly on repeated material.
- Static close-ups usually benefit from direct jump cuts. Do not add decorative transitions to conceal weak cuts.
- Treat cover/title claims as editorial claims: they must be supported by spoken content.
- Preserve sequence for counted narratives by default: overview → item 1 → item 2 → … → item N → conclusion. If an item is pulled forward as a hook, either restate it in sequence or mark the return explicitly with chapter text/audio.

For detailed selection and QA checks, read [references/editorial-qa.md](references/editorial-qa.md).

## Chinese subtitle and cover defaults

Adapt to user references. If none exist, use:

- subtitle: Microsoft YaHei Bold or available Chinese bold sans; white; black outline; 72–82 px at 1080×1920; yellow emphasis; one semantic line when possible; around 70–76% of frame height;
- highlight only terms carrying the argument: numbers, contrast, decisions, named tools, and outcomes;
- cover: two lines over a restrained dark gradient plate, white setup plus yellow/orange payoff; keep face and eyes unobstructed;
- no automatic color grade unless the source visibly needs correction.

Use [scripts/srt_to_ass.py](scripts/srt_to_ass.py) to preserve inline ASS colors that SRT parsers may discard. Use [scripts/make_cover.py](scripts/make_cover.py) for a deterministic reference-style cover.

## Windows safeguards

- Read and write JSON, SRT, ASS, and concat lists explicitly as UTF-8.
- Use forward slashes in FFmpeg subtitle filter paths and escape the drive colon.
- Decode captured FFmpeg output with `encoding="utf-8", errors="replace"`.
- Pass Chinese filesystem paths through PowerShell variables/environment variables instead of non-UTF-8 stdin literals.

## Handoff

Return clickable links to the final video, cover, and EDL. State runtime and technical specs. Name the single most important editorial question the user should judge; do not ask for generic feedback.
