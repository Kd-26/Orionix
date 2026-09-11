# Debugging

Start with `make doctor`, then run the smallest failing Ruff, mypy, or pytest target. Preserve job, attempt, run, agent, and correlation identifiers in sanitized logs. Never paste credentials, prompts, model outputs, customer paths, or unreviewed diagnostic bundles into issues.

Future agent diagnostics must be collected into a versioned manifest, redacted, and previewable before upload. GPU/provider troubleshooting procedures will be added with their implementations.
