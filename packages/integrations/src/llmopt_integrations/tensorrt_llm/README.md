# TensorRT-LLM boundary

This adapter will eventually translate Orionix serving and benchmark contracts into TensorRT-LLM compilation/runtime operations and normalized observations. Customer-agent composition code may depend on it through a narrow adapter interface. It must not expose TensorRT-LLM objects, engines, binaries, or configuration internals to domain, schemas, optimizer, capsule, or unrelated integrations. No implementation or mandatory TensorRT-LLM/CUDA dependency exists yet.
