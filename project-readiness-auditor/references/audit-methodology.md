# Audit Methodology

This method audits what a project actually contains, not what its documentation claims.

## Evidence Rules

- Treat README, specs, comments, diagrams, and presentations as intent until implementation evidence supports them.
- Treat code, tests, lock files, CI, deployment config, migrations, scripts, and inspected command output as evidence.
- Treat previous audit reports as excluded context for a new audit. They are never examples, sources of findings, source-of-truth evidence, or checklists.
- When comparison with previous reports is requested, first complete and freeze the new audit from primary evidence only. Then inspect older reports only as comparison artifacts.
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

Full report pack is the default for every project audit unless the user explicitly asks for a brief, summary, short, quick orientation, or otherwise constrained single-report output. A full report pack contains:

- `index.md`;
- `code-only-project-readiness-YYYY-MM-DD.md`;
- `project-readiness-YYYY-MM-DD.md`;
- `bug-audit-YYYY-MM-DD.md`.

Write the full report pack to `reports/customer/<project-slug>/` by default when the workspace is writable. If that path is unavailable, use the user-approved report directory or return the same four named reports in chat. Do not silently collapse a non-brief audit into one report.

Report language follows the user's request language unless the user explicitly asks for another language. For mixed-language requests, use the language of the main audit instruction.

Use separate report types for the three core audit questions:

1. What does the code/config/test/deploy evidence prove without trusting documentation?
2. How well does the implementation match documentation, stated goals, and inferred project objectives?
3. What concrete bug candidates and high-risk defects are visible, and what is the approval-gated reproduction/fix path?

Mandatory Bug Discovery is part of every audit, even for brief output. For non-brief output, always include the standalone `bug-audit` report.

For full project audits, the report pack must read like a decision aid, not just an evidence log. Start with the practical verdict, maturity stage, approximate readiness for the relevant use case when defensible, the top risks, and the next work batch. Then provide evidence. Do not hide the conclusion until the end.

Avoid over-compression. A useful report should be short enough to read, but deep enough that a team can understand what the project actually does, what is mature, what is incomplete, and what to do next. For non-brief audits, preserve depth by using the default index plus `code-only-project-readiness`, `project-readiness`, and `bug-audit` files rather than deleting sections or merging the three questions into one document.

## 1b. Compare Previous Reports Only After Freeze

If the user asks to compare a new audit with previous reports:

1. Do not open previous audit reports during discovery, bug ranking, evidence collection, report shaping, or work-order selection.
2. Generate the current audit from primary evidence: code, tests, config, CI, deploy files, migrations, scripts, docs-as-intent, and inspected command output.
3. Freeze the current audit by writing or delivering it before reading previous reports.
4. Read previous reports only after the freeze, and label them as comparison artifacts.
5. Put comparison output in a clearly separated section, file, or chat table.
6. Report whether differences are caused by new evidence, changed target code, different validation depth, stronger/weaker claims, or earlier report errors.
7. Do not retroactively rewrite the current audit findings from previous-report content unless the user explicitly asks for a revised audit and the revision cites primary evidence.

When writing the comparison, classify deltas explicitly:

- `Better`: primary evidence shows a real implementation, validation, operational, or product-readiness improvement.
- `Worse`: primary evidence shows a new risk, a clearer impact of an old risk, a regression, or a weaker claim than before.
- `Unchanged`: the same target commit, same unclosed defect, same missing evidence, or same validation level remains.

Use separate comparison rows for:

- same target commit with no real product progress;
- roadmap documentation vs implemented code;
- security risk became clearer but not fixed;
- test surface grew but validation level did not increase;
- old report mistake or overclaim corrected by the new audit.

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
- executive narrative that explains the code-only stage in plain language;
- what is actually implemented in code;
- code-visible tasks or workflows reconstructed from implementation evidence;
- factual project structure;
- strengths visible in code;
- major gaps and unfinished implementation;
- practical readiness estimate when evidence supports one;
- readiness stage by code evidence only;
- next validation steps.

### `project-readiness`

Purpose: answer readiness against the project's stated goals.

Evidence allowed:

- README/specs/docs as intent;
- implementation evidence from code, tests, config, deployment files, migrations, scripts, and inspected runtime output.

Must include:

- executive narrative for product, technical, and operational decision-makers;
- stated or inferred project goals;
- product maturity by phase, component, contour, or capability;
- maturity by component or capability;
- docs-vs-code mismatches;
- production-readiness risks;
- what is mature, what is still roadmap, and what blocks the target system;
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
- top-3 immediate bug-fix batch when at least three high-confidence candidates exist;
- second engineering batch and backlog/hardening batch when candidates differ in urgency or ownership;
- evidence from file paths and symbols;
- trigger or reproduction condition;
- confidence;
- proposed regression test;
- current reproduction status: `NOT_REPRODUCED`, `REPRODUCED`, `NO_BUG_PROVEN`, `INCONCLUSIVE`, or `REJECTED`;
- explicit note that project files were not modified unless the user approved exact reproduction files and commands.

Do not fix production code in `bug-audit` mode unless the user separately asks for fixes and approves the exact production files and transformation after a bug is reproduced.

## 1c. Specification Traceability

Apply within `docs-vs-code` and the `project-readiness` report; no separate audit mode or agent is needed. Specification Traceability connects expected behavior to evidence without treating the specification as proof. Keep the code-only baseline independent of specification claims.

### Select Applicable Sources

- Discover user-supplied specs, PRDs, `specs/**/spec.md`, acceptance criteria, API contracts, and relevant README claims. Support ordinary documents as well as Spec Kit; installation or execution of a spec tool is unnecessary.
- Record each source's path/section, version or date (or `UNKNOWN`), approval status, target release/component, and applicability decision in Specification Sources. A template is not a populated specification.
- Distinguish approved current requirements from draft, superseded, and future-release proposals. Do not make a draft or roadmap item a current-release obligation without user confirmation or other inspected scope evidence.
- Record conflicting sources and unresolved scope as `AMBIGUOUS`; explain which source is applicable and why when the conflict can be resolved. Do not silently prefer a newer file or infer approval from its filename.
- If no specification is available, write `Specification availability: NONE`, explain the search scope, and label inferred goals separately. Do not invent requirements or calculate specification coverage.

### Map Requirements To Evidence

New reports use `Specification traceability: v1` and `Specification availability: PRESENT` or `NONE`. With `PRESENT`, populate Specification Sources and Requirements Traceability using the report template.

Preserve requirement IDs such as `FR-001`/`SC-001`; assign local IDs plus source anchors when absent. Identify a requirement by its source and ID together when different specs reuse IDs. Split compound requirements where different clauses have different evidence, adding clause suffixes when necessary. Include acceptance scenarios, negative/edge cases, and measurable non-functional constraints. Record the inspected subset and exclusions when the timebox prevents full coverage; do not imply uninspected requirements were checked.

For every inspected requirement record expected behavior, source, implementation evidence, verification evidence, status, and gap/next check. Cite symbols/lines and test cases. A test file's existence is not proof that it passed; label inspected but unrun tests explicitly. Performance, availability, durability, security, and external-service claims need appropriate measured or runtime/framework evidence, not only code or an intended test command.

Use these requirement statuses (distinct from the report verdict):

- `CONFIRMED`: the cited evidence establishes the whole requirement at the explicitly stated validation depth. Static evidence can confirm a static property; runtime behavior needs corresponding execution evidence.
- `PARTIAL`: evidence supports only part of the requirement; identify the missing clause or verification.
- `CONTRADICTED`: inspected evidence conflicts with an applicable requirement; name the precise contradiction and its evidence strength.
- `NOT_CHECKED`: evidence is missing or the requirement was not inspected/run. This does not mean the capability is absent.
- `AMBIGUOUS`: wording, source precedence, applicability, or success criteria prevent a defensible judgment.
- `OUT_OF_SCOPE`: draft, superseded, future-release, or excluded requirement; explain why it is outside this audit.

Separate missing implementation from missing verification. A missing required capability is a `product/API gap` unless stronger correctness evidence establishes a bug. Feed defensible contradictions and acceptance edge cases into Mandatory Bug Discovery; do not promote every unmet requirement to a proven bug. Do not report a coverage percentage without a stated applicable-requirement denominator and inspected scope; evidence coverage and feature completeness are different measures.

For new report packs validate with `--strict-report-quality --require-spec-traceability --customer-report-pack <slug>`. For an explicitly requested brief standalone report use `--spec-traceability-report <path>`, which requires v1 traceability without scanning customer report packs. Strict validation automatically checks versioned traceability sections when present. The explicit flag requires them, while historical reports without the marker remain supported. These checks validate report structure and evidence references, not whether cited evidence truly proves behavior.

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

Show the top candidates and group them by actionability. Prefer a top-3 immediate bug-fix batch for the highest-confidence, smallest-reproduction defects, then separate second-batch engineering issues from product/API backlog or hardening work. If no candidate survives, report `NO_BUG_PROVEN` for the inspected scope and name the next useful evidence instead of inventing a bug.

### 3c. Claim Strength Rules

Classify every bug or risk claim by the strongest evidence actually inspected:

- `reproduced`: an approved test, smoke check, or command demonstrated the behavior.
- `direct code contradiction`: inspected code has an internal contradiction that does not depend on framework resolution, such as a caller using a missing method, wrong keyword argument, undefined variable, schema field not persisted, or producer payload missing a required consumer field.
- `static config contradiction`: inspected configuration cannot satisfy the target runtime contour, such as required settings missing from env examples, compose service names not matching monitoring targets, or Helm values that conflict with application settings.
- `framework/runtime candidate`: the claim depends on runtime dispatch, dependency injection, route ordering, middleware, serialization, database behavior, queue delivery, or external service behavior that was not executed.
- `product/API gap`: the implementation is internally consistent but incomplete or ambiguous against stated intent.

Do not label a framework/runtime candidate as proven until a route table, framework introspection, existing test, smoke command, or approved reproducer verifies it. Route ordering, dependency injection, middleware precedence, auth behavior, ORM lazy loading, retry delivery, and async cancellation claims need runtime or framework-specific evidence unless there is also a direct code contradiction.

When a single endpoint has both a direct code contradiction and a framework/runtime concern, report the direct contradiction as the proven static evidence and keep the runtime concern as a separate unverified risk.

### 3d. Reproduction Approval Gate

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

### 3e. Fix Approval Gate

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

For config-heavy projects, perform a consistency check instead of only listing files:

- compare settings schema and required environment variables against env examples, compose, Helm, CI, and deployment docs;
- compare compose service names, exposed ports, and healthchecks against monitoring targets and dashboard assumptions;
- compare Helm values and templates against application settings, secret names, queue names, storage buckets, and service ports;
- lower the readiness estimate when the project has tests or deploy files but the documented or visible setup cannot run without missing dependencies, missing env values, or unavailable toolchain commands.

## 5. Check Cross-Part Contracts

Compare:

- UI client calls against backend routes;
- router/controller parameters against service signatures;
- DTOs and serializers against stored data;
- producers against consumers for queues and events;
- models against migrations;
- environment settings against compose, Helm, CI, and deployment files;
- monitoring targets against service names, ports, metrics paths, and deployment contours;
- file paths and object storage keys across producers and consumers.

Also check required/optional fields, status codes, error shapes, serialization formats, retry semantics, and idempotency expectations.

## 6. Search For Incompleteness

Search for:

- TODO, FIXME, stub, placeholder, NotImplemented, pass, mock-only paths;
- dead routes and unregistered modules;
- registered routes with no reachable client and client/API paths with no registered backend route;
- routers, services, queues, or admin screens that exist but are not wired into the application entrypoint;
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

For customer or product readiness reports, also explain the stage in practical terms:

- what the project can credibly be used for now;
- what is mature enough for a pilot or stage contour;
- what is still a product, operational, security, or ML-lifecycle gap;
- what would be misleading to claim externally.

## 10. Build The Closure Plan

Prioritize remediation by risk and unblock value:

- First fix blockers that make the project untruthful, unsafe, unrunnable, or impossible to validate.
- Then fix high-risk contract, data, security, and reliability gaps.
- Then add smoke, contract, or e2e tests around the highest-value flows.
- Then update documentation to match verified implementation facts.

Each action should include the smallest next proof that would raise confidence.

## 11. Report

Report findings by severity, cite evidence, state the readiness stage, state validation level L0-L5, include missing evidence and residual risk, and name the smallest next check that would improve confidence.

Every substantial project report should include:

- an executive narrative before detailed evidence;
- code-visible tasks in code-only reports;
- product maturity in docs-vs-code and readiness reports;
- the top-3 immediate bug batch when bug candidates exist;
- a batch split between immediate fixes, second engineering work, and backlog/hardening when appropriate;
- a concise work order that helps a team decide what to do next.

For multi-project work, write report files using a stable per-project layout when writing to disk:

```text
reports/customer/<project-slug>/index.md
reports/customer/<project-slug>/code-only-project-readiness-YYYY-MM-DD.md
reports/customer/<project-slug>/project-readiness-YYYY-MM-DD.md
reports/customer/<project-slug>/bug-audit-YYYY-MM-DD.md
```

Create the full report pack by default and write it to `reports/customer/<project-slug>/` when the workspace is writable. Create a single report only when the user explicitly requests a brief/summary/short output or a tightly constrained single-report audit. Never omit Mandatory Bug Discovery from the audit evidence. If the user points to examples with all three styles and asks for the skill to support them, update the skill templates and validation rules rather than generating customer audit reports for this repository.
