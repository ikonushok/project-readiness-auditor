# Code-Only Project Readiness: private MT5 research system

## Summary

- Verdict: `HOLD`
- Readiness stage: Beta/pilot research candidate; explicitly not production-approved
- Practical readiness estimate: static evidence supports continued engineering use; runtime readiness not proven here.
- Validation level / evidence level: L1 static/docs-vs-code slice; no MT5/Wine/backtest commands run
- Validation basis: read-only static inspection of README/risk docs, project contract code/tests, package verifier, run-script surfaces, and dependency manifest; local filesystem paths were redacted and no MT5/Wine/backtest/live-broker command was executed.
- Audit mode: `code-only`
- Report type: `code-only-project-readiness`
- Target project: private MT5 research system
- Scope: source code, tests, configs, CI/deploy files, scripts, and command output listed in Evidence Log.
- Excluded context: previous audit reports and generated historical reports.
- Main risk: README explicitly leaves live-like, execution, recovery, broker, and forward gates open, so production or trading approval would be unsupported.

Static code evidence shows: Large MT5/MQL5 research system with portfolio builders, report parsers, package validators, run scripts, risk reports, strategy selection docs, and focused contract tests. The project is more than a notebook or loose script set, but this audit did not run its runtime path.

## What Is Implemented In Code

| Area | Evidence | Status |
|---|---|---|
| Core workflow | Large MT5/MQL5 research system with portfolio builders, report parsers, package validators, run scripts, risk reports, strategy selection docs, and focused contract tests. | Implemented by static inspection |
| Reproducibility path | scripts/configs/readme entrypoints | Present, not rerun |
| Tests/checks | inspected test or validation files when present | Partial |

## Code-Visible Tasks

| Task inferred from code | Readiness | Evidence | Main gap |
|---|---|---|---|
| Execute the main project workflow | Partial | scripts/configs/entrypoints | Runtime output missing |
| Validate core contracts | Partial | tests or validator files | Coverage incomplete or not run |
| Produce handoff artifacts | Partial | report/submission/output paths | External/data/runtime proof missing |

## Code Project Map

- Languages and frameworks: Python-centered project; domain-specific dependencies listed in manifests.
- Entrypoints: documented scripts and package modules.
- Services and workers: see inspected API/pipeline/run scripts where present.
- API/UI contracts: inspected when present; otherwise not applicable.
- Database and migrations: no migration proof inspected unless listed in files.
- Queues, caches, schedules: no queue/scheduler proof inspected.
- External integrations: data files, model artifacts, Docker/MT5/platform upload paths where present.
- Tests and CI: inspected only from committed files.
- Deployment and monitoring: inspected only when committed config exists.

## Strengths Visible In Code

| Strength | Evidence | Why it matters |
|---|---|---|
| Structured implementation | - `README.md`<br>- `README_BEST_SELECTED_MODELS_RISKS.md`<br>- `src/project_contract.py`<br>- `test/test_project_contract.py`<br>- `src/verify_package.py`<br>- `src/runers/*.sh`<br>- `requirements.txt` | Reduces notebook/script-only risk |
| Explicit workflow | scripts/configs/README paths | Gives a reproducibility target |
| Evidence discipline | tests/validators/docs where present | Makes future validation cheaper |

## Gaps And Risks

| Severity | Evidence strength | Area | What is proven | Recommended next action |
|---|---|---|---|---|
| BLOCKER | product/API gap | readiness | Production/trading approval is explicitly unsupported until live-like gates are closed. | Add the smallest focused check that proves or rejects this risk. |
| HIGH | security/operations risk | readiness | Run scripts warn that terminal64 can log into a live broker account. | Add the smallest focused check that proves or rejects this risk. |
| MEDIUM | missing evidence | readiness | Historical backtest evidence was not rerun and cannot prove future/live performance. | Add the smallest focused check that proves or rejects this risk. |

## Mandatory Bug Discovery

- Status: `INCONCLUSIVE` for reproduced bugs; read-only candidates recorded.
- Inspected paths: README.md, README_BEST_SELECTED_MODELS_RISKS.md, src/project_contract.py, test/test_project_contract.py, src/verify_package.py, src/runers/*.sh, requirements.txt
- Candidate count: 2
- Strongest candidate: run_harvest.sh and run_rebalancer_harvest.sh warn that they launch terminal64 on a live broker account; destructive/side-effect protection should be gated before general automation.
- Reproduction status: `NOT_REPRODUCED` unless explicitly marked `NO_BUG_PROVEN`.
- Proposed test-first next step: approve exact focused reproducer for the top candidate.

| # | Candidate | Evidence strength | Contract evidence | Trigger | Location | Confidence | Reproduction status |
|---|---|---|---|---|---|---|---|
| 1 | run_harvest.sh and run_rebalancer_harvest.sh warn that they launch terminal64 on a live broker account; destructive/side-effect protection should be gated before general automation. | product/API gap | Inspected code/config/docs | Static inspection path | See Evidence Log | Medium | `NOT_REPRODUCED` |
| 2 | Production approval remains blocked by forward, execution, recovery, quarantine, and broker-condition checks named in README. | product/API gap | Inspected code/config/docs | Static inspection path | See Evidence Log | Medium | `NOT_REPRODUCED` |

## Contract Reliability Security Checks

- Cross-part contracts: partially inspected through scripts/configs/tests.
- Error handling and queue/file/data loss risk: not fully proven without runtime.
- Idempotency, retries, and time/state handling: not fully proven.
- Auth, permissions, secrets, and public surfaces: inspected only where API/deploy files exist.
- Unfinished or dead paths: marker search performed; major candidates reported above.

## Findings

| Severity | Evidence strength | Area | What is proven | Recommended next action |
|---|---|---|---|---|
| BLOCKER | product/API gap | readiness | Production/trading approval is explicitly unsupported until live-like gates are closed. | Add the smallest focused check that proves or rejects this risk. |
| HIGH | security/operations risk | readiness | Run scripts warn that terminal64 can log into a live broker account. | Add the smallest focused check that proves or rejects this risk. |
| MEDIUM | missing evidence | readiness | Historical backtest evidence was not rerun and cannot prove future/live performance. | Add the smallest focused check that proves or rejects this risk. |

## Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 | Prove or reject the strongest candidate. | Bug/risk overclaiming | Focused test/smoke output |
| P1 | Run the smallest documented test/smoke path. | Static-only confidence | Command output |
| P2 | Update readiness docs after proof. | Docs-vs-code drift | Revised docs tied to evidence |

## Readiness Assessment

- Current stage: Beta/pilot research candidate; explicitly not production-approved
- Why not lower: structured code/config/test evidence exists.
- Why not production-ready: runtime, operational, deployment, rollback, security, or live evidence is missing or incomplete.
- Smallest next validation step: run the narrowest safe check named in the project docs.

## Evidence Log

- Files inspected:
- `README.md`
- `README_BEST_SELECTED_MODELS_RISKS.md`
- `src/project_contract.py`
- `test/test_project_contract.py`
- `src/verify_package.py`
- `src/runers/*.sh`
- `requirements.txt`
- Commands run:
- `find <private-mt5-research-system> -maxdepth 3 -type f`
- `sed -n '1,220p' <private-mt5-research-system>/README.md`
- `sed -n '1,220p' <private-mt5-research-system>/README_BEST_SELECTED_MODELS_RISKS.md`
- `sed -n '1,220p' <private-mt5-research-system>/src/project_contract.py`
- `sed -n '1,220p' <private-mt5-research-system>/test/test_project_contract.py`
- `sed -n '1,220p' <private-mt5-research-system>/src/verify_package.py`
- `rg -n "TODO|FIXME|placeholder|live|terminal64|broker|forward|quarantine|recovery" <private-mt5-research-system>`
- Command outcomes: read-only inspection succeeded; GitHub fetch/clone succeeded where applicable.
- Claims not verified: runtime performance, live/deployment behavior, full data-dependent workflows.
- Residual risk: static reports can miss framework/runtime/data-dependent failures.
