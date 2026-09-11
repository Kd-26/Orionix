# Integrations

**Purpose:** quarantine vendor-specific engine/provider details behind adapters. **Responsibilities:** future translation between typed Orionix contracts and supported integrations. **Non-responsibilities:** domain policy, candidate selection, orchestration state, or leaking vendor objects across package boundaries. **Allowed dependencies:** `domain`, `schemas`, and integration-specific optional extras only. **Future:** each adapter will be installed independently; the base CPU development environment includes none of them.

The namespaces are intentionally empty. No third-party code is vendored.
