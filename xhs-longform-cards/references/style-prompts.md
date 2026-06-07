# Style Prompt References

Use this file only when the task needs a style prompt, a Gemini-compatible instruction block, or a design variant. Do not load or paste long prompt text by default.

## Core Local Workflow Prompt

When asking another model to generate only the client preview HTML, require this architecture:

```text
最终产物是图片，HTML 只是预览和截图中间态。请生成一个独立的 index.html，用中文输出卡片内容。

卡片规格：每张 450px 宽、600px 高，横向排列。至少 3 张：开篇卡、核心内容卡、总结卡。核心内容卡数量根据内容长度控制在 2-5 张。每张卡只承担一个信息任务，避免文字溢出。

下载逻辑必须使用本地 Node/Puppeteer 服务，而不是 dom-to-image-more：
点击下载按钮时，使用 fetch 向 http://localhost:3000/api/screenshot 发送 POST 请求。请求 JSON 包含：
- fullHtml: document.documentElement.outerHTML
- cardId: 当前卡片 ID，如 card-1

服务器返回 image/png blob 后，用 URL.createObjectURL 触发下载。按钮必须放在卡片 div 外部，不能进入截图区域。

边角信息规则：不要添加与内容无关的装饰性角标、英文分类名或泛关键词，例如 OPENING、CORE NOTE、CLOSING、知识卡片/长文拆解/小红书。边角只允许放页码、日期、来源等真正有信息价值的内容；如果只剩日期，优先右下角对齐。
```

## Default Style: Vintage Didactic Journaling

Use for knowledge cards, essays, cultural notes, serious analysis, and reusable local defaults.

```text
设计风格：复古科教手帐笔记。整体气质知性、复古、严谨但不沉闷，像旧时代学者研究手稿。

视觉元素：
- 背景使用米白、象牙白、淡牛皮纸色，可叠加细网格、横线纸或轻微纸张纹理。
- 标题使用典雅衬线体或稳重中文宋体风格，正文必须清晰易读。
- 使用手绘双线框、细分割线、索引标签、便签式引用框、编号、脚注和关键词。
- 一级强调用于大标题和核心结论；二级强调用于内容关键词、数据和关键短语；三级强调用于日期、来源、脚注等内容相关信息。

排版原则：
- 信息分层比装饰重要。
- 每张卡避免堆字；多用短句、列表、核心引用。
- 底部注释区域不超过 40px。
- 禁止为了“显得像模板”而添加无关角标、泛关键词或英文分类名。
```

## Optional Style Variants

### Minimalist Modern

```text
设计风格：极简主义现代风。纯白、浅灰、黑色为主，少量低饱和点缀色。严格网格、留白、细线、现代无衬线字体。适合效率工具、商业分析和方法论内容。
```

### Fresh Healing Hand-drawn

```text
设计风格：清新治愈手绘风。米白、莫兰迪绿、浅蓝、茱萸粉等柔和色。使用轻微手绘线条、便利贴、胶带、手写感标题。适合生活方式、情绪价值、成长记录。
```

### Cute Cartoon / Doodle

```text
设计风格：可爱卡通插画风。明亮柔和色，圆润字体，涂鸦高亮、云朵框、小星星、爱心、贴纸感元素。适合轻松科普、亲子、娱乐和入门内容。
```

### Memphis Geometric Collage

```text
设计风格：孟菲斯几何拼贴。亮黄、宝蓝、鲜粉、薄荷绿、鲜橙，几何色块、波点、条纹、错位拼贴。适合观点鲜明、强视觉冲击的内容。
```
