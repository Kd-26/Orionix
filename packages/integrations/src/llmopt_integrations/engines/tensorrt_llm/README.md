# TensorRT-LLM engine adapter

**Purpose:** reserve a later TensorRT-LLM adapter. **Responsibilities:** eventually validate compilation/runtime contracts and emit typed launch specifications. **Non-responsibilities:** compilation today, CUDA installation, provisioning, or exposing engine binaries. **Allowed dependencies:** stable contracts and a future optional reviewed engine extra. **Prohibited dependencies:** control-plane, provider SDKs, and unrelated engines. **Status:** namespace only. **Next milestone:** deferred beyond initial vLLM production beta.
