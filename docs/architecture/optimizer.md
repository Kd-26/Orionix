# Optimizer boundary

The planned flow is:

```text
capability filtering
→ deterministic seed candidates
→ budgeted search with persisted observations
→ independent finalist validation and Pareto ranking
```

`CapabilityEvaluator`, `CandidateGenerator`, `OptimizationStrategy`, `ConstraintEvaluator`, and `ResultRanker` are ports only. Search budgets are explicit in `OptimizationRequest`. No rules, Optuna/Bayesian search, learned predictor, ranking, quality inference, or persistence exists.
