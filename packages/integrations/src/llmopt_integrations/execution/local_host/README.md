# Local Ubuntu/NVIDIA execution

The production shape is a host-installed customer agent using Docker or a tightly controlled host process, NVIDIA Container Toolkit, local model/cache paths, and environment/topology fingerprinting. This adapter may depend on integration ports and future optional host/GPU utilities. It must not expose subprocess handles, Docker sockets, CUDA objects, or model paths outside the agent boundary. The Docker socket is privileged and must not be casually mounted. Status: no host, Docker, NVIDIA, or CUDA access. Next milestone: CPU-safe capability inspection.
