# Foundry boundary

Foundry may eventually be evaluated as an Apache-2.0-licensed internal primitive for CUDA graph persistence, deterministic memory reconstruction, kernel binary restoration, and graph-template reconstruction.

Only customer-agent/capsule composition code may eventually depend on this adapter, through typed metadata contracts. Foundry APIs, binary layouts, CUDA handles, and restoration details must never leak into domain, schemas, optimizer, benchmark, telemetry, or unrelated integrations. No Foundry source, methodology, installation, SAVE/LOAD behavior, or implementation exists in this repository. License and security review is required before adoption.
