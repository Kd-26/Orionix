# Product metrics and experiment safety

This document is the canonical source for onboarding stages, benchmark measurements, optimization objectives, and initial experiment-safety hypotheses. Implementations must define one formula and explicit edge cases for every emitted metric before certification.

## Onboarding and time-to-value stages

Measure these intervals independently; never collapse them into one installation or time-to-value number:

| Stage | Starts | Ends | Prepared-environment target |
|---|---|---|---|
| Project creation | Create request accepted | Project ready | Observe; no target frozen |
| Worker startup | Provider/host start requested | Worker process ready | Report separately by backend |
| Enrollment | Enrollment initiated | Authenticated agent ready | P50 < 5 minutes; P95 < 10 minutes |
| Environment discovery | Discovery accepted | Versioned capability report complete | < 2 minutes |
| Runtime image acquisition | Image pull starts | Digest-verified image available | Report separately |
| Model acquisition | Model transfer/cache starts | Revision-verified model available | Report separately |
| Engine/model startup | Typed launch accepted | Readiness criteria pass | Report by profile |
| Time to baseline | Model and runtime available | Valid baseline accepted | < 20 minutes |
| Optimization duration | Baseline accepted | Confirmed recommendation available | Controlled by customer budget |

Targets are initial hypotheses until pilot evidence establishes distributions and measurement conditions.

## Benchmark measurements

- TTFT P50/P95/P99, TPOT P50/P95/P99, and end-to-end latency.
- Output-token and total-token throughput, request rate, and goodput.
- Error, timeout, cancellation, and OOM rates.
- GPU utilization, VRAM utilization, measurement duration, attributable cost, and cost per successful token.
- Baseline drift, run-to-run variance, sample count, warm-up policy, and partial-run status.

[Benchmark methodology](architecture/benchmark-methodology.md) owns the current formula definitions and edge cases. Provider startup, serverless cold start, image/model acquisition, engine startup, and steady-state inference remain separate observations.

## Optimization objectives

Supported objective identifiers are:

- `MAXIMIZE_GOODPUT`
- `MAXIMIZE_THROUGHPUT`
- `MINIMIZE_TTFT`
- `MINIMIZE_TPOT`
- `MINIMIZE_COST_PER_TOKEN`
- `BALANCED_WITH_EXPLICIT_WEIGHTS`

The recommended default is to maximize goodput subject to every configured latency, quality, cost, memory, and error constraint. A balanced objective must expose all weights; hidden composite scores are prohibited.

## Hard-limit contract

Every optimization job must eventually declare maximum candidate count, elapsed time, GPU-hours, estimated cost when knowable, consecutive OOM candidates, repeated infrastructure failures, and finalist confirmation runs. Exceeding a limit stops new work, preserves evidence, performs cleanup, and returns an explicit terminal reason.

Initial values are hypotheses, not production defaults:

| Limit | Initial hypothesis |
|---|---:|
| Maximum candidates | 20 |
| Maximum consecutive OOM candidates | 2 |
| Maximum repeated infrastructure failures | 3 |
| Minimum finalist confirmation runs | 2 |

Customer cost and GPU-hour limits take precedence over defaults. Certification must validate enforcement, cancellation, cleanup, and accounting behavior.
