# Scripts

`evaluate_compatibility_examples.py` runs the synthetic Day 4 candidate filter
and prints customer-facing decisions. It is CPU-only and needs no CUDA, GPU,
model weights, Docker, credentials, or live vLLM process.

Thin, developer-facing wrappers around the canonical uv commands. `doctor.sh` checks CPU-only prerequisites; `check.sh` runs the lock, format, lint, type, and CPU-safe test gates. They contain no product runtime behavior; `Makefile` provides the normal entry points.
