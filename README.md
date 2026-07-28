# project-readiness-auditor

Evidence-based project audit methodology and Codex skill for fast third-party software readiness reviews.

`project-readiness-auditor` helps a team lead, tech lead, reviewer, or due-diligence owner quickly answer practical questions about an unfamiliar project:

- Does the documentation match the code?
- Does the code match the stated project goals?
- What actually works, and what is only claimed?
- What are the main bugs, reliability risks, security risks, and unfinished parts?
- What is the smallest prioritized plan to close the gaps?

The core rule is simple: treat README files, specs, and presentations as intent until code, tests, configuration, CI, deployment files, migrations, or inspected runtime output prove the claim.

This repository follows the same public-package shape as [`agent-pack-designer`](https://github.com/ikonushok/agent-pack-designer): a compact installable skill, reference files loaded only when needed, package validation scripts, and root documentation that explains the operating model.

Tags: `project-audit`, `code-review`, `readiness-assessment`, `software-quality`, `evidence-based`, `technical-due-diligence`, `risk-analysis`, `markdown-reports`.

## Methodology

Use the method in a fixed order. The goal is not to decide whether a project is "good" or "bad"; the goal is to reconstruct its actual state and name the evidence behind every readiness claim.

### 1. Fix The Audit Mode

Choose the smallest mode that answers the current question.

| Mode | Use when | Evidence surface |
|---|---|---|
| `code-only` | You need a fast static review without running the project | Code, tests, configs, migrations, CI, Docker/Helm, scripts |
| `docs-vs-code` | You need to verify README/spec/product claims | Documentation as intent, then implementation evidence |
| `runtime` | You need proof that setup, tests, build, or flows work | Command output from setup, build, tests, smoke checks, or scenarios |
| `security` | You need auth, secrets, CORS, permissions, webhook, or destructive-path review | Middleware, config, env examples, route protections, external-call code, tests |
| `production-readiness` | You need deployability and operational confidence | Reproducibility, deployment, observability, migrations, rollback, security, CI |

### 2. Build A Project Map

Create the smallest defensible map of the project:

- languages and frameworks;
- entrypoints;
- services and workers;
- API routes and clients;
- database models and migrations;
- queues, caches, schedulers, and object storage;
- UI screens and backend dependencies;
- tests, fixtures, CI, and local run path;
- deployment, monitoring, and operational docs;
- external integrations.

If documentation is missing or weak, infer the factual project goals from names, routes, UI screens, DTOs, models, queues, deployment topology, and tests.

### 3. Check Reproducibility

Inspect whether a new reviewer can rebuild confidence from scratch:

- dependency manifests and lock files;
- supported runtime versions;
- install commands;
- build commands;
- test commands;
- required environment variables;
- local or dev startup path;
- database and migration setup;
- seed data or fixtures;
- CI or local verification commands.

Missing reproducibility evidence lowers the validation level even when the code looks reasonable.

### 4. Verify Cross-Part Contracts

Check both sides of important contracts, or mark the missing side as missing evidence.

- UI client calls vs backend routes.
- Router/controller parameters vs service signatures.
- DTO/schema fields vs persistence and serializers.
- Queue producers vs consumers.
- SQLAlchemy or ORM models vs migrations.
- Environment settings vs compose, Helm, CI, and deployment docs.
- Snapshot, clip, file, S3, or object-key paths across producers and consumers.
- Error shapes, status codes, required fields, optional fields, and serialization formats.

Contract mismatches are often higher priority than isolated code-style issues because they break integrated use.

### 5. Search For Incompleteness

Look for unfinished or misleading paths:

- `TODO`, `FIXME`, `pass`, `NotImplementedError`, `stub`, `placeholder`, `mock`, local-language equivalents;
- dead routes;
- unused modules;
- imported but unregistered routers;
- UI pages without API methods;
- schemas with fields that services do not save or return;
- tests that cover implementation details but miss user-visible behavior.

Do not automatically call every marker a bug. Classify it by impact and evidence.

### 6. Review Reliability Risks

Prioritize risks that can cause real runtime failure or data inconsistency:

- broad `except Exception`;
- queue ack/requeue behavior;
- message loss or duplicate processing;
- non-idempotent handlers;
- retries and timeouts;
- timezone/date handling;
- shared mutable state;
- in-memory deduplication;
- blocking I/O inside async code;
- resource cleanup and shutdown behavior.

### 7. Review Security Risks

Check:

- auth and authorization model;
- token storage and secret handling;
- CORS and public routes;
- debug endpoints;
- destructive commands or admin actions;
- webhook validation;
- external API calls and data exposure;
- test evidence for permission checks.

Security claims require actual middleware, permissions, configuration, and tests or runtime evidence. Documentation alone is not enough.

### 8. Classify Readiness Stage

Use stage labels as evidence-backed maturity states, not opinions:

- Draft prototype.
- Technical prototype.
- MVP.
- Integration MVP.
- Beta or pilot.
- Production-ready.
- Production with debt.

Never claim `Production-ready` without evidence for reproducible setup, deployment, migrations, security, observability, rollback, and critical tests.

### 9. Produce A Prioritized Closure Plan

Every report should include a remediation plan ordered by risk and unblock value:

- first fix blockers that make the project untruthful, unsafe, or unrunnable;
- then close high-risk contract, data, security, and reliability gaps;
- then add missing smoke, contract, or e2e checks around the most valuable flows;
- then improve documentation only after implementation facts are clear.

Each action should name the smallest next proof that would raise confidence.

## How This Differs

`project-readiness-auditor` is an evidence-based audit skill, not a generic static scanner, marketplace, or full software delivery framework.

| Nearby project | What it does | How `project-readiness-auditor` differs |
|---|---|---|
| [`howells/arc`](https://github.com/howells/arc) | Provides a broad Claude/Codex delivery workflow with skills for ideation, implementation, testing, audit, launch, commit, and release | Focuses narrowly on independent readiness audits: documentation-vs-code checks, evidence levels, missing evidence, readiness stage, severity-ranked findings, and a closure plan |
| [`github/awesome-copilot` `acquire-codebase-knowledge`](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md) | Maps, documents, and helps users onboard into an existing codebase | Uses codebase mapping as one audit step, then goes further into readiness verdicts, production evidence, contract risks, severity, residual risk, and next validation steps |
| [`github/awesome-copilot` `acreadiness-assess`](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md) | Runs AgentRC readiness assessment and produces an AI-readiness dashboard for a repository | Audits software/project readiness rather than AI-agent readiness: docs-vs-code, reproducibility, runtime proof, deployment, contracts, security, reliability, and truthful readiness claims |
| [`microsoft/agentrc`](https://github.com/microsoft/agentrc) | Reads a codebase, scores AI-readiness, generates agent instruction files, evals, and development configuration, and can monitor drift in CI | Treats AI-readiness as adjacent evidence, but produces a project audit report about actual product state, implementation gaps, operational risk, and evidence-backed readiness stage |
| [`oimiragieo/agent-studio`](https://github.com/oimiragieo/agent-studio) | Provides a large agent/skill framework with orchestration, plugin marketplace, headless execution, model routing, code review pipeline, and readiness scoring | Keeps the package small and methodology-specific: one installable audit skill with focused references, explicit stop rules, and no broad runtime or marketplace layer |

## Evidence Model

Use evidence levels to avoid overclaiming:

| Level | Meaning |
|---|---|
| L0 | Static file existence, Markdown/YAML, repository shape, and obvious contradictions |
| L1 | One realistic prompt, project slice, or narrow scenario checked |
| L2 | Cross-file consistency across relevant docs, code, configs, tests, and report format |
| L3 | One real project audit simulation with recorded findings and evidence |
| L4 | Repeated audits across several materially different project types |
| L5 | Public/release readiness with red-team review, install verification, documentation pass, and residual risk recorded |

Runtime, production, deployment, and release-readiness claims require inspected command output or recorded evidence. A static validator can prove package structure; it cannot prove a target project works.

## Severity Model

Findings should separate proven facts from plausible risks.

| Severity | Use for |
|---|---|
| `BLOCKER` | Prevents safe use, deployment, data integrity, or truthful readiness claims |
| `HIGH` | Likely serious runtime failure, security exposure, data loss, or cross-component breakage |
| `MEDIUM` | Material reliability, maintainability, or test gap that can affect normal use |
| `LOW` | Localized quality issue or incomplete evidence with limited impact |
| `INFO` | Observation, clarification, or non-blocking improvement |

If behavior was not reproduced, call it a likely risk or bug candidate, not a proven runtime bug.

## Timebox Profiles

Use timeboxes when the audit must be fast.

| Timebox | Goal | Typical output |
|---|---|---|
| 30 minutes | Orientation and obvious blockers | Project map, major contradictions, top blocker/high risks |
| 2 hours | Practical docs-vs-code audit | Claims matrix, contract risks, reproducibility gaps, test/CI status |
| 1 day | Runtime-backed readiness review | Setup/build/test/smoke evidence, security and reliability pass, prioritized plan |
| 3-5 days | Due diligence or production-readiness review | Cross-project evidence, operational gaps, rollback/observability/security proof, residual risk |

## Public Package

The installable Codex skill is under [`project-readiness-auditor/`](project-readiness-auditor/):

- [`SKILL.md`](project-readiness-auditor/SKILL.md): compact skill entry point and default workflow.
- [`agents/openai.yaml`](project-readiness-auditor/agents/openai.yaml): Codex interface metadata.
- [`references/audit-methodology.md`](project-readiness-auditor/references/audit-methodology.md): detailed audit workflow.
- [`references/readiness-rubric.md`](project-readiness-auditor/references/readiness-rubric.md): readiness stages, severities, evidence strength, verdicts, and validation levels.
- [`references/report-template.md`](project-readiness-auditor/references/report-template.md): Markdown report shape.
- [`scripts/validate_skill.py`](project-readiness-auditor/scripts/validate_skill.py): static package validation.

Root `AGENTS.md`, root `CLAUDE.md`, `.claude/`, `.codex/`, `.agents/`, and root `agents/` are local authoring files when present. They are ignored by Git and are not part of the public package.

## Install For Codex

From the repository root:

```bash
mkdir -p ~/.codex/skills
cp -R project-readiness-auditor ~/.codex/skills/project-readiness-auditor
```

Restart Codex, then use:

```text
Use $project-readiness-auditor to audit this repository in docs-vs-code mode. Compare README claims with code, tests, configuration, and deployment evidence. Produce findings, readiness stage, validation level, missing evidence, residual risk, and a prioritized closure plan.
```

## Expected Report

A useful audit report should include:

- audit mode;
- files inspected;
- commands run and outcomes;
- project map;
- readiness stage;
- validation level achieved;
- findings ordered by severity;
- evidence for each finding;
- missing evidence;
- residual risk;
- prioritized remediation plan;
- next smallest validation step.

## Validate

Validate the skill scaffold:

```bash
python3 project-readiness-auditor/scripts/validate_skill.py project-readiness-auditor
```

Expected result:

```text
RESULT: PASS L0
```

Current validation level: L0 until the skill package passes static validation and at least one realistic project-audit simulation is recorded.

## Repository Layout

- [`project-readiness-auditor/`](project-readiness-auditor/): public installable skill package.
- [`.github/workflows/validate.yml`](.github/workflows/validate.yml): package validation in CI.
- [`CHANGELOG.md`](CHANGELOG.md): release notes.
- [`README.md`](README.md): public project overview and audit methodology.
- [`VERSION`](VERSION): package version.
- [`LICENSE`](LICENSE): license.
- `.gitignore`: keeps local assistant workspace files out of Git.

## License

See [`LICENSE`](LICENSE).
