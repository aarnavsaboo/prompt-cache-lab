from collections import defaultdict
from statistics import median


def _p(values: list[float], q: float) -> float:
    values = sorted(values)
    if not values:
        raise ValueError("empty")
    index = round((len(values) - 1) * q)
    return values[index]


def group_latency(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        key = (row["model"], row["mode"], row["prefix_chars"], row["output_tokens_requested"])
        groups[key].append(row)

    out = []
    for key, group in sorted(groups.items()):
        model, mode, prefix_chars, output_tokens = key
        latency = [float(x["client_seconds"]) for x in group]
        prompt_ns = [x["prompt_eval_duration_ns"] for x in group if x.get("prompt_eval_duration_ns")]
        out.append({
            "model": model,
            "mode": mode,
            "prefix_chars": prefix_chars,
            "output_tokens": output_tokens,
            "runs": len(group),
            "median_seconds": median(latency),
            "p90_seconds": _p(latency, .9),
            "median_prompt_eval_ms": None if not prompt_ns else median(prompt_ns) / 1e6,
        })
    return out


def warmup_curve(rows: list[dict]) -> list[dict]:
    ordered = sorted(rows, key=lambda x: (x["mode"], x["prefix_chars"], x["request_index"]))
    return [
        {
            "mode": row["mode"],
            "prefix_chars": row["prefix_chars"],
            "request_index": row["request_index"],
            "client_seconds": row["client_seconds"],
        }
        for row in ordered
    ]
