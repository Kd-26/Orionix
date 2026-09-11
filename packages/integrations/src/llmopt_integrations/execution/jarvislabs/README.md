# JarvisLabs execution

VM or bare-metal mode may use the normal host-agent plus Docker model; managed-run mode may colocate the agent and engine in one prepared environment. Pause/resume always produces a new environment fingerprint. Provider API credentials remain separate from agent credentials, and automatic time/cost shutdown will be required before production use.

Provider SDK types remain inside this adapter. Status: schemas/docs only; no CLI/SDK/API dependency or call. Next milestone: specify lifecycle reconciliation and shutdown invariants using a fake provider.
