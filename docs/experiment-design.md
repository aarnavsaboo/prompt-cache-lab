# Experiment design

Run stable, mutated and alternating-prefix trials with the same model and output budget. Keep model warm-state explicit. Randomize trial order if the runtime or system temperature may drift over time.

A lower second-request latency does not by itself prove prefix reuse. Model loading, filesystem cache and runtime warmup can produce similar curves. The paired trial shapes exist to separate those effects as much as possible from the outside.
