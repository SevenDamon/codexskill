---
name: xhs-longform-cards
description: Use when converting Chinese long-form text into Xiaohongshu-style multi-image cards, creating local 450x600 card image exports, recreating a long-text-to-images workflow, or scaffolding a Node/Puppeteer preview-and-screenshot tool where PNG images are the final deliverable and HTML is only a preview/intermediate artifact.
---

# XHS Longform Cards

Create local Xiaohongshu-style card image workflows from Chinese long-form text. The final deliverable is PNG images. HTML is only for preview, layout inspection, and screenshot capture.

## First Judgment

Before building anything, check the user's real goal:

- If they ask for **images/files**, produce or scaffold a workflow that exports PNGs.
- If they ask for **a reusable local tool**, scaffold the bundled app in `assets/local-card-app`.
- If they provide only a prompt library, treat it as style reference, not a runnable project.
- If they want Gemini/LLM-generated HTML, keep that as an optional content-generation layer; do not make it required for local export.

Likely failure points to surface:

- A prompt-only solution does not guarantee reproducible images.
- Long Chinese text will overflow 450x600 cards unless content is aggressively summarized or split.
- Browser screenshots are more reliable than client-side DOM-to-image libraries for Chinese fonts and complex CSS.
- `npm` in PowerShell may fail due to execution policy; use `npm.cmd`.
- Network fonts/CDNs make exports fragile; prefer local/system fonts for the default tool.

## Workflow

1. **Choose output mode**
   - For a reusable project: copy `assets/local-card-app` to the target folder.
   - For a one-off result: create or adapt a local HTML preview, then screenshot each card with Puppeteer.

2. **Generate card content**
   - Build at least 3 cards: opening, core content, closing.
   - Default size: `450px` wide by `600px` high.
   - Use 2-5 core cards for ordinary long text; use more only when the user explicitly wants it.
   - Keep each card to one information task. Prefer bullets, short quotes, and compressed claims.

3. **Design constraints**
   - Default style: vintage didactic journaling / knowledge cards.
   - The bundled local app includes 5 selectable local styles: vintage didactic journaling, minimalist modern, fresh healing hand-drawn, cute cartoon/doodle, and Memphis geometric.
   - Use CSS texture, borders, labels, quotes, and typographic hierarchy.
   - Do not add decorative corner labels such as `OPENING`, `CORE NOTE`, or generic keyword strings unless the user explicitly asks for them.
   - Corner and footer text must carry content value. A page number and date are acceptable; unrelated style labels are not.
   - Do not rely on external images, online fonts, Tailwind CDN, or dom-to-image-more for the default local workflow.
   - Use flex/grid for card layout. Avoid absolute positioning for main text.
   - Buttons and UI controls must sit outside the `.xhs-card` screenshot target.

4. **Export images**
   - Use the local Node endpoint `POST /api/screenshot`.
   - Request body contract: `{ "fullHtml": document.documentElement.outerHTML, "cardId": "card-1" }`.
   - Return PNG blobs and trigger downloads with safe Chinese filenames.
   - For batch download, wait briefly between cards so rendering and download events settle.

5. **Validate**
   - Start with `npm.cmd install`, then `node server.js`.
   - Open `http://localhost:3000`.
   - Confirm generated cards are visible, horizontal, fixed at 450x600, and not visibly overflowing.
   - Download one card and all cards.
   - Inspect at least one PNG dimensions and confirm Chinese text is not garbled.

## Bundled App

Use `scripts/scaffold.js` to copy the bundled local app:

```powershell
node scripts/scaffold.js E:\path\to\new-project
```

Then run:

```powershell
cd E:\path\to\new-project
npm.cmd install
node server.js
```

If dependency installation needs network access and fails, ask for approval to run `npm.cmd install` with network access, or ask the user for an existing `node_modules`/package cache.

## Style References

For style variants or prompt wording, read `references/style-prompts.md` only when needed. Keep `SKILL.md` focused on process and judgment.
