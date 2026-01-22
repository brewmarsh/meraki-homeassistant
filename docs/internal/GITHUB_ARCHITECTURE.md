## 📋 Requirements: Modular GitHub Actions Architecture

### 1. Structure and Modularity

- **Directory Layout:** All reusable logic must reside in `.github/workflows/_reusable-*.yml`.
- **Dry Principle:** No workflow should manually set up Python or dependencies more than once. Use a single "base" setup workflow.
- **Matrix Execution:** Linting and HACS validation should run in parallel to reduce total CI time.

### 2. Parallelization Strategy

- **Split Linting:** Run `ruff` (formatting/linting) and `hassfest` (HA validation) as separate parallel jobs within the same workflow.
- **Targeted Matrix:** Validate against Python **3.13** (the 2026.1 standard) while maintaining a legacy check for **3.12** if necessary.

### 3. Agent-Native Integration (The "Jules" Guardrail)

- **Reflective Loop:** Jules must run a "Pre-flight Check" (compilation and linting) _before_ creating a PR.
- **Automated Cleanup:** Every Jules PR must include the "Fixes #<number>" tag in the first line of the description.

---

## 🛠 Implementation Steps for Jules

### Step 1: Create Reusable CI Base

**File:** `.github/workflows/_reusable-ci-base.yml`

- Define a `workflow_call` that accepts inputs for `python-version`.
- Encapsulate: Python setup, caching, and installation of `requirements_dev.txt`.
- **Benefit:** Centralizes environment management.

### Step 2: Implement Parallel Linting & HACS Validation

**File:** `.github/workflows/validate.yml`

- Create a job `lint` and a job `hassfest` that both `need` the repo checkout.
- Use a matrix strategy for `python-version: [3.12, 3.13]`.
- Integrate the HACS Action (`hacs/action@main`) to ensure repository compliance.

### Step 3: Refactor the Cognitive Loop

**File:** `.github/workflows/agent-cognitive-loop.yml`

- Add a **"Pre-flight"** step after the `jules-invoke` call.
- If `ruff check` or `python -m compileall` fails on the agent's branch, use the `gh` CLI to post a comment on the issue and halt the PR creation.
- Update the `base_branch` to be a dynamic input that defaults to `beta`.

### Step 4: Centralize Deployment Logic

**File:** `.github/workflows/_reusable-deploy.yml`

- Move the `bump-my-version` and HACS deployment logic here.
- Add a parameter for `release_type` (beta vs. stable).

---

## 🧪 Verification Tasks for Jules

1. **Run `gh workflow run validate.yml --ref beta**` and ensure the parallel jobs finish in under 2 minutes.
2. **Verify JSON Integrity:** Ensure `manifest.json` does not have trailing commas.
3. **Check Audit Trail:** Confirm that the first PR created with this new system correctly links to its source issue.
