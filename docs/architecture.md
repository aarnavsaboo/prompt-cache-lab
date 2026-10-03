# Architecture and experiment controls

`prompt-cache-lab` measures observable behavior in workloads with repeated prompt prefixes without assuming a backend exposes a particular cache implementation.

## Trial families

The planner generates related requests that differ in controlled ways:

- identical shared prefix
- minimally mutated prefix
- alternating prefix families
- growing conversation history
- cold/warm run sequences
- sequential and bounded-concurrency execution

The suffix and output budget remain explicit so prompt reuse is not confounded with an unrelated workload change.

## Data flow

```text
experiment config
       |
       v
trial families
       |
       v
concrete requests
       |
       v
local runtime
       |
       +--> prompt size
       +--> latency
       +--> output size
       +--> runtime metadata
       |
       v
raw JSONL
       |
       v
grouped comparisons
```

## Interpretation

A faster repeated request does not by itself prove prefix-cache reuse. Model loading, filesystem state, runtime warmup and queueing can create similar effects.

For that reason, the analysis compares related trial families and keeps cold/warm state and concurrency separate.

## Artifact contract

Raw records should contain enough information to reconstruct the comparison group: model/runtime, prefix family, mutation type, prefix/suffix sizes, generation budget, trial index and timing values.

Reports are derived from raw records and should not modify them.

## Extension points

Backend adapters should normalize observable timing fields but preserve backend-specific metadata. New trial families should be deterministic from their configuration so they can be regenerated without storing every prompt fixture manually.
