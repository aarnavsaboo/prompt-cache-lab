from __future__ import annotations

from pathlib import Path
from time import perf_counter
from urllib.request import Request, urlopen
from typing import Any
import json

from .planner import TrialSpec
from .trials import make_prefix


def build_prompt(spec: TrialSpec) -> tuple[str, str]:
    prefix = make_prefix(spec.prefix_chars)
    if spec.mode == "mutated" and prefix:
        pos = spec.request_index % len(prefix)
        prefix = prefix[:pos] + ("X" if prefix[pos] != "X" else "Y") + prefix[pos + 1:]
    elif spec.mode == "alternating" and spec.request_index % 2:
        prefix = prefix[::-1]
    suffix_unit = f" Request {spec.request_index}: compare repeated-prefix inference behaviour."
    suffix = (suffix_unit * (spec.suffix_chars // len(suffix_unit) + 1))[:spec.suffix_chars]
    return prefix + "\n" + suffix, prefix


def execute_ollama(
    spec: TrialSpec,
    model: str,
    endpoint: str = "http://127.0.0.1:11434",
    keep_alive: str = "10m",
) -> dict[str, Any]:
    prompt, prefix = build_prompt(spec)
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive,
        "options": {"num_predict": spec.output_tokens, "temperature": 0.0},
    }).encode()
    request = Request(
        endpoint.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = perf_counter()
    with urlopen(request, timeout=600) as response:
        result = json.load(response)
    elapsed = perf_counter() - started
    return {
        "trial_id": spec.id,
        "mode": spec.mode,
        "model": model,
        "prefix_chars": len(prefix),
        "prompt_chars": len(prompt),
        "request_index": spec.request_index,
        "output_tokens_requested": spec.output_tokens,
        "client_seconds": elapsed,
        "prompt_eval_count": result.get("prompt_eval_count"),
        "prompt_eval_duration_ns": result.get("prompt_eval_duration"),
        "eval_count": result.get("eval_count"),
        "eval_duration_ns": result.get("eval_duration"),
        "load_duration_ns": result.get("load_duration"),
        "total_duration_ns": result.get("total_duration"),
        "done_reason": result.get("done_reason"),
    }


def write_jsonl(path: str, rows: list[dict]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
