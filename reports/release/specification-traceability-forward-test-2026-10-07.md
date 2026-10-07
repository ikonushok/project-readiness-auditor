# Export CLI — brief project-readiness audit

## Summary

- Verdict: `BLOCK` for claiming conformance to the approved CLI release 1 specification.
- Audit mode: `docs-vs-code`.
- Report type: `project-readiness` (explicit brief, single-report exception).
- Target project: `/private/tmp/pra-spec-forward-016`; target release: CLI release 1.
- Auditor skill version: `0.1.6`.
- Readiness stage: Technical prototype.
- Validation level / evidence level: `L1`, static project slice only.
- Validation basis: all five raw fixture files inspected against the skill's specification, bug-discovery, and reporting rules. No target code, test, CLI, benchmark, or validator was executed. L1 describes this narrow audit exercise, not runtime confidence or package release readiness.

The small Python exporter implements normalization and writes CSV rows. Its source supports whitespace cleanup, removal of blank names, and preservation of order and duplicates. The inspected test encodes these expectations but has not been run. Release 1's required JSON format has no implementation path, so a claim of full specification conformance is unsupported. The laptop latency requirement also lacks measurements. Next work should address the release 1 format gap and obtain targeted behavioral and benchmark evidence; release 2 proposals do not belong in that batch.

## Scope and Project Map

Task specification: compare the approved release 1 requirements to raw source and tests; include mandatory read-only bug discovery and a compact report. Allowed operations were file listing/reading and creation of this external report. Execution, target modifications, new reproducers, dependency installation, and production fixes were excluded. Previous reports and parent implementation conclusions were excluded throughout.

Python standard-library CLI: `exporter.py:10-20` parses positional names, calls `normalize`, and writes one CSV row per normalized name to stdout. `normalize` is at `exporter.py:6-7`. One existing test is at `test_exporter.py:4-5`. The five-file inventory contains no package manifest, CI, deployment, monitoring, database, queue, service, or external integration files. Those absences describe the inspected fixture, not a wider repository.

Product maturity: normalization and CSV are visible prototype capabilities; approved JSON export is missing; benchmark and runtime verification are missing. Sorting, deduplication, and encryption are release 2 draft proposals. No production contour is evidenced.

## Specification Sources

- Specification traceability: v1
- Specification availability: PRESENT
- Inspected requirement scope: all five requirements in `spec.md`, including its acceptance example and performance constraint; both draft requirements inspected for applicability only.
- Excluded or conflicting sources and applicability rationale: the draft targets release 2 and is explicitly Draft; it is not an obligation for release 1. Its reused FR-001 is qualified by source below. README's CSV statement does not expressly say CSV-only, so it does not override the approved JSON requirement.

| Source | Version / date | Approval status | Target release / component | Applicability decision |
|---|---|---|---|---|
| `spec.md:3-9` | 1.0 / 2026-10-01 | Approved | CLI release 1 | Applicable current requirements; explicit metadata matches this audit. |
| `README.md:3` | UNKNOWN / UNKNOWN | UNKNOWN | CLI release 1; next-release pointer | Contextual CSV claim and explicit pointer to approved spec; not proof of behavior. |
| `draft-v2.md:3-6` | 2.0 / 2026-10-05 | Draft | CLI release 2 | OUT_OF_SCOPE for release 1, despite its newer date. |

## Requirements Traceability

Paths below are relative to the target project. Tests cited as verification evidence were inspected but unrun. Behavioral requirements are not confirmed solely by source inspection.

| Requirement | Source | Expected behavior | Implementation evidence | Verification evidence | Status | Gap / next check |
|---|---|---|---|---|---|---|
| FR-001 | `spec.md:5` | Trim edges and collapse repeated whitespace in non-empty names; acceptance example produces `Ada Lovelace`. | `exporter.py:6-7`, `normalize`: split followed by single-space join. | `test_exporter.py:4-5`, `test_normalization`, includes the stated example; inspected, unrun. | PARTIAL | Source and test align; execution of the acceptance example and other whitespace cases is missing. |
| FR-002 | `spec.md:6` | Ignore blanks; preserve relative order and duplicates. | `exporter.py:7` filters on `strip()` and iterates original names without sorting or deduplication. | `test_exporter.py:5` expects blank removal and duplicate `Bob` entries; inspected, unrun. | PARTIAL | Behavioral verification missing; test does not independently exercise varied input order. |
| FR-003 | `spec.md:7` | `--format json` emits a JSON array of normalized names. | `exporter.py:11-16`: only positional `names` is registered; output path uses `csv.writer`; no format selection or JSON emitter appears in the complete source. | No matching test or execution evidence. | CONTRADICTED | Missing implementation, not merely missing verification; classify as product/API gap. Add capability only under a separately authorized edit scope, then verify exact CLI invocation/output. |
| FR-004 | `spec.md:8`, interpreted with `spec.md:6` | Exports have stable ordering; release 1 order-preservation requirement supplies the applicable order. | `exporter.py:7,15-16` traverses normalized names in sequence. | Existing normalization test checks one sequence; no export/order scenario executed. | PARTIAL | CSV output ordering and repeated-run stability remain unverified. No release 2 sorting obligation applies. |
| SC-001 | `spec.md:9` | Normalize 100,000 names within 100 ms on deployment laptop. | `exporter.py:6-7` is the code path to measure; static inspection establishes no latency result. | No benchmark, laptop identity, representative workload, or timing output in fixture. | NOT_CHECKED | Missing measured verification; define workload and target laptop, then benchmark. |
| `draft-v2:FR-001` | `draft-v2.md:5` | Sort names and remove duplicates in release 2. | Current `exporter.py:7` preserves order and duplicates; comparison is contextual only. | None required for release 1. | OUT_OF_SCOPE | Draft / future release; do not label current release broken for following approved FR-002. |
| `draft-v2:FR-005` | `draft-v2.md:6` | Encrypt exported files in release 2. | Current stdout CSV path at `exporter.py:14-16`; applicability only. | None required for release 1. | OUT_OF_SCOPE | Draft / future release; no current obligation established. |

No percentage is reported: the five applicable requirements include behavioral, capability, and measured constraints, and static evidence coverage is not feature completeness.

## Findings

1. **MEDIUM — release 1 format capability gap.** Confidence: high for static absence. Evidence strength: `product/API gap`. `spec.md:7` requires JSON, while the complete CLI source at `exporter.py:11-16` registers only names and writes CSV. This establishes missing implementation; actual parser rejection and exact output were not executed. Impact: the advertised approved release scope cannot be treated as fulfilled. Next action: implement format selection in a separately authorized scope and obtain CLI acceptance evidence.
2. **MEDIUM — release performance claim lacks evidence.** Confidence: high for missing fixture evidence. Evidence strength: `product/API gap` (verification gap, not an assertion that code is too slow). `spec.md:9` names a numerical laptop target; all five fixture files contain no measurements. Impact: latency conformance cannot be assessed. Next action: define the laptop/workload and measure the actual normalization path.
3. **LOW — behavioral and release reproducibility evidence is incomplete.** Confidence: high for inspected scope. Evidence strength: `product/API gap` (verification gap). Only `test_exporter.py:4-5` is present; it is unrun, does not exercise CLI serialization, and the inventory has no declared Python/test-runner versions or CI. Impact: source alignment does not establish execution success or reproducible release behavior. Next action: approve a minimal read-only execution environment and inspect test/CLI output.

## Mandatory Bug Discovery

- Status: `NO_BUG_PROVEN` for the inspected scope.
- Inspected paths: CLI positional input → normalization → stdout CSV; empty/blank input, internal whitespace, order and duplicate preservation; existing test contract.
- Concrete candidate count: 0. No internal source contradiction with a defensible reachable trigger survived ranking. Missing JSON is an incomplete capability rather than an automatically proven correctness bug. Future-release sorting and deduplication are not current contracts.
- Reproduction status: no reproducer executed. No candidate table or immediate bug-fix batch is warranted.
- Immediate work batch: JSON capability and targeted behavioral verification. Backlog: reproducible release setup and, after scope confirmation, release 2 draft features. No speculative bugs added to fill a top-three batch.
- Project files modified: no. Tests, reproducers, dependencies, and production source were unchanged. Exact reproduction files/commands and production fixes would require separate approvals; this audit requests neither.

## Contract and Validation Review

Contract review was a separate pass over format/CLI arguments, stdout serialization, and expected normalization output. No upstream/downstream consumer is supplied; CSV interoperability beyond the source path is unverified. Auth, secrets, external services, queues, migrations, and server contracts are not visible in this fixture.

Validation review was a separate pass over evidence strength and claim wording. This report makes no runtime, measured performance, production-readiness, or package release-validation claim. The raw source supports static alignment only, the format gap is not presented as a reproduced parser failure, and the future draft is explicitly excluded. Residual uncertainty lowers behavioral statuses and limits the evidence level.

## Evidence Log

Target files inspected in full: `spec.md`, `README.md`, `exporter.py`, `draft-v2.md`, `test_exporter.py`, all under `/private/tmp/pra-spec-forward-016`.

Workflow sources inspected: root `agents/context_router.md`, `agents/project_readiness_auditor.md`, `agents/task_spec_short.md`, `agents/contract_risk_reviewer.md`, `agents/validation_reviewer.md`; public `project-readiness-auditor/SKILL.md`, `VERSION`, `references/audit-methodology.md`, `references/readiness-rubric.md`, `references/report-template.md`. Combined workflow output was partially truncated, so the rubric and first 65 template lines were read separately. The specification section and project-readiness template were visible in the combined output.

Commands run, exactly as issued (working directory `/Users/bobrsubr/PycharmProjects/_petprojects/project-readiness-auditor`):

```text
cat agents/context_router.md agents/project_readiness_auditor.md agents/task_spec_short.md
cat project-readiness-auditor/SKILL.md
rg --files /private/tmp/pra-spec-forward-016
cat project-readiness-auditor/VERSION project-readiness-auditor/references/audit-methodology.md project-readiness-auditor/references/readiness-rubric.md project-readiness-auditor/references/report-template.md
cat agents/contract_risk_reviewer.md agents/validation_reviewer.md
nl -ba /private/tmp/pra-spec-forward-016/spec.md
nl -ba /private/tmp/pra-spec-forward-016/README.md
nl -ba /private/tmp/pra-spec-forward-016/exporter.py
nl -ba /private/tmp/pra-spec-forward-016/draft-v2.md
nl -ba /private/tmp/pra-spec-forward-016/test_exporter.py
cat project-readiness-auditor/references/readiness-rubric.md
sed -n '1,65p' project-readiness-auditor/references/report-template.md
```

All commands exited 0. Target inventory returned five files; numbered reads exposed complete target contents. No target code/tests, generated project scripts, or report validator ran. This separate report was written with the file-editing tool; fixture and repository files were not modified.

## Missing Evidence, Residual Risk, and Closure Plan

Missing evidence: executed normalization/CLI acceptance output, JSON capability, laptop benchmark, defined deployment laptop/workload, declared supported Python/test environment, build/package/CI evidence, and any release/deployment/operations/rollback record. Broader Unicode whitespace, CSV quoting, terminal encoding, and error handling remain outside demonstrated behavior; no defect is asserted for these without stronger evidence.

Prioritized closure: (1) address required JSON capability under an authorized edit scope; (2) verify normalization and actual CSV/JSON CLI outputs, including blank input, order and duplicates; (3) measure SC-001 on the identified laptop and record the environment. Separate release 2 proposals from this work.

Next smallest validation step: obtain approval for a non-mutating existing-test/CLI execution plan in a disposable environment, with exact commands and inspected output. This audit has completed its authorized static scope and does not depend on that approval.

## Forward-Test Skill Feedback

The skill supports the task clearly: explicit brief exception, source metadata, applicable-release selection, seven-column traceability, distinct requirement/verdict vocabularies, unrun-test caveat, measurement requirement, and separation of product gaps from bugs were directly usable. It correctly prevents the newer draft from overriding approved release 1.

Two confusing rules remain. The readiness rubric defines `NOT_REPRODUCED` as an approved test that failed to reproduce a bug, while report templates use it for candidates not yet executed; a future audit with candidates may need clarification. Also, validation levels describe auditor-pack workflow depth rather than target runtime proof, so a report needs an explicit basis such as the L1 static slice here.

Report/validator compatibility is unverified: the methodology supplies a strict command for a full customer report pack, but does not give a corresponding command for this explicitly permitted single report at an arbitrary external path. No validator was run and no incompatibility is asserted. The v1 markers, source columns, requirement statuses, evidence separation, and mandatory bug status have been included to make the report reviewable; structural acceptance still needs a separate check by the authoring workflow.
