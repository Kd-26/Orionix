# Orionix: First 7 Days Execution Guide

This document explains the first seven execution days for Orionix in simple,
practical language. It is written for an early-stage startup using AI agents to
help build the product.

The goal of the first week is **not** to finish the optimizer. The goal is to
create a trustworthy base so that the optimizer, website, database, payments,
and deployment can be added without repeatedly rebuilding earlier work.

## What should exist after Day 7

At the end of the first seven days, Orionix should have:

- a clear definition of the first product and first customer;
- an organized Python repository with tested package boundaries;
- shared data formats for hardware, models, workloads, jobs, and results;
- rules that reject impossible or unsupported configurations;
- one small and honest launch target;
- the first working version of the website; and
- a local Supabase database that can be recreated from migrations.

Orionix will **not** optimize a real GPU deployment by Day 7. Real GPU
discovery, vLLM execution, benchmarking, optimization, billing, and production
deployment come later in the 50-day plan.

## Current starting point

Day 1 and Day 2 work already exists in the local repository. It includes the
architecture documents and Python monorepo foundation. However, that work must
still be reviewed, committed, and pushed before Day 3 begins.

Start by running:

```bash
git status --short
make check
```

Do not start Day 3 with a confusing or unexplained working tree.

## The rule for every day

Each day must have one main outcome. A day is complete only when:

1. The planned output exists.
2. Automated tests pass.
3. The main behavior is checked manually.
4. At least one failure case is checked.
5. Documentation matches the actual implementation.
6. No secret, customer data, model weight, or generated benchmark artifact is
   accidentally committed.
7. The changes are reviewed, committed with clear messages, and pushed.
8. The next day's first task is written down.

If an important test is failing, the day is not complete. Record the failure
and fix it before moving forward.

---

## Day 1: Decide exactly what Orionix is

### Goal

Create one clear product definition that every future task follows.

### In simple words

Before building software, decide what the software promises. Orionix is a tool
that tests different ways of running an LLM and recommends a measured
configuration. It is not a new inference engine and it does not replace vLLM.

### Work to complete

- Define the first customer: a technical team running an open-weight model on
  NVIDIA GPUs.
- Write the complete customer journey, from creating a project to downloading
  a recommended configuration.
- Separate work performed by the website from work performed by the customer
  agent.
- Define the support labels:
  - **Certified:** Orionix has enough test evidence to support the combination.
  - **Experimental:** it may work, but testing is incomplete.
  - **Unsupported:** Orionix knows the combination should not run.
- Define what information is allowed to leave the customer's GPU machine.
- State that customers manually review and apply recommendations during the
  first release.
- Write the first security and launch rules.

### Important files

- `docs/product-scope.md`
- `docs/architecture/product-workflow.md`
- `docs/architecture/overview.md`
- `docs/security/customer-data-boundaries.md`
- `docs/operations/launch-gates.md`
- `docs/supported-matrix.md`

### Do not build today

- GPU code
- vLLM launching
- website pages
- database tables
- authentication
- payments

### Manual checks

- Read the product definition as if you were a customer. Is the result clear?
- Pick one example customer and follow every step of the written workflow.
- Check that every step names who performs it: browser, control plane, agent,
  or GPU environment.
- Search the documentation for claims that every GPU or model is supported.
  Remove such claims unless test evidence exists.

### Day 1 is complete when

- [ ] The first customer is clearly described.
- [ ] The product promise and non-goals are clear.
- [ ] Every customer-workflow step has an owner.
- [ ] Certified and experimental support are not confused.
- [ ] Sensitive customer data stays on the customer side by default.
- [ ] Documentation checks pass.
- [ ] Changes are reviewed, committed, and pushed.

### Startup task

Write a two-sentence explanation of Orionix that a potential customer can
understand. Speak to at least one inference or platform engineer and ask
whether this problem is painful enough to pay for.

---

## Day 2: Organize the codebase

### Goal

Make every major part of Orionix importable and keep unrelated parts from
becoming tightly connected.

### In simple words

Think of the repository as a building. Day 2 creates labeled rooms for the
optimizer, benchmark runner, GPU discovery, agent, command-line tool, and
control plane. The rooms are mostly empty, but the doors and dependency rules
are clear.

This prevents a future change to vLLM from breaking the database or product
contracts.

### Work to complete

- Use Python 3.12 and one `uv` workspace.
- Keep one lockfile for repeatable dependency installation.
- Ensure every Python package can be imported.
- Add typed-package markers so type information is included in builds.
- Document what each package owns and what it may import.
- Keep CUDA, vLLM, cloud-provider SDKs, and GPU libraries optional.
- Add tests that detect forbidden dependency directions.
- Add a smoke test that imports every package on a machine without a GPU.
- Provide one command that runs formatting, linting, type checking, tests,
  packaging, and documentation checks.

### Important command

```bash
make check
```

This should work without CUDA, an NVIDIA GPU, model weights, cloud credentials,
or Docker.

### Do not build today

- Real package behavior
- GPU discovery
- Cloud provisioning
- Networking between the agent and control plane
- vLLM execution
- Database or UI behavior

### Manual checks

- Create a clean environment and install the workspace.
- Import every package from a Python shell.
- Build every distribution and confirm type markers are included.
- Deliberately add one forbidden import locally and verify the dependency test
  catches it. Revert that deliberate test change afterwards.

### Day 2 is complete when

- [ ] Clean installation succeeds.
- [ ] All packages import without a GPU.
- [ ] Dependency boundaries are documented and tested.
- [ ] `make check` passes.
- [ ] Package builds pass.
- [ ] No runtime feature is falsely described as implemented.
- [ ] Changes are reviewed, committed, and pushed.

### Startup task

Create a simple list of the three riskiest technical assumptions, such as
access to suitable GPUs, vLLM version compatibility, and whether customers will
install an agent on their machines.

---

## Day 3: Create the shared data formats

### Goal

Implement the first version of the information that Orionix components exchange.

### In simple words

The website, agent, benchmark runner, and optimizer need to agree on what words
such as “GPU environment,” “workload,” and “optimization job” mean. Day 3 turns
those meanings into versioned Python models and JSON examples.

These are data definitions, not the real GPU or optimization behavior.

### Data formats to add

Keep the first version small. Create formats for:

- **GPU:** vendor, model, architecture, memory, supported number formats, and a
  redacted identifier.
- **Machine:** CPU, RAM, storage, operating system, GPU list, and runtime.
- **Cluster:** machines, GPU count, topology, networking, and provider details.
- **Software environment:** driver, CUDA, PyTorch, NCCL, engine version, and
  container-image digest.
- **Model:** model identifier, exact revision, architecture, size, precision,
  quantization, context length, and tokenizer fingerprint.
- **Workload:** prompt lengths, output lengths, concurrency, request rate, and
  streaming behavior.
- **Requirements:** latency, throughput, quality, time, GPU-hour, and cost
  limits.
- **Optimization job:** requested inputs, state, timestamps, and owner.
- **Candidate configuration:** one possible engine configuration and the reason
  it was generated.
- **Benchmark result:** measurements, errors, environment fingerprint, and
  artifact references.
- **Recommendation:** winning candidate, alternatives, evidence, and warnings.
- **Execution Capsule:** everything needed to understand and reproduce a result.

Every saved format must contain a schema version.

### Suggested task order

1. Write one small valid JSON example for each format.
2. Implement the typed Python model.
3. Load the JSON into the Python model.
4. Convert the Python model back to JSON.
5. Add invalid examples and verify they are rejected.
6. Document which package owns each format.

### Do not build today

- Actual hardware inspection
- A running agent
- Database tables
- Optimizer algorithms
- vLLM commands

### Manual checks

- Change a GPU memory value to a negative number. It must be rejected.
- Remove the schema version. It must be rejected.
- Use an unknown future GPU architecture. It should be representable without
  pretending it is certified.
- Load and save every golden JSON example and compare the result.
- Confirm older data will not silently be interpreted using a newer meaning.

### Day 3 is complete when

- [ ] The first shared formats exist and are versioned.
- [ ] Valid examples load successfully.
- [ ] Invalid examples fail with understandable messages.
- [ ] JSON round-trip tests pass.
- [ ] Unknown future hardware can be represented safely.
- [ ] No format imports vLLM, CUDA, database, or web-framework code.
- [ ] `make check` passes.
- [ ] Changes are reviewed, committed, and pushed.

### Startup task

Ask one potential customer what information they can safely share about their
models and machines. Record what must remain private or be redacted.

---

## Day 4: Build the rules that reject bad configurations

### Goal

Create the first compatibility and candidate-filtering rules.

### In simple words

Orionix should never try every vLLM option. Most combinations are impossible,
unsafe, too expensive, or irrelevant. Day 4 builds the rule system that removes
bad choices before any GPU time is spent.

The rules operate on supplied test data today. Real discovery and vLLM execution
come later.

### Work to complete

- Create a versioned engine-capability record for one future pinned vLLM
  version.
- Define a common result for every rule:
  - allowed;
  - rejected;
  - unknown and therefore experimental.
- Give every rejection a short reason and a stable reason code.
- Add rules for:
  - insufficient GPU memory;
  - unsupported GPU architecture;
  - unsupported precision;
  - unsupported quantization;
  - model context exceeding the engine limit;
  - an invalid tensor-parallel GPU count;
  - a parallelism choice that does not match the topology;
  - a configuration exceeding the customer's time or cost budget;
  - a feature not supported by the pinned engine version;
  - speculative decoding without a compatible draft model;
  - expert parallelism requested for a non-MoE model.
- Keep “engine compatible” separate from “certified by Orionix.”
- Add tests for allowed, rejected, and unknown results.

### Example

```text
Input:
  Model requires about 50 GB after safety margin
  Available GPU memory is 24 GB

Output:
  Rejected
  Reason code: INSUFFICIENT_GPU_MEMORY
  Message: Estimated model and cache memory exceed available GPU memory.
```

### Do not build today

- A full optimization search
- Actual GPU memory profiling
- Real vLLM commands
- Speculative decoding execution
- Multi-node execution

### Manual checks

Create at least these five deliberately bad examples:

1. A model that does not fit in GPU memory.
2. FP8 requested on incompatible hardware.
3. Tensor parallelism requesting more GPUs than exist.
4. Speculative decoding without a compatible draft model.
5. An unknown vLLM feature.

Run each example and read the rejection as a customer would. The explanation
must be useful and must not expose internal secrets.

### Day 4 is complete when

- [ ] Every candidate receives allowed, rejected, or experimental status.
- [ ] Rejections include stable codes and useful explanations.
- [ ] Engine compatibility and Orionix certification remain separate.
- [ ] Invalid candidates are rejected before execution.
- [ ] Rule tests cover success, failure, and unknown information.
- [ ] `make check` passes.
- [ ] Changes are reviewed, committed, and pushed.

### Startup task

Show example rejection messages to one potential user. Ask whether the message
tells them what to fix without requiring an Orionix engineer to explain it.

---

## Day 5: Choose the exact beta launch target

### Goal

Turn the broad product idea into one small Day-50 launch promise.

### In simple words

Orionix may eventually support many models, GPUs, engines, and cloud providers.
Trying to certify all of them in 50 days will prevent launch. Day 5 chooses one
working path that can be tested deeply and sold honestly.

### Decisions to make

Choose and record:

- one pinned vLLM release or container image;
- one first model and exact model revision;
- one first NVIDIA GPU profile that is actually available for testing;
- one GPU count, preferably one GPU first;
- one first execution target, preferably a local/customer Ubuntu machine;
- one hosted provider to add after the local path works;
- one sample workload;
- the first latency and throughput requirements;
- the maximum GPU-hour and financial budget for one optimization job;
- one simple subscription plan or invite-only trial;
- whether the Day-50 beta will be free, paid, or design-partner only.

Do not select hardware that cannot be accessed repeatedly. A technically ideal
GPU is not a useful reference environment if it is unavailable or too costly to
test.

### Startup accounts to prepare

- GitHub organization and private repository access
- Vercel account for development previews
- Two Supabase projects: development and production
- Stripe test-mode account
- Domain-name shortlist
- Production email/SMTP provider shortlist
- One GPU-provider account or an available customer-owned GPU

If the company is based in India, check Stripe account eligibility on Day 5.
Do not wait until the payment-integration week because new Indian Stripe
accounts may require an invitation.

### Documents to produce

- A one-page beta promise
- A one-page certified-profile candidate
- A monthly development and production budget
- A list of launch features
- A separate list of experimental and postponed features
- A short pricing hypothesis
- A list of decisions that still need customer evidence

### Manual checks

- Confirm that the selected GPU can actually be rented or accessed.
- Confirm that the selected model license permits the planned use.
- Confirm that the vLLM version supports the chosen model and GPU combination.
- Calculate the worst-case cost of 20 failed experiments.
- Explain the beta promise aloud without using “all models,” “all GPUs,” or
  “fully automatic.”

### Day 5 is complete when

- [ ] One exact beta path is selected.
- [ ] Hardware access and budget are confirmed.
- [ ] Launch, experimental, and postponed features are separated.
- [ ] Payment-provider eligibility has been checked.
- [ ] The marketing promise matches the planned test evidence.
- [ ] Open decisions have owners and deadlines.
- [ ] Changes are reviewed, committed, and pushed.

### Startup task

Contact at least five relevant people. Try to schedule two short discovery calls
for the following week. Ask what they run today, their largest inference cost or
performance problem, and what evidence they would need before trusting a tool's
recommendation.

---

## Day 6: Start the website

### Goal

Create the first clean, deployable Next.js website and application shell.

### In simple words

Day 6 creates the pages and navigation customers will use. Most buttons will
not perform real optimization yet. The purpose is to establish the product
flow, visual structure, and deployment process early.

### Pages to create

Public pages:

- Home
- Product
- Pricing
- Documentation placeholder
- Security
- Contact
- Login
- Privacy
- Terms

Application pages:

- Onboarding
- Dashboard
- Projects
- Project details
- Agents
- Environments
- Workloads
- Optimization jobs
- Job results
- Billing settings

The application pages may show clearly labeled example or empty states. They
must not pretend that real optimization has happened.

### Work to complete

- Create the Next.js App Router application under `apps/web`.
- Use TypeScript.
- Add a simple shared layout, colors, typography, buttons, forms, tables, empty
  states, loading states, and error messages.
- Add mobile and desktop navigation.
- Add a clear call to action, such as “Request beta access.”
- Add environment-variable validation.
- Add a health route.
- Add basic unit or component tests.
- Connect the repository to a Vercel preview project.
- Keep development and production environment variables separate.

### Security rules

- Only variables intentionally prefixed for browser use may reach the browser.
- Never put a Supabase secret key, Stripe secret, or agent signing key into a
  public environment variable.
- Never display customer model identifiers or machine details on public pages.

### Manual checks

- Open every page and click every navigation link.
- Test common mobile and desktop widths.
- Use the keyboard to navigate forms and buttons.
- Verify that missing environment variables cause a clear startup error.
- Inspect the browser bundle and network requests for exposed secrets.
- Open the Vercel preview URL on a second device.
- Check that unfinished features are labeled as unavailable or coming later.

### Day 6 is complete when

- [ ] The website builds successfully.
- [ ] Public and application routes render.
- [ ] Mobile navigation works.
- [ ] Empty, loading, and error states exist.
- [ ] No secret appears in the browser.
- [ ] Automated frontend tests pass.
- [ ] A Vercel preview deployment succeeds.
- [ ] Changes are reviewed, committed, and pushed.

### Startup task

Show the home page to three people for ten seconds, then hide it and ask what
they think Orionix does. Rewrite the main heading if the answers are unclear.

---

## Day 7: Set up the database safely

### Goal

Create the first Supabase database structure for users, organizations, and
projects.

### In simple words

The database will eventually store customers, jobs, benchmark summaries,
recommendations, billing state, and audit records. Day 7 starts only with the
identity and project foundation.

Authentication behavior is completed on Day 9 of the full plan. Day 7 prepares
the database correctly so authentication can be added safely.

### Tables to create today

- `profiles`
- `organizations`
- `organization_members`
- `projects`
- `audit_events`

Every table should have:

- a stable primary key;
- creation and update timestamps where appropriate;
- clear ownership;
- required foreign keys;
- indexes for common lookups; and
- a documented deletion rule.

### Work to complete

- Install and configure the Supabase local-development tools.
- Create a migration for every schema change.
- Add seed data only for local development and tests.
- Enable row-level security on every exposed table.
- Give signed-in users only the operations they need.
- Add separate policies for reading, creating, updating, and deleting.
- Add database tests proving organization separation.
- Generate TypeScript database types for the website.
- Document how to rebuild the database from zero.
- Document how future production migrations will be applied and rolled back.

### Important security rule

A normal browser user must never be able to read or change another
organization's data. Server secret keys bypass normal row-level protection and
must stay only in protected server environments.

### Manual checks

Create two test users and two organizations:

1. User A creates Organization A and Project A.
2. User B creates Organization B and Project B.
3. User A attempts to read Project B.
4. User A attempts to update Project B.
5. User A attempts to delete Project B.
6. All three attempts must fail.
7. User A must still be able to work with Project A.

Then delete the local database, recreate it only from migrations, and rerun the
tests.

### Do not build today

- Optimization-job tables
- Benchmark metric storage
- Stripe subscriptions
- Agent tokens
- Production data
- A custom authentication system

### Day 7 is complete when

- [ ] A fresh local Supabase database starts successfully.
- [ ] All schema changes are represented by migrations.
- [ ] Core identity and project tables exist.
- [ ] Row-level security is enabled and tested.
- [ ] Cross-organization access fails for read and write operations.
- [ ] The database can be destroyed and rebuilt from migrations.
- [ ] Generated TypeScript types match the database.
- [ ] No production secret or customer data is committed.
- [ ] Database tests and `make check` pass.
- [ ] Changes are reviewed, committed, and pushed.

### Startup task

Write down exactly what customer information Orionix truly needs. Do not store
extra company, model, workload, or infrastructure data merely because it may be
useful later.

---

## End-of-week review

At the end of Day 7, perform one combined review.

### Product review

- Can a new person explain what Orionix does after reading the home page?
- Is one exact beta customer and use case selected?
- Are launch claims narrower than or equal to planned certification evidence?

### Engineering review

- Does `make check` pass?
- Does the web application build and deploy to preview?
- Can the database be recreated from migrations?
- Can packages install and import without a GPU?
- Are contracts versioned and tested?
- Do compatibility rules reject deliberately invalid examples?

### Security review

- Are secrets absent from Git and the browser bundle?
- Does User A fail to access Organization B?
- Is customer-sensitive information excluded or redacted by default?

### Business review

- Were at least five potential customers contacted?
- Were at least two discovery calls requested?
- Were the largest technical and business assumptions recorded?
- Is the expected GPU and hosting cost understood?

### Week 1 release gate

Proceed to Day 8 only when all of the following are true:

- [ ] Day 1 and Day 2 local changes are committed and pushed.
- [ ] The first seven days have clear evidence.
- [ ] The repository has no unexplained changes.
- [ ] The full CPU quality gate passes.
- [ ] The website preview is accessible.
- [ ] The local database rebuild and isolation tests pass.
- [ ] No critical security or product-scope question is being hidden.

## Simple daily agent prompt

Use this structure when asking an AI agent to perform a day:

```text
Complete Day N from docs/development/first-seven-days.md.

Read all repository instructions and the documents linked by that day first.
Inspect and preserve existing work. Before editing, report the current state,
the day's exact goal, and the files expected to change.

Implement only that day's scope. Add success and failure tests. Perform the
manual checks that can be automated, run make check, review the final diff, and
report each Day N completion checkbox as passed, failed, or blocked. Do not
claim the day is complete while a required checkbox is failed or unverified.
Do not commit or push unless I explicitly request it.
```

Keeping commit and push authorization separate makes it possible to inspect the
work before it becomes repository history.
