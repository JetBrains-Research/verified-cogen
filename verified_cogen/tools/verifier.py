import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


class Verifier:
    def __init__(self, verifier_cmd: str, timeout: int = 60):
        self.verifier_cmd = verifier_cmd
        self.timeout = timeout

    def verify(self, file_path: Path) -> Optional[tuple[bool, str, str]]:
        process = subprocess.Popen(
            '{} "{}"'.format(self.verifier_cmd, file_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=self.timeout)
            res = subprocess.CompletedProcess(
                args=process.args,
                returncode=process.returncode,
                stdout=stdout,
                stderr=stderr,
            )
        except subprocess.TimeoutExpired:
            os.system(f"pkill -9 -P {process.pid}")
            return None
        return (
            res.returncode == 0,
            res.stdout.decode("utf-8"),
            res.stderr.decode("utf-8"),
        )
