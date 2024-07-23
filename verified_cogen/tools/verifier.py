from pathlib import Path
import subprocess


class Verifier:
    def __init__(self, shell: str, verifier_cmd: str):
        self.shell = shell
        self.verifier_cmd = verifier_cmd

    def verify(self, file_path: Path) -> tuple[bool, str, str]:
        res = subprocess.run(
            '{} -i -l -c "{} {}"; exit'.format(
                self.shell, self.verifier_cmd, file_path
            ),
            capture_output=True,
            shell=True,
        )
        return (
            res.returncode == 0,
            res.stdout.decode("utf-8"),
            res.stderr.decode("utf-8"),
        )
