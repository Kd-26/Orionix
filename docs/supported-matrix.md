# Support status and profile matrix

Support is evaluated independently from architecture and engine compatibility. A GPU name or reference machine never defines overall product support.

## Support states

| State | Meaning | Permitted claim |
|---|---|---|
| `ARCHITECTURALLY_SUPPORTED` | Versioned contracts can represent the environment. | Representable only; no runtime claim. |
| `ENGINE_COMPATIBLE` | The pinned engine runtime declares the complete combination usable. | Eligible for evaluation; no product certification claim. |
| `CERTIFIED` | Required compatibility, reliability, benchmark, failure-recovery, and reproducibility evidence passed and is retained. | Production-supported for the exact profile and validity window. |
| `EXPERIMENTAL` | Representable and apparently compatible, but certification is incomplete. | May run only with explicit warnings and product policy approval. |
| `UNSUPPORTED` | Known invalid, prohibited, or outside the product boundary. | Must not run. Return a specific reason. |

Discovery reports facts and evidence provenance; it does not declare support. Capability evaluation determines representability, the engine adapter determines engine compatibility, and the certification registry determines whether a versioned profile is certified. A known invalid combination is `UNSUPPORTED`; lack of certification alone does not erase architectural support.

## Day-80 target dimensions

These rows are plans, not certification claims:

| Dimension | Planned scope | Current status |
|---|---|---|
| Accelerator families | Ampere, Hopper, and Blackwell where supported by the selected runtime | Architecturally planned; no profile certified |
| GPU count/topology | Single GPU and single-node multi-GPU first; multi-node represented for later runtime | Contracts require alignment; no runtime tested |
| Engines | vLLM production first; SGLang later/beta | Adapter namespaces only |
| Local execution | Customer-owned Ubuntu/NVIDIA hosts | Boundary only |
| Hosted execution | At least one P0 provider; Runpod and JarvisLabs candidates | Boundaries only; first provider undecided |
| Serverless execution | Modal specialized adapter | P2 experimental candidate; boundary only |
| Models | A small representative set selected from customer demand | Not selected |
| Deployment | Reproducible engine/Docker export with manual approval | Metadata contract only |

## Certification unit

A support profile binds provider and execution runtime; GPU architecture/count; node count and topology; driver/CUDA/PyTorch/NCCL versions; engine image digest; model architecture and revision; precision/quantization; feature set; and workload class. Certification is invalid outside that profile and its evidence validity window.

No profiles are certified today. Example rows remain `PLANNED` until the [certification policy](operations/certification-policy.md) evidence is complete and approved.
