#!/usr/bin/env python3
"""Static validation for the local project-readiness-auditor agent pack."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_AGENT_PACK_FILES = {
    "AGENTS.md": [
        "Project: project-readiness-auditor",
        "Mission",
        "Working Rules",
        "Evidence Rules",
        "Forbidden Changes",
        "Validation",
        "agents/context_router.md",
        "agents/project_readiness_auditor.md",
        "agents/contract_risk_reviewer.md",
        "agents/validation_reviewer.md",
        "agents/task_spec_short.md",
        "PASS",
        "PASS_WITH_RISKS",
        "RETEST",
        "HOLD",
        "BLOCK",
    ],
    "agents/context_router.md": [
        "Goal:",
        "Inputs",
        "Task Modes",
        "Mandatory Bug Discovery",
        "Routing",
        "Report Pack Routing",
        "Files To Avoid By Default",
        "agents/project_readiness_auditor.md",
        "agents/contract_risk_reviewer.md",
        "agents/validation_reviewer.md",
        "agents/task_spec_short.md",
        "none by default",
        "as triggered",
    ],
    "agents/project_readiness_auditor.md": [
        "Goal:",
        "When To Use",
        "Inspect First",
        "Prior Reports Rule",
        "Project Map Checklist",
        "Audit Checklist",
        "Mandatory Bug Discovery",
        "Findings Format",
        "Stop Rules",
        "Output",
    ],
    "agents/contract_risk_reviewer.md": [
        "Goal:",
        "When To Use",
        "Inspect First",
        "Checklist",
        "Verdicts",
        "Output",
        "PASS",
        "PASS_WITH_RISKS",
        "RETEST",
        "HOLD",
        "BLOCK",
    ],
    "agents/validation_reviewer.md": [
        "Goal:",
        "Evidence Levels",
        "Checklist",
        "Verdicts",
        "Report",
        "L0",
        "L1",
        "L2",
        "L3",
        "L4",
        "L5",
        "PASS",
        "PASS_WITH_RISKS",
        "RETEST",
        "HOLD",
        "BLOCK",
    ],
    "agents/task_spec_short.md": [
        "Goal:",
        "Audit mode:",
        "Non-goals:",
        "Target repository:",
        "Commands allowed:",
        "Commands forbidden:",
        "Mandatory bug discovery scope:",
        "Primary agent:",
        "Optional reviewer:",
        "Validation target:",
        "Acceptance criteria:",
        "Stop conditions:",
        "Completion Report",
    ],
}

EXPECTED_AGENT_FILES = {
    "context_router.md",
    "project_readiness_auditor.md",
    "contract_risk_reviewer.md",
    "validation_reviewer.md",
    "task_spec_short.md",
}

LOCAL_AUTHORING_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    ".claude",
    ".agents",
    ".codex",
]

LOCAL_AUTHORING_IGNORE_TERMS = [
    "/AGENTS.md",
    "/CLAUDE.md",
    "/.claude/",
    "/.agents/",
    "/.codex/",
    "/agents/",
]

SKILL_PACKAGE_LOCAL_TERMS = [
    "Root workspace files such as `AGENTS.md`, `CLAUDE.md`, `.claude/`, and root `agents/` are local authoring aids",
    "Do not depend on them for installed-skill behavior",
]

SKILL_PACKAGE_FILES = [
    "SKILL.md",
    "VERSION",
    "agents/openai.yaml",
    "references/audit-methodology.md",
    "references/prior-report-freeze-validation-scenario.md",
    "references/readiness-rubric.md",
    "references/report-template.md",
    "scripts/validate_skill.py",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for relative, terms in REQUIRED_AGENT_PACK_FILES.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required agent-pack file: {relative}")
            continue
        text = read_text(path)
        for term in terms:
            if term not in text:
                errors.append(f"{relative} missing required term: {term}")
    return errors


def validate_agent_inventory(root: Path) -> list[str]:
    agents_dir = root / "agents"
    if not agents_dir.is_dir():
        return ["missing required agent directory: agents"]

    actual_files = {path.name for path in agents_dir.iterdir() if path.is_file()}
    missing_files = sorted(EXPECTED_AGENT_FILES - actual_files)
    extra_files = sorted(actual_files - EXPECTED_AGENT_FILES)

    errors = []
    for filename in missing_files:
        errors.append(f"missing required agent file: agents/{filename}")
    for filename in extra_files:
        errors.append(f"unexpected agent file without routing validation: agents/{filename}")
    return errors


def validate_skill_boundary(root: Path) -> list[str]:
    errors: list[str] = []
    skill_root = root / "project-readiness-auditor"
    if not skill_root.is_dir():
        return ["missing installable skill package: project-readiness-auditor"]

    for relative in SKILL_PACKAGE_FILES:
        if not (skill_root / relative).is_file():
            errors.append(f"installable skill missing required file: {relative}")

    for relative in LOCAL_AUTHORING_PATHS:
        if (skill_root / relative).exists():
            errors.append(f"local authoring path must not be inside installable skill: {relative}")

    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        errors.append("installable skill missing SKILL.md")
    else:
        text = read_text(skill_md)
        for term in SKILL_PACKAGE_LOCAL_TERMS:
            if term not in text:
                errors.append(f"project-readiness-auditor/SKILL.md missing package boundary term: {term}")

    return errors


def validate_gitignore(root: Path) -> list[str]:
    gitignore = root / ".gitignore"
    if not gitignore.is_file():
        return ["missing .gitignore"]

    text = read_text(gitignore)
    return [
        f".gitignore missing local authoring ignore term: {term}"
        for term in LOCAL_AUTHORING_IGNORE_TERMS
        if term not in text
    ]


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_required_files(root))
    errors.extend(validate_agent_inventory(root))
    errors.extend(validate_skill_boundary(root))
    errors.extend(validate_gitignore(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the local project-readiness-auditor agent pack.")
    parser.add_argument("path", nargs="?", default=".", help="Repository root to validate.")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: agent-pack path is not a directory: {root}")
        print("RESULT: FAIL L0")
        return 2

    try:
        errors = validate(root)
    except UnicodeDecodeError as exc:
        print(f"ERROR: invalid UTF-8: {exc}")
        print("RESULT: FAIL L0")
        return 2
    except OSError as exc:
        print(f"ERROR: could not read agent pack: {exc}")
        print("RESULT: FAIL L0")
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print("RESULT: FAIL L0")
        return 1

    print("RESULT: PASS L2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
