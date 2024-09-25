set VERUS_TASKS_DIR "/Users/Stanislav.Alekseev/Projects/human-eval-verus/tasks"

for f in $VERUS_TASKS_DIR/*.rs
    python process_verus_task.py $f
end
