# Product scope

Orionix is a commercial optimization and orchestration layer above LLM inference engines. It will inspect a declared model, hardware target, workload profile, and SLO/quality/cost constraints; benchmark compatible configurations in customer- or provider-controlled GPU environments; validate and rank results; and export a versioned Execution Capsule and deployment configuration.

The Day-80 production-beta target is deliberately narrow: vLLM; NVIDIA H100 first and A100 after validation; one node with 1/2/4/8 GPUs; three to five explicitly certified models; local Ubuntu, Runpod Secure Cloud, and JarvisLabs VM execution; and a beta Modal adapter. Revalidation is scheduled but requires manual approval. No first-release workflow automatically mutates a live production deployment.

This milestone provides architecture, contracts, tests, and documentation only. It is not an inference engine and does not yet benchmark, provision, deploy, evaluate, or optimize.
