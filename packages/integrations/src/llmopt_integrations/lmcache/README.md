# LMCache boundary

This adapter will eventually map Orionix cache-policy contracts to LMCache capabilities and normalized metrics. Customer-agent composition code may depend on it through a narrow adapter interface. It must not expose LMCache objects or cache internals to domain, schemas, optimizer, capsule, or unrelated integrations. No cache execution or mandatory LMCache dependency exists yet.
