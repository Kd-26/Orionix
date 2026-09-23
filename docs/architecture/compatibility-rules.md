# Pre-execution compatibility rules

Day 4 implements a deterministic, CPU-only filter in `llmopt-optimizer`. It
uses versioned contracts from `llmopt-schemas` and supplied facts only. It does
not inspect a GPU, profile memory, launch vLLM, search configurations, or
allocate infrastructure.

## Public decisions

Every rule returns one of three decisions:

- `ALLOWED`: supplied evidence explicitly satisfies the rule.
- `REJECTED`: supplied evidence proves a hard incompatibility or limit violation.
- `EXPERIMENTAL`: evidence is missing, unknown, unverified, or outside Orionix
  certification.

Unknown information never becomes automatic approval. Candidate aggregation is
deterministic: any rejection makes the candidate rejected; otherwise any
experimental result makes it experimental; otherwise it is allowed. All rules
run in a fixed order, so a customer can correct multiple problems in one pass.

## Ownership

`llmopt-schemas` owns the serialized capability, input, rule-result, and
candidate-result formats. `llmopt-optimizer` owns the pure evaluation logic.
Execution adapters must consume only candidates that their caller has accepted
under an explicit product policy; the Day 4 filter itself calls no adapter.

The following rules run for every candidate:

| Rule | Supplied facts checked |
|---|---|
| GPU memory | Model, KV-cache, overhead, safety-margin estimates, placement memory, and utilization limit |
| GPU architecture | Vendor and architecture against explicit engine records |
| Precision | Requested precision against hardware facts and architecture-specific engine support |
| Quantization | Model quantization against architecture-specific engine support |
| Context length | Requested tokens against the engine limit |
| Tensor parallel size | Required/available GPUs, placement uniqueness, engine maximum, and supplied divisibility constraints |
| Parallelism topology | Placement membership, single-node restriction, and required peer access |
| Time budget | Supplied elapsed-time estimate against the customer limit |
| Cost budget | Supplied GPU-hour and cost estimates against customer limits |
| Engine features | Exact engine identity/version and explicit feature/parallelism declarations |
| Speculative decoding | Method support plus supplied draft ID, tokenizer, context, and verification evidence |
| Expert parallelism | Expert parallelism is limited to explicitly identified MoE models |
| Orionix certification | Exact profile match, evaluated separately from engine compatibility |

Memory, elapsed time, GPU-hours, and cost are labeled estimates. Day 4 does not
measure or invent them.

## Engine compatibility is not certification

The result contains separate `engine_compatibility` and
`orionix_certification` decisions. A combination may be engine-compatible while
remaining experimental because Orionix has not retained evidence for that
exact model, architecture, precision, quantization, feature, and engine-version
profile. “Not certified” must not be described as “engine unsupported.”

The repository fixture pins `0.0.0+day4.synthetic`. It proves record loading and
rule behavior only. It is not a real vLLM support statement. The production
vLLM version remains an open decision until release notes, image provenance,
security review, and GPU evidence are approved.

## Capability record versioning

`EngineCapabilityRecord` schema version `1.0` contains an exact engine name and
version, its own record revision, architecture-specific precision and
quantization declarations, context and tensor-parallel limits, feature states,
speculative methods, certification profiles, and provenance. Supported,
unsupported, and unverified values are disjoint.

To add a future engine version:

1. Create a new record; never edit old evidence to describe a different engine.
2. Pin the exact engine version and increment the record revision independently.
3. Record explicit provenance and verification date.
4. Put unknown facts in `unverified` or leave them absent; never infer support.
5. Add contract, rule, and customer-message tests.
6. Obtain the required product/security approval before adding production
   certification evidence.

## Stable reason codes

Reason codes are public identifiers. Existing meanings must not be repurposed;
messages and remediation text may become clearer without changing the code.
Codes cover insufficient memory, unsupported or unknown architecture,
precision/quantization incompatibility, context limits, parallelism and
topology errors, time/cost limits, unsupported or unknown engine features,
draft-model problems, dense-model expert parallelism, version mismatch, and
compatible-but-uncertified profiles.

To add a rule, add a stable rule ID and reason codes in `llmopt-schemas`, return
one versioned `RuleResult`, append the pure function to the ordered `RULES`
tuple, and test allowed, rejected, and experimental evidence. Messages must be
actionable and must not contain identifiers, paths, stack traces, credentials,
or private scoring details.

## Customer-facing examples

The synthetic examples can be reviewed without a GPU:

```bash
uv run python scripts/evaluate_compatibility_examples.py
```

Expected outcomes:

1. A memory estimate larger than usable GPU memory is rejected with
   `INSUFFICIENT_GPU_MEMORY`; reduce memory demand or select larger GPUs.
2. FP8 on hardware that explicitly lacks FP8 is rejected with
   `UNSUPPORTED_PRECISION`; select BF16/FP16 or verified compatible hardware.
3. Tensor parallelism requiring more GPUs than exist is rejected with
   `INVALID_TENSOR_PARALLEL_SIZE`; reduce the parallel size or add verified GPUs.
4. Speculative decoding without draft evidence is rejected with
   `SPECULATIVE_DRAFT_MODEL_REQUIRED`; select and validate a compatible draft.
5. A feature absent from the pinned record is experimental with
   `ENGINE_FEATURE_UNKNOWN`; verify it before execution. It is not falsely
   described as unsupported.

## Founder feedback checklist

Show the example output to a potential user and ask:

- Do you understand why this candidate was stopped or marked experimental?
- Does the message tell you what needs to change?
- Is any terminology confusing?
- Could you act on this without help from an Orionix engineer?

Record the response separately. This checklist does not claim that an interview
has occurred.

## Deliberately not implemented

Day 4 includes no production capability claim, hardware discovery, GPU memory
profiling, vLLM command, benchmark, optimization search, speculative execution,
multi-node execution, cloud operation, database, API, or UI behavior.
