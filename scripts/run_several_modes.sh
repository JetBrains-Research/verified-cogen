#!/bin/bash

vcmd=${1:-"dafny verify --allow-warnings --verification-time-limit 10"}
prompts_dir=${2:-"prompts/humaneval-dafny"}
dir=${3:-"benches/HumanEval-Dafny"}
ext=${4:-"dfy"}

PYLOG_LEVEL=INFO NOFILE=1 poetry run verified-cogen \
    --insert-conditions-mode=llm-single-step \
    --llm-profile=anthropic-claude-3.5-sonnet \
    --bench-types=validating,validating,validating,validating,validating,validating \
    --tries 10 \
    --runs 5 \
    --verifier-command="dafny verify --verification-time-limit 20" \
    --filter-by-ext dfy \
    --output-logging \
    --dir benches/HumanEval-Dafny \
    --modes=mode1,mode2,mode3,mode4,mode5,mode6 \
    --prompts-directory="prompts/dafny_eval","prompts/dafny_eval","prompts/dafny_eval_comment_without_impls","prompts/dafny_eval_comment_without_impls_textd","prompts/dafny_eval_comment_without_impls_textd","prompts/dafny_eval_comment_without_impls_textd"
