# Cover inspiration and adaptation

This public guide describes eight optional inspiration styles. The user's original Canva/Xiaohongshu screenshots are **not included in this public skill**; an authorized user may install them separately in `references/cover-inspirations/`. The guide remains usable without those files. Reference screenshots may contain third-party design, photography, faces, logos, and copy. Inspect them for **abstract design decisions only**. Do not paste, trace, redistribute, or closely recreate their artwork, people, logo treatments, or exact text. Generated covers should use the user's source footage and original shapes/type composition.

| Ref | Optional private filename | Useful design cue | When it fails for a screen-recorded lesson |
|---|---|---|---|
| 01 | `01-cyan-tech.png` | Electric cyan on near-black; strong hierarchy; technical framing | Too many border motifs overpower a small UI panel |
| 02 | `02-portrait-editorial.png` | Dark portrait plus expressive type | Requires a high-resolution, intentionally lit portrait; a 200px webinar bubble is not enough |
| 03 | `03-workflow-board.png` | Large promise and a compact process strip | Small screenshot labels become illegible on a phone |
| 04 | `04-quiet-lesson.png` | Authentic teaching frame; restrained type; generous negative space | Weak if the source frame lacks an obvious teaching action |
| 05 | `05-orange-contrast.png` | Warm accent and bold split headline | A fake oversized speaker portrait misrepresents a screen recording |
| 06 | `06-cosmic-minimal.png` | One evocative visual and very few words | Decorative imagery can bury the actual lesson evidence |
| 07 | `07-lifestyle-center.png` | Real-world photograph with central title | Only appropriate if the source genuinely contains that lifestyle subject |
| 08 | `08-yellow-statement.png` | High-contrast yellow emphasis and short opinion headline | Can look like clickbait if the clip does not support the claim |

## Selection rule

Start with the claim and proof in the actual clip, then choose visual grammar. For a UI-led explanation, use a legible source-screen excerpt, perhaps with 01/03/08's hierarchy; for a truly human-led clip with a good portrait, 02/04/05 may fit. Avoid 06/07 merely because they look attractive if their metaphor or photo has no source relationship. Keep varied covers within a series coherent through a modest common marker (series name, numbering, or type family), not a forced identical layout.

## Aspect and legibility

Treat 16:9 horizontal and 3:4 portrait as separate compositions. The portrait cover should use a cropped **evidence region**, not a shrunk full desktop; make the title readable at roughly 270×360 preview size. Avoid putting key text against the edges because feed and profile previews may crop differently. Verify the actual publication crop in the user's app before publishing. A portrait cover alone does not change the video's 16:9 playback.

Use explicit title and small-label font sizes, record the selected font file and license, and inspect full-resolution and mobile previews. Redact private account names, file paths, and project identifiers in source screenshots before they enter a cover. Do not promote stale UI prices, model multipliers, or unverified performance numbers into headline claims.

## Tested sparse direction for screen lessons

In the user's 2026-09-29 lesson series, covers 02/03/04/06 were preferred; dense versions of 01 and 05 felt cramped even when their colors suited the content. Removing repeated headings, three-item lists, and explanatory footers improved those two covers. For future *similar* screen-recorded lessons, consider a single short hook, one source-frame evidence region, and visible breathing room. This is project feedback, not permission to force the same palette or layout onto every video. If the source proof itself is a text-heavy slide, crop to the few lines needed to establish the topic; the cover need not teach the whole lesson.

## Portrait script

For that simple composition, run `scripts/make_portrait_cover.py` with a UTF-8 JSON manifest. Relative paths resolve from the manifest directory. The source can be an image or a video frame selected by `at`; all `crop` and `redact` coordinates are in original source pixels. The script makes a 1080×1440 image and a 270×360 `-mobile.png` preview. It preserves the entire selected evidence crop inside the panel rather than blindly cutting it again.

```json
{
  "series_label": "直播精剪",
  "palette": {"background": "#F5F5F1", "foreground": "#191D1E", "accent": "#8F4537"},
  "covers": [{
    "source": "cover-source.png",
    "output": "cover-portrait.png",
    "number": "01",
    "title_lines": ["让 AI 干活", "先说清楚"],
    "title_font_size": 135,
    "label_font_size": 29,
    "crop": [270, 218, 1270, 497],
    "evidence_box": [76, 840, 1004, 1100]
  }]
}
```

The dimensions and words above are illustrative, not a default for new content. Check the chosen installed fonts (the script defaults to Windows Microsoft YaHei, not a redistributable font asset) and inspect the mobile preview. If a source fragment needs a different composition, draw it deliberately instead of adding more text or shrinking the whole desktop.
