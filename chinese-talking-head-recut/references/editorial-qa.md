# Editorial and QA reference

## Topic viability

A proposed output is viable only when it has all four:

1. a supported hook;
2. at least one concrete fact, example, or lived consequence;
3. an ending that resolves the promise;
4. enough unique body material to avoid becoming a duplicate excerpt.

Useful structures:

- lived warning: surprising consequence → numbers/reality → advice → boundary conditions → current stance;
- transformation: before/after result → discovery → repeated application → mechanism or secondary benefit → decision;
- personal crossroads: present dilemma → prior choices → competing options → current principle → unresolved but honest close;

## Transcript audit

Mark and avoid:

- phone notifications, ringtones, coughs, and off-camera interruptions;
- corrected dates or self-contradictions;
- unfinished clauses that only work with omitted context;
- duplicate claims stated twice with weaker wording;
- filler-heavy passages that add no new evidence.

Sound-event timestamps are not safe cut padding. If an event overlaps a required word, start at the next grammatical phrase or omit the sentence.

## Boundary QA

For every rendered boundary, inspect ±1.5 seconds:

- face/hand discontinuity is acceptable only when audio logic is clean;
- no one-frame flash or stale frame;
- no waveform spike at the boundary;
- no clipped first/last phoneme;
- no ringtone tail inside the padding.

Limit self-correction to three passes. Report remaining problems rather than looping indefinitely.

## Counted-promise audit

Apply this whenever the title, cover, or speech promises a number: “three choices,” “four steps,” “five mistakes,” “two turning points,” and similar structures.

Before cutting, write a one-line ledger:

`promised N → item 1 → item 2 → … → item N → conclusion`

Then verify:

- every item is present as a distinct, understandable beat;
- the spoken order, chapter labels, and subtitle numbering agree;
- no item exists only as a cold-open hook and then disappears from the counted sequence;
- removing fillers has not removed the phrase that identifies an item's number or role;
- the conclusion comes only after item N is clearly complete.

Default to chronological enumeration. If a later item is pulled forward as a hook, either repeat/restage it when its numbered turn arrives or add an unmistakable return marker such as “第三次，就是现在.” Do not assume viewers will infer the mapping.

Final check: compare the count promised by the title/cover, the count audible in the cut, and the count visible in subtitles or chapter cards. All three must match.

## Subtitle QA

- Inspect at native final resolution; draft scaling can conceal an oversized font.
- Strip leading/trailing punctuation and non-speech labels such as `[笑声]`.
- Do not split a highlighted phrase across cues.
- Verify yellow emphasis in an actual rendered frame, not merely in the subtitle source.
- Use ASS for inline color. When the subtitle file is ASS, do not override its style with an SRT `force_style` string.

## Cover QA

- Readable at phone-thumbnail size.
- Claim is spoken or directly supported.
- Prefer 8–16 total Chinese characters across two lines.
- Do not cover eyes, mouth, or the primary gesture.
- Avoid making every word yellow; reserve color for the payoff.
