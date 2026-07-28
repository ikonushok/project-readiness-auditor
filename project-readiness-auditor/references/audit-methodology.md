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

## 3. Check Reproducibility

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

## 4. Check Cross-Part Contracts

Compare:

- UI client calls against backend routes;
- router/controller parameters against service signatures;
- DTOs and serializers against stored data;
- producers against consumers for queues and events;
- models against migrations;
- environment settings against compose, Helm, CI, and deployment files;
- file paths and object storage keys across producers and consumers.

Also check required/optional fields, status codes, error shapes, serialization formats, retry semantics, and idempotency expectations.

## 5. Search For Incompleteness

Search for:

- TODO, FIXME, stub, placeholder, NotImplemented, pass, mock-only paths;
- dead routes and unregistered modules;
- unused services and imports;
- UI pages without API methods;
- schemas with fields that are not persisted or returned;
- tests that assert implementation details but not user-visible behavior.

## 6. Review Reliability

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

## 7. Review Security

Check:

- auth and authorization model;
- token storage and secret handling;
- CORS and public routes;
- debug endpoints;
- destructive commands or admin actions;
- webhook validation;
- external API calls and data exposure.

## 8. Classify Readiness

Classify the project as one of:

- Draft prototype;
- Technical prototype;
- MVP;
- Integration MVP;
- Beta or pilot;
- Production-ready;
- Production with debt.

Use the readiness rubric. Do not claim Production-ready without reproducible setup, deployment, migrations, security, observability, rollback, and critical test evidence.

## 9. Build The Closure Plan

Prioritize remediation by risk and unblock value:

- First fix blockers that make the project untruthful, unsafe, unrunnable, or impossible to validate.
- Then fix high-risk contract, data, security, and reliability gaps.
- Then add smoke, contract, or e2e tests around the highest-value flows.
- Then update documentation to match verified implementation facts.

Each action should include the smallest next proof that would raise confidence.

## 10. Report

Report findings by severity, cite evidence, state the readiness stage, state validation level L0-L5, include missing evidence and residual risk, and name the smallest next check that would improve confidence.
