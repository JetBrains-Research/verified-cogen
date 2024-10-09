def dafny_separate(errors: str) -> tuple[str, str]:
    """
    Separate verifier errors from the rest of the errors.
    """
    lines = errors.split("\n")
    lines = [line for line in lines if "Dafny program verifier finished" not in line]
    line_with_ret0 = next((i for i, line in enumerate(lines) if "ret0" in line), None)
    if line_with_ret0 is None:
        return "\n".join(lines), ""
    else:
        non_verifier_errors = "\n".join(lines[: line_with_ret0 - 2]).strip()
        verifier_errors = "\n".join(lines[line_with_ret0 - 2 :]).strip()
        return non_verifier_errors, verifier_errors
