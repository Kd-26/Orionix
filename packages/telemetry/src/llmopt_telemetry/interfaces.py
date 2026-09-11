"""Telemetry contracts with a safe local default."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol


class MetricCategory(StrEnum):
    PRODUCT = "product"
    BENCHMARK = "benchmark"
    CUSTOMER_INFERENCE = "customer_inference"
    SYSTEM_HEALTH = "system_health"


@dataclass(frozen=True, slots=True)
class Metric:
    name: str
    value: float
    category: MetricCategory
    labels: dict[str, str] = field(default_factory=dict)


class MetricsSink(Protocol):
    def record(self, metric: Metric) -> None: ...


class NoOpMetricsSink:
    """Default sink; intentionally performs no transmission or persistence."""

    def record(self, metric: Metric) -> None:
        del metric
