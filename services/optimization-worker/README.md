# Optimization Worker

**Purpose:** future control-plane-side composition point for optimization planning. **Responsibilities:** eventually invoke optimizer ports using versioned inputs and produce versioned outputs. **Non-responsibilities:** inference execution, GPU access, engine lifecycle, database choice, queues, or algorithms today. **Allowed dependencies:** common, schemas, and optimizer abstractions. **Future:** execution infrastructure will be chosen only after real workload and reliability requirements exist.
