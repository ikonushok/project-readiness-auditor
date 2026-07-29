#!/usr/bin/env python3
"""Static validation for the project-readiness-auditor skill package."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
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
PUBLIC_CUSTOMER_REPORT_PACKS = (
    "recommender-systems-from-zero",
    "hiking-route-recommender-demo",
    "mt5-research",
)
DATE_RE = r"\d{4}-\d{2}-\d{2}"
QUALITY_REPORT_TYPES = {
    "code-only-project-readiness",
    "project-readiness",
    "bug-audit",
}
APPROVED_EVIDENCE_STRENGTHS = {
    "direct code contradiction",
    "static config contradiction",
    "framework/runtime candidate",
    "product/api gap",
    "reproduced",
}
VAGUE_COMMAND_PATTERNS = [
    re.compile(r"\btarget files\b", re.IGNORECASE),
    re.compile(r"\bmarkers?\b", re.IGNORECASE),
    re.compile(r"\bfiles?\s*$", re.IGNORECASE),
    re.compile(r"^sed\s+[\w/.-]+$", re.IGNORECASE),
]
SHELL_COMMAND_PREFIXES = {
    "./",
    "bash",
    "cat",
    "curl",
    "docker",
    "find",
    "git",
    "grep",
    "head",
    "ls",
    "make",
    "node",
    "npm",
    "pnpm",
    "pytest",
    "python",
    "python3",
    "rg",
    "sed",
    "tail",
    "uvicorn",
    "wc",
    "zsh",
}
COMMAND_SECTION_STOP_PREFIXES = (
    "- command outcomes:",
    "- claims not verified:",
    "- residual risk:",
    "- missing evidence:",
    "- inspection notes:",
)
COMPARISON_REQUIRED_COLUMNS = {
    "area",
    "current audit",
    "previous report",
    "better",
    "worse",
    "unchanged",
    "evidence",
    "interpretation",
}
QUALITY_FAILURE_MODE_DESCRIPTIONS = {
    "PACK_STRUCTURE": "Report pack is missing a required report file or required section.",
    "MISSING_VALIDATION_BASIS": "Report does not say what evidence level and inspection basis support its claims.",
    "VAGUE_COMMAND_ENTRY": "Commands Run contains shorthand instead of exact shell commands.",
    "NO_BUG_PROVEN_AS_CANDIDATE": "Bug audit lists NO_BUG_PROVEN as if it were a bug candidate.",
    "MISSING_EVIDENCE_AS_BUG_CANDIDATE": "Bug audit treats missing evidence as a bug candidate.",
    "UNSUPPORTED_EVIDENCE_STRENGTH": "Bug candidate uses an evidence-strength label outside the approved rubric.",
    "NON_BUG_IN_FIX_BATCH": "Immediate Bug-Fix Batch mixes evidence status or no-bug status into bug-fix work.",
    "COMPARISON_AFTER_FREEZE_NOTE": "Previous-report comparison does not state that old reports were opened after freeze.",
    "COMPARISON_CURRENT_FREEZE_ARTIFACT": "Previous-report comparison does not name the frozen current audit artifact.",
    "COMPARISON_PREVIOUS_ARTIFACT": "Previous-report comparison does not name the previous report artifact.",
    "COMPARISON_TABLE_MISSING": "Previous-report comparison section has no comparison table.",
    "COMPARISON_DELTA_COLUMNS": "Previous-report comparison table lacks Better/Worse/Unchanged/Evidence columns.",
    "UNCLASSIFIED": "Validator emitted an error that is not yet mapped to a product failure mode.",
}
QUALITY_FAILURE_MODE_PATTERNS = [
    ("PACK_STRUCTURE", re.compile(r"^customer report pack ")),
    ("MISSING_VALIDATION_BASIS", re.compile(r" missing Validation basis$")),
    ("VAGUE_COMMAND_ENTRY", re.compile(r" has vague command entry: ")),
    ("NO_BUG_PROVEN_AS_CANDIDATE", re.compile(r" puts NO_BUG_PROVEN in Bug Candidates$")),
    ("MISSING_EVIDENCE_AS_BUG_CANDIDATE", re.compile(r" treats missing evidence as bug candidate$")),
    ("UNSUPPORTED_EVIDENCE_STRENGTH", re.compile(r" has unsupported evidence strength: ")),
    ("NON_BUG_IN_FIX_BATCH", re.compile(r" mixes non-bug evidence status into Immediate Bug-Fix Batch$")),
    ("COMPARISON_AFTER_FREEZE_NOTE", re.compile(r" comparison missing after-freeze note$")),
    ("COMPARISON_CURRENT_FREEZE_ARTIFACT", re.compile(r" comparison missing current freeze artifact$")),
    ("COMPARISON_PREVIOUS_ARTIFACT", re.compile(r" comparison missing previous report artifact$")),
    ("COMPARISON_TABLE_MISSING", re.compile(r" comparison missing table$")),
    ("COMPARISON_DELTA_COLUMNS", re.compile(r" comparison table missing columns: ")),
]
CUSTOMER_REPORT_REQUIREMENTS = [
    (
        "index",
        re.compile(r"^index\.md$"),
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
        ],
    ),
    (
        "code-only-project-readiness",
        re.compile(rf"^code-only-project-readiness-{DATE_RE}\.md$"),
        [
            "Audit mode: `code-only`",
            "Report type: `code-only-project-readiness`",
            "Code-Visible Tasks",
            "Mandatory Bug Discovery",
            "Findings",
            "Evidence Log",
        ],
    ),
    (
        "project-readiness",
        re.compile(rf"^project-readiness-{DATE_RE}\.md$"),
        [
            "Audit mode: `docs-vs-code`",
            "Report type: `project-readiness`",
            "Product Maturity",
            "Mandatory Bug Discovery",
            "Readiness By Capability",
            "Evidence Log",
        ],
    ),
    (
        "bug-audit",
        re.compile(rf"^bug-audit-{DATE_RE}\.md$"),
        [
            "Report type: `bug-audit`",
            "Bug Candidates",
            "Immediate Bug-Fix Batch",
            "Reproduction Approval Gate",
            "Fix Approval Gate",
            "Evidence Log",
        ],
    ),
]
METHODOLOGY_REGRESSION_RULES = {
    "prior report isolation": {
        "SKILL.md": [
            "previous audit reports",
            "complete and freeze the new audit",
            "comparison artifacts",
        ],
        "references/audit-methodology.md": [
            "Do not open previous audit reports during discovery",
            "Generate the current audit from primary evidence",
            "Freeze the current audit",
            "Read previous reports only after the freeze",
            "same target commit with no real product progress",
            "roadmap documentation vs implemented code",
            "test surface grew but validation level did not increase",
        ],
        "references/report-template.md": [
            "Previous audit reports are excluded context",
            "Previous reports are comparison artifacts",
            "Old reports opened only after current audit freeze",
            "Better",
            "Worse",
            "Unchanged",
        ],
    },
    "mandatory bug discovery": {
        "SKILL.md": [
            "Run Mandatory Bug Discovery immediately for every audit",
            "Do not skip Mandatory Bug Discovery",
            "NO_BUG_PROVEN",
        ],
        "references/audit-methodology.md": [
            "Run this phase in every audit",
            "Reproduction Approval Gate",
            "Fix Approval Gate",
            "Do not label a framework/runtime candidate as proven",
        ],
        "references/report-template.md": [
            "Every audit report must include Mandatory Bug Discovery",
            "If no candidate survives ranking, set status to `NO_BUG_PROVEN`",
        ],
    },
    "readiness evidence guard": {
        "SKILL.md": [
            "Do not claim runtime validation unless commands were actually run and inspected",
            "Do not claim production readiness without deployment, security, observability, reproducibility, and rollback evidence",
        ],
        "references/audit-methodology.md": [
            "Runtime claims require commands that were actually run and inspected",
            "Production-readiness claims require reproducibility, deployment, operational, security, observability, and rollback evidence",
        ],
        "references/readiness-rubric.md": [
            "Production-ready requires reproducibility, deployment, migrations, security, observability, rollback, and critical tests",
        ],
    },
    "report pack separation": {
        "SKILL.md": [
            "audit each project separately",
            "Produce one report pack per project",
        ],
        "references/audit-methodology.md": [
            "one evidence log per target project",
            "one report pack per target project",
        ],
        "references/report-template.md": [
            "One target project per report file",
            "One evidence log per report file",
        ],
    },
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


def validate_methodology_regressions(root: Path) -> list[str]:
    errors: list[str] = []

    for rule_name, file_terms in METHODOLOGY_REGRESSION_RULES.items():
        for relative, terms in file_terms.items():
            path = root / relative
            if not path.is_file():
                continue
            text = read_text(path)
            for term in terms:
                if term not in text:
                    errors.append(f"methodology regression '{rule_name}' failed: {relative} missing {term}")

    return errors


def section_text(text: str, heading: str) -> str:
    lines = text.splitlines()
    collected: list[str] = []
    in_section = False
    marker = f"## {heading}".casefold()

    for line in lines:
        stripped = line.strip()
        if stripped.casefold() == marker:
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section:
            collected.append(line)

    return "\n".join(collected)


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def command_entries(text: str) -> list[str]:
    entries: list[str] = []
    in_commands = False

    for line in text.splitlines():
        stripped = line.strip()
        normalized = stripped.casefold()
        if normalized in {"## commands run", "- commands run:", "commands run:"}:
            in_commands = True
            continue
        if not in_commands:
            continue
        if stripped.startswith("## "):
            break
        if any(normalized.startswith(prefix) for prefix in COMMAND_SECTION_STOP_PREFIXES):
            break
        if stripped.startswith("- ") and stripped[2:].strip().endswith(":"):
            break
        if stripped.startswith("- "):
            entries.append(stripped[2:].strip())

    return entries


def is_exact_command_entry(entry: str) -> bool:
    normalized = entry.strip().strip("`").strip()
    if normalized.casefold() in {"none", "no commands run", "no shell commands were run"}:
        return True
    if not (entry.startswith("`") and entry.endswith("`")):
        return False
    if any(pattern.search(normalized) for pattern in VAGUE_COMMAND_PATTERNS):
        return False

    first_token = normalized.split(maxsplit=1)[0]
    return first_token in SHELL_COMMAND_PREFIXES or first_token.startswith("./")


def validate_report_quality(report_dir: Path, filename: str, report_type: str) -> list[str]:
    errors: list[str] = []
    path = report_dir / filename
    text = read_text(path)
    display_path = f"{report_dir.name}/{filename}"

    if report_type in QUALITY_REPORT_TYPES and "Validation basis:" not in text:
        errors.append(f"customer report quality {display_path} missing Validation basis")

    for entry in command_entries(text):
        if not is_exact_command_entry(entry):
            errors.append(f"customer report quality {display_path} has vague command entry: {entry}")

    errors.extend(validate_comparison_quality(text, display_path))

    if report_type != "bug-audit":
        return errors

    bug_section = section_text(text, "Bug Candidates")
    if "NO_BUG_PROVEN" in bug_section:
        errors.append(f"customer report quality {display_path} puts NO_BUG_PROVEN in Bug Candidates")

    rows = table_rows(bug_section)
    if rows:
        header = [cell.casefold() for cell in rows[0]]
        strength_index = header.index("evidence strength") if "evidence strength" in header else None
        for row in rows[1:]:
            row_text = " | ".join(row).casefold()
            if "missing evidence" in row_text:
                errors.append(f"customer report quality {display_path} treats missing evidence as bug candidate")
            if strength_index is not None and strength_index < len(row):
                strength = row[strength_index].casefold()
                if strength and strength not in APPROVED_EVIDENCE_STRENGTHS:
                    errors.append(
                        f"customer report quality {display_path} has unsupported evidence strength: {row[strength_index]}"
                    )

    immediate_section = section_text(text, "Immediate Bug-Fix Batch")
    for row in table_rows(immediate_section)[1:]:
        row_text = " | ".join(row).casefold()
        if "missing evidence" in row_text or "no_bug_proven" in row_text:
            errors.append(
                f"customer report quality {display_path} mixes non-bug evidence status into Immediate Bug-Fix Batch"
            )

    return errors


def validate_comparison_quality(text: str, display_path: str) -> list[str]:
    errors: list[str] = []
    comparison_section = section_text(text, "Previous Report Comparison")
    if not comparison_section:
        return errors

    if "Old reports opened only after current audit freeze:" not in comparison_section:
        errors.append(f"customer report quality {display_path} comparison missing after-freeze note")
    if "Current audit freeze artifact:" not in comparison_section:
        errors.append(f"customer report quality {display_path} comparison missing current freeze artifact")
    if "Previous report artifact" not in comparison_section:
        errors.append(f"customer report quality {display_path} comparison missing previous report artifact")

    rows = table_rows(comparison_section)
    if not rows:
        errors.append(f"customer report quality {display_path} comparison missing table")
        return errors

    header = {cell.casefold() for cell in rows[0]}
    missing_columns = sorted(COMPARISON_REQUIRED_COLUMNS - header)
    if missing_columns:
        errors.append(
            f"customer report quality {display_path} comparison table missing columns: "
            + ", ".join(missing_columns)
        )

    return errors


def classify_quality_failure(error: str) -> str:
    for code, pattern in QUALITY_FAILURE_MODE_PATTERNS:
        if pattern.search(error):
            return code
    return "UNCLASSIFIED"


def error_subject(error: str) -> str:
    quality_match = re.search(r"customer report quality ([^ ]+)", error)
    if quality_match:
        return quality_match.group(1)
    pack_match = re.search(r"customer report pack ([^ ]+)", error)
    if pack_match:
        return pack_match.group(1)
    return error


def summarize_quality_failures(errors: list[str]) -> list[str]:
    relevant_errors = [
        error
        for error in errors
        if error.startswith("customer report quality ") or error.startswith("customer report pack ")
    ]
    if not relevant_errors:
        return ["QUALITY SUMMARY: no customer report-pack failures"]

    counts: Counter[str] = Counter()
    examples: defaultdict[str, list[str]] = defaultdict(list)
    for error in relevant_errors:
        code = classify_quality_failure(error)
        counts[code] += 1
        subject = error_subject(error)
        if subject not in examples[code]:
            examples[code].append(subject)

    lines = ["QUALITY SUMMARY:"]
    for code, count in counts.most_common():
        example_text = ", ".join(examples[code][:3])
        description = QUALITY_FAILURE_MODE_DESCRIPTIONS[code]
        lines.append(f"- {code}: {count} - {description} Examples: {example_text}")

    return lines


def validate_customer_report_pack(
    repo_root: Path,
    strict_quality: bool = False,
    report_pack: str | None = None,
    public_examples: bool = False,
) -> list[str]:
    errors: list[str] = []
    customer_root = repo_root / CUSTOMER_REPORTS_DIR
    if not customer_root.exists():
        return errors

    if report_pack is not None and public_examples:
        return ["--customer-report-pack and --public-report-examples cannot be used together"]

    if public_examples:
        report_dirs = [customer_root / report_pack for report_pack in PUBLIC_CUSTOMER_REPORT_PACKS]
        missing_packs = [path.name for path in report_dirs if not path.is_dir()]
        if missing_packs:
            return [f"public customer report pack missing: {pack}" for pack in missing_packs]
    elif report_pack is not None:
        report_dirs = [customer_root / report_pack]
        if not report_dirs[0].is_dir():
            return [f"customer report pack not found: {report_pack}"]
    else:
        report_dirs = sorted(path for path in customer_root.iterdir() if path.is_dir())

    for report_dir in report_dirs:
        filenames = [path.name for path in report_dir.iterdir() if path.is_file()]
        for report_type, pattern, terms in CUSTOMER_REPORT_REQUIREMENTS:
            matching_filenames = sorted(filename for filename in filenames if pattern.match(filename))
            if not matching_filenames:
                errors.append(
                    f"customer report pack {report_dir.name} missing required "
                    f"{report_type} file matching {pattern.pattern}"
                )
                continue
            for filename in matching_filenames:
                path = report_dir / filename
                text = read_text(path)
                for term in terms:
                    if term not in text:
                        errors.append(
                            f"customer report pack {report_dir.name}/{filename} missing required term: {term}"
                        )
                if strict_quality:
                    errors.extend(validate_report_quality(report_dir, filename, report_type))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the project-readiness-auditor skill package.")
    parser.add_argument("skill_path", help="Path to the project-readiness-auditor skill package")
    parser.add_argument(
        "--strict-report-quality",
        action="store_true",
        help="Also validate report quality failure modes under reports/customer.",
    )
    parser.add_argument(
        "--customer-report-pack",
        help="Limit reports/customer validation to one project slug.",
    )
    parser.add_argument(
        "--public-report-examples",
        action="store_true",
        help="Validate only the official public customer example report packs.",
    )
    parser.add_argument(
        "--report-quality-summary",
        action="store_true",
        help="Print grouped customer report-pack failure modes after validation.",
    )
    args = parser.parse_args()

    root = Path(args.skill_path).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: skill path is not a directory: {root}")
        print("RESULT: FAIL L0")
        return 2

    try:
        errors = validate(root)
        errors.extend(validate_methodology_regressions(root))
        repo_root = root.parent
        errors.extend(
            validate_customer_report_pack(
                repo_root,
                strict_quality=args.strict_report_quality,
                report_pack=args.customer_report_pack,
                public_examples=args.public_report_examples,
            )
        )
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
        if args.report_quality_summary:
            for line in summarize_quality_failures(errors):
                print(line)
        print("RESULT: FAIL L0")
        return 1

    if args.report_quality_summary:
        for line in summarize_quality_failures(errors):
            print(line)
    print("RESULT: PASS L0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
