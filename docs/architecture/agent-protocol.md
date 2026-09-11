# Agent protocol

The future agent initiates an authenticated outbound connection, enrolls once, rotates narrowly scoped credentials, reports versioned capabilities/heartbeats, and claims work using expiring leases. Commands use the allowlisted `AgentCommandType` enum, expiry, attempt identity, and idempotency key. Results and append-only state transitions tolerate at-least-once delivery; reconciliation resolves expired leases and missing acknowledgements.

Arbitrary remote shell execution is prohibited. Engine launches use a separately validated executable and argument vector. Cancellation, timeout, isolated workspaces, cleanup, and redacted diagnostics are explicit command paths. Transport, authentication, enrollment, and networking are not implemented.
