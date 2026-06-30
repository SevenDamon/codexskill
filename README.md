# Codex Skills

This repository stores reusable Codex skills.

## Skills

### product-kickoff-review

Product kickoff review workflow for non-technical founders and AI-assisted builders.

Use it before coding a new product idea to check:

- whether anyone will pay;
- what price can be justified;
- whether customers will keep paying;
- whether the project can be delivered safely with AI agents;
- what PRD, architecture, data, prompt, evaluation, and TODO docs should exist before implementation.

Path:

```text
product-kickoff-review/
```

Default invocation:

```text
Use $product-kickoff-review to validate this product idea, define the MVP, and create the initial PRD/docs/TODO plan.
```

### story-video-director

Story-to-video direction skill.

### xhs-longform-cards

Xiaohongshu long-form card generation skill.

## Install A Skill Locally

Copy a skill directory into your local Codex skills folder:

```powershell
Copy-Item -Recurse .\product-kickoff-review "$env:USERPROFILE\.codex\skills\product-kickoff-review"
```

Restart Codex if the skill list does not refresh automatically.

## Repository Layout

Each skill should keep the standard structure:

```text
skill-name/
  SKILL.md
  agents/
    openai.yaml
  references/
    ...
```

Avoid adding extra files inside a skill directory unless they directly support that skill.
