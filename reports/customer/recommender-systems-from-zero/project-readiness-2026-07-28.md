# Project Readiness: Recommender Systems From Zero

Date: 2026-07-28
Target project: `ikonushok/recommender-systems-from-zero`
Audited commit: `6ad30d7c76bebab1fa28fbce35ddf7102792f04e`

## Summary

- Verdict: `PASS_WITH_RISKS`
- Readiness stage: MVP / beta-quality educational repository
- Practical readiness estimate: 80-88% for public educational use
- Validation level / evidence level: L2 docs-vs-code/config/test audit
- Audit mode: `docs-vs-code`
- Report type: `project-readiness`
- Scope: README goals, docs/notebooks/code/tests/config, existing safe runtime checks
- Main risk: advanced runtime reproducibility is less proven than the core path

This project is ready to be used publicly as an educational course-style repository for recommender systems fundamentals. The README positions it correctly: not as a production recommender service, but as a structured learning path with notebooks, explanations, reusable modules, and tests. Implementation evidence supports that positioning.

The strongest part is the core path. It has docs, notebooks, source modules, and passing tests for split logic, top-K metrics, popularity, content-based, item-item CF, hybrid fusion, and a sequential baseline. The advanced path is also materially implemented through docs, notebooks, and supporting modules, but this audit did not rerun advanced notebooks in the documented Python 3.12 environment or with the full advanced dependency set.

## Project Goals

- Stated goals: teach recommender-system basics, show minimal working implementations, teach correct evaluation, show common mistakes, introduce modern/neural recommenders.
- Inferred goals: provide a public portfolio-quality educational project with reproducible notebooks and importable helper modules.
- Non-goals: production recommender service, online API, feature store, A/B testing platform, real-time serving, orchestration infrastructure.

## Product Maturity

| Product layer | Current maturity | What is mature | What is missing for the target system |
|---|---|---|---|
| Public positioning | Mature | README clearly explains educational scope and non-goals. | Add a tighter install quickstart. |
| Core learning path | Strong MVP / beta | Docs, notebooks, source modules, and tests align. | CI and clean-env run proof. |
| Advanced learning path | Useful optional MVP | ALS, LightFM, NeuralCF, TwoTower, sequence, ranking docs/notebooks/modules exist. | Full dependency install and notebook run-all proof. |
| Reproducibility | Medium | `requirements.txt`, package metadata, tests README, notebook outputs. | Align Python version and package dependencies; add CI. |
| Production-readiness education | Conceptual guide | README and docs explicitly mark production topics as overview/non-goal. | No gap for stated scope; not intended to be production implementation. |

## Project Map

- Languages and frameworks: Python, pandas/numpy/scipy/scikit-learn, optional implicit/LightFM/PyTorch, Jupyter notebooks.
- Entrypoints: notebooks under `notebooks/basic` and `notebooks/advanced`; modules under `src/recsys_basics`.
- Services and workers: none.
- API/UI contracts: none.
- Database and migrations: none.
- Queues, caches, schedules: none.
- External integrations: public dataset downloads.
- Tests and CI: unittest tests exist and pass locally; CI not found.
- Deployment and monitoring: intentionally out of scope.

## Findings

### Finding 1

- Severity: `HIGH`
- Confidence: high
- Evidence strength: direct code contradiction
- Area: advanced model training
- Evidence: `src/recsys_basics/advanced/neural_cf.py:262-265`, `:316-319`; `src/recsys_basics/advanced/two_tower.py:334-337`
- What is proven: negative sampling loops keep drawing until a sampled item is not in the user's seen set, but there is no guard for the case where every item is already seen.
- Impact: advanced training can hang on dense toy datasets, which is especially painful in educational notebooks.
- Recommended next action: add a guard for empty negative pool and a tiny regression test.

### Finding 2

- Severity: `MEDIUM`
- Confidence: high
- Evidence strength: static config contradiction
- Area: packaging and onboarding
- Evidence: `pyproject.toml:5-16`, `requirements.txt:1-13`, `README.md:450`
- What is proven: `requirements.txt` contains the runtime/notebook dependencies, while `pyproject.toml` contains no project dependencies.
- Impact: users who install the package through Python packaging conventions can get an importable package without its required runtime libraries.
- Recommended next action: either add `[project.dependencies]`/extras or document the required install command prominently.

### Finding 3

- Severity: `MEDIUM`
- Confidence: medium-high
- Evidence strength: missing evidence
- Area: advanced reproducibility
- Evidence: `README.md:54`, notebook metadata inspection, command output showing missing local advanced packages
- What is proven: notebooks have executed metadata, but this audit did not rerun `restart kernel + run all`; local environment lacks several advanced dependencies.
- Impact: the advanced path looks useful but should not be represented as freshly runtime-verified by this audit.
- Recommended next action: add a script or CI job for selected notebook run-all checks.

### Finding 4

- Severity: `LOW`
- Confidence: high
- Evidence strength: missing evidence
- Area: CI
- Evidence: no `.github` workflow files found; tests pass locally
- What is proven: validation is documented and runnable, but not automated in repository evidence.
- Impact: regressions can slip into public examples.
- Recommended next action: add GitHub Actions for Python 3.12 unit tests.

## Mandatory Bug Discovery

- Status: bug candidates found; none reproduced with new reproduction files
- Inspected paths: `src/recsys_basics/**`, `tests/**`, config, README, notebook metadata
- Candidate count: 4
- Strongest candidate: negative sampling dense-history hang
- Reproduction status: `NOT_REPRODUCED`
- Proposed test-first next step: approved regression tests for NeuralCF/TwoTower all-items-seen behavior

| # | Candidate | Contract evidence | Trigger | Location | Confidence |
|---|---|---|---|---|---|
| 1 | NeuralCF negative sampling can hang. | Advanced recommender should either train or fail clearly on tiny fixtures. | User has seen every item. | `neural_cf.py:262-265`, `:316-319` | High |
| 2 | TwoTower negative sampling can hang. | Same sampling contract. | Dense post-intersection training set. | `two_tower.py:334-337` | High |
| 3 | Packaging install path omits dependencies. | README says environment is described by requirements and pyproject. | User runs package-style install. | `pyproject.toml`, `requirements.txt` | Medium-high |
| 4 | HF Amazon loader dependency is manual/implicit. | Function exists and raises install hint for `datasets`. | User calls HF loader after requirements install. | `data.py:549-560`, `requirements.txt` | Medium |

## Readiness By Capability

| Capability | Current status | Evidence | Readiness |
|---|---|---|---|
| Beginner learning route | Implemented | README, docs/basic, notebooks/basic, core modules, tests | High |
| Metrics and split correctness | Implemented and tested | `tests/test_metrics.py`, `tests/test_split.py`, command output | High |
| Baseline recommenders | Implemented and tested | popularity/content/item-item/hybrid tests | High |
| Advanced recommenders | Implemented with caveats | advanced modules, notebook metadata | Medium |
| Dataset onboarding | Implemented with local-file guidance | `data.py`, `data/raw/**/README.md` | Medium |
| Public reproducibility | Partial | requirements, tests README, passing local tests | Medium |

## Reproducibility

- Dependency evidence: `requirements.txt` pins core and advanced dependencies.
- Build evidence: package metadata exists in `pyproject.toml`.
- Test evidence: existing unittest suite passed: 27 tests.
- Runtime evidence: imports and AST parse passed; notebook metadata inspected.
- Required environment: docs expect Python 3.12.x; audit local runtime was Python 3.11.6.
- Missing evidence: clean Python 3.12 setup, full dependency install, full notebook run-all, CI.

## Contract Review

- UI vs backend: not applicable.
- API schemas vs services: not applicable.
- Producers vs consumers: not applicable.
- Models vs migrations: not applicable.
- Env settings vs deploy config: not applicable.
- Settings schema vs env examples: no env settings.
- Monitoring targets vs deploy service names: not applicable.
- Registered routes and clients: not applicable.
- File/object paths: dataset helpers and data README files describe expected raw-data layouts.

## Security And Reliability

- Auth and permissions: not applicable.
- Secrets and tokens: no secrets found in inspected files.
- CORS and public endpoints: not applicable.
- Error handling: dataset helpers raise explicit exceptions for missing files/network/SSL/archive errors.
- Idempotency and retries: downloads skip existing files unless overwrite is set; no retry/backoff layer.
- Time and state handling: time-aware split and leakage check are tested.

## Readiness Assessment

- Current stage: MVP / beta-quality educational repository.
- Why this stage: core path has code, docs, notebooks, and passing tests; advanced path is implemented but less freshly validated.
- What blocks the next stage: CI, clean-env dependency proof, notebook run-all automation, negative-sampling edge guard.
- Smallest next validation step: create a fresh Python 3.12 env, install `requirements.txt`, run unittest suite, run one basic and one advanced notebook end to end.

## Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P1 | Add negative-sampling guard/tests. | Advanced notebook hang risk. | Regression tests pass. |
| P1 | Align `pyproject.toml`, `requirements.txt`, and install docs. | Onboarding ambiguity. | Clean install command works. |
| P2 | Add GitHub Actions for tests. | Validation repeatability. | Public CI green. |
| P2 | Add notebook validation script for a smoke subset. | Advanced run-all confidence. | Recorded run-all output. |

## Evidence Log

- Files inspected: `README.md`, `pyproject.toml`, `requirements.txt`, `data/README.md`, `data/raw/**/README.md`, `docs/**`, `notebooks/**/*.ipynb` metadata, `src/recsys_basics/**`, `tests/**`.
- Commands run: clone, status, file search, targeted reads, unittest, import-all, AST parse, notebook metadata inspection, local package availability inspection.
- Command outcomes: tests passed; imports passed; AST passed; no target files modified.
- Claims not verified: full notebook run-all, full dependency install, dataset downloads, advanced model training.
- Residual risk: advanced readiness is supported by static and metadata evidence, not by fresh run-all evidence in this audit.
