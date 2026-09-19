# Contract versioning and golden examples

Orionix components exchange strict, immutable Pydantic contracts serialized as
JSON. The contracts describe data only; they do not implement discovery,
execution, optimization, persistence, or transport behavior.

## Version rule

Every independently saved or transmitted contract declares a
`schema_version`. The field must be present in input data and must exactly match
the Python model's declared version. Missing versions and unknown older or newer
versions fail validation. They are never silently interpreted as the current
shape.

When another version is introduced, compatibility must be handled by an
explicit, tested migration or a separate versioned model. Changing the meaning
of an existing field without changing the contract version is prohibited.

Nested value objects that are never saved independently do not need their own
version. Nested objects such as `AcceleratorSpec`, `NodeSpec`, and `ClusterSpec`
retain versions because they can also be saved and exchanged independently.

## Golden examples

Synthetic examples under `tests/fixtures/contracts/v1/` freeze the current JSON
shape for:

- accelerator, node, cluster, software, and complete hardware environments;
- model and workload descriptions;
- optimization requirements and hard experiment budgets;
- optimization jobs and candidate configurations;
- benchmark results, recommendations, and Execution Capsules.

The examples contain no customer data, provider credentials, model weights,
prompts, completions, or real certification evidence. A future architecture
name in a fixture proves that the contract is extensible; it does not claim that
Orionix or an engine supports that architecture.

## Ownership

`llmopt-schemas` owns shared data contracts. `llmopt-capsule` owns the Execution
Capsule manifest because capsule packaging and integrity policy form a separate
boundary. `llmopt-domain` owns lifecycle enums and stable identifiers, not JSON
transport models. The detailed mapping is maintained in the
[`llmopt-schemas` README](../../packages/schemas/README.md).
