# Benchmark

**Purpose:** engine-neutral benchmark planning and execution boundaries. **Responsibilities:** plan/run/environment contracts and a runner protocol. **Non-responsibilities:** launching engines, subprocess management, GPU measurement, synthetic load, CUDA access, or result fabrication. **Allowed dependencies:** `domain`, `schemas`, and Pydantic. **Future:** TTFT, TPOT, throughput, goodput, utilization, OOM, error, and cost collection will enter through explicit adapters.
