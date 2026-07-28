---
name: project-readiness-auditor
description: Evidence-based auditor for third-party software projects. Use for code-only review, docs-vs-code validation, readiness assessment, risk classification, technical due diligence, and actionable Markdown reports.
---

# Project Readiness Auditor

Audit third-party repositories by proving or rejecting project claims with concrete evidence.

## Default Workflow

1. Choose the audit mode:
   - `code-only`: inspect code, tests, configs, migrations, CI, Docker/Helm, and scripts.
   - `docs-vs-code`: compare documentation claims with actual implementation.
   - `runtime`: run setup, build, tests, smoke checks, or local scenarios when feasible.
   - `security`: inspect auth, secrets, CORS, permissions, debug endpoints, and external calls.
   - `production-readiness`: inspect reproducibility, deployment, observability, migrations, rollback, and operational risk.
2. If the user gives a timebox, scale depth to it: 30 minutes for orientation, 2 hours for docs-vs-code and contracts, 1 day for runtime-backed readiness, 3-5 days for due diligence.
3. Build a project map: languages, frameworks, entrypoints, services, workers, APIs, database, queues, caches, UI, tests, deploy, monitoring, and external integrations.
4. Check reproducibility: dependency manifests, lock files, setup commands, required environment variables, build commands, test commands, and local runtime path.
5. Check cross-part contracts: UI client vs backend routes, routers vs services, DTOs vs producers/consumers, models vs migrations, env settings vs compose/Helm, file/object paths across producers and consumers.
6. Search for unfinished work: TODO, FIXME, stubs, placeholder handlers, unregistered routes, dead modules, missing persistence, and UI pages without backing APIs.
7. Review reliability and security risks.
8. Classify project stage and produce an evidence-backed Markdown report with a prioritized closure plan.

## References

Read only what the task needs:

- `references/audit-methodology.md` for the full audit method, timeboxes, contracts, and closure planning.
- `references/readiness-rubric.md` for maturity stages, severity, verdicts, and evidence levels.
- `references/report-template.md` for the final Markdown report shape.

## Package Surface

This installable skill ships only the public audit workflow:

- `SKILL.md`;
- `agents/openai.yaml`;
- `references/audit-methodology.md`;
- `references/readiness-rubric.md`;
- `references/report-template.md`;

Root workspace files such as `AGENTS.md`, `CLAUDE.md`, `.claude/`, and root `agents/` are local authoring aids when present. Do not depend on them for installed-skill behavior.

## Stop Rules

- Do not trust README or product claims without implementation evidence.
- Do not claim runtime validation unless commands were actually run and inspected.
- Do not claim production readiness without deployment, security, observability, reproducibility, and rollback evidence.
- Do not run destructive target-repository commands without explicit approval.
- Do not report a plausible issue as a proven runtime bug unless it was reproduced or directly proven by code evidence.
- Do not inflate agent count unless a recurring audit workflow has a distinct trigger, checklist, and output.

## Output

Return:

- audit mode;
- project map;
- findings ordered by severity;
- evidence for each finding;
- readiness stage;
- validation level L0-L5;
- commands run;
- missing evidence;
- residual risk;
- prioritized remediation plan;
- next smallest validation step.
