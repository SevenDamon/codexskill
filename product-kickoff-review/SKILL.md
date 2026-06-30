---
name: product-kickoff-review
description: New product kickoff review workflow for non-technical founders or AI-assisted builders. Use when the user wants to start, plan, prototype, or commercialize a new product/project; asks for PRD, MVP scope, project structure, docs, TODO, vibe-coding workflow, AI-assisted delivery planning, or whether an idea has business value. The skill first checks commercial viability, then checks whether a non-technical founder can deliver it safely with AI agents. Do not use for small bug fixes, narrow implementation tasks, styling tweaks, or already-scoped coding work.
---

# Product Kickoff Review

## Purpose

Use this skill to stop premature coding. First prove the idea can become a paid, repeatable product; then prove a non-technical founder can deliver it safely with AI agents; then create the initial PRD, docs structure, MVP plan, development rules, and TODO.

The operating principle:

```text
First think beyond old constraints, then return to commercial reality.
```

- Think beyond old constraints: assume AI can change how products are built, delivered, and operated.
- Return to reality: force the idea through customer willingness to pay, price, repeatability, AI-assisted delivery risk, and verification constraints.

## Workflow

### Stage 0: Commercial Gate

Always start here for new products. Do not write code or detailed PRD before this gate.

Ask and answer the three core business questions:

1. Will anyone pay?
2. At what price?
3. Will they keep paying?

Use `references/commercial-gate.md` for the full checklist and pass/fail rules.

If the gate fails:

- Say why directly.
- Recommend a narrower customer, sharper pain, lighter delivery model, or different direction.
- Do not proceed to implementation planning unless the user explicitly wants speculative exploration.

### Stage 1: AI-Assisted Delivery Reality Check

Use this because the builder may not be a traditional engineer and may rely mainly on AI agents.

Ask:

- Can this project be split into small AI-executable tasks?
- Can each task be verified by a non-technical founder?
- What docs must exist before coding?
- What outputs must be structured and checkable?
- Which parts must not be left to AI improvisation?
- What tests, screenshots, sample data, or manual checks prove progress?
- How can broken changes be rolled back?
- Can a new AI agent continue from docs without private context?

Use `references/ai-delivery-rules.md`.

### Stage 2: Product Positioning

Define:

- Paying customer.
- End user.
- Current workaround.
- Pain and cost of current workaround.
- Product promise.
- Differentiation.
- Why now.
- What not to claim.

Focus on outcomes customers pay for, not features.

### Stage 3: MVP Scope

Create a small first version that validates the commercial loop.

Must include:

- MVP user journey.
- Core features.
- Feature blacklist.
- First customer segment.
- First measurable success criteria.
- Manual or light-delivery shortcuts.

Prefer high-frequency, standardized, repeatable needs over low-frequency custom work.

### Stage 4: AI Product Logic And Control

If the product itself uses AI, define exactly where product AI is useful and where it is unsafe. This is separate from using AI agents to build the product.

Must specify:

- AI task boundary.
- Input and output schema.
- Validation method.
- Human review rules.
- Fallback behavior.
- Prompt/version management.
- Cost and latency assumptions.

Use `references/ai-delivery-rules.md`.

### Stage 5: Docs Setup

If the idea passes the commercial gate and the user wants to proceed, create or propose project docs.

Use `references/prd-docs-workflow.md`.

Default docs:

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

Only create files when the user asks to apply this to a real local project. Otherwise, provide the content outline in chat.

### Stage 6: Development Plan

Generate a staged TODO that allows small, reversible development.

Each task must have:

- Goal.
- Allowed edit scope.
- Logic not to break.
- Acceptance criteria.
- Test or verification step.
- Git commit point.

Use `references/output-templates.md`.

## Output Order

For strategy-only conversations, answer in this order:

1. Commercial verdict.
2. Sharpest failure risk.
3. Recommended customer and use case.
4. MVP scope and feature blacklist.
5. AI-assisted delivery reality check.
6. Product AI control plan, if applicable.
7. Suggested docs/TODO structure.
8. Next validation action.

For local project setup, create the docs first, then report:

- Files created.
- Key decisions encoded.
- What remains unvalidated.
- Next implementation step.

## Hard Rules

- Do not let "interesting" substitute for "someone pays".
- Do not let "AI can build it" substitute for docs, task boundaries, tests, and rollback.
- Do not propose a full SaaS first when light delivery can validate demand faster.
- Do not include a feature in MVP unless it directly tests the commercial loop.
- Do not hide uncertainty. Mark assumptions that need interviews, pilots, or evaluation data.
- Do not write implementation code during kickoff unless the user explicitly asks to begin development after docs are accepted.

## References

- Read `references/commercial-gate.md` for the business gate.
- Read `references/prd-docs-workflow.md` when generating project docs.
- Read `references/ai-delivery-rules.md` when planning AI-assisted development or product AI behavior.
- Read `references/output-templates.md` when drafting deliverables.
