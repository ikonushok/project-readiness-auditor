# Code-Only Project Readiness: Recommender Systems From Zero

Date: 2026-07-28
Target project: `ikonushok/recommender-systems-from-zero`
Audited commit: `6ad30d7c76bebab1fa28fbce35ddf7102792f04e`

## Summary

- Verdict: `PASS_WITH_RISKS`
- Readiness stage: MVP educational codebase
- Practical readiness estimate: 78-85% for code-backed educational use
- Validation level / evidence level: L2 static/code/config review plus existing unit tests and import/AST checks
- Audit mode: `code-only`
- Report type: `code-only-project-readiness`
- Scope: source modules, tests, config, notebook metadata, data helper layout
- Excluded context as proof: README and docs were not used as proof in this code-only report
- Main risk: reproducibility and advanced-edge-case coverage, not core algorithm shape

By code and test evidence only, this is a real educational Python package rather than notebook-only material. The repository contains reusable modules for data preparation, time-aware splitting, top-K metrics, baseline recommenders, content-based and item-item recommenders, hybrid fusion, ALS/LightFM/NeuralCF/TwoTower wrappers, and a sequential recommender. The existing unit suite passed in the audit environment.

The code-only blockers are limited but concrete: package metadata does not declare runtime dependencies, local audit runtime is not the documented Python 3.12 environment, advanced dependency modules are import-tolerant but not executable here, and two advanced negative-sampling loops can hang when a user's seen set covers all candidate items.

## What Is Implemented In Code

| Area | Evidence | Status |
|---|---|---|
| Data loaders and canonical interaction builders | `src/recsys_basics/data.py` | Implemented for MovieLens, Retailrocket, Amazon Reviews 2023 local/raw paths. |
| Time-aware splits | `src/recsys_basics/split.py` | Implemented and covered by tests. |
| Ranking metrics | `src/recsys_basics/metrics.py` | Implemented and covered by tests for Precision, Recall, HitRate, MAP, NDCG. |
| Popularity baseline | `src/recsys_basics/basic/popularity.py`, `tests/test_popularity.py` | Implemented and covered. |
| Content-based TF-IDF | `src/recsys_basics/basic/content_based.py`, `tests/test_content_based.py` | Implemented and covered. |
| Item-item CF | `src/recsys_basics/basic/item_item.py`, `tests/test_item_item.py` | Implemented and covered. |
| Hybrid fusion | `src/recsys_basics/basic/hybrid.py`, `tests/test_hybrid.py` | Implemented and covered. |
| Sequential baseline | `src/recsys_basics/advanced/sequence_model.py`, `tests/test_sequence_model.py` | Implemented and covered. |
| Advanced wrappers | `src/recsys_basics/advanced/als.py`, `lightfm.py`, `neural_cf.py`, `two_tower.py` | Implemented but not covered by local tests in this audit except import/AST. |
| Notebook artifacts | `notebooks/**/*.ipynb` metadata inspection | 15 notebooks have executed code-cell metadata and outputs. |

## Code-Visible Tasks

| Task inferred from code | Readiness | Evidence | Main gap |
|---|---|---|---|
| Prepare public recommender datasets | Medium | `data.py`, data raw README files | Download paths were not smoke-tested. |
| Split interactions without future leakage | High | `split.py`, `tests/test_split.py`, passing tests | No CI evidence. |
| Evaluate top-K recommendations | High | `metrics.py`, `tests/test_metrics.py`, passing tests | No duplicate-recommendation metric edge test beyond existing grouping/order tests. |
| Generate baseline recommendations | High | popularity/content/item-item/hybrid modules and tests | Core path looks solid for teaching. |
| Demonstrate sequential recommendation | Medium-high | `sequence_model.py`, passing tests | Only lightweight baseline is covered, which matches educational scope. |
| Demonstrate advanced model classes | Medium | ALS, LightFM, NeuralCF, TwoTower modules | Advanced libraries were missing locally; notebook run-all not repeated. |

## Code Project Map

- Languages and frameworks: Python package with pandas, numpy, scipy, scikit-learn, optional implicit/LightFM/PyTorch wrappers.
- Entrypoints: notebooks and importable modules under `src/recsys_basics`.
- Services and workers: none; this is not a service project.
- API/UI contracts: none.
- Database and migrations: none.
- Queues, caches, schedules: none.
- External integrations: dataset downloads from GroupLens, Hugging Face, UCSD/McAuley-Lab sources.
- Tests and CI: `tests/` contains unittest suite; no `.github` workflow found.
- Deployment and monitoring: not applicable to stated educational scope.

## Strengths Visible In Code

| Strength | Evidence | Why it matters |
|---|---|---|
| Source code is not trapped inside notebooks | `src/recsys_basics/**` | Makes the project reviewable, testable, and reusable. |
| Core algorithms have focused tests | 27 passing unittest cases | Supports the claim that the beginner path is usable. |
| Advanced optional dependencies fail with explicit messages | `_require_implicit`, `_require_lightfm`, `_require_torch` | Missing local libraries do not break module import. |
| Notebook outputs are committed | Metadata inspection found executed code cells and outputs in all 15 notebooks | Supports, but does not prove today, previous run-all claims. |

## Gaps And Risks

| Priority | Area | Evidence | Impact |
|---|---|---|---|
| P1 | Packaging metadata | `pyproject.toml:10` and no `[project.dependencies]` | `pip install .` does not express the dependencies needed by importable modules. |
| P1 | Advanced negative sampling | `neural_cf.py:262-265`, `:316-319`; `two_tower.py:334-337` | Dense user histories can make training sample generation loop forever. |
| P2 | Python version contract | `pyproject.toml:10`, `tests/README.md:85-96`, command output `Python 3.11.6` | Project docs and package metadata do not give one clear supported interpreter contract. |
| P2 | CI evidence | no `.github` files found | Passing tests are local evidence only. |
| P2 | Advanced validation | local package check showed `implicit`, `lightfm`, `torch`, `optuna`, `jupyterlab` missing | Advanced paths need clean-env validation. |

## Mandatory Bug Discovery

- Status: ranked candidates found
- Inspected paths: `src/recsys_basics/**`, `tests/**`, `pyproject.toml`, `requirements.txt`, notebook metadata
- Candidate count: 4
- Strongest candidate: dense negative sampling can hang in NeuralCF/TwoTower helper loops
- Reproduction status: `NOT_REPRODUCED`
- Proposed test-first next step: add tiny tests where one user has interacted with every item and assert the sampler raises a clear `ValueError` or skips the user.

| # | Candidate | Contract evidence | Trigger | Location | Confidence |
|---|---|---|---|---|---|
| 1 | NeuralCF negative sampling can loop forever when no unseen item exists. | Sampler repeatedly draws from all item indices while the sample is in `seen_item_indices`. | A user has interacted with every item in the fitted item universe. | `src/recsys_basics/advanced/neural_cf.py:262-265`, `:316-319` | High |
| 2 | TwoTower negative sampling has the same all-items-seen loop risk. | Same while-loop pattern over all item indices and per-user seen set. | A dense user history covers all item IDs after feature-table intersection. | `src/recsys_basics/advanced/two_tower.py:334-337` | High |
| 3 | Package metadata omits runtime dependencies. | `pyproject.toml` has package metadata but no `[project.dependencies]`; runtime imports need pandas/numpy/scipy/sklearn/etc. | User installs with package tooling instead of `requirements.txt`. | `pyproject.toml:5-16`, `requirements.txt:1-13` | Medium-high |
| 4 | Optional Hugging Face Amazon loader depends on `datasets`, but requirements do not include it. | `data.py` imports `datasets` optionally and tells users to install it manually; `requirements.txt` omits `datasets`. | User calls `load_amazon_reviews_2023_frames_hf()` after installing project requirements. | `src/recsys_basics/data.py:23-29`, `:549-560`, `requirements.txt` | Medium |

## Contract Reliability Security Checks

- Cross-part contracts: source modules and tests align well for core path.
- Error handling and queue/file/data loss risk: no queues; dataset download helpers raise explicit exceptions for missing files and network errors.
- Idempotency, retries, and time/state handling: download helpers skip existing files unless overwrite is set; no retry layer visible.
- Auth, permissions, secrets, public surfaces: not applicable; no service/API/secrets found.
- Unfinished or dead paths: no TODO/FIXME/stub blockers found; advanced wrappers lack tests compared with core wrappers.

## Findings

| Severity | Evidence strength | Area | Evidence | What is proven | Impact | Recommended next action |
|---|---|---|---|---|---|---|
| `HIGH` | direct code contradiction | Advanced sampling | `neural_cf.py:262-265`, `:316-319`; `two_tower.py:334-337` | The sampler has no exit path when all candidates are in `seen_items`. | Advanced training can hang on dense toy fixtures. | Add available-negative guard and regression tests. |
| `MEDIUM` | static config contradiction | Packaging | `pyproject.toml:10`, no dependencies; `requirements.txt:1-13` | Package metadata does not declare runtime deps. | Onboarding can fail for users expecting package install semantics. | Add dependencies/extras or explicit install docs. |
| `MEDIUM` | missing evidence | CI/test automation | no `.github` workflow found | Local tests pass, but there is no repeatable public CI signal. | Future changes can regress unnoticed. | Add Python 3.12 CI running unittest suite. |
| `LOW` | missing evidence | Notebook validation | notebook metadata has outputs; run-all not repeated here | Current audit did not prove every notebook still runs from scratch. | README run-all claim depends on prior author evidence. | Add notebook smoke/run-all command or CI job. |

## Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 | No P0 action found for educational scope. | - | - |
| P1 | Add negative-sampling guard/tests for NeuralCF and TwoTower. | Advanced training hang. | New tests pass and fail on current behavior before fix if reproduced. |
| P1 | Align package metadata and install docs. | Reproducibility/onboarding ambiguity. | Clean env install command succeeds. |
| P2 | Add CI for tests and optional notebook validation. | Repeatability. | Public CI badge/logs passing. |

## Readiness Assessment

- Current stage: MVP educational codebase.
- Why not lower: source modules are importable, core tests pass, and notebooks have executed metadata.
- Why not production-ready: project is explicitly not a service or production platform; no serving, monitoring, deployment, rollback, or production ML lifecycle.
- Smallest next validation step: clean Python 3.12 environment with `requirements.txt`, then rerun unit tests and one basic notebook from scratch.

## Evidence Log

- Files inspected: `pyproject.toml`, `requirements.txt`, `README.md`, `tests/README.md`, `src/recsys_basics/**`, `tests/**`, notebook metadata, data README files.
- Commands run: clone, `git rev-parse HEAD`, file listing, unit tests, import-all script, AST parse script, package/version inspection, notebook metadata inspection.
- Command outcomes: unit tests `27 OK`; import-all `IMPORT_OK 13`; AST `AST_OK`; local Python `3.11.6`; current audit env missing several advanced dependencies.
- Claims not verified: fresh Python 3.12 install, full notebook run-all, dataset download smoke, advanced training runs.
- Residual risk: advanced course path is plausible and structured, but needs clean-env validation before being treated as fully refreshed runtime evidence.
