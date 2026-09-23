# Optimizer

**Purpose:** deterministic pre-execution compatibility filtering plus ports for
future configuration planning and selection. **Responsibilities:** pure
capability rules, candidate-level aggregation, candidate generation protocols,
strategy protocols, constraint evaluation, and result-ranking interfaces.
**Non-responsibilities:** inference execution, real benchmarking, GPU
inspection, memory profiling, Optuna/Bayesian search, quality inference,
persistence, or engine APIs. **Allowed dependencies:** `schemas` and the
standard library. **Prohibited dependencies:** integrations, agent/services,
engine/provider SDKs, CUDA, web frameworks, and ORMs.

`CandidateCompatibilityEvaluator` runs every Day 4 rule in stable order and
returns all safe reasons. Its output is not an optimization recommendation and
does not itself authorize execution. See the
[compatibility rule contract](../../docs/architecture/compatibility-rules.md).
