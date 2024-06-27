# Automation tool for verifying dafny using LLM

Example usage:

```
export GRAZIE_TOKEN=insert grazie token
python main.py --insert-invariants-mode=llm --llm-profile=gpt-4-1106-preview -i DafnyBench/hints_removed/630-dafny_tmp_tmpz2kokaiq_Solution_no_hints.dfy
```

Available invariants insertion mode: 
- regex - insert invariants manually after the loop, only works if the program has exactly one `while` loop
- llm - use LLM to insert invariants into the correct place, as a separate step from producing them
- llm-single-step - use LLM to add invariants to rewrite the program to include invariants, as a singlestep
- dafnybench - as llm-singlestep, but using exactly the prompts from DafnyBench paper

Profiles are from grazie, useful ones:
- gpt-4-1106-preview - GPT4-Turbo
- gpt-4o - GPT-4o
- anthropic-claude-3-opus - Calude 3 Opus