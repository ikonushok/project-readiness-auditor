# Changelog

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
