"""Export boundary; implementations may write files but never deploy them."""

from pathlib import Path
from typing import Protocol

from llmopt_schemas import ServingConfig
from llmopt_schemas.deployment import DeploymentExportMetadata


class DeploymentExporter(Protocol):
    def export(self, config: ServingConfig, destination: Path) -> DeploymentExportMetadata: ...
