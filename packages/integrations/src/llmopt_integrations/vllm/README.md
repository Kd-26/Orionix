# vLLM boundary

This adapter will eventually translate Orionix serving and benchmark contracts into vLLM lifecycle operations and normalized observations. Customer-agent composition code may depend on it through a narrow adapter interface. It must not expose vLLM objects, process handles, or configuration internals to domain, schemas, optimizer, capsule, or unrelated integrations. No implementation or mandatory vLLM dependency exists yet.
