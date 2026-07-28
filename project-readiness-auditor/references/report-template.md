# Audit Report Templates

Use these shapes for per-project audit reports. When multiple projects are supplied, produce one report pack per project. Do not combine unrelated projects into one findings report.

## Report Pack Rules

- One target project per report file.
- One evidence log per report file.
- Use stable filenames:
  - `code-only-project-readiness-YYYY-MM-DD.md`
  - `project-readiness-YYYY-MM-DD.md`
  - `bug-audit-YYYY-MM-DD.md`
- Put multi-project customer outputs under `reports/customer/<project-slug>/`.
- A cross-project index may link to per-project reports, but must not replace them.
- Every report must name its audit mode, report type, files inspected, commands run, evidence level, findings, missing evidence, residual risk, and next smallest validation step.
- Every report summary must name the target project.
- Every audit report must include Mandatory Bug Discovery. If no defensible bug candidate is found, report `NO_BUG_PROVEN` for the inspected scope instead of omitting the section.

## Code-Only Project Readiness

Use this shape when documentation must not be used as proof.

### Summary

- Verdict:
- Readiness stage:
- Validation level / evidence level:
- Audit mode: `code-only`
- Report type: `code-only-project-readiness`
- Target project:
- Scope:
- Excluded context:
- Main risk:

### What Is Implemented In Code

| Area | Evidence | Status |
|---|---|---|
|  |  |  |

### Code Project Map

- Languages and frameworks:
- Entrypoints:
- Services and workers:
- API/UI contracts:
- Database and migrations:
- Queues, caches, schedules:
- External integrations:
- Tests and CI:
- Deployment and monitoring:

### Strengths Visible In Code

| Strength | Evidence | Why it matters |
|---|---|---|
|  |  |  |

### Gaps And Risks

| Priority | Area | Evidence | Impact |
|---|---|---|---|
| P0 |  |  |  |
| P1 |  |  |  |
| P2 |  |  |  |

### Mandatory Bug Discovery

- Status:
- Inspected paths:
- Candidate count:
- Strongest candidate:
- Reproduction status:
- Proposed test-first next step:

| # | Candidate | Contract evidence | Trigger | Location | Confidence |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |

### Contract Reliability Security Checks

- Cross-part contracts:
- Error handling and queue/file/data loss risk:
- Idempotency, retries, and time/state handling:
- Auth, permissions, secrets, and public surfaces:
- Unfinished or dead paths:

### Findings

For every finding include severity, confidence, area, evidence, what is proven, impact, and recommended next action.

### Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 |  |  |  |
| P1 |  |  |  |
| P2 |  |  |  |

### Readiness Assessment

- Current stage:
- Why not lower:
- Why not production-ready:
- Smallest next validation step:

### Evidence Log

- Files inspected:
- Commands run:
- Command outcomes:
- Claims not verified:
- Residual risk:

## Project Readiness

Use this shape when docs/specs/goals are intent and code/config/tests are proof.

### Summary

- Verdict:
- Readiness stage:
- Validation level / evidence level:
- Audit mode:
- Report type: `project-readiness`
- Target project:
- Scope:
- Main risk:

### Project Goals

- Stated goals:
- Inferred goals:
- Non-goals:

### Project Map

- Languages and frameworks:
- Entrypoints:
- Services and workers:
- API/UI contracts:
- Database and migrations:
- Queues, caches, schedules:
- External integrations:
- Tests and CI:
- Deployment and monitoring:

### Findings

#### Finding 1

- Severity:
- Confidence:
- Area:
- Evidence:
- What is proven:
- Impact:
- Recommended next action:

### Mandatory Bug Discovery

- Status:
- Inspected paths:
- Candidate count:
- Strongest candidate:
- Reproduction status:
- Proposed test-first next step:

| # | Candidate | Contract evidence | Trigger | Location | Confidence |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |

### Readiness By Capability

| Capability | Current status | Evidence | Readiness |
|---|---|---|---|
|  |  |  |  |

### Reproducibility

- Dependency evidence:
- Build evidence:
- Test evidence:
- Runtime evidence:
- Required environment:
- Missing evidence:

### Contract Review

- UI vs backend:
- API schemas vs services:
- Producers vs consumers:
- Models vs migrations:
- Env settings vs deploy config:
- File/object paths:

### Security And Reliability

- Auth and permissions:
- Secrets and tokens:
- CORS and public endpoints:
- Error handling:
- Idempotency and retries:
- Time and state handling:

### Readiness Assessment

- Current stage:
- Why this stage:
- What blocks the next stage:
- Smallest next validation step:

### Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 |  |  |  |
| P1 |  |  |  |
| P2 |  |  |  |

### Evidence Log

- Files inspected:
- Commands run:
- Command outcomes:
- Claims not verified:
- Residual risk:

## Bug Audit

Use this shape for the mandatory bug discovery phase and when the user asks for likely bugs, regressions, or a bug-focused audit.

### Summary

- Verdict:
- Validation level / evidence level:
- Audit mode:
- Report type: `bug-audit`
- Target project:
- Scope:
- Main risk:

### Bug Candidates

| # | Candidate | Contract evidence | Trigger | Location | Confidence | Reproduction status |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  | `NOT_REPRODUCED` |

If no candidate survives ranking, set status to `NO_BUG_PROVEN` and describe the inspected scope plus next useful evidence.

### Reproduction Approval Gate

Use before creating or editing reproduction tests or harnesses.

- Candidate(s) to test:
- Why each could be a real bug:
- Exact files to create or edit:
- Minimal fixture or input:
- Test or harness command:
- Signal that will confirm each bug:
- Main risk or uncertainty:
- Project files modified so far: `no`

### Fix Approval Gate

Use only after a candidate is reproduced.

- Reproduction status: `REPRODUCED`
- Proven bug:
- Root cause:
- Exact production files to change:
- Proposed transformation:
- Behavior that must remain identical:
- Regression and broader test plan:
- Main risk:

### Commands Attempted

- Command:
- Outcome:
- Interpretation:

### Recommended Order

1. Discover and rank candidates read-only in every audit.
2. Prove or reject the highest-confidence candidates only after approval for exact reproduction files and commands.
3. Fix only reproduced defects after separate approval for exact production files and transformation.
4. Rerun the same tests red-to-green.
5. Move ambiguous contract gaps into the product/API backlog.

### Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 |  |  |  |
| P1 |  |  |  |
| P2 |  |  |  |

### Evidence Log

- Files inspected:
- Commands run:
- Command outcomes:
- Candidates not reproduced:
- Residual risk:
