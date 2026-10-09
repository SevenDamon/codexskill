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
  cover:
    aspect: "3:4" # independent of video.aspect; choose for the actual destination
    resolution: "1080x1440"
    title_font_file: ""
    title_font_size: 92
    title_max_lines: 2
    layout: headline-plus-source-evidence
  captions:
    font_file: ""
    font_size: 58
    font_weight: 700
    fill: "#FFFFFF"
    stroke: "#111111"
    stroke_width: 5
    bottom_margin: 110
    max_chars_per_line: 14
approvals:
  topic: false
  structure_and_boundary: false
  visual_profile: false
  pilot: false
```

Treat reference-image font and color matches as candidates. Freeze only real font files and explicit numeric sizes approved by the user.
