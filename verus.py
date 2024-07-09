import subprocess


class Verus:
    def __init__(self, shell, verus_path):
        self.shell = shell
        self.verus_path = verus_path

    def verify(self, file_path) -> tuple[bool, str, str]:
        res = subprocess.run(
            f"{self.shell} -i -l -c \"{self.verus_path} {file_path} --multiple-errors 10\"; exit",
            capture_output=True, shell=True
        )
        return res.returncode == 0, res.stdout.decode("utf-8"), res.stderr.decode("utf-8")
