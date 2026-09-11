# Testing

Tests are organized as unit, contract, integration, e2e, smoke, GPU, performance, and security suites. `make test` excludes `gpu`, `performance`, and `slow`; CUDA-marked tests skip automatically with a reason when CUDA is unavailable.

Bootstrap tests verify imports, schemas, configuration, and CLI startup. They must not simulate optimizer performance or claim runtime capabilities. Contract tests should pin serialized shapes deliberately as external compatibility commitments emerge.
