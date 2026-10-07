# Release 0.1.6 validation — 2026-10-07

Verdict: `PASS_WITH_RISKS` for the scoped specification-traceability release.

Both repository and installable package VERSION files contain `0.1.6`. The change extends the existing `docs-vs-code` workflow with applicable-source selection, individual requirements/acceptance scenarios/non-functional constraints, and separate implementation/verification evidence. It adds no audit mode or agent. Code-only evidence, mandatory bug discovery, prior-report isolation, and reproduction/fix approval gates remain separate.

## Task Scope

- Goal: implement specification traceability and commit a new version.
- Mode: scoped skill/package implementation and validation, plus a brief `docs-vs-code` forward-test.
- Source of truth: changed package files, regression-test results, raw fixture files, and independently generated forward-test output. Existing reports were not used to design or populate new audit findings.
- Allowed files: skill entrypoint, methodology, report template, validator, tests/fixture, README, VERSION files, CHANGELOG, and these new release artifacts.
- Non-goals: target production changes, dependency installation, broad refactoring, new agents, runtime or production-readiness claims, and GitHub publication.
- Validation method: structural/package checks, regression tests, clean-install smoke, independent read-only audit of a small fixture, separate validator review, and whitespace check.
- Acceptance criteria: versioned requirement/source sections, explicit no-specification path, missing evidence distinguished from missing implementation, source-scoped IDs, historical report compatibility, and passing scoped checks.

## Evidence And Results

| Check | Outcome | Scope |
|---|---|---|
| Package scaffold/methodology validation | `PASS L0` | Package shape and required workflow terms |
| Local authoring-pack validation | `PASS L2` | Router/role/package consistency, not target runtime |
| Regression suite | 32 tests, `OK` | All six statuses, no-spec path, evidence fields, source metadata, duplicate identities, headings, escaped pipes, historical compatibility, pack/standalone CLI gates, and existing package/install behavior |
| Strict historical public-report validation | `PASS L0`, no quality failures | Compatibility only; previous report conclusions were not used as new audit evidence |
| Clean-install smoke | `PASS install-smoke` | Copy/install and installed-validator behavior in a temporary directory |
| skill-creator quick validation | `Skill is valid!` | Frontmatter/name/scaffold checks |
| Independent forward-test | Completed, report schema passes `PASS L0` | Static application of new methodology to one small fixture |
| Separate validator review | No residual concrete issue after corrections | Legacy sections, source-scoped IDs, escaped pipes, closing-hash headings, and negative controls |
| Whitespace validation | Exit 0 | Changed-file whitespace |

The initial test run rejected a pre-existing ignored `.DS_Store` in the skill directory. It was moved reversibly to `/private/tmp/pra-skill-016.DS_Store`; no tracked source was removed. The generic Python and bundled Python lacked PyYAML for quick validation; the already-installed `school21` environment ran that check successfully, without installing dependencies.

## Commands Run

Repository working directory: `/Users/bobrsubr/PycharmProjects/_petprojects/project-readiness-auditor`. Final checks below exited 0; read-only inspection also used `cat`, `sed`, `rg`, `nl`, and Git status/diff commands.

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
python3 project-readiness-auditor/scripts/validate_skill.py project-readiness-auditor
python3 scripts/validate_pack.py .
python3 project-readiness-auditor/scripts/validate_skill.py project-readiness-auditor --strict-report-quality --public-report-examples --report-quality-summary
python3 project-readiness-auditor/scripts/install_smoke.py .
/Users/bobrsubr/venv/school21/bin/python -B /Users/bobrsubr/.codex/skills/.system/skill-creator/scripts/quick_validate.py project-readiness-auditor
python3 project-readiness-auditor/scripts/validate_skill.py project-readiness-auditor --spec-traceability-report reports/release/specification-traceability-forward-test-2026-10-07.md
git diff --check
```

The regression suite also runs install-smoke and temporary-repository CLI checks; it does not execute the audit fixture's source/test files. A final standalone install-smoke is recorded separately above.

## Forward-Test

The independently generated [brief audit](specification-traceability-forward-test-2026-10-07.md) was frozen before the separate validator review. Its target was a temporary copy of the committed [raw fixture](../../tests/fixtures/spec_traceability/README.md); paths and commands in that frozen report retain their original temporary locations. The fixture is synthetic and is not evidence about a real customer project.

Reproduce the evaluation by giving a separate auditor the current package and `tests/fixtures/spec_traceability/` with this request: “Perform a brief docs-vs-code audit for CLI release 1. Inspect only raw fixture files; do not execute target source/tests. Include specification sources, requirement traceability, mandatory bug discovery, exact commands, missing evidence, and residual risk.” Do not give the evaluator this release record or the frozen report as audit source material.

The observed audit separated approved release 1 from the newer release 2 draft, distinguished absent JSON capability from unrun tests and unmeasured performance, and reported `NO_BUG_PROVEN` for the target scope rather than promoting product gaps to proven bugs. Its `BLOCK` verdict concerns full fixture specification conformance, not this skill release.

Independent review found four structural false rejections during implementation: markerless historical tables, reused IDs across source documents, escaped Markdown pipes, and closing-hash headings. The scoped implementation now handles them, and regression/negative controls pass. The frozen report needed no formatting repair.

## Validation Level, Missing Evidence, And Residual Risk

Focused workflow evidence: **L1**, one static synthetic project slice. Package structural checks establish L0; the authoring-pack validator's separate L2 result does not establish target runtime or broad audit quality. No new full L3–L5 or production-readiness claim is made.

Missing evidence: repeated specification audits on materially different real projects, target runtime/benchmark execution, real Codex restart/invocation of the installed version, and external red-team review. The forward-test also noted pre-existing rubric ambiguity around `NOT_REPRODUCED` and workflow-oriented evidence levels; it mitigated this with explicit validation basis, and this release does not rewrite that vocabulary.

Residual risk: the validator checks structure and nonempty evidence references, not their truth, source precedence, exhaustive requirement coverage, or measured behavior. Historical reports need the explicit required flag to demand the new schema. User-language prose is supported with stable English machine-readable keys. Large/conflicting specs still need auditor judgment and explicit inspected scope.

Next smallest validation step: run the workflow on one real project with a current approved specification and execute its already-authorized acceptance checks, recording requirement decisions and actual output. Broaden beyond that only when the results justify it.

## Publication Preflight And CI Correction

Before tagging/publication, a clean tracked-tree export exposed a pre-existing CI dependency on ignored `AGENTS.md` and root `agents/` files. The authoring-pack step failed, and its three tests errored/failed in the public tree. The initial pushed commit's [GitHub run](https://github.com/ikonushok/project-readiness-auditor/actions/runs/37560956989) also failed. Earlier local success was limited to the author's workspace, where those files exist.

The user explicitly approved the exact `.github/workflows/validate.yml` and `tests/test_validate_pack.py` correction and test command. Public CI now conditionally runs the local authoring step when `AGENTS.md` exists; the local-only test class runs when all required authoring files exist. Missing local files are not added to the public package. Every public-package scaffold, methodology, report, and install check remains enabled.

Post-correction command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`. Authoring workspace: 32 tests, `OK`. Clean tree at `/private/tmp/pra-release-016-clean`: 32 discovered, 29 executed successfully and 3 local-only tests skipped, `OK (skipped=3)`. The clean tree was created using `git archive --format=tar --output=/private/tmp/pra-release-016-clean.tar HEAD`, extracted with `tar -xf /private/tmp/pra-release-016-clean.tar -C /private/tmp/pra-release-016-clean`, and received the explicitly approved patch. No audited target code was modified.

Publication will use annotated tag `v0.1.6` on the final correction commit after inspecting successful remote CI. The repository topic `spec-kit` describes supported specification input, not a runtime dependency on that toolkit.
