#!/usr/bin/env python3
"""Install-smoke for the project-readiness-auditor skill package.

The smoke simulates the documented manual Codex install path in a clean
temporary skills directory, then runs the validator from the installed copy.
It also copies the public customer examples needed by the installed validator,
so the installed package proves more than scaffold shape.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PUBLIC_CUSTOMER_REPORT_PACKS = (
    "recommender-systems-from-zero",
    "hiking-route-recommender-demo",
    "mt5-research",
)


def copytree_clean(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if completed.returncode != 0:
        print(completed.stdout, end="")
        print(completed.stderr, end="", file=sys.stderr)
    return completed


def assert_no_generated_files(path: Path) -> list[str]:
    bad: list[str] = []
    for item in path.rglob("*"):
        if item.name == "__pycache__" or item.name == ".DS_Store" or item.suffix == ".pyc":
            bad.append(str(item.relative_to(path)))
    return bad


def install_smoke(repo_root: Path, keep_tmp: bool = False) -> int:
    skill_source = repo_root / "project-readiness-auditor"
    if not skill_source.is_dir():
        print(f"ERROR: missing skill package: {skill_source}")
        print("RESULT: FAIL install-smoke")
        return 2

    tmp_context = tempfile.TemporaryDirectory(prefix="pra-install-smoke.")
    tmp_path = Path(tmp_context.name)
    try:
        install_root = tmp_path / "codex-skills"
        installed_skill = install_root / "project-readiness-auditor"
        reports_root = install_root / "reports" / "customer"

        install_root.mkdir(parents=True)
        copytree_clean(skill_source, installed_skill)
        shutil.copy2(repo_root / "VERSION", install_root / "VERSION")

        for report_pack in PUBLIC_CUSTOMER_REPORT_PACKS:
            source = repo_root / "reports" / "customer" / report_pack
            if not source.is_dir():
                print(f"ERROR: missing public report example: {source}")
                print("RESULT: FAIL install-smoke")
                return 1
            copytree_clean(source, reports_root / report_pack)

        generated = assert_no_generated_files(installed_skill)
        if generated:
            for item in generated:
                print(f"ERROR: generated file in installed skill: {item}")
            print("RESULT: FAIL install-smoke")
            return 1

        validator = installed_skill / "scripts" / "validate_skill.py"
        checks = [
            [sys.executable, str(validator), str(installed_skill)],
            [
                sys.executable,
                str(validator),
                str(installed_skill),
                "--strict-report-quality",
                "--public-report-examples",
                "--report-quality-summary",
            ],
        ]
        for command in checks:
            completed = run(command, cwd=install_root)
            print(completed.stdout, end="")
            if completed.returncode != 0:
                print("RESULT: FAIL install-smoke")
                return completed.returncode

        print(f"INSTALL_ROOT: {install_root}")
        print("RESULT: PASS install-smoke")
        return 0
    finally:
        if keep_tmp:
            print(f"KEPT_TMP: {tmp_path}")
        else:
            tmp_context.cleanup()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run install-smoke for project-readiness-auditor.")
    parser.add_argument("repo_root", nargs="?", default=".", help="Repository root to smoke-test.")
    parser.add_argument("--keep-tmp", action="store_true", help="Keep the temporary install directory.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.is_dir():
        print(f"ERROR: repository root is not a directory: {repo_root}")
        print("RESULT: FAIL install-smoke")
        return 2
    return install_smoke(repo_root, keep_tmp=args.keep_tmp)


if __name__ == "__main__":
    raise SystemExit(main())
