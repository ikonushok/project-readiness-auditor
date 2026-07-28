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
    "references/readiness-rubric.md",
    "references/report-template.md",
]

REQUIRED_TERMS = {
    "SKILL.md": [
        "Project Readiness Auditor",
        "Default Workflow",
        "references/audit-methodology.md",
        "references/readiness-rubric.md",
        "references/report-template.md",
        "L0-L5",
        "prioritized closure plan",
    ],
    "references/audit-methodology.md": [
        "Evidence Rules",
        "Timebox Profiles",
        "Fix The Audit Mode",
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
        "Validation Levels",
    ],
    "references/report-template.md": [
        "Summary",
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
