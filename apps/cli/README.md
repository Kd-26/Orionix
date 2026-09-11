# CLI

**Purpose:** human-facing entry point for future local and control-plane workflows. **Responsibilities:** command registration, help, argument validation, and later composition of application services. **Non-responsibilities:** optimization algorithms, engine execution, persistence, or domain logic. **Allowed dependencies:** application-level packages through explicit interfaces. **Future:** `inspect`, `analyze`, `benchmark`, `optimize`, `status`, `report`, `export`, and `cleanup` will delegate to services; today they only report that they are unimplemented.
