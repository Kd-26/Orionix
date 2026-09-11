# Deployment export

**Purpose:** export typed, reviewable deployment configuration without mutating live systems. **Responsibilities:** define an exporter port and export metadata. **Non-responsibilities:** deployment, Kubernetes control, autoscaling, secret materialization, or production mutation. **Allowed dependencies:** `schemas` only. **Prohibited dependencies:** provider/engine SDKs, cluster clients, web frameworks, and ORMs. **Status:** protocol only. **Next milestone:** render a local, deterministic vLLM environment-file artifact with no secrets.
