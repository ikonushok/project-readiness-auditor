# Audit Methodology

This method audits what a project actually contains, not what its documentation claims.

## Evidence Rules

- Treat README, specs, comments, diagrams, and presentations as intent until implementation evidence supports them.
- Treat code, tests, lock files, CI, deployment config, migrations, scripts, and inspected command output as evidence.
- Runtime claims require commands that were actually run and inspected.
- Production-readiness claims require reproducibility, deployment, operational, security, observability, and rollback evidence.
- If one side of a contract was not inspected, mark it as missing evidence.
- If behavior was not reproduced, report it as a risk or bug candidate rather than a proven runtime bug.

## Timebox Profiles

Use timeboxes to choose depth:

- 30 minutes: build the project map, spot obvious contradictions, identify top blocker/high risks.
- 2 hours: verify docs-vs-code claims, inspect contracts, check reproducibility, tests, and CI.
- 1 day: add runtime setup/build/test/smoke evidence plus reliability and security review.
- 3-5 days: perform due diligence or production-readiness review with operational, rollback, and observability evidence.

## 1. Fix The Audit Mode

- `code-only`: use source code, tests, configs, migrations, CI, Docker/Helm, and scripts.
- `docs-vs-code`: read docs as intent, then verify against implementation.
- `runtime`: additionally run setup, build, tests, smoke checks, or realistic scenarios.
- `security`: focus on auth, secrets, permissions, debug endpoints, webhooks, and external calls.
- `production-readiness`: focus on reproducibility, deployment, observability, migrations, rollback, and operational risk.

When more than one project is supplied, split the work before auditing:

- one target project at a time;
- one evidence log per target project;
- one report pack per target project;
- no shared findings table across unrelated repositories.

Cross-project summaries are allowed only as an index after all per-project reports exist. A cross-project summary is not a substitute for per-project evidence.

## 1a. Choose The Report Pack

Use separate report types for separate questions. Mandatory Bug Discovery is part of every audit, even when the requested report is not a standalone `bug-audit`. If the user asks for a full customer-style audit, produce the relevant report types below for each project and always include `bug-audit`.

### `code-only-project-readiness`

Purpose: answer what the project is, how complete it is, and where it breaks if documentation is ignored.

Evidence allowed:

- source code;
- tests and fixtures;
- executable config;
- package manifests and lock files;
- CI/deployment/monitoring files;
- inspected command output if runtime checks are allowed.

Documentation, specs, diagrams, roadmaps, and changelogs may be listed as excluded context, but must not be used as proof in this report.

Must include:

- short verdict;
- what is actually implemented in code;
- factual project structure;
- strengths visible in code;
- major gaps and unfinished implementation;
- readiness stage by code evidence only;
- next validation steps.

### `project-readiness`

Purpose: answer readiness against the project's stated goals.

Evidence allowed:

- README/specs/docs as intent;
- implementation evidence from code, tests, config, deployment files, migrations, scripts, and inspected runtime output.

Must include:

- stated or inferred project goals;
- maturity by component or capability;
- docs-vs-code mismatches;
- production-readiness risks;
- recommended work order;
- explicit claims not verified.

### `bug-audit`

Purpose: identify concrete likely bugs and the smallest test-first plan to prove or reject them. This report type is the full output form for the mandatory bug discovery phase.

Evidence allowed:

- code-level contradictions;
- route/service/schema mismatches;
- model/migration mismatches;
- producer/consumer mismatches;
- command output when allowed.

Must include:

- ranked bug candidates;
- evidence from file paths and symbols;
- trigger or reproduction condition;
- confidence;
- proposed regression test;
- current reproduction status: `NOT_REPRODUCED`, `REPRODUCED`, `NO_BUG_PROVEN`, `INCONCLUSIVE`, or `REJECTED`;
- explicit note that project files were not modified unless the user approved exact reproduction files and commands.

Do not fix production code in `bug-audit` mode unless the user separately asks for fixes and approves the exact production files and transformation after a bug is reproduced.

## 2. Build A Project Map

Identify:

- languages and frameworks;
- entrypoints;
- services and workers;
- API contracts;
- database models and migrations;
- queues, caches, schedules, and object storage;
- UI screens and clients;
- tests and fixtures;
- deployment, CI, monitoring, and runtime configuration;
- external integrations.

If documentation is missing or untrusted, infer factual goals from service names, API routes, UI screens, DTOs, database models, queues, deployment topology, tests, and fixtures.

## 3. Mandatory Bug Discovery

Run this phase in every audit. It is not optional and should happen immediately after the initial project map gives enough context to trace real paths.

### 3a. Discover Candidates Read-Only

Before explicit approval for a reproducer, do not create or edit target-project files, install dependencies, run formatters or migrations, modify configuration, generate target-project reports, or run commands likely to mutate project state. Read source, configuration, documentation, existing tests, user-supplied logs, and Git history when available. Existing targeted tests may be run only when clearly safe and non-mutating.

Look for falsifiable correctness defects:

- off-by-one boundaries;
- inverted conditions;
- missing empty, null, or absent-field handling;
- unsafe state transitions;
- ordering or deduplication errors;
- stale cache keys;
- permission checks after side effects;
- precision, locale, or timezone mistakes;
- async races and shared mutable state;
- inconsistent validation;
- error paths that violate a surrounding contract.

For every candidate, record:

- reachable path;
- contract evidence for expected behavior;
- triggering input or state;
- expected result;
- likely actual result;
- source location;
- impact;
- confidence.

Reject vague suspicions. A candidate must have a reachable path, defensible expected behavior, and a specific trigger.

### 3b. Rank Candidates

Rank by:

1. contract strength from tests, types, schemas, docs-as-intent, callers, or consistent nearby behavior;
2. reachability by real callers or valid input;
3. reproducibility with a small deterministic test or harness;
4. impact on outputs, data, permissions, crashes, or user-visible workflows.

Show at most five candidates. If no candidate survives, report `NO_BUG_PROVEN` for the inspected scope and name the next useful evidence instead of inventing a bug.

### 3c. Reproduction Approval Gate

Before creating or editing reproduction tests or harnesses, stop and present:

- candidate or candidates to test;
- why each could be a real bug;
- exact files to create or edit;
- minimal fixture or input;
- exact test or harness command;
- signal that will confirm each bug;
- main risk or uncertainty;
- statement that no project files have been modified.

Approval covers only the displayed reproduction files and commands.

### 3d. Fix Approval Gate

After a candidate is genuinely reproduced and root cause is isolated, stop again before changing production code. Present:

- reproduction status: `REPRODUCED`;
- proven bug;
- root cause;
- exact production files to change;
- proposed transformation;
- behavior that must remain identical;
- regression and broader test plan;
- main risk.

Approval covers only the displayed production files and transformation. After an approved fix, prove red-to-green by rerunning the same targeted reproducer and the broadest relevant checks.

## 4. Check Reproducibility

Look for:

- dependency manifests and lock files;
- supported runtime versions;
- install commands;
- build commands;
- test commands;
- required environment variables;
- local or dev startup path;
- database and migration setup;
- seed data or fixtures.

## 5. Check Cross-Part Contracts

Compare:

- UI client calls against backend routes;
- router/controller parameters against service signatures;
- DTOs and serializers against stored data;
- producers against consumers for queues and events;
- models against migrations;
- environment settings against compose, Helm, CI, and deployment files;
- file paths and object storage keys across producers and consumers.

Also check required/optional fields, status codes, error shapes, serialization formats, retry semantics, and idempotency expectations.

## 6. Search For Incompleteness

Search for:

- TODO, FIXME, stub, placeholder, NotImplemented, pass, mock-only paths;
- dead routes and unregistered modules;
- unused services and imports;
- UI pages without API methods;
- schemas with fields that are not persisted or returned;
- tests that assert implementation details but not user-visible behavior.

## 7. Review Reliability

Check:

- broad exception handling;
- ack/requeue behavior;
- message loss and duplicate processing;
- idempotency;
- timeout and retry behavior;
- timezone/date handling;
- shared mutable state;
- in-memory deduplication;
- blocking I/O inside async code;
- resource cleanup and shutdown behavior.

## 8. Review Security

Check:

- auth and authorization model;
- token storage and secret handling;
- CORS and public routes;
- debug endpoints;
- destructive commands or admin actions;
- webhook validation;
- external API calls and data exposure.

## 9. Classify Readiness

Classify the project as one of:

- Draft prototype;
- Technical prototype;
- MVP;
- Integration MVP;
- Beta or pilot;
- Production-ready;
- Production with debt.

Use the readiness rubric. Do not claim Production-ready without reproducible setup, deployment, migrations, security, observability, rollback, and critical test evidence.

## 10. Build The Closure Plan

Prioritize remediation by risk and unblock value:

- First fix blockers that make the project untruthful, unsafe, unrunnable, or impossible to validate.
- Then fix high-risk contract, data, security, and reliability gaps.
- Then add smoke, contract, or e2e tests around the highest-value flows.
- Then update documentation to match verified implementation facts.

Each action should include the smallest next proof that would raise confidence.

## 11. Report

Report findings by severity, cite evidence, state the readiness stage, state validation level L0-L5, include missing evidence and residual risk, and name the smallest next check that would improve confidence.

For multi-project work, write report files using a stable per-project layout when writing to disk:

```text
reports/customer/<project-slug>/code-only-project-readiness-YYYY-MM-DD.md
reports/customer/<project-slug>/project-readiness-YYYY-MM-DD.md
reports/customer/<project-slug>/bug-audit-YYYY-MM-DD.md
```

Create the report types that match the user's request, but never omit Mandatory Bug Discovery from the audit evidence. For full customer-style audits, include the standalone `bug-audit` report. If the user points to examples with all three styles and asks for the skill to support them, update the skill templates and validation rules rather than generating customer audit reports for this repository.
