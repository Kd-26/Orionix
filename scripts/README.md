# Scripts

Thin, developer-facing wrappers around the canonical uv commands. `doctor.sh` checks CPU-only prerequisites; `check.sh` runs the lock, format, lint, type, and CPU-safe test gates. They contain no product runtime behavior; `Makefile` provides the normal entry points.
