from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "project-readiness-auditor/scripts/validate_skill.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_skill", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_clean_report_pack(report_root: Path, date: str = "2026-08-15") -> None:
    write_file(
        report_root / "index.md",
        "\n".join(
            [
                "Target project:",
                "Verdict",
                "Practical readiness stage",
                "Evidence level",
                "Three Main Risks",
                "Reports",
                "Recommended Work Order",
                "Commands Run",
                "Missing Evidence",
                "Residual Risk",
                "## Commands Run",
                "- `git -C /tmp/example-project status -sb`",
            ]
        ),
    )
    write_file(
        report_root / f"code-only-project-readiness-{date}.md",
        "\n".join(
            [
                "Audit mode: `code-only`",
                "Report type: `code-only-project-readiness`",
                "Validation level / evidence level: L1",
                "Validation basis: static inspection of README, package config, source, and tests.",
                "Code-Visible Tasks",
                "Mandatory Bug Discovery",
                "Findings",
                "Evidence Log",
                "- Commands run:",
                "- `git -C /tmp/example-project status -sb`",
                "- `rg -n TODO /tmp/example-project/src`",
            ]
        ),
    )
    write_file(
        report_root / f"project-readiness-{date}.md",
        "\n".join(
            [
                "Audit mode: `docs-vs-code`",
                "Report type: `project-readiness`",
                "Validation level / evidence level: L1",
                "Validation basis: docs-vs-code inspection of one static capability slice.",
                "Product Maturity",
                "Mandatory Bug Discovery",
                "Readiness By Capability",
                "Evidence Log",
                "- Commands run:",
                "- `sed -n '1,120p' /tmp/example-project/README.md`",
            ]
        ),
    )
    write_file(
        report_root / f"bug-audit-{date}.md",
        "\n".join(
            [
                "Report type: `bug-audit`",
                "Validation level / evidence level: L1",
                "Validation basis: static bug discovery against source and config contracts.",
                "Bug Candidates",
                "| # | Candidate | Evidence strength | Contract evidence | Trigger | Location | Confidence | Reproduction status |",
                "|---|---|---|---|---|---|---|---|",
                "| 1 | Config contradicts documented production posture. | static config contradiction | Config file | Deploy | config.yml | Medium | `NOT_REPRODUCED` |",
                "Immediate Bug-Fix Batch",
                "| # | Severity | Candidate | Trigger | Evidence | Confidence | Status |",
                "|---|---|---|---|---|---|---|",
                "| 1 | HIGH | Config contradicts documented production posture. | Deploy | config.yml | Medium | `NOT_REPRODUCED` |",
                "Reproduction Approval Gate",
                "Fix Approval Gate",
                "Evidence Log",
                "- Commands run:",
                "- `find /tmp/example-project -maxdepth 2 -type f`",
            ]
        ),
    )


def clean_comparison_section() -> str:
    return "\n".join(
        [
            "## Previous Report Comparison",
            "",
            "- Old reports opened only after current audit freeze: yes",
            "- Current audit freeze artifact: current-report.md",
            "- Previous report artifact(s): previous-report.md",
            "- Same target commit: yes",
            "- Comparison basis: compare frozen current audit to old report text only.",
            "",
            "| Area | Current audit | Previous report | Better | Worse | Unchanged | Evidence | Interpretation |",
            "|---|---|---|---|---|---|---|---|",
            "| Validation level | L1 | L1 |  |  | yes | command log | Test surface grew but validation level did not increase. |",
        ]
    )


def write_clean_public_examples(repo_root: Path) -> None:
    for report_pack in validator.PUBLIC_CUSTOMER_REPORT_PACKS:
        write_clean_report_pack(repo_root / "reports/customer" / report_pack)


class ValidateSkillTests(unittest.TestCase):
    def traceability_report(self, rows: str | None = None, level: str = "##") -> str:
        if rows is None:
            rows = "| FR-001 | spec.md#fr-001 | Trim input | parser.py:3 | Static inspection parser.py:3 | CONFIRMED | - |"
        return "\n".join([
            "Report type: `project-readiness`",
            "Validation basis: static inspection, tests not run.",
            f"{level} Specification Sources",
            "- Specification traceability: v1",
            "- Specification availability: PRESENT",
            "- Inspected requirement scope: FR-001 through FR-006, CLI release 1.",
            "| Source | Version / date | Approval status | Target release / component | Applicability decision |",
            "|---|---|---|---|---|",
            "| spec.md | UNKNOWN | UNKNOWN | CLI release 1 | Scope supplied by user; approval unknown |",
            f"{level} Requirements Traceability",
            "| Requirement | Source | Expected behavior | Implementation evidence | Verification evidence | Status | Gap / next check |",
            "|---|---|---|---|---|---|---|",
            rows,
        ])

    def test_spec_traceability_accepts_all_statuses_at_both_heading_depths(self) -> None:
        rows = "\n".join([
            "| FR-001 | spec.md#1 | Trim input | parser.py:3 | Static inspection parser.py:3 | CONFIRMED | - |",
            "| FR-002 | spec.md#2 | Normalize and validate | parser.py:4 | - | PARTIAL | Validation is missing |",
            "| FR-003 | spec.md#3 | Keep case | parser.py:4 lowercases | - | CONTRADICTED | Compare approved scope with implementation |",
            "| FR-004 | spec.md#4 | p95 under 100ms | - | - | NOT_CHECKED | Run an approved load check |",
            "| FR-005 | spec.md#5 | Preserve stable ordering | - | - | AMBIGUOUS | Clarify meaning of stable |",
            "| FR-006 | roadmap.md#6 | Export JSON | - | - | OUT_OF_SCOPE | Future release draft |",
        ])
        for level in ("##", "###"):
            with self.subTest(level=level):
                self.assertEqual([], validator.validate_spec_traceability(self.traceability_report(rows, level), "sample.md", required=True))

    def test_spec_traceability_rejects_unsupported_confirmation_and_incomplete_rows(self) -> None:
        cases = [
            ("| FR-001 | spec.md | Trim | parser.py:3 | - | CONFIRMED | - |", "missing verification evidence"),
            ("| FR-001 | spec.md | Trim | - | Static review | CONFIRMED | - |", "missing implementation evidence"),
            ("| FR-001 | spec.md | Trim | - | - | NOT_CHECKED | - |", "missing gap / next check"),
            ("| FR-001 | spec.md | Trim | - | - | PASS | next |", "unsupported status"),
            ("| FR-001 | spec.md | Trim | parser.py:3 | static | CONFIRMED |", "wrong column count"),
            ("| FR-001 | - | Trim | parser.py:3 | static | CONFIRMED | - |", "missing source"),
        ]
        for row, signal in cases:
            with self.subTest(signal=signal):
                errors = validator.validate_spec_traceability(self.traceability_report(row), "sample.md")
                self.assertTrue(any(signal in error for error in errors), errors)

    def test_spec_traceability_rejects_duplicate_ids_and_empty_scope(self) -> None:
        report = self.traceability_report()
        duplicate = report + "\n" + report.splitlines()[-1]
        self.assertTrue(any("duplicate requirement ID" in e for e in validator.validate_spec_traceability(duplicate, "sample.md")))
        blank_scope = report.replace("FR-001 through FR-006, CLI release 1.", "")
        self.assertTrue(any("missing inspected requirement scope" in e for e in validator.validate_spec_traceability(blank_scope, "sample.md")))

    def test_spec_traceability_accepts_explicit_no_spec_and_rejects_invented_rows(self) -> None:
        report = "\n".join([
            "## Specification Sources",
            "- Specification traceability: v1",
            "- Specification availability: NONE",
            "- Inspected requirement scope: No documented requirements available.",
            "- No-specification basis: Inspected README/docs/specs; inferred goal: normalize CLI input.",
        ])
        self.assertEqual([], validator.validate_spec_traceability(report, "sample.md", required=True))
        invented = report + "\n## Requirements Traceability\n| Requirement | Status |\n|---|---|\n| FR-001 | CONFIRMED |"
        self.assertTrue(any("NONE must omit" in e for e in validator.validate_spec_traceability(invented, "sample.md")))
        no_basis = report.split("- No-specification basis:")[0]
        self.assertTrue(any("missing No-specification basis" in e for e in validator.validate_spec_traceability(no_basis, "sample.md")))

    def test_spec_traceability_preserves_legacy_but_required_gate_rejects_it(self) -> None:
        self.assertEqual([], validator.validate_spec_traceability("Legacy report", "sample.md"))
        self.assertTrue(validator.validate_spec_traceability("Legacy report", "sample.md", required=True))
        legacy_matrix = "## Requirements Traceability\n| Requirement | Status |\n|---|---|\n| FR-001 | Implemented |"
        self.assertEqual([], validator.validate_spec_traceability(legacy_matrix, "sample.md"))
        for report in (self.traceability_report().replace("v1", "v2"), self.traceability_report().replace("Specification traceability: v1", "Other metadata: v1")):
            self.assertTrue(validator.validate_spec_traceability(report, "sample.md", required=True))

    def test_spec_traceability_handles_scoped_ids_escaped_pipes_and_closed_headings(self) -> None:
        report = self.traceability_report()
        report += "\n| FR-001 | draft.md#fr-001 | Sort names | - | - | OUT_OF_SCOPE | Future draft |"
        report = report.replace("Trim input", r"Trim Ada\|Bob input")
        report = report.replace("## Specification Sources", "## Specification Sources ##")
        report = report.replace("## Requirements Traceability", "## Requirements Traceability ##")
        self.assertEqual([], validator.validate_spec_traceability(report, "sample.md", required=True))
        self.assertEqual([["a", r"b\|c", "d"]], validator.table_rows(r"| a | b\|c | d |"))

    def test_spec_traceability_gate_is_integrated_and_scoped_to_readiness_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            reports = root / "reports/customer/sample"
            write_clean_report_pack(reports)
            errors = validator.validate_customer_report_pack(root, require_spec_traceability=True)
            self.assertEqual(1, len(errors), errors)
            self.assertIn("project-readiness-2026-08-15.md", errors[0])
            self.assertNotIn("code-only", errors[0])
            path = reports / "project-readiness-2026-08-15.md"
            path.write_text(path.read_text() + "\n" + self.traceability_report(), encoding="utf-8")
            self.assertEqual([], validator.validate_customer_report_pack(root, require_spec_traceability=True))

    def test_required_spec_gate_rejects_missing_customer_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.assertTrue(validator.validate_customer_report_pack(root, require_spec_traceability=True))
            (root / "reports/customer").mkdir(parents=True)
            self.assertTrue(validator.validate_customer_report_pack(root, require_spec_traceability=True))

    def test_spec_traceability_rejects_missing_tables_columns_and_source_metadata(self) -> None:
        report = self.traceability_report()
        cases = [
            (report.split("## Requirements Traceability")[0], "missing populated table"),
            (report.replace("| Verification evidence |", "| Test plan |"), "missing or duplicate columns"),
            (report.replace("| spec.md | UNKNOWN | UNKNOWN |", "| spec.md | - | UNKNOWN |"), "missing version / date"),
            (report.replace("| Applicability decision |", "| Source |"), "missing or duplicate columns"),
        ]
        for text, signal in cases:
            with self.subTest(signal=signal):
                errors = validator.validate_spec_traceability(text, "sample.md")
                self.assertTrue(any(signal in error for error in errors), errors)

    def test_spec_traceability_cli_flag_requires_new_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skill = root / "project-readiness-auditor"
            shutil.copytree(REPO_ROOT / "project-readiness-auditor", skill, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
            shutil.copy2(REPO_ROOT / "VERSION", root / "VERSION")
            reports = root / "reports/customer/sample"
            write_clean_report_pack(reports)
            command = [sys.executable, "-B", str(skill / "scripts/validate_skill.py"), str(skill), "--require-spec-traceability", "--customer-report-pack", "sample"]
            rejected = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(1, rejected.returncode, rejected.stdout + rejected.stderr)
            self.assertIn("requires exactly one v1 marker", rejected.stdout)
            path = reports / "project-readiness-2026-08-15.md"
            path.write_text(path.read_text() + "\n" + self.traceability_report(), encoding="utf-8")
            accepted = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(0, accepted.returncode, accepted.stdout + accepted.stderr)
            standalone = root / "brief-audit.md"
            standalone.write_text(self.traceability_report(), encoding="utf-8")
            single_command = command[:4] + ["--spec-traceability-report", str(standalone)]
            single = subprocess.run(single_command, capture_output=True, text=True)
            self.assertEqual(0, single.returncode, single.stdout + single.stderr)
            standalone.write_text("Validation basis: static inspection.", encoding="utf-8")
            missing = subprocess.run(single_command, capture_output=True, text=True)
            self.assertEqual(1, missing.returncode, missing.stdout + missing.stderr)

    def test_live_skill_package_passes_static_and_methodology_checks(self) -> None:
        skill_root = REPO_ROOT / "project-readiness-auditor"

        errors = validator.validate(skill_root)
        errors.extend(validator.validate_methodology_regressions(skill_root))

        self.assertEqual([], errors)

    def test_skill_package_rejects_version_mismatch(self) -> None:
        skill_root = REPO_ROOT / "project-readiness-auditor"
        skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmpdir:
            temporary_repo = Path(tmpdir)
            temporary_skill = temporary_repo / "project-readiness-auditor"
            temporary_skill.mkdir()
            write_file(temporary_skill / "SKILL.md", skill_text)
            write_file(temporary_skill / "VERSION", "999.999.999\n")
            write_file(temporary_repo / "VERSION", "0.1.4\n")

            errors = validator.validate(temporary_skill)

        self.assertTrue(any("skill package VERSION does not match repository VERSION" in error for error in errors))

    def test_skill_package_rejects_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_root = Path(tmpdir) / "project-readiness-auditor"
            write_file(skill_root / "SKILL.md", "---\nname: project-readiness-auditor\n---\n")
            write_file(skill_root / "scripts/__pycache__/validate_skill.cpython-311.pyc", "")

            errors = validator.validate(skill_root)

            self.assertTrue(any("__pycache__" in error for error in errors))

    def test_customer_report_pack_accepts_any_iso_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            report_root = repo_root / "reports/customer/example-project"

            write_file(
                report_root / "index.md",
                "\n".join(
                    [
                        "Target project:",
                        "Verdict",
                        "Practical readiness stage",
                        "Evidence level",
                        "Three Main Risks",
                        "Reports",
                        "Recommended Work Order",
                        "Commands Run",
                        "Missing Evidence",
                        "Residual Risk",
                    ]
                ),
            )
            write_file(
                report_root / "code-only-project-readiness-2026-08-15.md",
                "\n".join(
                    [
                        "Audit mode: `code-only`",
                        "Report type: `code-only-project-readiness`",
                        "Code-Visible Tasks",
                        "Mandatory Bug Discovery",
                        "Findings",
                        "Evidence Log",
                    ]
                ),
            )
            write_file(
                report_root / "project-readiness-2026-08-15.md",
                "\n".join(
                    [
                        "Audit mode: `docs-vs-code`",
                        "Report type: `project-readiness`",
                        "Product Maturity",
                        "Mandatory Bug Discovery",
                        "Readiness By Capability",
                        "Evidence Log",
                    ]
                ),
            )
            write_file(
                report_root / "bug-audit-2026-08-15.md",
                "\n".join(
                    [
                        "Report type: `bug-audit`",
                        "Bug Candidates",
                        "Immediate Bug-Fix Batch",
                        "Reproduction Approval Gate",
                        "Fix Approval Gate",
                        "Evidence Log",
                    ]
                ),
            )

            self.assertEqual([], validator.validate_customer_report_pack(repo_root))

    def test_customer_report_pack_requires_each_report_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            report_root = repo_root / "reports/customer/example-project"
            write_file(report_root / "index.md", "Target project:\n")

            errors = validator.validate_customer_report_pack(repo_root)

            self.assertTrue(any("code-only-project-readiness" in error for error in errors))
            self.assertTrue(any("project-readiness" in error for error in errors))
            self.assertTrue(any("bug-audit" in error for error in errors))

    def test_strict_customer_report_quality_accepts_clean_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_clean_report_pack(repo_root / "reports/customer/example-project")

            errors = validator.validate_customer_report_pack(repo_root, strict_quality=True)

            self.assertEqual([], errors)

    def test_customer_report_pack_can_be_scoped_to_one_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_clean_report_pack(repo_root / "reports/customer/clean-project")
            write_file(repo_root / "reports/customer/broken-project/index.md", "Target project:\n")

            errors = validator.validate_customer_report_pack(
                repo_root,
                strict_quality=True,
                report_pack="clean-project",
            )

            self.assertEqual([], errors)

    def test_public_report_examples_ignore_non_allowlisted_customer_packs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_clean_public_examples(repo_root)
            write_file(repo_root / "reports/customer/legacy-broken/index.md", "Target project:\n")

            errors = validator.validate_customer_report_pack(
                repo_root,
                strict_quality=True,
                public_examples=True,
            )

            self.assertEqual([], errors)

    def test_public_report_examples_require_every_allowlisted_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_clean_report_pack(repo_root / "reports/customer/recommender-systems-from-zero")

            errors = validator.validate_customer_report_pack(repo_root, public_examples=True)

            self.assertTrue(any("hiking-route-recommender-demo" in error for error in errors))
            self.assertTrue(any("mt5-research" in error for error in errors))

    def test_public_report_examples_conflict_with_scoped_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_clean_public_examples(repo_root)

            errors = validator.validate_customer_report_pack(
                repo_root,
                report_pack="recommender-systems-from-zero",
                public_examples=True,
            )

            self.assertEqual(
                ["--customer-report-pack and --public-report-examples cannot be used together"],
                errors,
            )

    def test_strict_report_quality_rejects_no_bug_proven_as_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_root = Path(tmpdir) / "reports/customer/example-project"
            filename = "bug-audit-2026-08-15.md"
            write_file(
                report_root / filename,
                "\n".join(
                    [
                        "Report type: `bug-audit`",
                        "Validation basis: static bug discovery.",
                        "## Bug Candidates",
                        "| # | Candidate | Evidence strength | Reproduction status |",
                        "|---|---|---|---|",
                        "| 1 | NO_BUG_PROVEN for inspected scope. | missing evidence | `NO_BUG_PROVEN` |",
                    ]
                ),
            )

            errors = validator.validate_report_quality(report_root, filename, "bug-audit")

            self.assertTrue(any("NO_BUG_PROVEN" in error for error in errors))

    def test_strict_report_quality_rejects_vague_command_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_root = Path(tmpdir) / "reports/customer/example-project"
            filename = "code-only-project-readiness-2026-08-15.md"
            write_file(
                report_root / filename,
                "\n".join(
                    [
                        "Report type: `code-only-project-readiness`",
                        "Validation basis: static inspection.",
                        "## Evidence Log",
                        "- Commands run:",
                        "- `find target files`",
                    ]
                ),
            )

            errors = validator.validate_report_quality(
                report_root, filename, "code-only-project-readiness"
            )

            self.assertTrue(any("vague command entry" in error for error in errors))

    def test_strict_report_quality_rejects_missing_evidence_in_bug_fix_batch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_root = Path(tmpdir) / "reports/customer/example-project"
            filename = "bug-audit-2026-08-15.md"
            write_file(
                report_root / filename,
                "\n".join(
                    [
                        "Report type: `bug-audit`",
                        "Validation basis: static bug discovery.",
                        "## Bug Candidates",
                        "| # | Candidate | Evidence strength | Reproduction status |",
                        "|---|---|---|---|",
                        "| 1 | Config contradiction. | static config contradiction | `NOT_REPRODUCED` |",
                        "## Immediate Bug-Fix Batch",
                        "| # | Severity | Candidate | Evidence |",
                        "|---|---|---|---|",
                        "| 1 | HIGH | Missing evidence for runtime tests. | missing evidence |",
                    ]
                ),
            )

            errors = validator.validate_report_quality(report_root, filename, "bug-audit")

            self.assertTrue(any("Immediate Bug-Fix Batch" in error for error in errors))

    def test_strict_report_quality_accepts_after_freeze_comparison_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_root = Path(tmpdir) / "reports/customer/example-project"
            filename = "project-readiness-2026-08-15.md"
            write_file(
                report_root / filename,
                "\n".join(
                    [
                        "Report type: `project-readiness`",
                        "Validation basis: frozen primary-evidence audit.",
                        clean_comparison_section(),
                    ]
                ),
            )

            errors = validator.validate_report_quality(report_root, filename, "project-readiness")

            self.assertEqual([], errors)

    def test_strict_report_quality_rejects_comparison_without_freeze_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_root = Path(tmpdir) / "reports/customer/example-project"
            filename = "project-readiness-2026-08-15.md"
            write_file(
                report_root / filename,
                "\n".join(
                    [
                        "Report type: `project-readiness`",
                        "Validation basis: frozen primary-evidence audit.",
                        "## Previous Report Comparison",
                        "",
                        "- Current audit freeze artifact: current-report.md",
                        "- Previous report artifact(s): previous-report.md",
                        "",
                        "| Area | Current audit | Previous report | Better | Worse | Unchanged | Evidence | Interpretation |",
                        "|---|---|---|---|---|---|---|---|",
                        "| Verdict | HOLD | HOLD |  |  | yes | files | Same verdict. |",
                    ]
                ),
            )

            errors = validator.validate_report_quality(report_root, filename, "project-readiness")

            self.assertTrue(any("after-freeze note" in error for error in errors))

    def test_strict_report_quality_rejects_comparison_without_delta_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_root = Path(tmpdir) / "reports/customer/example-project"
            filename = "project-readiness-2026-08-15.md"
            write_file(
                report_root / filename,
                "\n".join(
                    [
                        "Report type: `project-readiness`",
                        "Validation basis: frozen primary-evidence audit.",
                        "## Previous Report Comparison",
                        "",
                        "- Old reports opened only after current audit freeze: yes",
                        "- Current audit freeze artifact: current-report.md",
                        "- Previous report artifact(s): previous-report.md",
                        "",
                        "| Criterion | Current audit | Previous report | Interpretation |",
                        "|---|---|---|---|",
                        "| Verdict | HOLD | HOLD | Same verdict. |",
                    ]
                ),
            )

            errors = validator.validate_report_quality(report_root, filename, "project-readiness")

            self.assertTrue(any("comparison table missing columns" in error for error in errors))

    def test_quality_summary_groups_repeated_customer_failure_modes(self) -> None:
        errors = [
            "customer report quality alpha/index.md has vague command entry: `find target files`",
            "customer report quality alpha/code-only-project-readiness-2026-08-15.md "
            "has vague command entry: `sed README/tests`",
            "customer report quality alpha/bug-audit-2026-08-15.md missing Validation basis",
            "customer report quality beta/bug-audit-2026-08-15.md puts NO_BUG_PROVEN in Bug Candidates",
        ]

        summary = validator.summarize_quality_failures(errors)

        self.assertIn("QUALITY SUMMARY:", summary)
        self.assertTrue(any(line.startswith("- VAGUE_COMMAND_ENTRY: 2") for line in summary))
        self.assertTrue(any(line.startswith("- MISSING_VALIDATION_BASIS: 1") for line in summary))
        self.assertTrue(any(line.startswith("- NO_BUG_PROVEN_AS_CANDIDATE: 1") for line in summary))

    def test_quality_summary_reports_no_customer_failures(self) -> None:
        summary = validator.summarize_quality_failures([])

        self.assertEqual(["QUALITY SUMMARY: no customer report-pack failures"], summary)


if __name__ == "__main__":
    unittest.main()
