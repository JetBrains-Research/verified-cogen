#!/bin/bash

vcmd=${1:-"dafny verify --allow-warnings --verification-time-limit 10"}
prompts_dir=${2:-"prompts/humaneval-dafny"}
dir=${3:-"benches/HumanEval-Dafny"}
ext=${4:-"dfy"}

PYLOG_LEVEL=INFO NOFILE=1 poetry run incremental_run \
    --grazie-token=$GRAZIE_JWT_TOKEN \
    --llm-profile="anthropic-claude-3.5-sonnet" \
    --insert-conditions-mode=llm-single-step \
    --tries 10 \
    --verifier-command="$vcmd" \
    --prompts-directory="$prompts_dir" \
    --dir="$dir" \
    --filter-by-ext="$ext"
