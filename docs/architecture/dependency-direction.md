# Dependency direction

The automated import-boundary test enforces inward dependencies for stable Python packages. `common` imports no Orionix package. `domain` imports only `common`; `schemas` imports `common` and `domain`. Feature packages import stable contracts only. Integration ports and adapters import schemas, and composition roots may import interfaces and adapters.

Prohibited inward dependencies include engine/provider SDKs, CUDA libraries, web frameworks, ORMs, deployment clients, and outer application modules. Vendor objects never cross an adapter boundary. A manifest-cycle test rejects circular workspace dependencies.
