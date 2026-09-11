# Testing

Tests are organized as unit, contract, integration, smoke, and GPU suites. `make test` excludes `gpu`; CUDA-marked tests also skip automatically when CUDA is unavailable. `slow` is an orthogonal marker.

Bootstrap tests verify imports, schemas, configuration, and CLI startup. They must not simulate optimizer performance or claim runtime capabilities. Contract tests should pin serialized shapes deliberately as external compatibility commitments emerge.
