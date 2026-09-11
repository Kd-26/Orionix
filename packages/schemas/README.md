# Schemas

**Purpose:** versioned, serialization-safe contracts between subsystems. **Responsibilities:** model, hardware, workload, SLO, serving, benchmark, optimization, and compatibility metadata. **Non-responsibilities:** discovery, benchmarking, ranking, persistence, or engine execution. **Allowed dependencies:** `domain` and Pydantic only. **Future:** compatibility migrations and generated language-neutral schemas may be added without coupling contracts to an ORM.
