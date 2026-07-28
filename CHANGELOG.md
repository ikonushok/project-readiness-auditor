# Changelog

## 0.1.2

- Added an unconditional previous-report isolation rule: older audit reports cannot be examples, evidence, finding sources, or checklists for a new audit.
- Added after-freeze comparison rules for audit reruns so comparisons happen only after the new report is completed from primary evidence.
- Added claim-strength labels to separate reproduced bugs, direct code contradictions, static config contradictions, framework/runtime candidates, and product/API gaps.
- Expanded reproducibility and contract checks to compare settings schema, env examples, compose, Helm, CI, monitoring targets, service names, ports, and metrics paths.
- Expanded incompleteness checks for unregistered routers, unwired modules, API paths without clients, and clients without registered backend routes.
- Added private-run discrepancy validation notes as a local ignored artifact for improving the auditor workflow.
- Added a public customer example report pack for `ikonushok/recommender-systems-from-zero`.
- Added a prior-report freeze validation scenario to preserve the older-report isolation workflow.
- Expanded static validation to check customer report pack structure when public examples are present.

## 0.1.1

- Added explicit per-project report pack rules for customer audits.
- Added supported report types: `code-only-project-readiness`, `project-readiness`, and `bug-audit`.
- Made bug discovery a mandatory phase of every audit and added approval-gated reproduction/fix rules adapted from `codex-bug-reproducer`.
- Expanded static validation to check that the public skill preserves the report-pack contract.
- Ignored local audit target checkouts under `.audit-targets/`.

## 0.1.0

- Added the initial `project-readiness-auditor` installable skill package.
- Kept local assistant workspace files out of the public package surface.
- Added static L0 validation for the skill scaffold.
- Expanded the root README and skill references with the evidence-based audit methodology, timebox profiles, finding confidence, and prioritized closure planning.
