# Codex Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

可复用的 Codex Skills 合集，覆盖证件照处理、内容配图、短视频制作、HTML 演示稿、产品立项与小红书图文卡片。每个目录都是可单独安装的 skill；请复制整个目录，而不只是 `SKILL.md`。

## Skills 介绍表

| Skill | 介绍与适用场景 | 输入 → 输出 | 主要依赖 | 使用方法 |
| --- | --- | --- | --- | --- |
| [id-photo](id-photo/) | 人像抠图、换底、构图裁切及体积压缩，适合报名照和学籍照制作 | 正面人像及规格 → JPG / 透明 PNG，可批量多规格 | Python 3.10+、NumPy、Pillow、ONNX Runtime、U²-Net 模型 | [证件照使用方法](#id-photo) |
| [chinese-talking-head-recut](chinese-talking-head-recut/) | 将散乱中文长口播按独立主题重组，处理口误、重复和话题跳跃 | 原视频及目标 → 竖屏短视频、字幕和封面 | 外部 `video-use` skill、FFmpeg / FFprobe、Python / Pillow；新转录需 ElevenLabs API key | [口播重剪使用方法](#chinese-talking-head-recut) |
| [damon-zhihu-image](damon-zhihu-image/) | 根据文章语义生成知乎配图，支持摄影合成、扁平插画、极简白底和手绘速写 | 文章段落及风格 → 默认 16:9、2K 配图 | Node.js / npx、Bun（通过 npx 运行）、火山方舟 API key | [知乎配图使用方法](#damon-zhihu-image) |
| [html-ppt-author](html-ppt-author/) | 新建、改造与检查可离线编辑的 HTML 演示稿，支持文字编辑、图片替换及拖动缩放 | 大纲或已有 HTML → 可编辑 HTML 演示稿及检查结果 | 浏览器；Full 保存与 PDF / PPTX 导出需外部 HTML PPT Toolkit | [HTML PPT 使用方法](#html-ppt-author) |
| [product-kickoff-review](product-kickoff-review/) | 编码前审查付费意愿、定价、持续付费和 AI 辅助交付风险，再定义 MVP | 产品想法及业务背景 → 立项判断、MVP、PRD / 文档 / TODO 规划 | 可使用 skill 的 Agent；基础审查无需额外 API key | [立项审查使用方法](#product-kickoff-review) |
| [story-video-director](story-video-director/) | 将故事或课文分解为可审阅的视觉事件，管理人物、场景、姿态和镜头连续性 | 故事、对白或场景描述 → 一致性卡、分段表、导演板及 Seedance 提示词 | 规划阶段使用 Agent；实际出图、生成视频需另备对应工具 | [故事导演使用方法](#story-video-director) |
| [xhs-longform-cards](xhs-longform-cards/) | 将中文长文整理为小红书多图卡片，提供本地预览和 PNG 导出工具 | 中文长文 → 默认 450×600 PNG 卡片及本地预览 | Node.js、npm、Puppeteer 及可用浏览器环境 | [图文卡片使用方法](#xhs-longform-cards) |

## 安装与调用

先克隆仓库，再按需安装。下面以 `id-photo` 为例，安装其他 skill 时替换目录名即可。更新已有安装前先备份本地修改。

### Windows PowerShell

```powershell
git clone https://github.com/SevenDamon/codexskill.git
cd codexskill
$skillName = "id-photo"
$skillsRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $env:USERPROFILE ".codex\skills" }
$destination = Join-Path $skillsRoot $skillName
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Path ".\$skillName\*" -Destination $destination -Recurse -Force
```

### macOS / Linux

```bash
git clone https://github.com/SevenDamon/codexskill.git
cd codexskill
skill_name="id-photo"
skills_root="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills_root/$skill_name"
cp -R "./$skill_name/." "$skills_root/$skill_name/"
```

安装后重新开启 Codex 对话；若技能列表未刷新，重启客户端。下面的 `$skill-name` 是在 **Codex 对话框**输入的调用方式，不是终端命令。脚本命令示例均以仓库根目录为起点，除非另有说明。

## 各 Skill 的使用方法

### id-photo

自动抠人像、换纯色底、按头部比例裁切，并尝试压缩到指定大小。支持内置尺寸、RGB 自定义底色和一次输出多规格。详细说明见 [README](id-photo/README.md)，处理边界见 [技术参考](id-photo/references/technique.md)。

**准备：** 安装 Python 3.10+ 和依赖：

```bash
python -m pip install numpy onnxruntime Pillow
python id-photo/scripts/idphoto.py --list
```

首次实际处理会下载 U²-Net 模型（约 168 MiB），默认缓存到 `~/.workbuddy/models/u2net.onnx`；这是原工具的共享缓存位置，在 Codex 下也保留。可通过 `--model` 指向其他位置的模型文件。模型就绪后，脚本在本机处理照片。

**在 Codex 中调用：**

```text
使用 $id-photo，把附件中的正面半身照处理成 236×315 像素的证件照，
底色 RGB(67,142,219)，JPG，不超过 60KB，不做肤色美白。
请检查头顶留白、肩部完整度、头发边缘、实际尺寸及文件大小，输出到指定目录。
```

**也可直接运行：**

```bash
python id-photo/scripts/idphoto.py --src photo.jpg --spec "236x315@67-142-219" --out out.jpg --max-kb 60
python id-photo/scripts/idphoto.py --src photo.jpg --spec "一寸+蓝,二寸+白,学籍照+淡蓝" --outdir ./out
python id-photo/scripts/idphoto.py --src photo.jpg --spec "600x800" --out transparent.png
```

**注意：** 内置“一寸”为 236×315，“一寸标准”为 295×413，“学籍照”为 358×441；这些是工具预设，不代表所有单位的要求。请优先提供接收方要求的像素、底色、格式和体积。默认 `--gamma 0.68` 会整体提亮，`--gamma 1` 可关闭；`--skin-gamma` 仅在需要肤色美白时启用。全身照、侧脸、遮挡或复杂背景容易失败；压缩后仍可能超限，必须核验成品。工具不能保证通过报名或证件审核。

### chinese-talking-head-recut

先从逐字稿识别独立选题，再重排钩子、证据、结论与 CTA；确认结构后进行词边界剪切，生成中文字幕、关键词和封面。适合未写稿的一镜到底中文口播，不适合以屏幕操作为主的课程录屏。详见 [SKILL.md](chinese-talking-head-recut/SKILL.md)。

**准备：** 另行安装 [video-use](https://github.com/browser-use/video-use)，配置 FFmpeg / FFprobe、Python / Pillow。只有新转录需要 ElevenLabs API key，已有缓存逐字稿可复用。

**调用示例：**

```text
使用 $chinese-talking-head-recut 处理这段中文长口播：<视频路径>。
面向初学者，拆成 2～3 条独立主题的竖屏短视频，每条约 60～90 秒。
先提供选题和重组结构供我确认，再剪辑；去掉口误、重复、铃声和无关支线。
最终交付字幕、关键词高亮、封面和成片，并核对标题中的数量承诺。
```

### damon-zhihu-image

先理解文本含义并选择风格，再调用内置 Seedream 脚本生成图片。详见 [SKILL.md](damon-zhihu-image/SKILL.md)。

**准备：** 安装 Node.js（含 `npx`），在用户目录 `.damon-skills/.env` 中设置：

```dotenv
ARK_API_KEY=replace-with-your-volcengine-ark-api-key
```

创建 `.damon-skills/damon-imagine/EXTEND.md`，内容如下：

```yaml
---
version: 1
default_provider: seedream
default_quality: 2k
default_aspect_ratio: 16:9
---
```

Windows 用户目录通常是 `C:\Users\<用户名>`，macOS / Linux 为 `$HOME`。API key 仅保存在本机；已有配置请追加或修改对应字段，不要覆盖其他密钥。该 skill 会调用外部图片 API，需有可用额度。

**调用示例：**

```text
使用 $damon-zhihu-image，为下面这段知乎回答生成一张 16:9 配图。
风格选极简白底，不在图上叠加文字，突出“学习路径的选择”。
正文：<粘贴回答段落及必要上下文>
```

![知乎配图示例](damon-zhihu-image/assets/cover.png)

### html-ppt-author

适合新建演示稿、为已有 HTML 安装编辑器，或只检查兼容性。默认 Lite 支持网页内编辑；Full 的源文件保存、PDF / PPTX 导出需配合 [HTML PPT Toolkit](https://github.com/SevenDamon/HTML-PPT-Toolkit)。详见 [使用说明](html-ppt-author/README.md)。

**调用示例：**

```text
使用 $html-ppt-author，根据以下大纲制作 8 页可离线编辑的 HTML 演示稿。
使用 Lite，16:9，支持文字编辑、图片替换、拖动缩放和导出新版 HTML。
输出到新目录，完成兼容性检查和浏览器实测。
大纲：<粘贴大纲>
```

改造已有 HTML 时，请说明输入路径、要修改的内容、保留项以及 Lite / Full 选择。Full HTML 与同级 `html-ppt-editor/` 文件夹需一起移动或分享；没有工作台，仅安装工具栏无法获得导出后台。

### product-kickoff-review

面向非技术创始人和依赖 AI 构建产品的人。先判断谁付钱、为什么付钱、能否持续付钱，再检查交付风险；通过后才进入 MVP 和项目文档。详见 [SKILL.md](product-kickoff-review/SKILL.md)。

**准备：** 提供目标客户、痛点、现有替代方案、定价假设、预算和时间限制。基础流程无需安装额外运行时。

**调用示例：**

```text
使用 $product-kickoff-review 审查这个产品想法，先不要写代码。
产品：<一句话描述>；付费客户：<客户群>；痛点：<具体问题>。
现有替代方案：<方案>；定价假设：<价格>；预算与时间：<限制>。
先判断最可能失败的原因和需要验证的商业假设。
如果值得继续，再定义最小 MVP、PRD、文档结构和 TODO。
```

商业审查可能得出暂缓或缩小范围的结论；它不等于市场需求已经被验证，也不适用于已明确范围的小修复。

### story-video-director

将课文、故事、对白或短片构想变成分阶段的视频制作材料，重点是人物、道具、场景、声音和镜头连续性。详见 [README](story-video-director/README.md) 和 [SKILL.md](story-video-director/SKILL.md)。

**准备：** 一段故事或场景描述即可开始；参考图片、音频和上一段尾帧可在后续补充。明确用途、风格、改编尺度和生成模式。实际图片、视频生成工具需另行准备。

**调用示例：**

```text
使用 $story-video-director，将以下故事规划成 4 段 AI 视频。
用途：课堂导入；风格：克制电影感；改编尺度：基本忠实原文。
先做可视化可行性诊断、人物与场景一致性卡和分段表。
我选择片段后，再生成导演板提示词和 Seedance 提示词。
当前只做导演板，最终时长待生成模式和音频确认。
故事：<粘贴原文>
```

交付的是制作规划和提示词，不能把它理解成一键生成成片。多段视频先锁定一致性资产，再制作分段提示词；时长按该 skill 中的生成模式约束确认。

### xhs-longform-cards

把中文长文拆成开场、核心内容和收尾卡片，默认输出 450×600 PNG；HTML 用于预览和截图。内置复古知识手账、极简现代、清新治愈手绘、可爱涂鸦、孟菲斯几何五种样式。详见 [SKILL.md](xhs-longform-cards/SKILL.md)。

**调用示例：**

```text
使用 $xhs-longform-cards，把下面长文整理成 5 张小红书知识卡片。
使用极简现代风格，每张只表达一个要点，尺寸 450×600。
最终交付 PNG 图片和本地预览，检查中文显示及文字溢出。
正文：<粘贴长文>
```

**需要可反复使用的本地工具时：** 先安装 Node.js，再在仓库根目录执行。目标目录请选择新目录，脚手架拒绝覆盖同名文件。

```powershell
node xhs-longform-cards/scripts/scaffold.js ../my-xhs-cards
cd ../my-xhs-cards
npm.cmd install
node server.js
```

macOS / Linux 将 `npm.cmd install` 改为 `npm install`。打开 `http://localhost:3000` 预览，下载单张或全部 PNG。首次安装依赖可能需要下载浏览器；长文应先压缩或拆页，避免固定画布溢出。

## 仓库结构

```text
skill-name/
  SKILL.md          # 技能名称、触发条件与工作流程（必需）
  README.md         # 面向使用者的说明（可选）
  agents/           # Agent 元数据（可选）
  references/       # 按需阅读的参考资料（可选）
  scripts/          # 执行脚本（可选）
  assets/           # 模板与静态素材（可选）
```

只安装需要的 skill。仓库不包含外部 API 凭据、U²-Net 模型、用户原始素材或生成结果；各项依赖按对应 skill 配置。

## 开源许可证

除另有说明的内容外，本仓库的代码、技能文档和随附素材采用 [MIT License](LICENSE)，版权归 SevenDamon 所有。允许使用、复制、修改、分发和商业使用；分发副本或实质性部分时，须保留版权声明与许可证正文。软件按原样提供，不附带担保。

- 每个 skill 目录均附有 `LICENSE`，单独复制或分发 skill 时请一并保留。
- `xhs-longform-cards/assets/local-card-app/` 已声明使用 ISC，继续按该目录中的 [ISC License](xhs-longform-cards/assets/local-card-app/LICENSE) 授权；其 `package.json` 的许可证字段保持不变。
- 外部依赖、另行下载的模型权重、API 服务及用户提供的素材适用各自许可证或服务条款，本仓库的 MIT 许可证不改变这些授权。
- `html-ppt-author` 是同一维护者的 HTML PPT Toolkit 的便携发布副本；本许可证适用于本仓库内的发布内容，不修改外部仓库的许可证设置。

安装说明中的目录复制应包含许可证文件；分享小红书本地应用时，也须保留其内置 ISC 许可证。
