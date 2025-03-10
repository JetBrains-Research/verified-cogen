import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


class Verifier:
    def __init__(self, verifier_cmd: str, test_cmd: str = None, timeout: int = 60):
        self.verifier_cmd = verifier_cmd
        self.test_cmd = test_cmd
        self.timeout = timeout

    def verify(self, file_path: Path) -> Optional[tuple[bool, str, str]]:
        try:
            res = subprocess.run(
                '{} "{}"'.format(self.verifier_cmd, file_path),
                capture_output=True,
                shell=True,
                timeout=self.timeout,
            )
        except subprocess.TimeoutExpired:
            os.system("killall z3")
            return None
        return (
            res.returncode == 0,
            res.stdout.decode("utf-8"),
            res.stderr.decode("utf-8"),
        )

    def test(self, file_path: Path) -> Optional[tuple[bool, str, str]]:
        try:
            res = subprocess.run(
                '{} "{}"'.format(self.test_cmd, file_path),
                capture_output=True,
                shell=True,
                timeout=self.timeout,
            )
        except subprocess.TimeoutExpired:
            return False, "", "Timed out"
        ret = (
            res.returncode == 0,
            res.stdout.decode("utf-8"),
            res.stderr.decode("utf-8"),
        )
        return ret
