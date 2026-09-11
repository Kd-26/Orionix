# Benchmark methodology

Initial metrics use monotonic client-side timestamps: TTFT is accepted request to first emitted output token; TPOT is the mean inter-token interval after the first token; end-to-end latency is accepted request to terminal response. Generated tokens/second counts emitted output tokens; total tokens/second counts accepted input plus emitted output tokens. Requests/second counts successful terminal requests. Goodput counts successful requests satisfying all configured latency/SLO constraints per measurement second. Cost/token divides attributable benchmark cost by successfully generated tokens.

P50/P95/P99 use the recorded per-request population and a documented deterministic percentile method. Warm-up requests are excluded from all reported distributions and rates. Failed and cancelled requests are excluded from latency percentiles but included in error/cancellation rates. Zero-token successes have TTFT/TPOT undefined and cannot contribute to cost/token; one-token successes have TTFT but TPOT undefined. A streaming timestamp is captured when the client receives each token event, not when a server claims it sent one. OOMs are errors and counted separately.

Partial runs set `partial=true`, retain their duration and counts, and are ineligible for recommendation unless an explicit later policy permits them. Environment and workload fingerprints, plan/run IDs, exact warm-up window, timeout, engine image digest, and configuration are required provenance. No load generator or metric collector exists yet.

Provider provisioning duration, serverless cold-start duration, and model-load duration are independent optional measurements and never folded into steady-state TTFT/TPOT without an explicitly labeled report view.
