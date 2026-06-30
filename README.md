# Codex Skills

This repository stores reusable Codex skills.

## Skills

### damon-zhihu-image

Zhihu image generation skill for matching article paragraphs with 16:9 illustrations.

Use it when you need:

- cover images for Zhihu answers;
- illustrations that match article paragraphs;
- Seedream/Volcengine image generation through local API key configuration.

Path:

```text
damon-zhihu-image/
```

Default invocation:

```text
Use $damon-zhihu-image to generate a 16:9 Zhihu cover image for this paragraph.
```

Quick start for Windows PowerShell:

```powershell
git clone https://github.com/SevenDamon/codexskill.git
cd codexskill
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\damon-zhihu-image "$env:USERPROFILE\.codex\skills\damon-zhihu-image"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.damon-skills\damon-imagine" | Out-Null
Set-Content -Encoding UTF8 "$env:USERPROFILE\.damon-skills\.env" "ARK_API_KEY=replace-with-your-volcengine-ark-api-key"
@'
---
version: 1
default_provider: seedream
default_quality: 2k
default_aspect_ratio: 16:9
---
'@ | Set-Content -Encoding UTF8 "$env:USERPROFILE\.damon-skills\damon-imagine\EXTEND.md"
```

Quick start for macOS/Linux:

```bash
git clone https://github.com/SevenDamon/codexskill.git
cd codexskill
mkdir -p "$HOME/.codex/skills" "$HOME/.damon-skills/damon-imagine"
cp -R ./damon-zhihu-image "$HOME/.codex/skills/damon-zhihu-image"
printf 'ARK_API_KEY=replace-with-your-volcengine-ark-api-key\n' > "$HOME/.damon-skills/.env"
cat > "$HOME/.damon-skills/damon-imagine/EXTEND.md" << 'EOF'
---
version: 1
default_provider: seedream
default_quality: 2k
default_aspect_ratio: 16:9
---
EOF
```

After configuration, restart Codex and ask:

```text
Use $damon-zhihu-image to generate a 16:9 Zhihu cover image for this paragraph:
把你的文章段落粘贴在这里。
```

If it fails, check these first:

- Replace `replace-with-your-volcengine-ark-api-key` with a real Volcengine Ark API key.
- Make sure Node.js provides `npx`; the skill runs Bun through `npx -y bun`.
- Restart Codex after copying the skill directory.

### product-kickoff-review

Product kickoff review workflow for non-technical founders and AI-assisted builders.

Use it before coding a new product idea to check:

- whether anyone will pay;
- what price can be justified;
- whether customers will keep paying;
- whether the project can be delivered safely with AI agents;
- what PRD, architecture, data, prompt, evaluation, and TODO docs should exist before implementation.

Path:

```text
product-kickoff-review/
```

Default invocation:

```text
Use $product-kickoff-review to validate this product idea, define the MVP, and create the initial PRD/docs/TODO plan.
```

### story-video-director

Story-to-video direction skill.

### xhs-longform-cards

Xiaohongshu long-form card generation skill.

## Install A Skill Locally

Copy a skill directory into your local Codex skills folder:

```powershell
Copy-Item -Recurse .\damon-zhihu-image "$env:USERPROFILE\.codex\skills\damon-zhihu-image"
```

Restart Codex if the skill list does not refresh automatically.

## Repository Layout

Each skill should keep the standard structure:

```text
skill-name/
  SKILL.md
  agents/
    openai.yaml
  references/
    ...
```

Avoid adding extra files inside a skill directory unless they directly support that skill.
