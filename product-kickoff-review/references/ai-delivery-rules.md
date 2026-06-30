# AI-Assisted Delivery Rules

Use this for two different checks:

1. Can a non-technical founder deliver the product safely with AI agents?
2. If the product itself uses AI, how is that product AI constrained and verified?

## Core Rule

Humans define goals, rules, scope, acceptance criteria, and risk boundaries. AI agents execute bounded tasks inside those constraints.

## Non-Technical Founder Delivery Check

Ask these before coding:

- Can the product be split into small tasks an AI agent can complete one at a time?
- Can each task be verified without deep technical expertise?
- What visible output proves progress: UI screen, local file, test result, sample data, API response, screenshot?
- What docs must exist so a future AI agent can continue without hidden conversation context?
- Which files or modules are allowed to change in each stage?
- What logic must not be broken?
- What command or manual check validates each step?
- Where is the git rollback point?
- What parts require a human decision before AI writes code?

Pass condition:

- The project can be staged into small, testable tasks.
- Each stage has an observable acceptance check.
- The repo has docs and TODO before coding starts.
- There is a clear rollback plan.

Fail signals:

- The first task is "build the whole app".
- No one can tell whether the AI output is correct.
- There are no tests, sample data, screenshots, or manual checks.
- The plan relies on the AI remembering prior chat context.
- The founder cannot explain what changed after a coding step.

## Required Docs For AI-Assisted Development

For meaningful projects, prefer:

- `PRD.md`: product goal, customer, MVP, blacklist, acceptance.
- `DESIGN.md`: UI direction and interaction states.
- `ARCHITECTURE.md`: stack, modules, data flow, constraints.
- `DATA.md`: entities, tables, events, schemas.
- `PROMPTS.md`: AI prompts and output schemas, if product AI exists.
- `EVAL.md`: sample cases and pass/fail rules, if AI or data quality matters.
- `TODO.md`: staged execution plan.

## Product AI Control

If the product itself uses AI, define:

- What AI receives.
- What AI returns.
- Required JSON/schema.
- What must be validated.
- What confidence means.
- When to ask a human.
- What fallback to show.
- What must never be automated.

## Structure Outputs

Prefer JSON or typed records over free-form text when outputs feed a workflow.

Each AI output should include when relevant:

- `result`
- `reason`
- `confidence`
- `needsHumanReview`
- `tags`
- `nextAction`

## Break Work Down

Do not ask AI to solve the whole business process or rewrite the whole codebase.

Break into small steps:

1. Define.
2. Scaffold.
3. Implement one module.
4. Verify.
5. Commit.
6. Continue.

For product AI tasks, also break into:

1. Extract.
2. Classify.
3. Generate.
4. Validate.
5. Summarize.
6. Ask for human review when needed.

## Version Prompts

Prompts are product logic. Treat them like code.

Track:

- Prompt name.
- Version.
- Input schema.
- Output schema.
- Last changed date.
- Evaluation notes.

## Evaluation

Before commercial use, create a small evaluation set when AI output affects user trust.

Minimum:

- 20-50 representative samples.
- Expected labels or outputs.
- Failure categories.
- Manual review notes.

## Human Review

Require human review when:

- Output affects money, grades, medical/legal/financial decisions, reputation, or safety.
- Confidence is low.
- Input is incomplete.
- AI detects conflict or ambiguity.
- The product is in early pilot.
- The non-technical founder cannot verify the result directly.

## Cost Control

Estimate:

- Calls per user per day.
- Average tokens or media cost.
- Monthly cost per customer.
- Who pays API cost.
- Failure mode if quota is exceeded.

## Forbidden Claims

Do not claim:

- "AI is always correct."
- "Fully automated" when humans are still needed.
- "Replaces teachers/experts" unless the workflow truly supports it.
- "Private and secure" without defining data handling.
