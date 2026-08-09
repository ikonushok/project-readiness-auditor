# How To Create Audit Skill

Use this guide when turning a repeatable project-audit workflow into a small installable skill.

## Decision

Create a new audit skill only when the workflow is repeatable and narrower than `project-readiness-auditor`.

Good reasons:

- a distinct audit domain has recurring evidence rules, such as security, data pipelines, trading systems, ML notebooks, or deployment readiness;
- the workflow needs its own report template, rubric, or validation scenarios;
- the same instructions are being pasted into multiple audits;
- the workflow needs bundled scripts, references, or assets.

Do not create a new skill for a one-off checklist, a single customer report, or a future workflow that has not repeated yet.

## Minimal Shape

Use this package shape:

```text
audit-skill-name/
├── SKILL.md
├── VERSION
├── agents/
│   └── openai.yaml
├── references/
│   ├── audit-methodology.md
│   ├── readiness-rubric.md
│   └── report-template.md
└── scripts/
    └── validate_skill.py
```

Keep local authoring files outside the installable skill:

```text
AGENTS.md
CLAUDE.md
agents/
.claude/
.agents/
.codex/
```

## SKILL.md Checklist

The frontmatter must contain only:

```yaml
---
name: audit-skill-name
description: What the skill does and exactly when to use it.
---
```

The body should include:

- installed-version instructions that tell the agent to read `VERSION` in the skill directory when version traceability is relevant;
- default workflow;
- audit modes;
- evidence rules;
- mandatory bug discovery;
- report pack shape;
- approval gates for reproduction and production fixes;
- references to detailed files;
- stop rules;
- output contract.

Put trigger-critical information in `description`. Put long rubrics, examples, and templates in `references/`.

## Audit Method Rules

Every audit skill should preserve these rules unless it has a documented reason not to:

- README, specs, and presentations are intent, not proof.
- Runtime claims require commands that were actually run and inspected.
- Production-readiness claims require reproducibility, deployment, operations, security, observability, rollback, and critical tests.
- Bug discovery is mandatory in every audit.
- Plausible bugs are candidates until reproduced or directly proven by code evidence.
- Reproduction files, test edits, dependency installs, and mutating commands require explicit approval.
- Production fixes require a second explicit approval after reproduction.
- Previous audit reports are not evidence for a new audit.

## Report Pack

Use a full report pack by default for non-brief audits:

```text
reports/customer/<project-slug>/index.md
reports/customer/<project-slug>/code-only-project-readiness-YYYY-MM-DD.md
reports/customer/<project-slug>/project-readiness-YYYY-MM-DD.md
reports/customer/<project-slug>/bug-audit-YYYY-MM-DD.md
```

Use one compact report only when the user explicitly asks for a brief, summary, short orientation, or constrained single-report output.

## Agent Pack

Use the smallest local authoring pack:

- `AGENTS.md` for project-wide rules;
- `agents/context_router.md` for minimal context routing;
- one primary workflow agent;
- `agents/validation_reviewer.md`;
- `agents/task_spec_short.md`;
- one risk reviewer only when a recurring risk needs a distinct checklist.

Do not add agents for hypothetical future audit types.

## Validation

Before calling the skill ready:

```bash
python3 project-readiness-auditor/scripts/validate_skill.py project-readiness-auditor --public-report-examples --report-quality-summary
python3 scripts/validate_pack.py .
python3 -m unittest discover -s tests
```

Validation meaning:

- `validate_skill.py` checks the installable public skill package and public report examples.
- `validate_pack.py` checks the local authoring agent pack.
- Unit tests check validator regressions.

Do not claim L3 or higher from static validation alone. L3 requires applying the skill to one real project case and inspecting the generated output.

## Versioning

Raise the patch version when changing package behavior, validation rules, report templates, or public skill instructions.

Keep the root repository `VERSION`, installable skill `VERSION`, and release notes aligned.

Do not create a git tag just because the version changed. Create a tag only when publishing a release after validation passes.
