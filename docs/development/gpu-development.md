# GPU development

A future reference validation environment will be selected from available hardware, customer demand, engine compatibility, representative topology, repeatability, and cost. It may exercise one or more Ampere, Hopper, or Blackwell profiles and available single-node GPU counts, but it is an operational fixture rather than a product dependency or support definition.

Every run records driver, CUDA, libraries, engine image digest, accelerator architecture/count/memory/partitions, rank mapping, topology, provider runtime, and redacted physical identity in a versioned fingerprint. GPU tests never enter default setup or pull-request CI and run only on explicitly managed runners.

No GPU host, NVIDIA Container Toolkit setup, vLLM environment, or runner is configured in this milestone. Multi-node runtime testing is a later explicit gate even though cluster schemas must represent it.
