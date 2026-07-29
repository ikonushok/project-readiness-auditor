# Project Readiness: ikonushok/hiking-route-recommender-demo

## Summary

- Verdict: `PASS_WITH_RISKS`
- Readiness stage: Integration MVP / stable P0 demo baseline
- Practical readiness estimate: strong commercial-style synthetic demo; not production recommender readiness.
- Validation level / evidence level: L1 static/docs-vs-code slice.
- Validation basis: README/docs were treated as intent, then implementation/tests/config were checked at `c3494bc` with exact read-only commands; no runtime command was executed.
- Audit mode: `docs-vs-code`
- Report type: `project-readiness`
- Target project: ikonushok/hiking-route-recommender-demo
- Scope: README/docs as intent, implementation/tests/config as proof.
- Main risk: demo infrastructure and synthetic results can be overclaimed as production readiness.

The README’s core claim is supported: the repository is a synthetic commercial-style recommender demo with data generation/loading, feature engineering, retrieval, merge, business rules, evaluation, and API serving. The implementation evidence is coherent, but all quality claims remain bounded to synthetic data and unrerun static evidence in this audit.

## Project Goals

- Stated goals: demonstrate a practical hiking/tourism route recommendation pipeline on synthetic data.
- Inferred goals: provide a portable P0 baseline for catalog recommender handoff and customer discussion.
- Non-goals: production code, client data, proprietary schemas, real business impact claims.

## Product Maturity

| Product layer | Current maturity | What is mature | What is missing for the target system |
|---|---|---|---|
| Demo pipeline | Integration MVP | Modules and tests cover the full P0 path | Fresh runtime test output |
| API serving | MVP | FastAPI app and TestClient checks | Deployment/auth hardening |
| Evaluation | MVP | Synthetic offline metrics and report | Real target-domain data and repeated evals |
| Operations | Prototype | Prometheus/Grafana compose exists | Secure deployment profile and smoke proof |

## Project Map

- Languages and frameworks: Python, FastAPI, pandas/numpy, pytest, Prometheus/Grafana.
- Entrypoints: synthetic data generation, baseline/hybrid smoke, offline evaluation, FastAPI app.
- Services and workers: API service with metrics; no background workers.
- API/UI contracts: `/health`, `/recommendations`, optional web UI files.
- Database and migrations: no DB; synthetic CSV data.
- Queues, caches, schedules: none.
- External integrations: local Docker monitoring stack.
- Tests and CI: test suite present; CI not observed.
- Deployment and monitoring: Docker Compose and Prometheus config present; Grafana settings are local-demo-only.

## Findings

| Severity | Evidence strength | Area | What is proven | Recommended next action |
|---|---|---|---|---|
| HIGH | static config contradiction | readiness/security | `docker-compose.yml` enables Grafana anonymous Admin access and sets `GF_SECURITY_ADMIN_PASSWORD=admin`; this is acceptable only as local demo infrastructure, not production readiness. | Document local-only boundary or harden Grafana before any shared deployment. |
| MEDIUM | framework/runtime candidate | observability | `prometheus.yml` targets `host.docker.internal:8001`, while README API examples use `127.0.0.1:8000`; scrape success depends on runtime port alignment not proven here. | Run API plus Prometheus smoke on the intended ports. |
| MEDIUM | product/API gap | product maturity | README/docs state that data and metrics are synthetic/demo-only and not production business-impact claims. | Validate on target-domain data before claiming recommender quality. |

## Mandatory Bug Discovery

- Status: `INCONCLUSIVE` / candidates only.
- Inspected paths: README, package modules, tests, docker-compose, prometheus, docs.
- Candidate count: 2
- Strongest candidate: Grafana anonymous Admin/admin password in `docker-compose.yml` is a deployment/security bug candidate if this compose file is reused outside local demo.
- Reproduction status: `NOT_REPRODUCED` for runtime behavior.
- Proposed test-first next step: pytest + API/metrics smoke; deploy hardening check for compose.

| # | Candidate | Evidence strength | Contract evidence | Trigger | Location | Confidence | Reproduction status |
|---|---|---|---|---|---|---|---|
| 1 | Grafana anonymous Admin/admin password in docker-compose.yml is unsafe if this compose file is reused outside a local demo. | static config contradiction | `docker-compose.yml` environment section | Shared or non-local deployment | `docker-compose.yml` | High | `NOT_REPRODUCED` as exploit; static config visible |
| 2 | Monitoring scrape target may not match the README API startup port unless the API is explicitly bound to 8001. | framework/runtime candidate | `prometheus.yml`, README API example, load-test default | Start monitoring with API on README default port | `prometheus.yml`, README | Medium | `NOT_REPRODUCED` |

## Readiness By Capability

| Capability | Current status | Evidence | Readiness |
|---|---|---|---|
| Synthetic data and validation | Implemented | `data_loader.py`, tests, committed CSVs | Strong static |
| Retrieval and merge | Implemented | package modules and tests | Strong static |
| Business rules | Implemented | module and tests | Strong static |
| Offline evaluation | Implemented | script/report/CSV output | Moderate, not regenerated |
| API serving | Implemented | `api.py`, tests | Moderate, not started |
| Monitoring | Configured | compose/prometheus/metrics modules | Partial |
| Production security | Not ready | anonymous Grafana Admin config | Demo-only |

## Reproducibility

- Dependency evidence: `pyproject.toml`, `requirements.txt`.
- Build evidence: not run.
- Test evidence: test files inspected, not executed.
- Runtime evidence: no service started in this audit.
- Required environment: local Python package install; Docker only for monitoring stack.
- Missing evidence: recorded pytest/API/Docker smoke output.

## Contract Review

- UI vs backend: optional web UI not deeply audited; API contract tested.
- API schemas vs services: static alignment visible through Pydantic schemas and tests.
- Producers vs consumers: data/evaluation/API share package modules.
- Models vs migrations: not applicable.
- Env settings vs deploy config: monitoring scrape target depends on host API port alignment.
- Settings schema vs env examples: minimal config surface.
- Monitoring targets vs deploy service names: Prometheus targets `host.docker.internal:8001`, while README uvicorn example defaults to 8000.
- Registered routes and clients: `/health` and `/recommendations` present and tested.
- File/object paths: committed `data/`, `outputs/`, `docs/` paths align with scripts by inspection.

## Security And Reliability

- Auth and permissions: API has no auth, appropriate for demo; Grafana anonymous Admin is unsafe outside local demo.
- Secrets and tokens: no app secrets found; Grafana password literal `admin` exists.
- CORS and public endpoints: no CORS review performed; API is demo-only.
- Error handling: invalid difficulty returns 400 through tested ValueError path.
- Idempotency and retries: mostly read-only serving; not production-reviewed.
- Time and state handling: in-memory runtime builds at import; suitable for small synthetic demo, not production scale.

## Readiness Assessment

- Current stage: Integration MVP / stable P0 demo baseline.
- Why this stage: full demo workflow and tests exist across modules.
- What blocks the next stage: rerun tests/smoke, harden or scope monitoring compose, validate on real target data.
- Smallest next validation step: run `python -m pytest` and record output.

## Prioritized Closure Plan

| Priority | Action | Risk addressed | Evidence needed to close |
|---|---|---|---|
| P0 | Run pytest. | Test suite may have drifted | Command output |
| P1 | Run API and scrape metrics. | Serving/monitoring mismatch | HTTP/Prometheus output |
| P2 | Harden or label compose. | Demo security | Config/documentation evidence |

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
- Inspection notes: README/docs used as intent only; previous reports excluded from evidence.
- Command outcomes: checkout at `c3494bc`; marker search found Grafana admin/anonymous settings, Prometheus target `host.docker.internal:8001`, README API example on port 8000, and explicit synthetic/non-production scope.
- Claims not verified: current runtime, production security, real-data quality.
- Residual risk: static audit only.
