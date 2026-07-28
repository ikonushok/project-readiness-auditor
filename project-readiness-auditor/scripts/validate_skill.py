#!/usr/bin/env python3
"""Static validation for the project-readiness-auditor skill package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/audit-methodology.md",
    "references/prior-report-freeze-validation-scenario.md",
    "references/readiness-rubric.md",
    "references/report-template.md",
]

REQUIRED_TERMS = {
    "SKILL.md": [
        "Project Readiness Auditor",
        "Default Workflow",
        "one report pack per project",
        "code-only-project-readiness",
        "bug-audit",
        "Mandatory Bug Discovery",
        "Classify claim strength",
        "NO_BUG_PROVEN",
        "route ordering",
        "settings schema",
        "monitoring targets",
        "references/audit-methodology.md",
        "references/readiness-rubric.md",
        "references/report-template.md",
        "L0-L5",
        "executive narrative",
        "code-visible tasks",
        "product maturity",
        "top-3 immediate bug batch",
        "prioritized closure plan",
        "previous audit reports",
        "complete and freeze the new audit",
        "comparison artifacts",
    ],
    "references/audit-methodology.md": [
        "Evidence Rules",
        "Timebox Profiles",
        "Fix The Audit Mode",
        "Choose The Report Pack",
        "Compare Previous Reports Only After Freeze",
        "Claim Strength Rules",
        "framework/runtime candidate",
        "direct code contradiction",
        "static config contradiction",
        "settings schema",
        "monitoring targets",
        "previous audit reports",
        "freeze the new audit",
        "comparison artifacts",
        "one report pack per target project",
        "Mandatory Bug Discovery",
        "Reproduction Approval Gate",
        "Fix Approval Gate",
        "executive narrative",
        "code-visible tasks",
        "product maturity",
        "top-3 immediate bug-fix batch",
        "Build A Project Map",
        "Check Cross-Part Contracts",
        "Build The Closure Plan",
        "Report",
    ],
    "references/readiness-rubric.md": [
        "Readiness Stages",
        "Severity",
        "Evidence Strength",
        "Finding Confidence",
        "Bug Discovery Status",
        "NO_BUG_PROVEN",
        "Validation Levels",
    ],
    "references/prior-report-freeze-validation-scenario.md": [
        "Prior Report Freeze Validation Scenario",
        "Prevent prior-report leakage",
        "Do not open previous audit reports",
        "Complete and freeze the new audit report pack",
        "comparison artifacts",
        "false old-report finding",
        "Pass Conditions",
        "Fail Conditions",
    ],
    "references/report-template.md": [
        "Summary",
        "Report Pack Rules",
        "Report Pack Index",
        "Previous Report Comparison",
        "Previous reports are comparison artifacts",
        "Evidence strength",
        "framework/runtime candidate",
        "Settings schema vs env examples",
        "Monitoring targets vs deploy service names",
        "Target project",
        "Validation level / evidence level",
        "Code-Only Project Readiness",
        "Code-Visible Tasks",
        "Contract Reliability Security Checks",
        "Project Readiness",
        "Product Maturity",
        "Bug Audit",
        "Mandatory Bug Discovery",
        "Immediate Bug-Fix Batch",
        "Second Engineering Batch",
        "Backlog / Hardening Batch",
        "Reproduction Approval Gate",
        "Fix Approval Gate",
        "Project Map",
        "Findings",
        "Prioritized Closure Plan",
        "Evidence Log",
    ],
}

FORBIDDEN_PACKAGE_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    ".claude",
]

NAME_RE = re.compile(r"^name:\s*project-readiness-auditor\s*$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:\s*.+", re.MULTILINE)
CUSTOMER_REPORTS_DIR = Path("reports/customer")
CUSTOMER_REQUIRED_FILES = [
    "index.md",
    "code-only-project-readiness-2026-07-28.md",
    "project-readiness-2026-07-28.md",
    "bug-audit-2026-07-28.md",
]
CUSTOMER_REQUIRED_TERMS = {
    "index.md": [
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
    ],
    "code-only-project-readiness-2026-07-28.md": [
        "Audit mode: `code-only`",
        "Report type: `code-only-project-readiness`",
        "Code-Visible Tasks",
        "Mandatory Bug Discovery",
        "Findings",
        "Evidence Log",
    ],
    "project-readiness-2026-07-28.md": [
        "Audit mode: `docs-vs-code`",
        "Report type: `project-readiness`",
        "Product Maturity",
        "Mandatory Bug Discovery",
        "Readiness By Capability",
        "Evidence Log",
    ],
    "bug-audit-2026-07-28.md": [
        "Report type: `bug-audit`",
        "Bug Candidates",
        "Immediate Bug-Fix Batch",
        "Reproduction Approval Gate",
        "Fix Approval Gate",
        "Evidence Log",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")

    for relative in FORBIDDEN_PACKAGE_PATHS:
        if (root / relative).exists():
            errors.append(f"local workspace file must not be inside skill package: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = read_text(skill_path)
        if not skill_text.startswith("---\n"):
            errors.append("SKILL.md must start with YAML frontmatter")
        if not NAME_RE.search(skill_text):
            errors.append("SKILL.md frontmatter must name project-readiness-auditor")
        if not DESCRIPTION_RE.search(skill_text):
            errors.append("SKILL.md frontmatter must include description")

    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.is_file():
        text = read_text(openai_yaml)
        for term in [
            'display_name: "Project Readiness Auditor"',
            "short_description:",
            "default_prompt:",
            "allow_implicit_invocation: true",
        ]:
            if term not in text:
                errors.append(f"agents/openai.yaml missing {term}")

    for relative, terms in REQUIRED_TERMS.items():
        path = root / relative
        if not path.is_file():
            continue
        text = read_text(path)
        for term in terms:
            if term not in text:
                errors.append(f"{relative} missing required term: {term}")

    return errors


def validate_customer_report_pack(repo_root: Path) -> list[str]:
    errors: list[str] = []
    customer_root = repo_root / CUSTOMER_REPORTS_DIR
    if not customer_root.exists():
        return errors

    for report_dir in sorted(path for path in customer_root.iterdir() if path.is_dir()):
        for filename in CUSTOMER_REQUIRED_FILES:
            path = report_dir / filename
            if not path.is_file():
                errors.append(f"customer report pack {report_dir.name} missing required file: {filename}")
                continue
            text = read_text(path)
            for term in CUSTOMER_REQUIRED_TERMS.get(filename, []):
                if term not in text:
                    errors.append(f"customer report pack {report_dir.name}/{filename} missing required term: {term}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the project-readiness-auditor skill package.")
    parser.add_argument("skill_path", help="Path to the project-readiness-auditor skill package")
    args = parser.parse_args()

    root = Path(args.skill_path).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: skill path is not a directory: {root}")
        print("RESULT: FAIL L0")
        return 2

    try:
        errors = validate(root)
        repo_root = root.parent
        errors.extend(validate_customer_report_pack(repo_root))
    except UnicodeDecodeError as exc:
        print(f"ERROR: invalid UTF-8: {exc}")
        print("RESULT: FAIL L0")
        return 2
    except OSError as exc:
        print(f"ERROR: could not read skill package: {exc}")
        print("RESULT: FAIL L0")
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print("RESULT: FAIL L0")
        return 1

    print("RESULT: PASS L0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
