#!/bin/bash

source .venv/bin/activate

PYLOG_LEVEL=INFO NOFILE=1 incremental_run \
    --grazie-token=$GRAZIE_JWT_TOKEN \
    --llm-profile="anthropic-claude-3.5-sonnet" \
    --prompts-directory=prompts/humaneval-dafny \
    --verifier-command="dafny verify --allow-warnings --verification-time-limit 10" \
    --insert-conditions-mode=llm-single-step \
    --dir="Benches/HumanEval-Dafny"
