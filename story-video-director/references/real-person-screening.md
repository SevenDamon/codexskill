# Real-Person Screening

Load this reference before writing any downstream director-note, image, or video generation prompt for a character who is named, visually identifiable, or possibly identifiable as a real person.

This is a hard gate. If the source includes an uploaded image/video frame, historical setting, public-figure context, distinctive face, costume, inscription, event, or composition that could reasonably point to a real person, ask first. Do not rely on aliases to skip the question.

## Screening Question

Ask exactly one concise question before generating prompts:

```text
这位人物是否是、或意图表现为可识别真实人物/历史人物/已故名人/公众人物？
```

Do not ask when the user has already answered this question for the current character set.

## Trigger Conditions

Ask the screening question when any condition is true:

- The user names a real person, public figure, historical figure, or deceased famous person.
- The character appears in an uploaded image or video frame and could be recognized from face, clothing, posture, scene, text, or context.
- The character is unnamed but the request strongly implies a specific real person.
- You are unsure whether the character is fictional or real.

Until the user answers, only provide risk notes, workflow suggestions, high-level feasibility diagnosis, or abstract segmentation. Do not provide director-note cards, GPT Image prompts, Seedance prompts, expression/action instructions, or camera-language plans that depend on the possible real person's likeness.

## Branches

### User answers no

- Continue using the supplied names.
- Do not imply that this overrides target-platform rules.

### User answers yes

- Keep real names only in internal analysis so the narrative remains understandable.
- Create one stable neutral alias per person from visible staging or narrative role: `学生`, `左侧青年`, `右侧黑衣人物`, `年长学者`, `画面右侧说话者`.
- Use aliases in director-note image prompts, reference-image prompts, Seedance prompts, visible page text, continuity blocks, and negative constraints.
- Maintain an internal mapping: `真实姓名 -> 稳定角色代号`. Never expose the left side in a downstream generation prompt.
- Prefer position-based aliases when the composition is locked; prefer role-based aliases when screen position may change.
- Remove direct and indirect identity cues from downstream prompts: real name, title, famous quote, exact event, signature costume detail, institution/event pairing, or resemblance language that preserves recognition.

## Boundaries

- Aliasing is prompt hygiene, not a guarantee of generation permission.
- Do not use euphemisms or near-explicit hints intended to preserve the person's identity while hiding the name.
- If a supplied reference image, requested likeness, or context remains restricted, offer either a non-identifiable fictional proxy or planning-only output.
- Director-note figures must remain simplified placeholders regardless of branch.

## Internal Mapping Template

```text
【真实人物筛查】
是否命中：是 / 否
用户确认：

【内部角色映射，不进入生成提示词】
真实姓名：
稳定角色代号：
代号依据：画面位置 / 叙事角色 / 可见服装类别

【下游提示词检查】
- 不含真实姓名
- 不含间接身份暗示
- 导演板、参考图、Seedance使用同一代号
- 不承诺代号替换可以绕过平台限制
```
