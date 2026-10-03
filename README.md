# prompt-cache-lab

Local inference experiments for workloads that repeatedly reuse large prompt prefixes.

A lot of practical LLM traffic is structurally repetitive: the same instructions, document collection, schema description or long reference block is sent with a relatively small request-specific suffix. This repository builds repeatable experiments around that pattern and records enough timing information to compare stable prefixes, slightly changed prefixes and completely different prefixes.

The project does not assume a runtime implements any specific cache. It treats the backend as a black box and measures observable behaviour.

## Experiment dimensions

- shared prefix length
- request-specific suffix length
- identical vs mutated prefixes
- alternating prefix families
- cold vs warm model state
- output token budget
- sequential vs concurrent requests
- model/runtime combination
- repeated conversations with growing history

## Workflow

```text
experiment.json
      |
      v
trial generator
      |
      +--> stable prefix
      +--> one-character mutation
      +--> alternating prefixes
      +--> growing conversation
      |
      v
bounded runner --> local runtime
      |
      v
raw request JSONL
      |
      +--> latency grouping
      +--> prefix-family comparison
      +--> warmup curves
      +--> prompt-length curves
```

## Example

```bash
python -m prompt_cache_lab plan configs/workload.example.json > runs/plan.jsonl
python -m prompt_cache_lab execute runs/plan.jsonl --model qwen3:4b --out runs/raw.jsonl
python -m prompt_cache_lab report runs/raw.jsonl
```

The raw data is more important than a single summary number. A faster second request can come from model loading, filesystem effects or runtime warmup even when no reusable prompt state exists.

## Repository layout

- `trials.py` — deterministic prompt families
- `planner.py` — experiment matrix generation
- `runner.py` — local request execution
- `analysis.py` — grouped latency and warmup summaries
- `conversation.py` — controlled history growth
- `configs/` — workload manifests
- `docs/` — experiment design and interpretation notes
- `tests/` — deterministic generation and analysis tests

Maintained by **Aarnav Saboo**.
