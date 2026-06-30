---
name: damon-zhihu-image
description: 为知乎回答生成配图，根据用户选择的风格，通过 damon-imagine 调用火山引擎豆包模型出图。当需要给知乎回答配图、为文章段落生成插图、或需要与文字内容匹配的视觉图像时使用。使用此 skill 前先确认 damon-qa-voice 是否已触发。
---

# 知乎配图生成器

为知乎回答段落生成匹配的配图，根据用户选择的风格，使用火山引擎豆包（Seedream）模型。

## 前置检查

### 1. 检查 API key 是否已配置

```bash
test -f "$HOME/.damon-skills/.env" && echo "env file exists" || echo "env file missing"
```

如果未配置，让用户在 `$HOME/.damon-skills/.env` 写入自己的火山方舟 API key：

```bash
mkdir -p "$HOME/.damon-skills"
cat > "$HOME/.damon-skills/.env" << 'ENVEOF'
ARK_API_KEY=replace-with-your-volcengine-ark-api-key
ENVEOF
```

不要把真实 `.env` 内容提交到仓库或发送给他人。

### 2. 检查 EXTEND.md 是否已配置

```bash
test -f "$HOME/.damon-skills/damon-imagine/EXTEND.md" && echo "configured" || echo "not configured"
```

如果未配置，先创建默认 EXTEND.md：

```bash
mkdir -p "$HOME/.damon-skills/damon-imagine"
cat > "$HOME/.damon-skills/damon-imagine/EXTEND.md" << 'EXTENDEOF'
---
# damon-imagine preferences
version: 1
default_provider: seedream
default_quality: 2k
default_aspect_ratio: 16:9
---
EXTENDEOF
```

### 3. 检查脚本目录

```bash
ls "$DAMON_ZHIHU_IMAGE_DIR/scripts/main.ts" 2>/dev/null && echo "scripts ready" || echo "scripts missing"
```

脚本已内置在 skill 中，路径为：
- `scripts/main.ts` — 主入口
- `scripts/types.ts` — 类型定义
- `scripts/providers/seedream.ts` — 火山引擎豆包（Seedream）驱动

注意：不要用 AskUserQuestion 问用户确认，直接按 seedream 默认配置写好。

## 输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| **文本内容** | 是 | 需要配图的文章段落，尽量提供上下文 |
| **有无文字** | 否 | 是否在图片上叠加文字。可选：无（默认）、金句、标题 |
| **参考图** | 否 | 已有的参考图片路径 |

## Prompt 工程指南

### 通用 Prompt 原则

先根据文章段落判断画面要表达的具体意思，再按用户选择的风格写 prompt。不要在用户未选择时默认套用某一种视觉风格。

**构图偏好：**
- 每张图只表达一个核心概念
- 主体清晰，背景不要抢戏
- 优先匹配段落里的具体场景，而不是做泛泛装饰图
- 避免不可读的杂乱元素，除非用户明确需要复杂信息感

**Prompt 结构模板：**

```
[已选风格关键词]，[场景描述]，[主体/人物动作]，[光线/色调]，[构图方式]，高质量，细节丰富
```

**示例 Prompt：**

| 内容类型 | 示例 Prompt |
|---------|------------|
| 学习/教育 | [已选风格关键词]，一张书桌的特写，桌面上摊开的笔记本和一杯茶，窗边光线照进来，画面聚焦学习过程，高质量 |
| 科技/AI | [已选风格关键词]，电脑屏幕与桌面设备，屏幕上是不可读的数据图形，画面表达人与 AI 工具协作，高质量 |
| 个人成长 | [已选风格关键词]，一个人站在岔路前，画面有纵深感，表达选择和思考，高质量 |
| 行业观察 | [已选风格关键词]，城市建筑群与室内工作场景形成对比，画面表达行业变化和个体处境，高质量 |

### 风格选择

每次使用 skill 生成配图时，如果本轮对话中尚未选择过风格，先选择风格再写 prompt。选过一次后本轮对话不再重复提问。

**可选风格：**

| 风格 | 适用场景 | Prompt 关键词 |
|------|---------|--------------|
| ① 摄影合成 | 通用、真实场景 | `专业摄影，[场景描述]，[光线/色调]，[构图方式]，摄影合成风格，高质量，细节丰富，电影感色调` |
| ② 扁平插画 | 人文/轻松 | `扁平矢量插画风格，[场景描述]，色块鲜明，简洁有设计感，留白，柔和色彩搭配，高质量` |
| ③ 极简白底 | 干货/方法论 | `极简风格，纯白背景，[主体]居中构图，干净简洁，高质感，产品摄影打光，柔光，高质量` |
| ④ 手绘/速写 | 教育/思维过程 | `铅笔手绘速写风格，[场景描述]，线条质感，不完全着色，草稿感，纸张纹理背景，高质量` |

**选择方式：** 在 Step 1 分析完成后、Step 2 写 prompt 之前，如果本轮对话尚未选择风格，输出风格选项让用户回复编号（1-4），收到编号后记录已选择。后续 Step 2 按对应风格的 Prompt 模板编写。

### 图片文字叠加

如果用户选择叠加文字：

先判断 damon-imagine 的当前模型是否支持 prompt 内文字渲染。如果不稳定，改用以下两步方案：

1. 生成纯图：
   ```bash
   ${BUN_X} ${DAMON_ZHIHU_IMAGE_DIR}/scripts/main.ts --prompt "..." --image output.png --ar 16:9 --quality 2k --provider seedream
   ```
2. 用 ImageMagick（`magick`）或 Python Pillow 叠加文字。如果没有现成工具，直接用 HTML+CSS 生成带文字的图片：
   ```
   用 html 画一个带文字的图片，然后把屏幕截图保存成 png
   ```
   图片尺寸推荐 1600×900（16:9 顺滑的 2k 输出）。

   图片排版比例：上方图片占 70%，下方文字占 30%。
   字体：系统 sans-serif，灰白色，居中。

## 执行流程

### Step 1: 分析内容

阅读输入的文章段落，提取核心概念、场景、情感基调。确定：
- **画面主体**：人、物、场景？
- **色调**：暖色、冷色、中性？
- **构图**：特写、中景、远景？
- **文字叠加**：是否需要？叠加什么文字？

### Step 1.5: 选择风格

如果本轮对话中已经选择过风格（上一次调用本 skill 时已确定），直接使用之前选择的风格，跳过此步。

否则，输出上方「风格选择」表格的 4 个选项，让用户回复编号（1-4）。用户回复后记住选择，后续本对话中所有配图都使用同一风格。

### Step 2: 编写 Prompt

按已选风格对应的 prompt 模板写出完整句子。用一个句子写完整，好过用几个短句拼凑。

### Step 3: 检查脚本就绪

检查 `scripts/main.ts` 是否存在，如果缺失则重新复制（从 damon-imagine）。

### Step 4: 生成图片

```bash
${BUN_X} ${DAMON_ZHIHU_IMAGE_DIR}/scripts/main.ts --prompt "<prompt>" --image <output-path> --ar 16:9 --quality 2k --provider seedream
```

其中：
- `${BUN_X}` = `npx -y bun`（如果没装 bun）
- `${DAMON_ZHIHU_IMAGE_DIR}` = damon-zhihu-image skill 目录，即 `$CODEX_HOME/skills/damon-zhihu-image` 或 `~/.codex/skills/damon-zhihu-image`
- `<output-path>` = 保存路径，用相对路径如 `zhihu-images/eval-<id>-<n>.png`

`--quality 2k` 是最佳平衡点，高于 2k 可能被知乎压缩反而效果差。

### Step 5: 处理文字叠加（可选）

如果选择了文字叠加，生成纯图后，用独立步骤在图片下方叠加文字区域。

### Step 6: 返回结果

返回图片文件路径，以及简短的图片说明（用于 markdown 的 alt text）。

## 输出格式

```
图片路径：<path>
图片说明：<alt text>
```

## 注意事项

- 不要预先假设 EXTEND.md 已经配置好。每次使用时先检查。
- 火山引擎模型对 prompt 的中文理解很好，prompt 可以中英文混合。
- 16:9 是最安全的知乎配图比例，4:3 也可以。
- 图片质量统一用 2k，高于 2k 可能被知乎压缩反而效果差。
- 相同段落不要重复出图。如果已经在同一轮生成了类似内容的图，复用即可。
