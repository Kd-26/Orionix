"""Schema invariants that are independent of golden serialization examples."""

import json
from pathlib import Path

import pytest
from llmopt_benchmark import BenchmarkEnvironment, BenchmarkPlan, BenchmarkRun
from llmopt_capsule import ExecutionCapsuleManifest
from llmopt_schemas import (
    AgentCapabilities,
    AgentCommand,
    BenchmarkResult,
    CandidateConfiguration,
    ClusterSpec,
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
    ModelSpec,
    OptimizationJobSpec,
    OptimizationRequest,
    OptimizationRequirements,
    OptimizationResult,
    PreparedEnvironment,
    ProvisioningRequest,
    QualityConstraint,
    QualityEvaluation,
    Recommendation,
    ServingConfig,
    SLOSpec,
    SoftwareEnvironmentSpec,
    TokenDistribution,
    WorkloadSpec,
)
from pydantic import ValidationError

FIXTURES = Path(__file__).parents[1] / "fixtures" / "contracts" / "v1"


def _load(name: str) -> dict[str, object]:
    payload: object = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


@pytest.mark.contract
def test_core_schemas_load_golden_examples() -> None:
    workload = WorkloadSpec.model_validate(_load("workload.json"))
    result = BenchmarkResult.model_validate(_load("benchmark-result.json"))
    model = ModelSpec.model_validate(_load("model.json"))
    hardware = HardwareSpec.model_validate(_load("hardware.json"))

    assert workload.streaming is True
    assert result.schema_version == "2.0"
    assert model.revision == "revision-0001"
    assert hardware.cluster.accelerator_count == 0


@pytest.mark.contract
def test_distribution_order_is_validated() -> None:
    with pytest.raises(ValidationError):
        TokenDistribution(p50=100, p95=50, max=200)


@pytest.mark.contract
def test_execution_capsule_is_metadata_only() -> None:
    manifest = ExecutionCapsuleManifest.model_validate(_load("execution-capsule.json"))

    assert manifest.schema_version == "2.0"
    assert manifest.compilation_artifacts == ()


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
        CandidateConfiguration,
        ClusterSpec,
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
        OptimizationJobSpec,
        OptimizationRequest,
        OptimizationRequirements,
        OptimizationResult,
        PreparedEnvironment,
        ProvisioningRequest,
        QualityConstraint,
        QualityEvaluation,
        Recommendation,
        SLOSpec,
        ServingConfig,
        SoftwareEnvironmentSpec,
        WorkloadSpec,
    ),
)
def test_top_level_contracts_declare_schema_versions(contract: type[object]) -> None:
    assert isinstance(getattr(contract, "SCHEMA_VERSION"), str)  # noqa: B009
