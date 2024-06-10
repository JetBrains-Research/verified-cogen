import subprocess


class Dafny:

    def __init__(self, dafny_path):
        self.dafny_path = dafny_path

    def verify(self, file_path) -> (bool, str):
        res = subprocess.run([self.dafny_path, 'verify', file_path], capture_output=True)
        return res.returncode == 0, res.stdout.decode('utf-8')