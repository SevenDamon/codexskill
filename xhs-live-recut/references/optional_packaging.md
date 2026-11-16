# Optional motion, covers, and publishing copy

## Stage-specific questions

Offer each addition when its stage is reached. Use the user's current instructions and the approved series profile to determine what is already decided. Ask one compact question covering the undecided choices at that stage. Wait for an answer before doing the dependent optional work, while continuing any independent work already authorized.

| Stage | Suggested question when undecided |
| --- | --- |
| Visual direction, before composition | 要不要加配合原声的动效？例如左侧渐变面板，随讲话显示重点、引语、聊天气泡或步骤卡，可以先做一段样片。 |
| Cover preparation | 要不要为每条制作封面？可以选16:9、4:3、3:4，是否加入你的真实人像？ |
| Publishing preparation | 要不要一起配好发布标题、简短说明和末尾话题？准备发视频号、小红书、抖音中的哪些平台？ |

Record `unasked`, `approved`, or `declined` for the optional decisions in `project-profile.yaml`. Missing optional fields in an older profile mean that the decision must be resolved from the active conversation. A direct request for an option supplies approval for that option. For example, “三种比例都做，加我的人像” authorizes the chosen ratios and portrait insertion. Ask only for information that is still needed to implement it.

A user-approved sample and “其他也照这样做” authorize that treatment for the series. Reuse the decision for subsequent clips. A declined option stays declined for that series until the user changes it. For a new series, offer the saved approach when its stage is reached.

## Speech-aligned semantic motion

Choose a graphic because it explains the spoken point. Keep the original picture and voice synchronized and keep the essential screen evidence and captions readable.

| Spoken point | Candidate treatment |
| --- | --- |
| Select one concrete problem from several scenarios | Several cards converge into one focus card |
| Recount an expert's feedback | Quote card, with the speaker's retelling identified |
| Ask AI to clarify missing information | Chat bubbles that reveal the questions in speech order |
| Explain a procedure | Step cards revealed as each step is spoken |
| State a final judgment | One concise focus statement |

The 2026-11 series used a left-side gradient panel that fades in and carries the graphic. Record its placement, opacity gradient, text sizes, palette, and entry/exit times after approval. Determine its width from the underlying screen content. Show enough of the same example in the pilot to judge readability and timing.

Record editorial overlay text separately from spoken subtitles. Map its meaning and timing to the source. Use source-derived wording for actual quotations and identify illustrative chat text as an example when needed.

### External motion references

When the user supplies a library such as `https://github.com/motiontemplates/all`, examine its current descriptions, previews, usage instructions, and applicable terms. Select a few relevant treatments with a reason tied to the speech. Use locally supplied packages where appropriate and follow their supported entry points.

Record the component/source, required runtime, and actual implementation used. If a runtime or approval review blocks execution, explain the specific outcome and choose a feasible approach within the existing authorization. An independently authored visual treatment should be identified as such in the delivery. Store personal access files and protected package material only where their intended workflow requires them.

## Cover variants and a real speaker portrait

After the user selects a set, compose each chosen ratio independently. The tested three-format set is a useful proposal.

| Ratio | Output size |
| --- | --- |
| 16:9 | 1920×1080 |
| 4:3 landscape | 1600×1200 |
| 3:4 portrait | 1080×1440 |

Use a short cover headline and one meaningful source-screen fragment. Keep the publishing title as a separate field because platform limits can require different wording. Read `cover_style_guide.md` for evidence selection and mobile review.

When portrait insertion is approved, inspect a user-supplied photo or a known local user portrait before asking for a new image. A reusable portrait may be present in the current project's assets or, when installed, in `education-promo-visuals/assets/portrait.png`. Confirm its provenance and visual quality. Copy the selected asset into the delivery so the editable source has a local dependency.

Use the person's actual appearance. Preserve the portrait's aspect ratio and check hair, glasses, clothing, and cutout edges. Use appropriate image-editing tools if extraction or retouching is necessary. A small webinar bubble supports a small headshot, and a larger half-body placement needs a sufficiently detailed asset.

The tested layout placed the real cutout on the right, using roughly 20–25% of the visible composition for the person. This is a starting point for the selected design. Reflow the evidence cards to preserve readable text and adjust the portrait's size for each canvas. Review the final composition at full resolution and at phone-thumbnail size.

Deliver final PNGs and the editable composition with its local assets. HTML/CSS is suitable for this series and allows exact Chinese type and spacing. A native source appropriate to another selected design is also suitable. Include a contact sheet and a 270×360 preview of each selected portrait-ratio cover.

## Platform-ready publishing copy

Resolve the destination platforms explicitly. The confirmed 2026-11 set is 视频号、小红书、抖音. Platform names and per-platform settings belong in the profile so a correction can be applied to the whole package.

### Titles

Use the title limits supplied by the user. For reuse of this series, the confirmed settings are 视频号16字以内、小红书和抖音20字以内. These are saved project requirements. Check current requirements when the user requests verification or a publishing interface supplies a different limit.

For a conservative local count, count each Unicode code point, including each Latin letter, punctuation mark, and space. For example, `AI` counts as two. Display the counted length alongside the title in the delivery, outside the copyable title. Keep titles on one line. If the actual editor counts differently, its counter determines acceptance.

A supported short title can be shared across platforms. Every title must match the clip's actual claim and evidence. Frame a brief method/example clip with a scope that it delivers.

### Descriptions and topics

Write one concise, conversational paragraph for each clip. Around 50–100 Chinese characters is a useful proposal for this series, and the user's preferred length controls the result. Preserve approved wording during later platform or topic revisions.

Use a stable subject-area topic, a relevant audience/scenario topic, and topics specific to the clip. The tested candidates included `#AI赋能教育`, `#教师成长`, `#参赛选题`, `#教学创新`, `#提示词`, `#AI备课`, and `#知识库`. Add tool-name topics only when the tool actually appears or is discussed in that clip.

The series used four topics for 视频号 and five each for 小红书 and 抖音. These counts are editable copy choices. Append the selected topics as the last line of each platform's description block. Claims about current topic popularity need current evidence.

### Package and validation

Save `视频发布文案.md` grouped by clip, then platform. Each platform block contains its title, the count and confirmed limit, and a copyable description with topics on its final line. This makes platform-name or limit corrections straightforward to apply consistently.

For deterministic title checks, prepare `publish-package.json` using this shape and run `python scripts/validate_publish_copy.py <path-to-publish-package.json>`. The validator checks the selected platform coverage, title limits, descriptions, and topic fields. It returns JSON with counts and errors. Verify the generated Markdown matches the validated fields.

```json
{
  "title_limits": {"视频号": 16, "小红书": 20, "抖音": 20},
  "clips": [{
    "id": "01",
    "video_file": "01_example.mp4",
    "cover_files": {"16:9": "covers/01_16x9.png", "3:4": "covers/01_3x4.png"},
    "posts": [
      {"platform": "视频号", "title": "参赛选题，先抓一个真实痛点", "description": "从真实教学痛点出发，聚焦一个具体场景，再说清AI能帮上什么忙。", "topics": ["#AI赋能教育", "#参赛选题"]},
      {"platform": "小红书", "title": "AI参赛选题怎么定？先抓一个真实痛点", "description": "从真实教学痛点出发，聚焦一个具体场景，再说清AI能帮上什么忙。", "topics": ["#AI赋能教育", "#教学创新"]},
      {"platform": "抖音", "title": "AI参赛选题怎么定？先抓一个真实痛点", "description": "从真实教学痛点出发，聚焦一个具体场景，再说清AI能帮上什么忙。", "topics": ["#AI赋能教育", "#教师成长"]}
    ]
  }]
}
```

An empty topics list represents a user choice to omit topics. Use the selected package settings to judge completeness. Keep any provenance notes and source links outside the copyable publishing blocks. Check the actual cover crop in a publishing UI when that surface is available.
