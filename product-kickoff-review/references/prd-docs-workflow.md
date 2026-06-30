# PRD And Docs Workflow

Use this after the commercial gate passes or when the user explicitly asks to create planning docs.

## Default Docs

```text
docs/
  PRD.md
  DESIGN.md
  ARCHITECTURE.md
  DATA.md
  PROMPTS.md
  EVAL.md
TODO.md
```

Create only the docs that matter for the project. For non-AI products, `PROMPTS.md` may be omitted. For non-data products, `DATA.md` may be short.

## PRD.md

Include:

- One-sentence positioning.
- Problem.
- Paying customer.
- End user.
- Current workaround.
- Why current workaround is insufficient.
- MVP scope.
- Feature blacklist.
- Core user journey.
- Acceptance criteria.
- Commercial assumptions to validate.
- Main risks.

## DESIGN.md

Include:

- Product feel and audience.
- Layout principles.
- Main screens.
- Component rules.
- Empty/loading/error states.
- Interaction states.
- Visual constraints.

Do not over-design before core workflow is validated.

## ARCHITECTURE.md

Include:

- Technical stack.
- Directory structure.
- Module boundaries.
- Data flow.
- External integrations.
- Security boundaries.
- Things not to build yet.
- Test and verification expectations.

## DATA.md

Include:

- Core entities.
- Tables/collections.
- Event schema.
- Required identifiers.
- Retention and privacy assumptions.
- Export/sync shape.

## PROMPTS.md

Use for AI products.

Include:

- AI roles.
- Prompt templates.
- Input schema.
- Output schema.
- Validation rules.
- Versioning rules.
- Fallback and human review rules.

## EVAL.md

Include:

- Evaluation samples.
- Expected outputs.
- Pass/fail criteria.
- Manual review checklist.
- Known limitations.

## TODO.md

Break work into stages. Each stage should be small enough to test and commit.

Each task should include:

- Objective.
- Allowed edit scope.
- Acceptance criteria.
- Test command or manual check.
- Commit point.

## File Creation Rule

When working in a real repo:

- Check whether docs already exist.
- Do not overwrite existing docs without reading them.
- Add new docs or update carefully.
- Keep docs aligned with the chosen MVP, not a future platform.
