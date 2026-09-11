# Supported and planned matrix

| Dimension | Production-beta target | Current status |
|---|---|---|
| Engine | vLLM | Boundary only |
| GPUs | H100 primary; A100 after validation | Not certified |
| Topology | One node; 1/2/4/8 GPUs | Not tested |
| Models | 3–5 explicitly certified models | Not selected |
| Persistent execution | Local Ubuntu, Runpod Secure Cloud, JarvisLabs VM | Boundaries only |
| Serverless execution | Modal beta | Boundary only |
| Deployment | Export plus manual approval | Metadata contract only |

Anything not explicitly certified is unsupported, even when a schema can represent it. Certification must bind model revision, engine/image digest, GPU/topology, provider environment, workload envelope, and test evidence.
