"""Print the synthetic Day 4 compatibility examples without using a GPU."""

import json
from copy import deepcopy
from pathlib import Path

from llmopt_optimizer import CandidateCompatibilityEvaluator
from llmopt_schemas import (
    CandidateFilterInput,
    EngineCapabilityRecord,
    RuleDecision,
)

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "compatibility" / "v1"


def _load_object(path: Path) -> dict[str, object]:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected a JSON object in {path.name}")
    return value


def _merge(base: dict[str, object], patch: dict[str, object]) -> dict[str, object]:
    merged = deepcopy(base)
    for key, value in patch.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = _merge(current, value)
        else:
            merged[key] = deepcopy(value)
    return merged


def main() -> None:
    capabilities = EngineCapabilityRecord.model_validate(
        _load_object(FIXTURES / "engine-capability.json")
    )
    base = _load_object(FIXTURES / "allowed-candidate.json")
    suite = _load_object(FIXTURES / "example-cases.json")
    cases = suite.get("cases")
    if not isinstance(cases, list):
        raise TypeError("example-cases.json requires a cases list")

    evaluator = CandidateCompatibilityEvaluator()
    for raw_case in cases:
        if not isinstance(raw_case, dict):
            raise TypeError("each example case must be an object")
        name = raw_case.get("name")
        patch = raw_case.get("patch")
        expected_code = raw_case.get("expected_reason_code")
        if not isinstance(name, str) or not isinstance(patch, dict):
            raise TypeError("each example requires a name and object patch")
        input_ = CandidateFilterInput.model_validate(_merge(base, patch))
        result = evaluator.evaluate(input_, capabilities)
        relevant = [
            item
            for item in result.rule_results
            if item.reason_code == expected_code
            or (result.decision is RuleDecision.ALLOWED and item.rule_id.value == "gpu_memory")
        ]
        item = relevant[0] if relevant else result.rule_results[0]
        print(f"Candidate: {name}")
        print(f"Status: {result.decision.value.upper()}")
        print(f"Code: {item.reason_code.value}")
        print(f"Message: {item.message}")
        if item.remediation:
            print(f"Suggested action: {item.remediation}")
        print()


if __name__ == "__main__":
    main()
