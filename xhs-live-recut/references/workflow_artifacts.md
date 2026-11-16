# Workflow Artifacts

Use these schemas as compact contracts. Adapt values to the project, but keep the provenance and approval fields.

## source-map.md

```markdown
# Source Map

| Output section | Claim or visual | Source timecode | Treatment | Risk/notes |
|---|---|---:|---|---|
| Hook | ... | 00:12:04–00:12:26 | rewritten | Stronger wording; approve boundary |
| Framework | ... | 00:28:10–00:29:02 | compressed | Meaning preserved |
| Example | dashboard screen | 00:41:20 | verbatim visual | UI text must remain readable |
| Summary | ... | 00:28:10 + 01:03:18 | combined | Distant passages combined |
| CTA | ... | none | newly written | Marketing copy, not source speech |
```

Allowed `Treatment` values:

- `verbatim`: exact source language or unmodified source visual.
- `compressed`: shortened without changing meaning.
- `rewritten`: new wording grounded in one source passage.
- `combined`: synthesis of multiple source passages.
- `newly written`: editorial bridge, hook, or CTA not stated in the source.

Never label rewritten or combined text as a quotation.

## project-profile.yaml

```yaml
version: 1
profile_status: draft # draft | frozen
series_name: ""
content:
  target_audience: ""
  conversion_goal: ""
  style: knowledge-breakdown
  cta_policy: ""
  disclosure_boundary: ""
video:
  aspect: "16:9"
  resolution: "1920x1080"
  fps: 30
voice:
  mode: tts # tts | human-script-only | supplied-audio
  name: "zh-CN-YunxiNeural"
visual:
  reference_images: []
  palette:
    background: "#111111"
    foreground: "#FFFFFF"
    accent: "#FF5A00"
  font_files: []
  motion:
    enabled: false
    placement: ""
    treatments: []
    template_sources: []
  cover:
    aspect: "3:4" # independent of video.aspect; choose for the actual destination
    resolution: "1080x1440"
    title_font_file: ""
    title_font_size: 92
    title_max_lines: 2
    layout: headline-plus-source-evidence
    variants: [] # selected items with aspect and resolution
    portrait_asset: ""
    portrait_placement: ""
    editable_source: true
  captions:
    font_file: ""
    font_size: 58
    font_weight: 700
    fill: "#FFFFFF"
    stroke: "#111111"
    stroke_width: 5
    bottom_margin: 110
    max_chars_per_line: 14
optional_packaging:
  semantic_motion: unasked # unasked | approved | declined
  cover_set: unasked
  portrait: unasked
  publish_copy: unasked
publishing:
  platforms: []
  title_limits: {} # confirmed maximum character counts, keyed by platform
  description_target_chars: null
  topics_enabled: true
  topic_counts: {} # editorial choices, keyed by platform
approvals:
  topic: false
  structure_and_boundary: false
  visual_profile: false
  pilot: false
```

Treat reference-image font and color matches as candidates. Freeze only real font files and explicit numeric sizes approved by the user.

The optional packaging settings are executed when the user requests them or their decision is `approved`. Preserve explicit choices already given in the conversation. For older profiles, resolve missing optional decisions from the active task. Existing `visual.cover.aspect` and `resolution` fields still describe a single cover. Use `visual.cover.variants` only for a selected multi-ratio set, such as items with `aspect: "4:3"` and `resolution: "1600x1200"`.

Once the user selects the tested three-platform setup, `publishing.platforms` can be `["视频号", "小红书", "抖音"]` and `publishing.title_limits` can be `{"视频号": 16, "小红书": 20, "抖音": 20}`. Record the current project's confirmed values. Stage-specific questions and publishing output fields are described in [optional_packaging.md](optional_packaging.md).
