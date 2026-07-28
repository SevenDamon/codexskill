# Compatible GPT Image 2 Director-Note Prompt

Load this reference when generating a GPT Image 2 director-note image prompt. Load [real-person-screening.md](real-person-screening.md) first when a named or identifiable real person appears.

## Adapter Rules

- Build the full internal director-note card first; do not paste the whole card into the image prompt.
- If real-person screening returns yes, use only stable role aliases in this prompt and visible page text.
- Use one key shot by default and at most two only when one cannot express the segment.
- Limit the page to six zones plus one execution strip, 3-5 short annotations, and at most five highest-priority restrictions.
- Keep full pose state, precise percentages, frame-selection criteria, full dialogue, and long negative lists in internal planning or the Seedance workflow.
- When a previous director-note page is supplied, use it only as the style/layout anchor. Use the scene or stable frame as the pose/spatial anchor.

## Prompt Skeleton

```text
你是一位经验丰富、略带懒散气质的电影导演。生成一页16:9横版中文手写导演手记，用于指导一个符合当前Seedance生成模式时长上限的短视频片段。

标题：《{片段标题}》
风格：{核心情绪与视觉风格}
时长：{目标时长}
角色：{稳定角色代号}

参考图分工：上一张导演板只用于纸张、笔迹和版式风格；场景图或稳定帧用于人物姿态、空间关系和机位方向。

页面只设置六个主要区域：
1. 标题
2. 整体节奏图：{整体节奏}
3. 唯一关键镜头草图：{关键镜头1}
4. 俯视调度草图：{调度关系}
5. 表演指导：{表演指导摘要}
6. 结尾衔接：{衔接类型}；{本段结束姿态摘要}；下一段继承{下一段继承摘要}

底部增加一条很短的执行条：{执行条}

姿态锁定：{姿态锁定一句话}

最高优先级限制最多五条：
{最高优先级限制}

人物只画成火柴人、萝卜人或人体占位块，不画真实脸部、发型和服装细节。图片只使用3-5条简短中文手写批注，保持明显留白。

不要显示完整台词、完整姿态状态、精确运动百分比、选帧标准、长负面清单、正式表格或密集工作表。
```

## Execution Strip

Compress persistent visual constraints into 3-5 short labels, for example:

```text
双人侧面中景｜学生左／年长人物右｜两人站立｜保持侧脸｜同机位轻推
```

## Constraint Selection

Choose restrictions by failure cost, not completeness. Prefer camera angle, identity exposure, support state, screen direction, and one movement boundary. Move lower-risk constraints to the internal card or concise Seedance prompt.
