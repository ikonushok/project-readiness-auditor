from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate_pack.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_pack", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class ValidatePackTests(unittest.TestCase):
    def test_live_agent_pack_passes_static_consistency_checks(self) -> None:
        self.assertEqual([], validator.validate(REPO_ROOT))

    def test_agent_pack_rejects_unrouted_extra_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temporary_root = Path(tmpdir)
            for relative in validator.REQUIRED_AGENT_PACK_FILES:
                source = REPO_ROOT / relative
                write_file(temporary_root / relative, source.read_text(encoding="utf-8"))
            write_file(temporary_root / ".gitignore", (REPO_ROOT / ".gitignore").read_text(encoding="utf-8"))
            write_file(
                temporary_root / "project-readiness-auditor/SKILL.md",
                (REPO_ROOT / "project-readiness-auditor/SKILL.md").read_text(encoding="utf-8"),
            )
            write_file(temporary_root / "agents/future_reviewer.md", "# Future Reviewer\n")

            errors = validator.validate(temporary_root)

        self.assertTrue(any("unexpected agent file" in error for error in errors))

    def test_agent_pack_rejects_local_authoring_files_inside_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temporary_root = Path(tmpdir)
            for relative in validator.REQUIRED_AGENT_PACK_FILES:
                source = REPO_ROOT / relative
                write_file(temporary_root / relative, source.read_text(encoding="utf-8"))
            write_file(temporary_root / ".gitignore", (REPO_ROOT / ".gitignore").read_text(encoding="utf-8"))
            write_file(
                temporary_root / "project-readiness-auditor/SKILL.md",
                (REPO_ROOT / "project-readiness-auditor/SKILL.md").read_text(encoding="utf-8"),
            )
            write_file(temporary_root / "project-readiness-auditor/AGENTS.md", "# Wrong place\n")

            errors = validator.validate(temporary_root)

        self.assertTrue(any("local authoring path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
