# Configuration

Configuration is namespaced for `control_plane`, `agent`, `database`, `storage`, `benchmark`, `optimizer`, and `telemetry`. Non-secret defaults belong in `development/`, `testing/`, and `production/`; secrets exist only in environment variables or an approved secret store. Telemetry is disabled in every committed environment.

Precedence, lowest first: safe compiled default → environment-specific non-secret TOML → `LLMOPT_*` environment variable → explicit CLI/runtime override. Nested environment fields use a double underscore, for example `LLMOPT_AGENT__CREDENTIAL`. The typed implementation is `llmopt_config.load_settings`.

`examples/` contains safe synthetic examples. `schemas/` is reserved for human/tool validation schemas; canonical Python contracts live in `llmopt_schemas`.
