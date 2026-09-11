# Agent command security

Agents accept only versioned, allowlisted command types over a future authenticated outbound channel. Commands include job/attempt identity, expiry, and idempotency key; leases and reconciliation tolerate at-least-once delivery. Agent credentials are separate from provider provisioning credentials, narrowly scoped, rotatable, and revocable.

Arbitrary remote shell execution is prohibited. Future subprocess invocation uses validated executables and typed argument vectors. Workspaces are isolated per job; cancellation, timeout, cleanup, and diagnostics are explicit. Diagnostic bundles are redacted and previewable before upload. No transport, credential, or process execution exists today.
