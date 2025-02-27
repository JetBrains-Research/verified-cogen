import logging
import os
import subprocess
from pathlib import Path
from sys import platform
from typing import Optional

log = logging.getLogger(__name__)


def cleanup_z3_processes(timeout: int = 60):
    if platform.startswith("linux"):
        command: str = (
            f"ps -eo pid,etimes,comm | awk '$2 > {timeout + 10} && $3 ~ /z3/" + " {print $1}' | xargs -r kill -9"
        )
        os.system(command)


class Verifier:
    def __init__(self, verifier_cmd: str, timeout: int = 60):
        self.verifier_cmd = verifier_cmd
        self.timeout = timeout

    def verify(self, file_path: Path) -> Optional[tuple[bool, str, str]]:
        process = subprocess.Popen(
            f'{self.verifier_cmd} "{file_path}"',
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
            cleanup_z3_processes(self.timeout)

            return (
                res.returncode == 0,
                res.stdout.decode("utf-8"),
                res.stderr.decode("utf-8"),
            )
        except subprocess.TimeoutExpired:
            cleanup_z3_processes(self.timeout)
            return None
