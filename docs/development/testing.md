# Testing

Tests are organized as unit, contract, integration, e2e, smoke, GPU, performance, and security suites. `make test` excludes `gpu`, `performance`, and `slow`; CUDA-marked tests skip automatically with a reason when CUDA is unavailable.

Bootstrap tests verify imports, schemas, configuration, and CLI startup. They must not simulate optimizer performance or claim runtime capabilities. Contract tests should pin serialized shapes deliberately as external compatibility commitments emerge.

`make check` is the complete CPU quality gate. It verifies the lockfile,
formatting, linting, strict typing, CPU-safe tests, internal Markdown links, all
workspace package builds, and the presence of `py.typed` in every built wheel.
Run it before review. GPU, performance, and slow suites remain separate and
must provide their own environment-specific evidence.
