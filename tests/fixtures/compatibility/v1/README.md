# Synthetic Day 4 compatibility examples

These fixtures exercise the CPU-only pre-execution filter. They contain no
customer data and make no production vLLM, GPU, or Orionix certification claim.

`engine-capability.json` deliberately uses version
`0.0.0+day4.synthetic`; selecting and verifying a production vLLM release
remains an open decision. `allowed-candidate.json` is a complete versioned input.
The cases in `example-cases.json` apply small recursive patches to that input so
the reason for each decision remains easy to review.

Run all examples from the repository root:

```bash
uv run python scripts/evaluate_compatibility_examples.py
```
