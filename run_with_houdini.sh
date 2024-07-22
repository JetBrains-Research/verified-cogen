#!/bin/bash

source .venv/bin/activate
source .envrc

export PYTHONPATH=PYTHONPATH:"$(pwd)/src"

PYLOG_LEVEL=DEBUG NOFILE=1 python src/experiments/use_houdini.py \
    --grazie-token=$GRAZIE_TOKEN \
    --profile=gpt-4o \
    --prompt-dir=prompts/rust_invariants \
    --verifier-command="verus --multiple-errors=100" \
    --program=$1
