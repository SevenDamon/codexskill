# Codex Skills

This repository stores reusable Codex skills.

## Skills

### damon-zhihu-image

`damon-zhihu-image` 是一个用于生成知乎配图的 Codex Skill。它会把文章段落、知乎回答草稿或内容提纲转成具体的视觉 prompt，按用户选择的风格生成 16:9 配图，并通过内置脚本调用火山方舟 Seedream 出图。

![damon-zhihu-image cover](damon-zhihu-image/assets/cover.png)

项目功能：

- 为知乎回答、文章段落、内容小节生成匹配配图。
- 根据文本含义生成具体画面，而不是泛泛的装饰图。
- 支持四种常用风格：摄影合成、扁平插画、极简白底、手绘速写。
- API key 只放在本地 `.damon-skills/.env`，不会进入仓库。

设计思路：

- `SKILL.md` 负责告诉 Codex 什么时候使用、如何分析文本、如何选择风格。
- `scripts/main.ts` 和 provider 文件负责稳定执行图片生成，避免每次都临时拼命令。
- 默认使用 Seedream、16:9、2k 输出，适合知乎配图的展示和压缩场景。
- 把 prompt 设计和图片调用分开：Codex 先理解内容并写 prompt，脚本再负责调用模型出图。

使用方法：

1. 把 `damon-zhihu-image/` 复制到本地 Codex skills 目录。
2. 在 `$HOME/.damon-skills/.env` 写入火山方舟 API key：`ARK_API_KEY=...`。
3. 重启 Codex。
4. 让 Codex 使用 `$damon-zhihu-image`，并贴上需要配图的段落。

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
