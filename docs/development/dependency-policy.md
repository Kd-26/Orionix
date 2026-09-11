# Dependency policy

Direct dependencies are exactly pinned and `uv.lock` is committed. Add a library only when standard-library or existing capabilities are insufficient. GPU and inference-engine packages must be optional extras and cannot enter the base developer install.

Every addition needs maintainer approval, provenance and third-party license review, vulnerability review, and a lockfile update. Pull requests run dependency review; Dependabot monitors supported ecosystems; `make security` runs a lightweight Python dependency audit. Vendored source is prohibited without a dedicated review and preserved upstream licensing.
