# Codex Skills

This repository stores reusable Codex skills.

## Skills

### chinese-talking-head-recut

`chinese-talking-head-recut` 是一个面向中文散乱口播的重组剪辑 Skill。它会先通过逐字稿识别独立选题，再将一镜到底、存在口误、重复或话题跳跃的长口播，重组为一条或多条可发布的竖屏短视频。

项目功能：

- 从长口播中拆分多个独立主题，而不是只按原时间线切片。
- 重排钩子、证据、结论和 CTA，并在真正剪辑前让人确认结构。
- 按词边界删除口误、重复、假开头、铃声和无关支线。
- 生成中文语义字幕、黄色关键词和独立封面。
- 逐个检查剪切边界、音频波形、字幕大小和最终输出规格。
- 对“三个选择”“四个步骤”这类计数型叙事执行强制数量审计，避免标题承诺与正文不一致。

适用于：

- 没有写稿、一镜到底的中文口播；
- 长口播拆成多条独立选题；
- 口误、重复、停顿和干扰声较多的原始素材；
- 需要重排叙事，而不是只做去停顿的口播。

不适合直接处理以屏幕操作为主的课程录屏、直播回放、多机位剧情片，或已经剪好只需视觉包装的视频。

依赖：

- 已安装的 [`video-use`](https://github.com/browser-use/video-use) Skill，用于逐字稿、词边界切片、音频淡化和渲染；
- FFmpeg / FFprobe；
- Python 和 Pillow（封面脚本）；
- ElevenLabs API key（仅在需要新转录时使用，已缓存逐字稿时不会重复调用）。

Path:

```text
chinese-talking-head-recut/
```

Default invocation:

```text
Use $chinese-talking-head-recut to restructure this raw Chinese talking-head recording into publishable short videos.
```

Windows PowerShell 安装：

```powershell
git clone https://github.com/SevenDamon/codexskill.git
cd codexskill
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\chinese-talking-head-recut "$env:USERPROFILE\.codex\skills\chinese-talking-head-recut"
```

复制完成后重启 Codex，并确认 `video-use` 及其转录环境已正确配置。

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

例如安装中文口播重剪 Skill：

```powershell
Copy-Item -Recurse -Force .\chinese-talking-head-recut "$env:USERPROFILE\.codex\skills\chinese-talking-head-recut"
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
  scripts/
    ...
```

Avoid adding extra files inside a skill directory unless they directly support that skill.
