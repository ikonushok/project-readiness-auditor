# Audit Report Templates

Use these shapes for per-project audit reports. When multiple projects are supplied, produce one report pack per project. Do not combine unrelated projects into one findings report.

## Report Pack Rules

- One target project per report file.
- One evidence log per report file.
- Previous audit reports are excluded context for new audit findings. If comparison with older reports is requested, generate the current report pack from primary evidence first, then compare against older reports in a clearly separated comparison section or file.
- Use stable filenames:
  - `code-only-project-readiness-YYYY-MM-DD.md`
  - `project-readiness-YYYY-MM-DD.md`
  - `bug-audit-YYYY-MM-DD.md`
- Put multi-project customer outputs under `reports/customer/<project-slug>/`.
- A cross-project index may link to per-project reports, but must not replace them.
- Every report must name its audit mode, report type, files inspected, commands run, evidence level, findings, missing evidence, residual risk, and next smallest validation step.
- Every report summary must name the target project.
- Every audit report must include Mandatory Bug Discovery. If no defensible bug candidate is found, report `NO_BUG_PROVEN` for the inspected scope instead of omitting the section.
- Full project audits should include a short `index.md` decision brief when report files are written to disk. The index should name the overall verdict, practical readiness stage, top risks, report links, and recommended work order.
- Do not over-compress real project audits. Keep reports concise, but include enough narrative, product/context explanation, and evidence for a team to make a decision.

## Report Pack Index

Use this shape when writing a multi-report pack.

### Executive Decision

- Target project:
- Verdict:
- Practical readiness stage:
- Practical readiness estimate, if defensible:
- Main decision:
- Main reason:
- Evidence level:

### Three Main Risks

| Risk | Why it matters | First proof needed |
|---|---|---|
|  |  |  |

### Reports

| Report | Purpose | Best audience |
|---|---|---|
| `code-only-project-readiness-YYYY-MM-DD.md` |  |  |
| `project-readiness-YYYY-MM-DD.md` |  |  |
| `bug-audit-YYYY-MM-DD.md` |  |  |

### Recommended Work Order

| Step | Action | Reason |
|---|---|---|
| 1 |  |  |

## Previous Report Comparison

Use only after the current audit report pack has been completed from primary evidence. Previous reports are comparison artifacts, not audit evidence.

| Criterion | Current audit | Previous report A | Previous report B | Interpretation |
|---|---|---|---|---|
| Verdict |  |  |  |  |
| Readiness stage |  |  |  |  |
| Validation level |  |  |  |  |
| Top blockers |  |  |  |  |
| Bug candidates |  |  |  |  |
| Runtime evidence |  |  |  |  |
| Missing evidence |  |  |  |  |
| New findings |  |  |  |  |
| Weaker or unsupported claims |  |  |  |  |
| Recommended next step |  |  |  |  |

When writing the interpretation, distinguish:

- newly discovered primary evidence;
- changed target-project files;
- different validation depth;
- stronger or weaker claim wording;
- likely mistakes in older reports.

## Code-Only Project Readiness

Use this shape when documentation must not be used as proof.

### Summary

- Verdict:
- Readiness stage:
- Practical readiness estimate:
- Validation level / evidence level:
- Audit mode: `code-only`
- Report type: `code-only-project-readiness`
- Target project:
- Scope:
- Excluded context:
- Main risk:

Start with 1-3 plain-language paragraphs explaining what the code proves about the project, what stage it appears to be in, and what prevents a higher readiness claim.

### What Is Implemented In Code

| Area | Evidence | Status |
|---|---|---|
|  |  |  |

### Code-Visible Tasks

Use implementation evidence only. Reconstruct what jobs the project actually tries to perform.

| Task inferred from code | Readiness | Evidence | Main gap |
|---|---|---|---|
|  |  |  |  |

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

Use one of these evidence-strength labels for each finding: `reproduced`, `direct code contradiction`, `static config contradiction`, `framework/runtime candidate`, or `product/API gap`. Keep route ordering, middleware, dependency-injection, database, queue, and external-service behavior as `framework/runtime candidate` unless inspected runtime or framework-specific evidence proves it.

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
- Practical readiness estimate:
- Validation level / evidence level:
- Audit mode:
- Report type: `project-readiness`
- Target project:
- Scope:
- Main risk:

Start with an executive narrative for product and engineering decision-makers. Explain whether the project is a prototype, MVP, stage pilot, beta, production candidate, or production system with debt, and why.

### Project Goals

- Stated goals:
- Inferred goals:
- Non-goals:

### Product Maturity

Use for product/customer audits. Name phases, contours, operational readiness, and roadmap-only capabilities when visible.

| Product layer | Current maturity | What is mature | What is missing for the target system |
|---|---|---|---|
|  |  |  |  |

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
- Evidence strength:
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
- Settings schema vs env examples:
- Monitoring targets vs deploy service names:
- Registered routes and clients:
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

| # | Candidate | Evidence strength | Contract evidence | Trigger | Location | Confidence | Reproduction status |
|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  | `NOT_REPRODUCED` |

If no candidate survives ranking, set status to `NO_BUG_PROVEN` and describe the inspected scope plus next useful evidence.

### Immediate Bug-Fix Batch

Use when at least three high-confidence candidates exist. Pick the smallest highest-confidence defects to prove first.

| # | Severity | Candidate | Trigger | Evidence | Confidence | Status |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  | `NOT_REPRODUCED` |

### Second Engineering Batch

| # | Severity | Candidate | Trigger | Evidence | Confidence | Status |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

### Backlog / Hardening Batch

| # | Severity | Candidate | Why backlog | Evidence | Status |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

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
