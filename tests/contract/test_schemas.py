"""Initial schema construction and invariant tests."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from llmopt_benchmark import BenchmarkEnvironment, BenchmarkPlan, BenchmarkRun
from llmopt_capsule import ExecutionCapsuleManifest
from llmopt_common import CapsuleId, ConfigurationId
from llmopt_schemas import (
    AgentCapabilities,
    AgentCommand,
    BenchmarkResult,
    CompatibilityFingerprint,
    ComputeStatus,
    ComputeTarget,
    DeploymentExportMetadata,
    DiagnosticBundleManifest,
    EngineEvent,
    EngineHandle,
    EngineLaunchSpec,
    ExecutionRequest,
    HardwareSpec,
    JobStateTransition,
    MetricDistribution,
    ModelSpec,
    OptimizationRequest,
    OptimizationResult,
    PreparedEnvironment,
    ProvisioningRequest,
    QualityConstraint,
    QualityEvaluation,
    ServingConfig,
    SLOSpec,
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
        generated_tokens_per_second=100,
        total_tokens_per_second=200,
        requests_per_second=10,
        goodput_requests_per_second=9,
        duration_seconds=60,
        environment_fingerprint="sha256:environment",
        workload_fingerprint="sha256:workload",
    )

    assert workload.schema_version == "1.0"
    assert result.schema_version == "2.0"
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
            execution_backend="local_host",
            engine="placeholder",
            capsule_schema_version="2.0",
        ),
        serving_configuration=ServingConfig(engine="placeholder"),
        workload_assumptions=WorkloadSpec(
            input_tokens=TokenDistribution(p50=1, p95=2, max=4),
            output_tokens=TokenDistribution(p50=1, p95=2, max=4),
        ),
        slo=SLOSpec(),
    )

    assert manifest.schema_version == "2.0"
    assert manifest.compilation_artifacts == ()


@pytest.mark.contract
def test_contract_round_trip_preserves_schema_version() -> None:
    model = ModelSpec(model_id="synthetic/test", parameter_count=1)

    restored = ModelSpec.model_validate_json(model.model_dump_json())

    assert restored == model
    assert restored.schema_version == "1.0"


@pytest.mark.contract
@pytest.mark.parametrize(
    "contract",
    (
        AgentCapabilities,
        AgentCommand,
        BenchmarkEnvironment,
        BenchmarkPlan,
        BenchmarkResult,
        BenchmarkRun,
        CompatibilityFingerprint,
        ComputeStatus,
        ComputeTarget,
        DeploymentExportMetadata,
        DiagnosticBundleManifest,
        EngineEvent,
        EngineHandle,
        EngineLaunchSpec,
        ExecutionCapsuleManifest,
        ExecutionRequest,
        HardwareSpec,
        JobStateTransition,
        ModelSpec,
        OptimizationRequest,
        OptimizationResult,
        PreparedEnvironment,
        ProvisioningRequest,
        QualityConstraint,
        QualityEvaluation,
        SLOSpec,
        ServingConfig,
        WorkloadSpec,
    ),
)
def test_top_level_contracts_declare_schema_versions(contract: type[object]) -> None:
    assert isinstance(getattr(contract, "SCHEMA_VERSION"), str)  # noqa: B009
