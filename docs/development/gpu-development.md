# GPU development

A future dedicated Ubuntu/NVIDIA host will validate H100 first, then A100, across 1/2/4/8 GPUs on one node. Its driver, CUDA, topology, engine image digest, and physical GPU identity must be fingerprinted. GPU tests are never part of default setup or pull-request CI and run only on explicitly managed runners.

No GPU host, NVIDIA Container Toolkit setup, vLLM environment, or runner is configured in this milestone.
