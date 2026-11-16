# Horizontal Screen Footage: Reusable Frame Decision

Use this when the source or an insert is a horizontal screen recording, filmed monitor, software demo, PPT, code view, or browser tutorial intended for Xiaohongshu. This is a decision workflow, not a preset crop. Do not reuse crop coordinates, fonts, or labels from another video without checking the new source.

## Decide before rendering

1. Probe source resolution, aspect, duration, and audio. Distinguish a native digital screen recording from a camera recording of a display. Upscaling the latter does not restore unreadable text.
2. Identify the information the viewer must see at each beat: whole-screen relationships, a local control, a speaker, or two regions at once. Check the smallest important text at the target phone display size.
3. Choose the least destructive layout:
   - **Keep horizontal** when a full PPT, code editor, spreadsheet, multi-panel UI, or navigation path must remain visible. Make a separate mobile-readable cover; do not assume video and cover need the same aspect.
   - **Recompose vertically** when the lesson follows one local control or small UI region at a time. Use shot-specific crops/pan-and-zoom, a clear title or short step label, and only enough contextual screen to understand the action.
   - **Mixed portrait + screen** when a portrait speaker leads the lesson. Preserve the speaker full-frame and recompose the horizontal demonstration only during its own intervals. Keep original speech and screen action synchronized.
   - **Retain a full-width panel inside a vertical canvas** only when preserving the whole UI matters more than its small apparent size; do not decorate unused space while essential text remains unreadable.
4. If uncertain, make one representative 8–15 second A/B sample (horizontal and recomposed vertical) and inspect both on a phone. Choose by readable teaching evidence, not presumed reach. A publishing UI preview can change crop or safe area; check it before release.

## Render and privacy invariants

- Record the chosen mode, source-to-output time mapping, shot-specific crop regions, target aspect, and any private areas in the project notes. Use source-native pixels for crop/redaction coordinates. Do not carry hard-coded coordinates to a new recording.
- Keep the source immutable. For source recuts, retain the source voice; align any screen insert to the same spoken interval and verify beginning/end transitions.
- If QR codes, names, paths, account identifiers, messages, or sensitive URLs appear, track them through the entire affected shot. A fixed blur can fail when the camera or UI moves. Prefer a crop that **fully excludes** the sensitive region when the lesson remains understandable; otherwise use a tracked opaque mask or sufficiently strong mosaic. Do not leave a partial code visible at frame edges.
- Redaction must survive frame changes, zooms, and transitions. Review every QR-risk transition frame-by-frame and sample the rest of the insert. A QR detector such as FFmpeg `quirc`, if available, is useful as an extra check only: compare against a known-positive source segment and do not interpret zero detections as proof of safety.
- Verify rendered frame size, frame rate, duration, audio presence/sync, screen legibility, important UI not cropped, and the platform's cover/preview crop. State resolution limits or unresolved privacy risk before calling an output publishable.

## Stop condition

If no vertical layout can keep the teaching action readable and private, keep a horizontal video or request a cleaner screen capture. Do not force a portrait conversion because another video in the series used one.
