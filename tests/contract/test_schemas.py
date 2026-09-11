"""Initial schema construction and invariant tests."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from llmopt_capsule import ExecutionCapsuleManifest
from llmopt_domain import CapsuleId, ConfigurationId
from llmopt_schemas import (
    BenchmarkResult,
    CompatibilityFingerprint,
    HardwareSpec,
    MetricDistribution,
    ModelSpec,
    ServingConfig,
    TokenDistribution,
    WorkloadSpec,
)
from pydantic import ValidationError


@pytest.mark.contract
def test_core_schemas_instantiate() -> None:
    workload = WorkloadSpec(
        input_tokens=TokenDistribution(p50=128, p95=1024, max=4096),
        output_tokens=TokenDistribution(p50=64, p95=256, max=1024),
    )
    result = BenchmarkResult(
        configuration_id=ConfigurationId(uuid4()),
        ttft_ms=MetricDistribution(p50=20, p95=50, p99=80),
        tpot_ms=MetricDistribution(p50=5, p95=8),
        tokens_per_second=100,
        requests_per_second=10,
        goodput=90,
        duration_seconds=60,
        environment_fingerprint="sha256:environment",
    )

    assert workload.schema_version == "1.0"
    assert result.schema_version == "1.0"
    assert ModelSpec(model_id="synthetic/test").model_id == "synthetic/test"
    assert HardwareSpec().gpu_count == 0


@pytest.mark.contract
def test_distribution_order_is_validated() -> None:
    with pytest.raises(ValidationError):
        TokenDistribution(p50=100, p95=50, max=200)


@pytest.mark.contract
def test_execution_capsule_is_metadata_only() -> None:
    manifest = ExecutionCapsuleManifest(
        capsule_id=CapsuleId(uuid4()),
        created_at=datetime.now(UTC),
        compatibility=CompatibilityFingerprint(
            model_hash="sha256:model",
            engine="placeholder",
            capsule_schema_version="1.0",
        ),
        serving_configuration=ServingConfig(engine="placeholder"),
    )

    assert manifest.schema_version == "1.0"
    assert manifest.compilation_artifacts == ()
