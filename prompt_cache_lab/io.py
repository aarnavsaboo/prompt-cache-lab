from pathlib import Path
import json
from .planner import TrialSpec


def read_specs(path: str) -> list[TrialSpec]:
    return [TrialSpec(**json.loads(line)) for line in Path(path).read_text().splitlines() if line.strip()]


def read_rows(path: str) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
