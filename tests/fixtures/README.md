# Test fixtures

Only small synthetic, non-customer, non-secret fixtures may be stored here. Model weights, prompts, outputs, provider payloads, and binary capsule artifacts are prohibited.

`contracts/v1/` is the first golden-fixture set for shared JSON contracts. The
individual files retain their independent `schema_version`; the directory name
identifies the fixture set rather than forcing every contract to share one
version.
