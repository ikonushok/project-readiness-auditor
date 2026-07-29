# Code-Only Project Readiness: ikonushok/hiking-route-recommender-demo

## Summary

- Verdict: `PASS_WITH_RISKS`
- Readiness stage: Integration MVP / stable P0 demo baseline
- Practical readiness estimate: good synthetic demo and engineering handoff artifact; not production-ready.
- Validation level / evidence level: L1 static source/config/test/docs slice.
- Validation basis: target checkout inspected at `c3494bc`; static files and marker search were inspected with exact read-only commands; no runtime command was executed.
- Audit mode: `code-only`
- Report type: `code-only-project-readiness`
- Target project: ikonushok/hiking-route-recommender-demo
- Scope: code, tests, configs, scripts, Docker/Prometheus files, and inspected command output.
- Excluded context: previous audit reports.
- Main risk: demo infrastructure can be overread as production-ready infrastructure.

The inspected code proves a real end-to-end recommender demo: synthetic CSV validation, feature engineering, popularity/collaborative/content retrieval, candidate merge, business rules, offline evaluation, FastAPI serving, and monitoring metrics. It is materially stronger than a notebook-only prototype because P0 behavior is represented in package modules and tests.

## What Is Implemented In Code

| Area | Evidence | Status |
|---|---|---|
| Data contracts | `src/hiking_recommender/data_loader.py`, `tests/test_data_loader.py` | Implemented by static inspection |
| Retrieval and merge | package retrieval modules, `tests/test_hybrid_retrieval.py` | Implemented by static inspection |
| Business rules | `src/hiking_recommender/business_rules.py`, `tests/test_business_rules.py` | Implemented by static inspection |
| API serving | `src/hiking_recommender/api.py`, `tests/test_api.py` | Implemented; not runtime-rerun |
| Evaluation | `scripts/run_offline_evaluation.py`, `docs/evaluation_report.md` | Implemented with synthetic metrics |
| Monitoring | `src/hiking_recommender/monitoring.py`, `prometheus.yml`, `docker-compose.yml` | Configured; not runtime-rerun |

## Code-Visible Tasks

| Task inferred from code | Readiness | Evidence | Main gap |
|---|---|---|---|
| Load validated synthetic datasets | Strong static | `data_loader.py`, tests | Runtime not rerun |
| Produce hybrid recommendations | Strong static | API/retriever/business-rule tests | Service not started here |
| Compare offline models | Moderate | evaluation script/report | Metrics not regenerated here |
| Expose observability | Partial | monitoring config | Scrape path not runtime-proven |

## Code Project Map

- Languages and frameworks: Python 3.10+, pandas, numpy, FastAPI, uvicorn, pytest.
- Entrypoints: `scripts/generate_synthetic_data.py`, `scripts/run_baseline_smoke.py`, `scripts/run_hybrid_smoke.py`, `scripts/run_offline_evaluation.py`, `uvicorn hiking_recommender.api:app`.
- Services and workers: FastAPI app with `/health`, `/recommendations`, metrics middleware.
- API/UI contracts: API schemas and tests inspected; `web_ui.py`/template present but not deeply audited.
- Database and migrations: no database; synthetic CSV files are committed.
- Queues, caches, schedules: none inspected.
- External integrations: Docker Compose for Prometheus, Pushgateway, and Grafana.
- Tests and CI: tests present; no GitHub workflow found in inspected file list.
- Deployment and monitoring: compose/prometheus present; Grafana config is demo-only insecure.

## Strengths Visible In Code

| Strength | Evidence | Why it matters |
|---|---|---|
| Full P0 path | package modules and scripts | Demonstrates more than isolated algorithms |
| Contract tests | `tests/test_api.py`, `tests/test_business_rules.py`, `tests/test_data_loader.py` | Protects API/data/rules behavior |
| Honest synthetic boundary | README and docs mention synthetic data and non-production scope | Reduces risk of overclaiming production quality |

## Gaps And Risks

| Severity | Evidence strength | Area | What is proven | Recommended next action |
|---|---|---|---|---|
| HIGH | static config contradiction | readiness/security | `docker-compose.yml` enables Grafana anonymous Admin access and sets `GF_SECURITY_ADMIN_PASSWORD=admin`; this is acceptable only as local demo infrastructure, not production readiness. | Document local-only boundary or harden Grafana before any shared deployment. |
| MEDIUM | framework/runtime candidate | observability | `prometheus.yml` targets `host.docker.internal:8001`, while README API examples use `127.0.0.1:8000`; scrape success depends on runtime port alignment not proven here. | Run API plus Prometheus smoke on the intended ports. |
| MEDIUM | product/API gap | product readiness | Docs explicitly bound the project to synthetic data and non-production scope. | Validate on target-domain data before claiming recommender quality. |

## Mandatory Bug Discovery

- Status: `INCONCLUSIVE` for runtime bugs; two concrete static/runtime candidates recorded.
- Inspected paths: README, package modules, tests, Docker/Prometheus config, docs.
- Candidate count: 2
- Strongest candidate: Grafana anonymous Admin/admin password in `docker-compose.yml` is a deployment/security bug candidate if this compose file is reused outside local demo.
- Reproduction status: `NOT_REPRODUCED` for runtime candidates; static config risk is directly visible.
- Proposed test-first next step: run pytest and local API/monitoring smoke; for deploy risk, assert compose is local-only or harden Grafana.

| # | Candidate | Evidence strength | Contract evidence | Trigger | Location | Confidence | Reproduction status |
|---|---|---|---|---|---|---|---|
| 1 | Grafana anonymous Admin/admin password in docker-compose.yml is unsafe if this compose file is reused outside a local demo. | static config contradiction | `docker-compose.yml` environment section | Shared or non-local deployment | `docker-compose.yml` | High | `NOT_REPRODUCED` as exploit; static config visible |
| 2 | Monitoring scrape target may not match the README API startup port unless the API is explicitly bound to 8001. | framework/runtime candidate | `prometheus.yml`, README API example, load-test default | Start monitoring with API on README default port | `prometheus.yml`, README | Medium | `NOT_REPRODUCED` |

## Contract Reliability Security Checks

- Cross-part contracts: API tests align `/health` and `/recommendations`; business rules tests cover filters, fallback, and deduplication.
- Error handling and data loss risk: CSV loaders reject missing columns, nulls, bad IDs, and bad event weights by inspection.
- Idempotency, retries, and time/state handling: not a stateful production service in inspected scope.
- Auth, permissions, secrets, and public surfaces: Grafana anonymous Admin/admin password is visible in compose.
- Unfinished or dead paths: marker search found no TODO/FIXME core gap; placeholder text only in HTML input placeholder.

## Findings

| Severity | Evidence strength | Area | What is proven | Recommended next action |
|---|---|---|---|---|
| HIGH | static config contradiction | readiness/security | `docker-compose.yml` enables Grafana anonymous Admin access and sets `GF_SECURITY_ADMIN_PASSWORD=admin`. | Document local-only boundary or harden Grafana before any shared deployment. |
| MEDIUM | framework/runtime candidate | observability | Prometheus target and README API port can diverge without an explicit runtime contour. | Run API plus Prometheus smoke on the intended ports. |
| MEDIUM | product/API gap | product readiness | The repository explicitly disclaims production code and real-data claims. | Validate on target-domain data before quality or business-impact claims. |

## Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 | Run `python -m pytest`. | Static-only test confidence | Test output |
| P1 | Run API smoke for health/recommendations/metrics. | Serving and monitoring confidence | HTTP output |
| P2 | Harden or label docker-compose Grafana settings as local-only. | Security overclaim | Config diff or documented boundary |

## Readiness Assessment

- Current stage: Integration MVP / stable P0 demo baseline.
- Why not lower: core modules, tests, scripts, metrics, synthetic data, and API exist.
- Why not production-ready: synthetic data, demo-only compose security, no rerun runtime output, no auth/deploy hardening.
- Smallest next validation step: `python -m pytest` in the target checkout.

## Evidence Log

- Files inspected:
- `README.md`
- `pyproject.toml`
- `requirements.txt`
- `docker-compose.yml`
- `prometheus.yml`
- `src/hiking_recommender/api.py`
- `src/hiking_recommender/data_loader.py`
- `src/hiking_recommender/business_rules.py`
- `src/hiking_recommender/evaluation.py`
- `src/hiking_recommender/monitoring.py`
- `src/hiking_recommender/pipeline_metrics.py`
- `scripts/run_offline_evaluation.py`
- `tests/test_api.py`
- `tests/test_business_rules.py`
- `tests/test_data_loader.py`
- `tests/test_hybrid_retrieval.py`
- `tests/test_evaluation.py`
- `docs/evaluation_report.md`
- `docs/p0_baseline.md`
- `docs/data_readiness_checklist.md`
- Commands run:
- `git -C .audit-targets/github/hiking-route-recommender-demo status -sb`
- `git -C .audit-targets/github/hiking-route-recommender-demo log --oneline -1`
- `find .audit-targets/github/hiking-route-recommender-demo -maxdepth 2 -type f`
- `rg -n "TODO|FIXME|placeholder|mock|admin|anonymous|host.docker.internal|8001|8000|NO PRODUCTION|production" .audit-targets/github/hiking-route-recommender-demo`
- `sed -n '1,180p' .audit-targets/github/hiking-route-recommender-demo/docker-compose.yml`
- Inspection notes: read-only static inspection; previous reports excluded from evidence.
- Command outcomes: checkout at `c3494bc`; marker search found Grafana admin/anonymous settings, Prometheus target `host.docker.internal:8001`, README API example on port 8000, and explicit synthetic/non-production scope.
- Claims not verified: current test pass, API startup, Docker/Prometheus/Grafana runtime, real-data quality.
- Residual risk: static inspection can miss runtime dependency and framework behavior.
