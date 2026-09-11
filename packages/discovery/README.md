# Discovery

**Purpose:** stable ports for infrastructure and model inspection. **Responsibilities:** define CPU/GPU/environment and model metadata inspection boundaries. **Non-responsibilities:** performing GPU discovery today, provider provisioning, engine launch, optimization, or persistence. **Allowed dependencies:** `schemas` only. **Prohibited dependencies:** CUDA, engine/provider SDKs, subprocess/Docker implementations, web frameworks, and ORMs. **Status:** protocols only. **Next milestone:** implement harmless local CPU/platform inspection and separately gated NVIDIA discovery.
