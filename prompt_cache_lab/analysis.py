from statistics import median


def group_latency(rows: list[dict]) -> dict[str, dict]:
    groups: dict[str, list[float]] = {}
    for row in rows:
        groups.setdefault(row["mode"], []).append(float(row["client_seconds"]))
    return {
        name: {
            "runs": len(values),
            "median_seconds": median(values),
            "min_seconds": min(values),
            "max_seconds": max(values),
        }
        for name, values in sorted(groups.items())
    }
