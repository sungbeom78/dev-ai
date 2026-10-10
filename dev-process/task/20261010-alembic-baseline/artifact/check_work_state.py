import json
from pathlib import Path

state = json.loads(
    Path("dev-process/task/20261010-alembic-baseline/task_state.json").read_text(
        encoding="utf-8"
    )
)
assert state["completion"]["work"] == "done"
assert all(item["status"] == "met" for item in state["acceptance"])
print("work_state=done acceptance_met=5")
