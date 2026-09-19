"""Base behavior shared by versioned contracts."""

from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, model_validator


class ContractModel(BaseModel):
    """Strict, immutable base for cross-boundary data."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    @model_validator(mode="before")
    @classmethod
    def require_exact_schema_version(cls, value: object) -> object:
        """Reject absent or mismatched versions for every saved top-level contract."""

        expected = getattr(cls, "SCHEMA_VERSION", None)
        if not isinstance(expected, str) or isinstance(value, cls):
            return value
        if not isinstance(value, Mapping) or "schema_version" not in value:
            raise ValueError(f"{cls.__name__} requires an explicit schema_version")
        if value["schema_version"] != expected:
            raise ValueError(
                f"{cls.__name__} supports schema_version {expected!r}, "
                f"received {value['schema_version']!r}"
            )
        return value
