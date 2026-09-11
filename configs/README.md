# Configuration

Configuration is namespaced for `control_plane`, `agent`, `benchmarking`, `optimization`, and `telemetry`. Non-secret defaults belong in versioned files under `configs/`; secrets exist only in environment variables or an approved secret store. `environments/` keeps explicit development, testing, and production overlays with telemetry disabled by default.

Precedence, highest first: explicit CLI/runtime argument → environment variable → environment-specific non-secret file → code default. Environments are `development`, `testing`, and `production`; they share the same schema and never duplicate secrets.

`examples/` contains safe synthetic examples. `schemas/` is reserved for human/tool validation schemas; canonical Python contracts live in `llmopt_schemas`.
