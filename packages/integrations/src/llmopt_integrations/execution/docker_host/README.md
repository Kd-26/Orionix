# Docker host execution

This adapter will eventually run an allowlisted image and typed arguments on a customer-controlled Docker host. It may depend on integration ports and a reviewed optional Docker client. It must not accept arbitrary shell strings, own provider provisioning, or leak Docker SDK objects. Socket access is a privileged trust boundary. Status: no Docker access. Next milestone: define the certified image and argument allowlist.
