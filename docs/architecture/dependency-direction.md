# Dependency direction

The lightweight architecture test performs three static checks. It parses Python AST imports for all 16 package roots and rejects internal imports outside the source allowlist; it parses every workspace manifest and rejects declared internal dependencies outside the distribution allowlist; and it rejects cycles in the declared workspace graph. `common` imports no Orionix package. `domain` imports only `common`; `schemas` imports `common` and `domain`. Feature packages import stable contracts only. Integration ports/adapters import stable lower packages, and application composition roots may import approved interfaces and adapters.

These checks validate direct declared dependencies and syntactically visible `llmopt_*` imports. They do not prove runtime behavior, detect dynamically constructed imports, certify optional third-party dependencies, or replace code review. Smoke tests separately verify that adapter namespaces import without loading optional SDKs.

Prohibited inward dependencies include engine/provider SDKs, CUDA libraries, web frameworks, ORMs, deployment clients, and outer application modules. Vendor objects never cross an adapter boundary.
