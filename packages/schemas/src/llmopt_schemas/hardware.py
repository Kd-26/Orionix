"""Capability-adaptive hardware, cluster, and software-environment contracts."""

from enum import StrEnum
from typing import ClassVar

from pydantic import Field, JsonValue, model_validator

from llmopt_schemas.base import ContractModel


class ObservationSource(StrEnum):
    REPORTED = "reported"
    MEASURED = "measured"
    INFERRED = "inferred"


class NumericObservation(ContractModel):
    value: float = Field(ge=0)
    source: ObservationSource
    confidence: float = Field(ge=0, le=1)


class AcceleratorPartitionSpec(ContractModel):
    partition_type: str = Field(min_length=1)
    partition_identifier_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    memory_bytes: int = Field(gt=0)


class AcceleratorSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    vendor: str = Field(min_length=1)
    device_name: str = Field(min_length=1)
    device_identifier_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    architecture_family: str = Field(min_length=1)
    compute_capability: str | None = None
    vram_bytes: int = Field(gt=0)
    memory_bandwidth_gbps: NumericObservation | None = None
    supported_numeric_formats: tuple[str, ...] = Field(min_length=1)
    partition: AcceleratorPartitionSpec | None = None
    power_limit_watts: NumericObservation | None = None
    thermal_limit_celsius: NumericObservation | None = None
    feature_metadata: dict[str, JsonValue] = Field(default_factory=dict)


class StorageSpec(ContractModel):
    storage_id: str = Field(min_length=1)
    capacity_bytes: int = Field(ge=0)
    storage_class: str | None = None
    filesystem_type: str | None = None


class NetworkInterfaceSpec(ContractModel):
    interface_id: str = Field(min_length=1)
    link_type: str = Field(min_length=1)
    speed_gbps: NumericObservation | None = None
    rdma_capable: bool | None = None


class NodeSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    node_id: str = Field(min_length=1)
    roles: tuple[str, ...] = ()
    cpu_architecture: str = Field(min_length=1)
    cpu_count: int = Field(ge=1)
    ram_bytes: int = Field(gt=0)
    storage: tuple[StorageSpec, ...] = ()
    accelerators: tuple[AcceleratorSpec, ...] = ()
    numa_topology: dict[str, JsonValue] = Field(default_factory=dict)
    network_interfaces: tuple[NetworkInterfaceSpec, ...] = ()
    operating_system: str = Field(min_length=1)
    operating_system_version: str | None = None
    container_runtime: str | None = None
    healthy: bool | None = None

    @model_validator(mode="after")
    def unique_accelerators(self) -> "NodeSpec":
        identifiers = [item.device_identifier_hash for item in self.accelerators]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("accelerator identifiers must be unique within a node")
        return self


class InterconnectEndpoint(ContractModel):
    node_id: str = Field(min_length=1)
    accelerator_identifier_hash: str | None = Field(default=None, pattern=r"^sha256:[0-9a-f]{64}$")


class InterconnectSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    link_id: str = Field(min_length=1)
    link_type: str = Field(min_length=1)
    endpoint_a: InterconnectEndpoint
    endpoint_b: InterconnectEndpoint
    peer_access_capable: bool | None = None
    bandwidth_gbps: NumericObservation | None = None
    latency_microseconds: NumericObservation | None = None
    rdma_capable: bool | None = None
    fabric_metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def distinct_endpoints(self) -> "InterconnectSpec":
        if self.endpoint_a == self.endpoint_b:
            raise ValueError("interconnect endpoints must be distinct")
        return self


class ProviderEnvironmentSpec(ContractModel):
    provider_name: str | None = None
    region: str | None = None
    instance_type: str | None = None
    resource_identifier_hash: str | None = Field(default=None, pattern=r"^sha256:[0-9a-f]{64}$")
    extensions: dict[str, JsonValue] = Field(default_factory=dict)


class ClusterSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    cluster_id: str = Field(min_length=1)
    nodes: tuple[NodeSpec, ...] = Field(min_length=1)
    interconnects: tuple[InterconnectSpec, ...] = ()
    accelerator_count: int = Field(ge=0)
    homogeneous: bool
    collective_capabilities: tuple[str, ...] = ()
    provider: ProviderEnvironmentSpec = Field(default_factory=ProviderEnvironmentSpec)
    cluster_fingerprint: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")

    @model_validator(mode="after")
    def validate_membership_and_counts(self) -> "ClusterSpec":
        node_ids = [node.node_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("cluster node identifiers must be unique")

        actual_accelerator_count = sum(len(node.accelerators) for node in self.nodes)
        if self.accelerator_count != actual_accelerator_count:
            raise ValueError("accelerator_count must equal accelerators present on cluster nodes")

        known_nodes = set(node_ids)
        known_accelerators = {
            accelerator.device_identifier_hash
            for node in self.nodes
            for accelerator in node.accelerators
        }
        for interconnect in self.interconnects:
            for endpoint in (interconnect.endpoint_a, interconnect.endpoint_b):
                if endpoint.node_id not in known_nodes:
                    raise ValueError("interconnect endpoint references an unknown node")
                if (
                    endpoint.accelerator_identifier_hash is not None
                    and endpoint.accelerator_identifier_hash not in known_accelerators
                ):
                    raise ValueError("interconnect endpoint references an unknown accelerator")

        accelerator_shapes = {
            (
                accelerator.vendor,
                accelerator.device_name,
                accelerator.architecture_family,
                accelerator.vram_bytes,
            )
            for node in self.nodes
            for accelerator in node.accelerators
        }
        if self.homogeneous and len(accelerator_shapes) > 1:
            raise ValueError("homogeneous clusters cannot contain different accelerator shapes")
        return self


class SoftwareEnvironmentSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    operating_system: str = Field(min_length=1)
    kernel_version: str | None = None
    driver_version: str | None = None
    cuda_version: str | None = None
    pytorch_version: str | None = None
    nccl_version: str | None = None
    engine_name: str = Field(min_length=1)
    engine_version: str | None = None
    engine_image_digest: str | None = Field(default=None, pattern=r"^sha256:[0-9a-f]{64}$")
    kernel_library_versions: dict[str, str] = Field(default_factory=dict)
    container_runtime: str | None = None
    provider_runtime: str | None = None


class HardwareSpec(ContractModel):
    """Complete normalized execution-environment snapshot."""

    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    cluster: ClusterSpec
    software: SoftwareEnvironmentSpec
