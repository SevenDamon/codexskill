# Production Inputs And Seedance Modes

Load this reference when deciding what materials are required, starting from a bare description, planning dialogue audio, or splitting segments for Seedance.

## Conditional Inputs

At least one creative source is required: story, dialogue, plot passage, or character-and-scene description. Everything else is optional by stage:

- Character/look reference: strongly recommended for recurring visual identity.
- Scene reference: strongly recommended for recurring geography, pose, light, and camera axis.
- Completed audio: strongly recommended for dialogue timing, voice, delivery, and lip sync.
- Voice ID/profile: useful when completed audio does not exist.
- Stable previous tail frame: only available and useful in continuation mode.
- Previous director-note page: optional style/layout anchor, never a pose source.

Rename input sections to `可用素材，没有可留空`; never imply blank fields block director-note creation.

## Entry Modes

### Description-first

Input may be only a sentence describing characters and scene. Produce:

1. Conservative task assumptions.
2. Minimal narrative skeleton and visible event.
3. Character/look cards.
4. Scene/spatial card.
5. Voice consistency cards for speaking roles.
6. Segment plan for user review.
7. Reference prompts and director-note prompts after approval.

Do not require the user to write a screenplay or storyboard first.

### Text-first

Segment the story/dialogue, then create missing character, scene, style, pose, and voice assets.

### Asset-first

Inspect supplied images/audio and treat them as source-of-truth anchors. State what each asset controls.

### Continuation

Use a stable frame near the prior clip's end, not necessarily the literal final frame. Preserve the original scene/reference assets to prevent cumulative drift.

## Seedance Generation Modes

Ask only when the mode is not already clear:

```text
【Seedance生成模式】
A. Agent模式，上传已有音频：单个音频最长13秒
B. 视频生成模式，使用模型自带音效：单段视频最长15秒
C. 暂时只做导演板：时长暂定，生成前再校准
```

### Agent uploaded-audio mode

- Recommended segment: 8-12 seconds.
- Hard audio-file limit: 13 seconds.
- Use the actual exported file duration, including silence/padding.
- If longer than 13 seconds, split at complete semantic boundaries and natural pauses.
- Never truncate automatically.
- If no clean split exists, ask the user to choose: semantic rewrite/re-record, delivery adjustment, or explicit removal of a named portion.
- Allow roughly 0.1-0.3 seconds of necessary boundary room only when the complete exported file still remains within 13 seconds.

### Model-generated-sound video mode

- Recommended segment: 8-12 seconds.
- Hard video limit: 15 seconds.
- Split anything longer than 15 seconds.
- Mark voice consistency as less reliable than using a completed shared audio track.

### Planning-only mode

- Create provisional director-note timing.
- Label duration `暂定`.
- Recalculate segment duration, action beats, and board labels after the audio/mode is finalized.

## Over-Limit Decision

```text
当前音频为{实际时长}，超过Agent模式13秒上限。请选择：
1. 按语义停顿拆成多个片段（推荐）
2. 精简台词后重新生成或录制
3. 调整表达速度后重新生成或录制
4. 明确指定要删除的内容
```

## Voice Consistency

Prefer one master performance recorded/generated with one voice, then cut it into segments. If generating lines separately, keep the same voice ID/model and baseline settings.

For a named or identifiable real person covered by real-person screening, do not request imitation of the person's real voice. Use a non-identifiable actor/narrator voice profile.

## Timing Fields

```text
【生成模式】Agent上传音频 / 自带音效视频 / 暂只做导演板
【音频状态】完整母带 / 已分段 / 尚无音频
【实际音频时长】
【当前硬上限】13秒 / 15秒 / 待定
【时长状态】已锁定 / 暂定
【是否超限】
【超限处理】语义拆分 / 重录改写 / 调整表达 / 用户指定删除
【导演板采用时长】
```
