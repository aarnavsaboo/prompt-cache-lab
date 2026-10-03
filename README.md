# prompt-cache-lab

Experiments around repeated prompt prefixes and warm local inference.

Many local workloads reuse a large system prompt, document preamble or instruction block across requests. This lab builds paired trials where the shared prefix is held constant, slightly modified or completely replaced, then records latency and generation metadata from a local runtime.

The project is deliberately runtime-agnostic at the analysis layer. An Ollama adapter is included for convenient local experiments.

## Trial shapes

- identical long prefix + changing suffix
- one-character prefix mutation
- prefix length sweep
- cold model vs warm model
- repeated conversation preamble
- alternating between two large prefixes

```bash
python -m prompt_cache_lab make --prefix-chars 16000 --requests 20 > trial.jsonl
```

The aim is to observe reuse behaviour and latency curves, not to assume a backend implements a particular cache strategy.

Maintained by **Aarnav Saboo**.
