import logging
import os
import signal
import subprocess
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


class Verifier:
    def __init__(self, shell: str, verifier_cmd: str, timeout: int = 60):
        self.shell = shell
        self.verifier_cmd = verifier_cmd
        self.timeout = timeout

    def verify(self, file_path: Path) -> Optional[tuple[bool, str, str]]:
        proc = subprocess.Popen(
            [self.shell, "-i", "-l", "-c", f'{self.verifier_cmd} "{file_path}"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            out, err = proc.communicate(timeout=self.timeout)
            return proc.returncode == 0, out.decode(), err.decode()
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
