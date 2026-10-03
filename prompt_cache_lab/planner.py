from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1
from itertools import product
from typing import Any
import json


@dataclass(frozen=True)
class TrialSpec:
    id: str
    mode: str
    prefix_chars: int
    suffix_chars: int
    request_index: int
    output_tokens: int

    def to_dict(self):
        return asdict(self)


def expand(config: dict[str, Any]) -> list[TrialSpec]:
    modes = config.get("modes", ["stable"])
    prefixes = config.get("prefix_chars", [8000])
    suffixes = config.get("suffix_chars", [256])
    output = config.get("output_tokens", [64])
    requests = int(config.get("requests_per_cell", 5))
    rows = []
    for mode, prefix, suffix, tokens, request_index in product(
        modes, prefixes, suffixes, output, range(requests)
    ):
        payload = {
            "mode": mode,
            "prefix_chars": int(prefix),
            "suffix_chars": int(suffix),
            "request_index": request_index,
            "output_tokens": int(tokens),
        }
        ident = sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
        rows.append(TrialSpec(id=ident, **payload))
    return rows
