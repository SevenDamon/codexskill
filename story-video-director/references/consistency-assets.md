# Consistency Assets

Load this reference when the user wants multi-segment video generation, parallel segment generation, recurring characters, recurring objects, a continuous story, or reference images for visual consistency.

## Purpose

Reference images are shared anchors. They are not final video frames and not director-note pages. Use them to lock identity, object form, scene geography, scale, color, and style before generating per-segment director-note images and Seedance prompts.

## Consistency Asset Output

```text
## 一致性资产设定

### 【角色设定卡】
角色名：
叙事功能：
年龄段：
体型/轮廓：
固定服装：
固定颜色：
固定道具：
动作习惯：
情绪基调：
禁止变化：
参考图建议：

### 【关键物体设定卡】
物体名：
叙事功能：
固定外观：
尺寸/比例：
材质/颜色：
状态变化规则：
禁止变化：
参考图建议：

### 【场景设定卡】
场景名：
叙事功能：
固定空间结构：
关键地标：
入口/出口/窗户/主体物方向：
光线基调：
可变化因素：
禁止变化：
参考图建议：

### 【统一视觉风格卡】
整体风格：
画幅：
色彩：
光线：
镜头质感：
颗粒/清晰度：
运动风格：
禁止变化：

### 【参考图生成顺序】
1. 角色参考图：
2. 关键物体参考图：
3. 场景参考图：
4. 统一视觉风格参考图：
5. 合成关系参考图（可选）：

### 【跨片段一致性锁定】

### 【允许跨片段变化】
```

## Character Reference Image Prompt

```text
生成一张角色参考图，用于后续多段 AI 视频保持角色一致。

角色：{角色名}
年龄段：{年龄段}
体型/轮廓：{体型/轮廓}
固定服装：{固定服装}
固定颜色：{固定颜色}
固定道具：{固定道具}
动作习惯/气质：{动作习惯}，{情绪基调}

画面要求：
- 16:9 或 4:3 均可，简洁中性背景。
- 同一角色展示正面、侧面、背面三视图，保持同一服装和道具。
- 重点锁定体型轮廓、服装颜色、道具、年龄段和整体气质。
- 不需要电影场景，不需要复杂动作。
- 可写少量中文标签标注固定锚点。

禁止：
- 不要更换服装。
- 不要增加饰品。
- 不要改变年龄段、体型、发色、主要颜色或固定道具。
- 不要生成多个人物版本。
```

## Object Reference Image Prompt

```text
生成一张关键物体参考图，用于后续多段 AI 视频保持物体一致。

物体：{物体名}
固定外观：{固定外观}
尺寸/比例：{尺寸/比例}
材质/颜色：{材质/颜色}
叙事功能：{叙事功能}
状态变化规则：{状态变化规则}

画面要求：
- 简洁中性背景。
- 展示物体的主视角、侧视角、近景细节。
- 用少量中文标签标注尺寸、材质、颜色和不可改变特征。
- 重点是可识别和可复用，不追求海报感。

禁止：
- 不要改变物体类型。
- 不要增加图案、文字、品牌、额外装饰。
- 不要把物体变成其他材质或比例。
```

## Scene Reference Image Prompt

```text
生成一张场景参考图，用于后续多段 AI 视频保持空间一致。

场景：{场景名}
固定空间结构：{固定空间结构}
关键地标：{关键地标}
方向关系：{入口/出口/窗户/主体物方向}
光线基调：{光线基调}
可变化因素：{可变化因素}

画面要求：
- 一张主视角环境图 + 一张简化俯视空间图。
- 标出入口、出口、窗户、主体物、角色常用站位、摄影机轴线。
- 保持空间方向清楚，方便多个片段继承。
- 中文短标签，少量即可。

禁止：
- 不要频繁改变空间布局。
- 不要增加无关房间或地标。
- 不要改变入口、窗户、主体物和摄影机轴线的相对方向。
```

## Unified Style Reference Prompt

```text
生成一张统一视觉风格参考图，用于约束整组视频的色彩、光线和镜头质感。

整体风格：{整体风格}
画幅：{画幅}
色彩：{色彩}
光线：{光线}
镜头质感：{镜头质感}
运动风格：{运动风格}

画面要求：
- 不是具体剧情画面，而是风格板。
- 包含色彩条、光线示意、镜头质感样例和简短中文标签。
- 重点锁定整组视频的统一观感。

禁止：
- 不要引入新的角色、道具或剧情。
- 不要偏离既定色彩和光线。
```

## Per-Segment Inheritance Block

Use this block inside each director-note input card and Seedance prompt:

```text
【继承参考图】
角色参考图：
物体参考图：
场景参考图：
统一风格参考图：

【一致性锁定】
本段必须保持：

【允许变化】
本段只允许改变：

【禁止漂移】
不得改变人物年龄、体型、服装颜色、关键道具、物体形态、场景方向、统一色彩和镜头质感。
```
