# Compatible GPT Image 2 Director-Note Prompt

Load this reference when the user wants the director-note image prompt to match the "experienced, slightly lazy film director" style, or when generating GPT Image 2 prompts from director-note input cards.

## Adapter Rule

Do not pass a raw story paragraph directly into this image prompt. First convert the story into one selected 8-15 second segment and a director-note input card. Then fill this image prompt from the card.

Required fields from the card:

- Segment title
- Target duration
- Story action
- Scene
- Characters
- Core emotion
- Visual style
- Overall rhythm
- 1-2 key shots with emotional target, camera position, lens/movement language, and viewer focus
- Blocking/staging relationship
- Cinematography notes
- Performance notes
- Lighting and atmosphere
- Color design
- Music and sound
- Dialogue, if any
- Negative constraints

If any field is missing, infer a short, conservative value from the card. Do not invent a new plot event.

## Prompt Skeleton

```text
你是一位经验丰富、略带懒散气质的电影导演，正在为 GPT Image 2 编写一页简洁的「导演手记」。

生成一页完整的导演手记页面，用于指导一个不超过 15 秒的短视频片段。它不是详细分镜表，不是逐镜头镜头表，不是制作圣经。导演只关心 1-2 个最关键的镜头、整体节奏、调度关系和现场执行重点。

页面比例：16:9。
页面感觉：像被钉在前期筹备板上的中文手写导演备忘录。简洁、有选择性、实用、易读，有留白，不拥挤。

【片段信息】
标题：《{片段标题}》
时长：{目标时长}，最长不超过 15 秒
风格说明：{核心情绪}，{视觉风格建议}
剧情动作：{剧情动作}
场景：{场景}
角色：{角色}

【页面必须包含】
1. 标题区：中文标题、中文风格说明、中文时长说明。
2. 整体节奏概览区：用「起 -> 承 -> 转 -> 合」或适合场景的节奏流程展示片段变化。每个节奏点旁边加极简中文批注，说明情绪变化或视觉变化。
3. 1-2 个关键镜头区：只画真正重要的镜头，不做完整 storyboard。
4. 调度草图区：多人场景必须有俯视调度图；单人场景画摄影机与空间关系图。
5. 简短中文批注区：摄影机位、演员站位、关键布景、灯光重点、氛围控制、表演提示、色彩、音乐音效、关键台词。
6. 色彩区域：说明色彩搭配和情绪作用。
7. 音乐/声音区域：说明音乐进入点、静默、环境音、冲击音或关键台词。

【整体节奏】
{整体节奏}

【关键镜头】
{关键镜头细项}

关键镜头草图风格：
- 火柴人、萝卜人、人体占位块、动势线。
- 每个关键镜头旁边用中文短标签标明：情绪目标、摄影机位置、镜头语言、观众必须注意什么。
- 可使用专业中文短语，如中近景慢推、低机位压迫、手持逼近、高机位俯压、弧线环绕、长焦压缩。

【调度】
{调度关系}

调度草图要求：
- 展示人物位置、摄影机位置、运动方向和空间关系。
- 使用火柴人、箭头、圆圈、简化人体符号。
- 禁止服装细节、面部细节、角色轮廓设计。

【导演批注内容】
摄影指导：{摄影指导}
表演指导：{表演指导}
灯光与氛围：{灯光与氛围}
色彩设计：{色彩设计}
声音设计：{声音设计}
台词：{台词}
导演重点：{导演重点一句话}

【文字规则】
图片中出现的所有文字必须全部为中文。文字像导演手写笔记，短、碎、实用、有选择性。优先使用标签、提醒、关键词。禁止长段落、表格、大量标题和密密麻麻的工作表。

【人物绘制规则】
人物必须是极度简化、不可识别的占位草图：火柴人、萝卜人或人体占位块。禁止可识别人脸、发型、服装、身体细节、身份特征和角色设计。

【视觉风格】
整体像有经验导演的拍摄备忘录，而不是详细 storyboard。电影感、老练、有重点。视觉重点放在关键镜头草图、调度草图和少量批注上。

【禁止项】
{禁止项}
不要画真实人脸。不要画精细人体。不要生成正式分镜表。不要生成技术文档。不要生成精致插画。不要把完整故事塞进一页。不要让页面拥挤。
```
