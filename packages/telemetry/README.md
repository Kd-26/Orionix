# Telemetry

**Purpose:** an explicit, no-op-by-default metrics boundary. **Responsibilities:** distinguish product telemetry, benchmark metrics, customer inference metrics, and system health metrics. **Non-responsibilities:** external transmission, Prometheus endpoints, OpenTelemetry exporters, Grafana dashboards, or distributed tracing. **Allowed dependencies:** standard library only. **Future:** exporters must be opt-in and must enforce customer-data boundaries.
