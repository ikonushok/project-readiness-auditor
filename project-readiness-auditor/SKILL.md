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
2. If multiple projects are supplied, audit each project separately. Never merge unrelated projects into one findings report. Produce one report pack per project.
3. Treat previous audit reports as excluded context for the new audit. They are never examples, sources of findings, source-of-truth evidence, or checklists. If the user asks to compare with older reports, first complete and freeze the new audit from primary evidence only; then inspect older reports only as comparison artifacts.
4. If the user asks for "all reports", "customer reports", "full readiness", or gives examples that include several report styles, produce these per-project report types:
   - `code-only-project-readiness`: code, tests, executable config, CI/deploy evidence only; documentation is not proof.
   - `project-readiness`: goals/docs-vs-code readiness against stated project objectives.
   - `bug-audit`: mandatory ranked bug candidates with reproduction plan and test-first next steps.
5. If the user gives a timebox, scale depth to it: 30 minutes for orientation, 2 hours for docs-vs-code and contracts, 1 day for runtime-backed readiness, 3-5 days for due diligence.
6. Build a project map: languages, frameworks, entrypoints, services, workers, APIs, database, queues, caches, UI, tests, deploy, monitoring, and external integrations.
7. Run Mandatory Bug Discovery immediately for every audit. Trace reachable inputs, contracts, state transitions, edge cases, error paths, and real callers; rank concrete bug candidates by contract strength, reachability, reproducibility, and impact.
8. Classify claim strength before writing findings: `reproduced`, `direct code contradiction`, `static config contradiction`, `framework/runtime candidate`, or `product/API gap`. Do not treat route ordering, dependency injection, middleware, database, queue, or external-service behavior as proven without runtime or framework-specific evidence.
9. Check reproducibility: dependency manifests, lock files, setup commands, required environment variables, build commands, test commands, and local runtime path. Compare settings schema against env examples, compose, Helm, and CI instead of only listing those files.
10. Check cross-part contracts: UI client vs backend routes, routers vs services, DTOs vs producers/consumers, models vs migrations, env settings vs compose/Helm, monitoring targets vs service names/ports/metrics paths, file/object paths across producers and consumers.
11. Search for unfinished work: TODO, FIXME, stubs, placeholder handlers, unregistered routes, dead modules, missing persistence, UI pages without backing APIs, and routers/services/admin screens that exist but are not wired into the application entrypoint.
12. Review reliability and security risks.
13. Write reports as decision documents, not scanner dumps:
   - start with an executive narrative that names the practical stage, the main decision, the main risks, and the next work batch;
   - include product maturity for customer/product audits, including phases, stage/prod contour, operations, and roadmap-only capabilities when visible;
   - include code-visible tasks in code-only audits so readers understand what the project actually does without documentation;
   - keep detailed evidence, commands, and missing proof, but avoid duplicating the same findings table across every section.
14. Classify project stage and produce evidence-backed Markdown reports with prioritized closure plans.

## References

Read only what the task needs:

- `references/audit-methodology.md` for the full audit method, timeboxes, contracts, and closure planning.
- `references/prior-report-freeze-validation-scenario.md` for validating that older reports are opened only after a new audit is complete and frozen.
- `references/readiness-rubric.md` for maturity stages, severity, verdicts, and evidence levels.
- `references/report-template.md` for per-project report pack rules and Markdown report shapes.

## Package Surface

This installable skill ships only the public audit workflow:

- `SKILL.md`;
- `agents/openai.yaml`;
- `references/audit-methodology.md`;
- `references/prior-report-freeze-validation-scenario.md`;
- `references/readiness-rubric.md`;
- `references/report-template.md`;

Root workspace files such as `AGENTS.md`, `CLAUDE.md`, `.claude/`, and root `agents/` are local authoring aids when present. Do not depend on them for installed-skill behavior.

## Stop Rules

- Do not trust README or product claims without implementation evidence.
- Do not use previous audit reports as templates, source evidence, finding sources, or audit checklists for a new audit.
- Do not claim runtime validation unless commands were actually run and inspected.
- Do not claim production readiness without deployment, security, observability, reproducibility, and rollback evidence.
- Do not run destructive target-repository commands without explicit approval.
- Do not report a plausible issue as a proven runtime bug unless it was reproduced or directly proven by code evidence.
- Do not skip Mandatory Bug Discovery. If no defensible candidate is found, report `NO_BUG_PROVEN` for the inspected scope and state the next useful evidence.
- Do not create reproduction files, edit tests, install dependencies, or run mutating commands for bug proof without explicit approval for the exact files and commands.
- Do not change production code for a reproduced bug without a second explicit approval for the exact production files and fix.
- Do not inflate agent count unless a recurring audit workflow has a distinct trigger, checklist, and output.
- Do not combine findings for multiple target projects into a single readiness report.
- Do not write customer-style audit output until you have chosen the report type and target project for that output.
- Do not produce an over-compressed report for a real project audit. Unless the user requests a brief summary, each report must include enough narrative and evidence for a team to make a decision without asking what the project actually does.

## Output

Return:

- audit mode;
- report type;
- target project;
- project map;
- executive narrative;
- code-visible tasks for code-only reports;
- product maturity view for product/readiness reports;
- mandatory bug discovery result;
- top-3 immediate bug batch and backlog split when bug candidates exist;
- findings ordered by severity;
- evidence for each finding;
- readiness stage;
- validation level L0-L5;
- commands run;
- missing evidence;
- residual risk;
- prioritized remediation plan;
- next smallest validation step.
