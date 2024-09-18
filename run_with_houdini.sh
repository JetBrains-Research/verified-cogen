#!/bin/bash

source .venv/bin/activate
source .envrc

PYLOG_LEVEL=INFO NOFILE=1 poetry run python verified_cogen/experiments/use_houdini.py \
    --grazie-token=$GRAZIE_JWT_TOKEN \
    --profile="anthropic-claude-3.5-sonnet" \
    --prompt-dir=prompts/rust_invariants \
    --verifier-command="verus --multiple-errors=100" \
    --program=$1
