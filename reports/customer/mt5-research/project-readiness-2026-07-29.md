# Project Readiness: private MT5 research system

## Summary

- Verdict: `HOLD`
- Readiness stage: Beta/pilot research candidate; explicitly not production-approved
- Practical readiness estimate: credible for inspected development/research use; not stronger than recorded runtime evidence.
- Validation level / evidence level: L1 static/docs-vs-code slice; no MT5/Wine/backtest commands run
- Validation basis: docs-vs-code static inspection of README/risk docs, project contract code/tests, package verifier, run-script surfaces, and dependency manifest; local filesystem paths were redacted and no MT5/Wine/backtest/live-broker command was executed.
- Audit mode: `docs-vs-code`
- Report type: `project-readiness`
- Target project: private MT5 research system
- Scope: docs as intent, implementation/config/tests as proof.
- Main risk: README explicitly leaves live-like, execution, recovery, broker, and forward gates open, so production or trading approval would be unsupported.

The project goal is clear: Build and validate an MT5 rent-oriented portfolio under controlled drawdown, margin, replenishment, and monthly cashflow constraints. Implementation evidence supports a real project rather than a pure concept: Large MT5/MQL5 research system with portfolio builders, report parsers, package validators, run scripts, risk reports, strategy selection docs, and focused contract tests. The limiting factor is not intent, but missing current runtime proof in this audit.

## Project Goals

- Stated goals: Build and validate an MT5 rent-oriented portfolio under controlled drawdown, margin, replenishment, and monthly cashflow constraints.
- Inferred goals: produce reusable, auditable artifacts for the project domain.
- Non-goals: this report does not certify production/live behavior.

## Product Maturity

| Product layer | Current maturity | What is mature | What is missing for the target system |
|---|---|---|---|
| Core workflow | Beta/pilot research candidate; explicitly not production-approved | Strong evidence discipline in README, explicit PASS_WITH_RISKS limits, leverage contract tests, package verification, and many BLOCK guards in builders. | Headless MT5/Wine and live-broker scripts are operationally sensitive; no runtime commands were run; many claims depend on historical backtests and external tester state. |
| Validation | Partial | Some tests/checks/docs exist | Current command output and broader regression proof |
| Operations | Partial or missing | Config/deploy files when present | Security/rollback/runtime proof |

## Project Map

- Languages and frameworks: Python and domain-specific libraries.
- Entrypoints: documented scripts/API/validators listed in Evidence Log.
- Services and workers: API/service layer only when present in inspected project.
- API/UI contracts: inspected from committed route/dashboard/test files where present.
- Database and migrations: not fully audited unless named in Evidence Log.
- Queues, caches, schedules: no queue delivery proof.
- External integrations: external data/model/platform/MT5/Docker surfaces where present.
- Tests and CI: inspected from repository files; not run unless listed.
- Deployment and monitoring: inspected from Docker/monitoring/CI files when present.

## Findings

| Severity | Evidence strength | Area | What is proven | Recommended next action |
|---|---|---|---|---|
| BLOCKER | product/API gap | readiness | Production/trading approval is explicitly unsupported until live-like gates are closed. | Add the smallest focused check that proves or rejects this risk. |
| HIGH | security/operations risk | readiness | Run scripts warn that terminal64 can log into a live broker account. | Add the smallest focused check that proves or rejects this risk. |
| MEDIUM | missing evidence | readiness | Historical backtest evidence was not rerun and cannot prove future/live performance. | Add the smallest focused check that proves or rejects this risk. |

## Mandatory Bug Discovery

- Status: `INCONCLUSIVE` / candidates only.
- Inspected paths: README.md, README_BEST_SELECTED_MODELS_RISKS.md, src/project_contract.py, test/test_project_contract.py, src/verify_package.py, src/runers/*.sh, requirements.txt
- Candidate count: 2
- Strongest candidate: run_harvest.sh and run_rebalancer_harvest.sh warn that they launch terminal64 on a live broker account; destructive/side-effect protection should be gated before general automation.
- Reproduction status: `NOT_REPRODUCED` unless candidate says `NO_BUG_PROVEN`.
- Proposed test-first next step: approve a focused reproducer or safe smoke check.

| # | Candidate | Evidence strength | Contract evidence | Trigger | Location | Confidence | Reproduction status |
|---|---|---|---|---|---|---|---|
| 1 | run_harvest.sh and run_rebalancer_harvest.sh warn that they launch terminal64 on a live broker account; destructive/side-effect protection should be gated before general automation. | product/API gap | Inspected code/config/docs | Static inspection path | See Evidence Log | Medium | `NOT_REPRODUCED` |
| 2 | Production approval remains blocked by forward, execution, recovery, quarantine, and broker-condition checks named in README. | product/API gap | Inspected code/config/docs | Static inspection path | See Evidence Log | Medium | `NOT_REPRODUCED` |

## Readiness By Capability

| Capability | Current status | Evidence | Readiness |
|---|---|---|---|
| Main workflow | Present | README/scripts/configs/code | Partial to strong static |
| Validation | Present but incomplete | tests/validators when present | Partial |
| Runtime reproducibility | Claimed or configured | reproduce/run scripts | Missing current output |
| Production/live readiness | Not proven | deployment/security/live gates | Not certified |

## Reproducibility

- Dependency evidence: manifests/configs inspected when present.
- Build evidence: no build command run in this audit.
- Test evidence: test files inspected when present; not executed.
- Runtime evidence: no runtime flow executed.
- Required environment: external data/dependencies/services may be required.
- Missing evidence: command output for the smallest realistic scenario.

## Contract Review

- UI vs backend: inspected only when UI/API files exist.
- API schemas vs services: partial static inspection where API exists.
- Producers vs consumers: not fully proven without runtime.
- Models vs migrations: not applicable or not fully inspected.
- Env settings vs deploy config: partial when Docker/CI/config present.
- Settings schema vs env examples: partial.
- Monitoring targets vs deploy service names: partial where monitoring exists.
- Registered routes and clients: partial where API exists.
- File/object paths: partial through scripts/configs.

## Security And Reliability

- Auth and permissions: not fully proven.
- Secrets and tokens: no secret scan beyond inspected files.
- CORS and public endpoints: inspected only where API/deploy exists.
- Error handling: partial static evidence.
- Idempotency and retries: not fully proven.
- Time and state handling: domain-specific; needs runtime tests.

## Readiness Assessment

- Current stage: Beta/pilot research candidate; explicitly not production-approved
- Why this stage: structured implementation exists, but current runtime evidence is absent.
- What blocks the next stage: focused runtime validation and closure of reported risks.
- Smallest next validation step: run the safest documented smoke/test path.

## Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 | Run/approve focused reproducer for top candidate. | Bug uncertainty | Reproducer output |
| P1 | Run documented smoke/test command. | Runtime uncertainty | Command log |
| P2 | Update docs/readiness claims. | Overclaim risk | Docs tied to proof |

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
- Command outcomes: read-only inspection completed.
- Claims not verified: current runtime, production/live, and data-dependent behavior.
- Residual risk: static analysis can miss data/runtime/framework behavior.
