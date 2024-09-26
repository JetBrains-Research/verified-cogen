from sys import argv
from pathlib import Path

dafny_files = Path(
    "/Users/Stanislav.Alekseev/Projects/verified-cogen/benches/HumanEval-Dafny"
).glob("*.dfy")
dafny_files = [x.stem for x in dafny_files]
# print(dafny_files)

with open(argv[1]) as task_file:
    code = task_file.read()
    if "TODO" in code:
        exit(1)
    else:
        import re

        # Remove single-line comments
        code = re.sub(r"//.*", "", code)

        code = re.sub(r"^\s+\n", "", code, flags=re.MULTILINE)

        # Remove multi-line comments
        code = re.sub(r"/\*[\s\S]*?\*/", "", code, flags=re.MULTILINE)

        code = re.sub(r"^\s+", "", code)
        code = re.sub(r"\s+$", "", code)

        code += "\n"

        # Create 'processed' folder if it doesn't exist

        processed_dir = Path("processed")
        processed_dir.mkdir(exist_ok=True)

        number = Path(argv[1]).stem[-3:]
        print(number)
        result_name = None
        for file in dafny_files:
            if file.startswith(number):
                result_name = file

        assert result_name is not None
        # Save processed code to file in 'processed' folder
        output_file = processed_dir / f"{result_name}.rs"
        if not output_file.exists():
            output_file.write_text(code)
