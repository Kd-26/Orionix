# Workload

**Purpose:** define how versioned workload profiles enter the platform. **Responsibilities:** a narrow loader port around `WorkloadSpec`. **Non-responsibilities:** traffic capture, prompt storage, synthetic generation, inference, optimization, or persistence. **Allowed dependencies:** `schemas` only. **Prohibited dependencies:** engines, provider SDKs, CUDA, control-plane/web frameworks, and ORMs. **Status:** protocol only. **Next milestone:** accept a small local customer-authored workload document with schema validation.
