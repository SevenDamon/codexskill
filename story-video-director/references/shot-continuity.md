# Shot Continuity

Load this reference for multi-segment generation, continuation from an existing video, or repair of visible jumps between generated clips.

## Boundary Classification

Classify every segment boundary before writing the next prompt:

- `同镜头续接`: the next clip should look like the same uninterrupted take.
- `有动机切镜`: a deliberate cut caused by speaker change, action, reveal, reaction, or narrative emphasis.

Never leave the boundary type implicit.

## Same-Shot Continuation

Use a stable frame near the prior clip's end as the next first-frame anchor. Also inherit:

- Framing and subject scale.
- Camera position, height, lens feel, axis side, and background crop.
- Camera-motion state: fixed, pushing, pulling, panning, tilting, or settled.
- Character support state, feet/base, torso, hands, head, gaze, contacts, and screen position.
- Lighting direction, exposure, color, and atmosphere.

Select a stable frame from roughly the final 0.3-0.8 seconds when possible; avoid blink, extreme mouth shape, hand deformation, motion blur, or background distortion. Do not require the literal last frame.

Prompt compactly:

```text
这是上一段的同镜头续接。首帧严格保持输入稳定帧的构图、景别、机位、人物姿态、视线、背景范围和光线，不重新建立镜头；延续上一段的摄影机运动状态，只发生{唯一变化}。
```

Do not restart the same push-in from a wider frame. Prefer settling the camera near a segment boundary when reliable continuation is more important than continuous motion.

## Motivated Cut

Record the reason: speaker handoff, reaction, action match, reveal, or emphasis. Preserve:

- Screen direction and eye line.
- World-space pose and contacts.
- Character identity, wardrobe, scene geography, light, and time.
- Continuous master audio and room tone.

Prefer a hard cut at a natural dialogue/action boundary. Use J-cuts or L-cuts when audio continuity helps bind the images. A reverse shot changes camera position, not character posture or furniture.

## Audio Continuity

- Prefer one complete master audio track on the edit timeline.
- Use segmented audio for generation/lip-sync, then mute generated clip audio and restore the master track when practical.
- Align visual cuts to natural pauses or speaker handoffs.
- Preserve room tone; avoid five separate noise floors or volume resets.

## Existing-Clip Repair

Classify each bad join:

- Small mismatch: trim re-establishing frames, match crop/scale/color, and hard-cut at a blink, pause, or action boundary. A 3-6 frame dissolve is acceptable only when images already match.
- Medium mismatch: reinterpret as a motivated cut, preserve eye line, and bridge with continuous audio.
- Large mismatch: regenerate the later clip from the prior stable frame plus original character/scene references. Transitions cannot repair major pose, identity, or geography drift.
- Last resort: insert one brief neutral cutaway such as hands, environment, feet, or listener reaction; do not use repeated cutaways to hide every boundary.

## Boundary Card

```text
【衔接类型】同镜头续接 / 有动机切镜
【切镜动机】无 / 说话权交接 / 动作 / 反应 / 揭示 / 强调
【首帧依据】上一段稳定帧 / 新机位首帧 / 场景参考图
【继承景别与构图】
【继承摄影机状态】固定 / 推进 / 拉远 / 摇移 / 已稳定
【继承人物姿态与视线】
【继承背景范围与光线】
【本段唯一变化】
【结尾稳定状态】
【音频衔接】完整母带 / J-cut / L-cut / 自然停顿硬切
```
