# %%
import os
from collections import Counter


def format_error(error):
    if "cannot find" in error:
        return "cannot find"
    if "type annotations needed for" in error:
        return "type annotations needed for"
    if "with mode spec" in error:
        return "cannot call with mode spec"
    if "`main` function not found" in error:
        return "`main` function not found"
    return error

def extract_errors_from_file(file_path):
    """Extract errors from a single file."""
    errors = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "error:" in line or line.startswith("error["):
                if "aborting" in lines[i].strip() or len(lines[i].strip()) >= 200:
                    continue
                errors.append(format_error(lines[i].strip()))
    return errors

def collect_errors(directory_path):
    """Collect errors from all files in a directory."""
    all_errors = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_errors.extend(extract_errors_from_file(file_path))
    return all_errors

# %%
directory_path = "verified_cogen/results/history_VerusProofSynthesisBench_0_mode1_0"
if not os.path.isdir(directory_path):
    print("Invalid directory path. Please try again.")
else:
    errors = collect_errors(directory_path)
    error_counts = Counter(errors)
    sorted_errors = error_counts.most_common()

    print("\nErrors sorted by frequency (decreasing):")
    for error, count in sorted_errors:
        print(f"{count} occurrences: {error}")
