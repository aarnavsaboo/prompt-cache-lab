# Interpreting repeated-prefix experiments

The main difficulty is separating several warmup effects that look similar from the outside.

A first request may pay for model loading. Later requests may benefit from operating-system file cache, runtime allocation reuse, compiled kernels, model residency or reusable prompt state. Stable-prefix trials alone cannot distinguish those effects.

Mutated-prefix and alternating-prefix families provide comparison groups. If only the stable prefix improves while equally warm mutated requests do not, the result is more suggestive of prefix-specific reuse.

Prompt processing time is worth keeping separate from total latency because a short output can hide a large input-side cost. For longer generations, decode time can dominate instead.

The lab intentionally reports observations rather than naming a cache implementation.
