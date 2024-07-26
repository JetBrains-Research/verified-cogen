from pathlib import Path
import subprocess
from typing import Optional
import logging


log = logging.getLogger(__name__)


class Verifier:
    def __init__(self, shell: str, verifier_cmd: str, timeout: int = 60):
        self.shell = shell
        self.verifier_cmd = verifier_cmd
        self.timeout = timeout

    def verify(self, file_path: Path) -> Optional[tuple[bool, str, str]]:
        try:
            res = subprocess.run(
                '{} -i -l -c "{} "{}""; exit'.format(
                    self.shell, self.verifier_cmd, file_path
                ),
                capture_output=True,
                shell=True,
                timeout=self.timeout,
            )
        except subprocess.TimeoutExpired:
            return None
        return (
            res.returncode == 0,
            res.stdout.decode("utf-8"),
            res.stderr.decode("utf-8"),
        )
