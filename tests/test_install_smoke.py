from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_SMOKE = REPO_ROOT / "project-readiness-auditor" / "scripts" / "install_smoke.py"


class InstallSmokeTests(unittest.TestCase):
    def test_install_smoke_passes_from_live_repository(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(INSTALL_SMOKE), str(REPO_ROOT)],
            text=True,
            capture_output=True,
        )

        self.assertEqual(
            0,
            completed.returncode,
            completed.stdout + completed.stderr,
        )
        self.assertIn("RESULT: PASS install-smoke", completed.stdout)


if __name__ == "__main__":
    unittest.main()
