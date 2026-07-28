# Readiness Rubric

## Readiness Stages

- Draft prototype: useful idea or isolated code exists, but setup, contracts, and tests are incomplete.
- Technical prototype: core path is visible in code, but integration, reproducibility, and coverage are weak.
- MVP: main workflow works by inspection or limited runtime proof, with known gaps and manual operations.
- Integration MVP: main components are wired together, contracts are mostly explicit, and smoke checks exist.
- Beta or pilot: realistic users or environments can exercise the system, with monitoring and rollback partially addressed.
- Production-ready: reproducible setup, deployment, migrations, security, observability, rollback, and critical tests are evidenced.
- Production with debt: production path exists, but residual risks or missing evidence should be tracked explicitly.

## Severity

- `BLOCKER`: likely prevents safe use, deployment, data integrity, or truthful readiness claims.
- `HIGH`: likely causes serious runtime failure, security exposure, data loss, or cross-component breakage.
- `MEDIUM`: material reliability, maintainability, or test gap that can affect normal use.
- `LOW`: localized quality issue or incomplete evidence with limited impact.
- `INFO`: observation, clarification, or non-blocking improvement.

## Evidence Strength

- Strong: source code plus tests or inspected runtime output prove the claim.
- Moderate: source code and configuration align, but runtime or test evidence is missing.
- Weak: documentation, comments, or naming suggest intent, but implementation proof is incomplete.
- Missing: claim has no supporting evidence in inspected files.

## Finding Confidence

- Proven bug: directly demonstrated by inspected code contradiction, failing test, command output, or reproduced behavior.
- Bug candidate: plausible failure path supported by code or contract evidence, but not reproduced.
- Missing evidence: a claim may be true, but inspected files or commands do not prove it.
- Documentation mismatch: docs claim behavior that inspected implementation does not support.

## Bug Discovery Status

- `REPRODUCED`: a focused approved case fails deterministically for the predicted reason.
- `NOT_REPRODUCED`: the approved case does not produce the predicted failure.
- `NO_BUG_PROVEN`: mandatory read-only discovery found no defensible candidate in the inspected scope, or approved tests did not prove a correctness defect.
- `INCONCLUSIVE`: environment, nondeterminism, missing access, or ambiguous signals prevent a conclusion.
- `REJECTED`: the candidate failed the reachability, contract, reproducibility, or impact filter.
- `FIX_PROVEN`: the same reproducer goes red to green and relevant broader checks pass after an approved fix.

Bug candidates are mandatory audit output, but reproduction tests and production fixes require separate explicit approval gates.

## Verdicts

- `PASS`: checks passed with sufficient evidence.
- `PASS_WITH_RISKS`: checks passed, but residual risk or missing evidence remains.
- `RETEST`: a change was made or a claim depends on checks that must be rerun.
- `HOLD`: design or evidence needs revision before release or final claim.
- `BLOCK`: unsafe, misleading, or unsupported claims must be fixed before proceeding.

## Validation Levels

- L0: file structure, Markdown/YAML, naming, and obvious contradiction checks.
- L1: one realistic audit prompt or project slice.
- L2: generated pack consistency across router, agents, references, and report format.
- L3: one real project audit simulation.
- L4: cross-project regression across several project types.
- L5: public/release readiness with red-team and install verification.

## Readiness Claim Rules

- Draft prototype through MVP can be assigned from static or limited runtime evidence if gaps are explicit.
- Integration MVP requires inspected evidence for the main component contracts.
- Beta or pilot requires evidence that realistic users or environments can exercise the system.
- Production-ready requires reproducibility, deployment, migrations, security, observability, rollback, and critical tests.
- Production with debt requires an evidenced production path plus explicit residual risks.
