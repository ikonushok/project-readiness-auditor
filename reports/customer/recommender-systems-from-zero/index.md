# Recommender Systems From Zero: Audit Report Pack

Date: 2026-07-28
Target project: `ikonushok/recommender-systems-from-zero`
Repository URL: https://github.com/ikonushok/recommender-systems-from-zero
Audited commit: `6ad30d7c76bebab1fa28fbce35ddf7102792f04e`

## Executive Decision

| Field | Result |
|---|---|
| Verdict | `PASS_WITH_RISKS` |
| Practical readiness stage | MVP / beta-quality educational course repository |
| Practical readiness estimate | 80-88% for public educational use; not a production recommender platform by design |
| Main decision | Good public example for `reports/customer/`, with a few reproducibility and advanced-validation caveats |
| Main reason | The project has coherent docs, notebooks, reusable source modules, dataset helpers, and 27 passing unit tests for the core learning path. |
| Evidence level | L2: static docs/code/config review plus existing unit tests, module imports, AST parse, and notebook metadata inspection |

The project is substantially aligned with its stated scope: it explicitly positions itself as an educational recommender-systems course, not a production service. The strongest evidence is the combination of structured README/docs, modular Python code under `src/recsys_basics`, executed notebook metadata, and a passing unit test suite for metrics, split logic, baseline models, content-based, item-item, hybrid, and sequential components.

The main risks are not product blockers. They are reproducibility and validation gaps: `pyproject.toml` does not declare runtime dependencies, its `requires-python = ">=3.10"` is weaker than the documented Python 3.12 path, there is no CI evidence, and advanced notebooks were not rerun in a fresh Python 3.12 environment during this audit.

## Three Main Risks

| Risk | Why it matters | First proof needed |
|---|---|---|
| Packaging metadata is weaker than the learning environment contract | `pip install .` would install the package metadata without the dependencies listed in `requirements.txt`; this can surprise users who expect package-style installation. | Add `[project.dependencies]` or document `pip install -r requirements.txt && pip install -e .`; verify in a clean env. |
| Advanced path has less fresh runtime proof than core | Existing metadata shows notebooks have outputs, but this audit did not rerun all notebooks with `implicit`, `lightfm`, `torch`, and `optuna`. | Run all notebooks in Python 3.12.1 or equivalent CI job and publish the command/result. |
| Negative sampling in neural/two-tower helpers can hang on dense user histories | If a user has seen every candidate item, the sampling loop has no available negative item. | Add a tiny regression test for all-items-seen users and fail fast or skip those users. |

## Reports

| Report | Purpose | Best audience |
|---|---|---|
| `code-only-project-readiness-2026-07-28.md` | Code/config/test baseline without using docs as proof | Maintainer, reviewer |
| `project-readiness-2026-07-28.md` | Readiness against the public README goals | Author, users, course/product owner |
| `bug-audit-2026-07-28.md` | Mandatory ranked bug candidates and test-first plan | Maintainer |

## Recommended Work Order

| Step | Action | Reason |
|---|---|---|
| 1 | Fix packaging/runtime contract: align Python version and dependency installation path. | This is the highest-leverage public onboarding improvement. |
| 2 | Add focused tests for dense negative-sampling edge cases in `neural_cf.py` and `two_tower.py`. | Prevents a real hang scenario in advanced experiments. |
| 3 | Add CI for `PYTHONPATH=src python -m unittest discover -s tests -v` on Python 3.12. | Converts local test evidence into repeatable public evidence. |
| 4 | Add an optional notebook validation script or documented run-all checklist. | Makes the README's run-all claim easier to refresh and trust. |

## Commands Run

| Command | Outcome |
|---|---|
| `git ls-remote https://github.com/ikonushok/recommender-systems-from-zero.git HEAD` | Resolved HEAD `6ad30d7c76bebab1fa28fbce35ddf7102792f04e`. |
| `git clone https://github.com/ikonushok/recommender-systems-from-zero.git .audit-targets/github/ikonushok/recommender-systems-from-zero` | Clone succeeded. |
| `git rev-parse HEAD` | Confirmed audited commit. |
| `rg --files` and targeted file reads | Project map built from README, docs, notebooks, `src`, tests, config, data notes. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v` | Passed: 27 tests, `OK`. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 - <<'PY' ... import modules ... PY` | Passed: imported 13 project modules. |
| `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY' ... ast.parse ... PY` | Passed: `AST_OK`. |
| Notebook metadata inspection script | Found 15 notebooks with executed code-cell metadata and outputs. |
| `PYTHONDONTWRITEBYTECODE=1 python3 --version` | Local audit runtime is Python 3.11.6, while project docs expect Python 3.12.x. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m pip index versions pandas` | Failed due restricted network/DNS in audit environment; not treated as project failure. |

## Missing Evidence

- Clean Python 3.12 environment creation from `requirements.txt`.
- Full notebook `restart kernel + run all` during this audit.
- CI workflow evidence.
- Runtime validation for advanced libraries not installed in the local audit environment: `implicit`, `lightfm`, `torch`, `optuna`, `jupyterlab`.
- Download smoke checks for MovieLens, Amazon Reviews 2023, and Retailrocket.

## Residual Risk

The public course is usable and coherent by repository evidence, but the "fully runnable advanced path" claim should remain conditional until the advanced notebooks are rerun in a clean Python 3.12 environment and the dependency contract is made explicit.
