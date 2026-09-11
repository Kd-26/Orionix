# Common

**Purpose:** small cross-cutting foundations. **Responsibilities:** error conventions, environment-backed settings, and safe structured-log setup. **Non-responsibilities:** domain entities, vendor SDK wrappers, business logic, distributed tracing, or secret retrieval. **Allowed dependencies:** lightweight runtime utilities such as Pydantic Settings. **Future:** add context propagation adapters only when consumers require them.
