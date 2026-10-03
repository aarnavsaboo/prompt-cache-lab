from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class Trial:
    index: int
    mode: str
    prefix_hash: str
    prefix_chars: int
    prompt: str


def make_prefix(chars: int) -> str:
    unit = "Local inference experiments compare repeated prefixes across otherwise similar requests. "
    return (unit * (chars // len(unit) + 1))[:chars]


def make_trials(prefix_chars: int, requests: int, mode: str = "stable") -> list[Trial]:
    base = make_prefix(prefix_chars)
    out = []
    for i in range(requests):
        prefix = base
        if mode == "mutated" and prefix:
            pos = i % len(prefix)
            prefix = prefix[:pos] + ("X" if prefix[pos] != "X" else "Y") + prefix[pos + 1:]
        elif mode == "alternating" and i % 2:
            prefix = make_prefix(prefix_chars)[::-1]
        prompt = prefix + f"\nRequest {i}: summarize the repeated preamble in one sentence."
        out.append(Trial(i, mode, sha256(prefix.encode()).hexdigest()[:16], len(prefix), prompt))
    return out
