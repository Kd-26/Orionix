# Shared contract golden examples

These files are small synthetic examples used to freeze and test Orionix's
shared JSON formats. They contain no customer data and provide no hardware,
model, engine, or provider certification evidence.

Each file is loaded by its owning Pydantic model, serialized to JSON, loaded
again, and compared for equality. Contract tests also prove that a missing or
older `schema_version` is rejected.
