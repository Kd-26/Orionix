# Engine integrations

Engine adapters validate provider-neutral model/hardware/serving contracts and produce typed `EngineLaunchSpec` values. They may depend on `schemas` and the integration ports; optional engine SDKs may be added only inside their adapter extra. They must not expose SDK objects, arbitrary shell commands, orchestration state, credentials, or optimization policy. Status: namespaces only. Next milestone: implement a bounded vLLM adapter after its certified launch surface is approved.
