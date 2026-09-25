# Holographic foil route

Use this route for a single character artwork with physical depth and foil shimmer.

Prepare four aligned transparent PNG layers: `background.png`, `subject.png`, `lineart.png`, and `text.png`. The background carries the full environmental painting and foil foundation. The subject isolates the character and primary foreground effects. Lineart reinforces selected ink contours. Text contains only typography and marks.

The Blender builder places the layers at separate depths over a card body, adds foil and sparkle geometry, renders previews, and exports a GLB. Keep the character readable when the camera tilts. Use `config.holographic.example.json` as the starting config and run:

```powershell
python scripts/run_pipeline.py --project <project-dir> --mode holographic
```

This route is the default when no two-state or lenticular behavior is requested.

## Web presentation

Keep the holographic viewer visually quiet so the card carries the experience. Use a flat white canvas, black sans-serif typography, no border around the card stage, and no decorative seals, framed panels, feature claims, archive copy, or “about this card” section. Show only the studio wordmark, card title metadata, direct card actions, and the four material/depth sliders. Buttons remain flat and borderless. The generated card back uses simple English typography instead of an ornamental emblem.

Do not apply these interface rules to the two-image lenticular viewer; that route has its own template and interaction model.
