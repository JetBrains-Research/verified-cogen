# Automation tool for verifying code using LLMs

Example usage:

```sh
export GRAZIE_JWT_TOKEN=insert grazie token
poetry run verified-cogen --insert-conditions-mode=llm --llm-profile=gpt-4-1106-preview --prompts-directory=prompts/rust_invariants -i RustBench/ground_truth/binary_search.rs
```

or

```sh
export GRAZIE_JWT_TOKEN=insert grazie token
poetry run verified-cogen --insert-conditions-mode=llm --llm-profile=gpt-4-1106-preview --prompts-directory=prompts/dafny_invariants -i DafnyBench/hints_removed/630-dafny_tmp_tmpz2kokaiq_Solution_no_hints.dfy
```

To run the gui, run it directly from the verified-cogen directory or install the cli using poetry:

```sh
poetry install
```

Add `.venv/bin` to your PATH and use `verified-cogen` freely.

```sh
cargo run --manifest-path=gui/Cargo.toml
```

![Screenshot of GUI](screenshots/gui.png)

Available insertion modes:

- regex - insert invariants manually after the loop, only works if the program has exactly one `while` loop, works only for dafny
- llm - use LLM to insert invariants into the correct place, as a separate step from producing them
- llm-single-step - use LLM to add invariants to rewrite the program to include invariants, as a singlestep

Profiles are from grazie, useful ones:

- gpt-4-1106-preview - GPT4-Turbo
- gpt-4o - GPT-4o
- anthropic-claude-3-opus - Claude 3 Opus
