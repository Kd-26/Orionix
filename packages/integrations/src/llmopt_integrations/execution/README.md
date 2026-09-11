# Execution integrations

Execution adapters implement `ExecutionBackend`; provider provisioning adapters separately implement `ProvisioningBackend`. Credentials and provider SDK types remain private to the owning adapter. No adapter may offer generic remote shell execution or leak provider objects into contracts. Status: namespaces and provider-neutral ports only. Next milestone: a harmless local capability collector followed by a constrained Docker execution adapter.
