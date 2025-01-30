#!/bin/bash

PYLOG_LEVEL=INFO NOFILE=1 poetry run several_modes \
    --insert-conditions-mode=llm-single-step \
    --llm-profile=openai-o1 \
    --bench-type validating \
    --skip-failed \
    --tries 10 \
    --runs 5 \
    --verifier-command="verus --multiple-errors 15" \
    --filter-by-ext rs \
    --output-logging \
    --dir benches/HumanEval-RustBench \
    --modes mode4 \
    --prompts-directory prompts/humaneval-verus-without-impls-few-shot-text-description
