# Execution Capsule

**Purpose:** metadata definitions for a future reusable deployment artifact. **Responsibilities:** manifest, artifact descriptors, compatibility fingerprint, engine metadata, policy metadata, and integrity metadata. **Non-responsibilities:** binary storage/extraction, signing, CUDA graph restoration, deterministic memory reconstruction, deployment, or Foundry behavior. **Allowed dependencies:** `domain`, `schemas`, and Pydantic. **Future:** artifact transport and cryptographic verification must be threat-modeled before implementation.
