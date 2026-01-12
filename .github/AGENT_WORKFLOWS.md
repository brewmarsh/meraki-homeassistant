# Agent Workflow Documentation

This document describes the automated AI agent workflows used in this repository for issue handling, code review, and self-healing CI.

## Overview

We use two AI agents:

- **Jules** (Google Labs) - Primary coding agent for implementing features and fixing bugs
- **Cursor** - Code review agent for quality assurance and validation

Both agents can be assigned issues directly:

- Label an issue with `jules-issue` → Jules handles it
- Label an issue with `cursor-work` → Cursor handles it directly (bypasses Jules)

## Workflow Diagram

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AGENT WORKFLOW                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

   ┌──────────┐
   │  ISSUE   │ ← User creates issue with label: jules-issue
   └────┬─────┘
        │
        ▼
┌───────────────────┐
│ jules-issue-      │ Triggers on: issues.labeled (jules-issue)
│ handler.yaml      │ Action: Launches Jules agent
└────────┬──────────┘
         │
         ▼
   ┌──────────────┐
   │ Jules Agent  │ Works on the issue, creates branch
   │ (Google Labs)│ e.g., bugfix/dashboard-fix-59-abc123
   └──────┬───────┘
          │
          ├──────────────────────────────────────────┐
          │                                          │
     JULES COMPLETES                          JULES GETS STUCK
          │                                          │
          ▼                                          ▼
   ┌──────────────┐                        ┌───────────────────┐
   │ Jules PR     │                        │ Jules creates PR  │
   │ Created      │                        │ + adds label:     │
   │              │                        │ jules-needs-help  │
   │ Targets: beta│                        │ + help comment    │
   └──────┬───────┘                        └────────┬──────────┘
          │                                         │
          │                                         ▼
          │                              ┌───────────────────┐
          │                              │ jules-needs-      │
          │                              │ help.yaml         │
          │                              │                   │
          │                              │ • Extracts help   │
          │                              │   request context │
          │                              │ • Invokes Cursor  │
          │                              │   with progress   │
          │                              │ • Adds label:     │
          │                              │   cursor-reviewing│
          │                              └────────┬──────────┘
          │                                       │
          │                                       ▼
          │                              ┌───────────────────┐
          │                              │ Cursor continues  │
          │                              │ from Jules'       │
          │                              │ progress          │
          │                              │                   │
          │                              │ Pushes to same    │
          │                              │ Jules branch      │
          │                              └────────┬──────────┘
          │                                       │
          │◄──────────────────────────────────────┘
          │
          ▼
┌───────────────────┐
│ jules-pr-         │ Triggers on: pull_request.opened
│ linker.yaml       │ Action: Links PR to issue, updates labels
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ beta-ci.yaml      │ Triggers on: pull_request (branches-ignore: main)
│                   │ Runs: lint, type-check, tests, frontend build
└────────┬──────────┘
         │
         ├─────────────────────────────────────────┐
         │                                         │
    CI FAILS                                  CI PASSES
         │                                         │
         ▼                                         ▼
┌───────────────────┐                    ┌───────────────────┐
│ jules-ci-fix.yaml │                    │ cursor-launcher   │
│ (or cursor-fix    │                    │ .yaml             │
│  if cursor-       │                    │                   │
│  reviewing label) │                    │ • Adds label:     │
│                   │                    │   cursor-reviewing│
│ • Gets error logs │                    │ • Creates branch: │
│ • Invokes agent   │                    │   cursor-review/* │
│   with errors     │                    │ • Cursor creates  │
│ • Agent pushes    │                    │   PR → Jules      │
│   fix             │                    │   branch          │
│ • Max attempts:   │                    └────────┬──────────┘
│   Jules=3→handoff │                             │
│   Cursor=10→human │                             │
└────────┬──────────┘                             │
         │                                        ▼
         │ (loops until pass              ┌──────────────┐
         │  or escalation)                │ Cursor PR    │
         │                                │ Created      │
         │                                └──────┬───────┘
         │                                       │
         │                                       ▼
         │                              ┌───────────────────┐
         │                              │ beta-ci.yaml      │
         │                              │ (runs on Cursor   │
         │                              │  PRs too)         │
         │                              └────────┬──────────┘
         │                                       │
         │                    ┌──────────────────┴──────────────────┐
         │                    │                                     │
         │               CI FAILS                              CI PASSES
         │                    │                                     │
         │                    ▼                                     ▼
         │         ┌───────────────────┐              ┌───────────────────┐
         │         │ cursor-fix.yaml   │              │ cursor-fix.yaml   │
         │         │                   │              │                   │
         │         │ • Invokes Cursor  │              │ • Auto-merge      │
         │         │   to fix errors   │              │   Cursor PR into  │
         │         │ • Max 10 attempts │              │   Jules branch    │
         │         │ • Then escalate   │              │ • Delete cursor-  │
         │         │   to human        │              │   review/* branch │
         │         └────────┬──────────┘              │ • Add labels:     │
         │                  │                         │   cursor-reviewed │
         │                  │                         │   ready-for-review│
         │                  │ (loops until pass)      └────────┬──────────┘
         │                  └──────────► CI PASSES ────────────┘
         │                                                     │
         └──────────────────► CI PASSES ───────────────────────┘
                                                               │
                                                               ▼
                                                    ┌──────────────────┐
                                                    │ READY FOR HUMAN  │
                                                    │ REVIEW           │
                                                    └────────┬─────────┘
                                                             │
                                                             ▼
                                                    ┌──────────────────┐
                                                    │ Human reviews    │
                                                    │ and merges to    │
                                                    │ beta             │
                                                    └────────┬─────────┘
                                                             │
                                                             ▼
                                               ┌───────────────────────┐
                                               │ beta-version-update   │
                                               │ .yaml                 │
                                               │                       │
                                               │ • Delete Jules branch │
                                               │ • Update issue labels │
                                               │ • Bump version        │
                                               │ • Create release      │
                                               └───────────────────────┘
```

## Workflow Files

| Workflow                       | Trigger                           | Purpose                             |
| ------------------------------ | --------------------------------- | ----------------------------------- |
| `jules-issue-handler.yaml`     | Issue labeled `jules-issue`       | Launch Jules to work on issue       |
| `cursor-issue-handler.yaml`    | Issue labeled `cursor-work`       | Launch Cursor directly on issue     |
| `jules-pr-linker.yaml`         | PR opened by any agent            | Link PR to issue, update labels     |
| `jules-ci-fix.yaml`            | Beta CI fails on Jules PR         | Self-heal: Jules fixes CI errors    |
| `jules-needs-help.yaml`        | PR labeled OR repository_dispatch | Handoff: Jules asks Cursor for help |
| `cursor-launcher.yaml`         | Beta CI passes on Jules PR        | Launch Cursor for code review       |
| `cursor-fix.yaml`              | Beta CI on Cursor PR              | Handle Cursor PR: fix or merge      |
| `ready-for-review-merger.yaml` | CI passes + ready-for-review      | Auto-merge reviewed PRs             |
| `beta-ci.yaml`                 | PR to any branch except main      | Run all CI checks                   |
| `beta-version-update.yaml`     | PR merged to beta                 | Cleanup, version bump, release      |

**Note:** `jules-pr-linker.yaml` handles BOTH Jules and Cursor PRs. It detects the agent type from the branch name or author.

## Labels

| Label                | Color  | Meaning                            |
| -------------------- | ------ | ---------------------------------- |
| `jules-issue`        | Purple | Issue assigned to Jules            |
| `cursor-work`        | Blue   | Issue assigned directly to Cursor  |
| `status: todo`       | Gray   | Task not yet started               |
| `in-progress`        | Yellow | Agent is working on this           |
| `pr-pending`         | Green  | PR created, awaiting CI/review     |
| `jules-needs-help`   | Orange | Jules got stuck, requesting Cursor |
| `cursor-reviewing`   | Blue   | Cursor is reviewing the PR         |
| `cursor-ci-fixed`    | Blue   | Cursor fixed CI, now reviewing     |
| `cursor-reviewed`    | Green  | Cursor completed review            |
| `ready-for-review`   | Green  | Ready for human review             |
| `needs-human-review` | Red    | Escalated - agent couldn't fix     |
| `released-beta`      | Green  | Merged and released in beta        |

## Branch Naming

| Pattern                        | Created By | Targets      |
| ------------------------------ | ---------- | ------------ |
| `bugfix/*-{issue}-*`           | Jules      | `beta`       |
| `feat/*-{issue}-*`             | Jules      | `beta`       |
| `cursor-review/{jules-branch}` | Cursor     | Jules branch |

## Escalation Thresholds

- **Jules**: 3 CI fix attempts before handing off to Cursor
- **Cursor**: 10 fix attempts before escalating to human (Cursor is more capable)

### Handoff Flow (CI Failures)

1. **Jules attempts 1-3**: Jules tries to fix CI failures via Jules API
2. **Attempt 3+ fails**: Jules hands off to Cursor permanently
   - `cursor-reviewing` label added (prevents Jules from running again)
   - Cursor invoked via API to take over
3. **Cursor handles remaining attempts (up to 10)**: Cursor works on the same branch
   - Cursor self-corrects and pushes fixes
   - Once CI passes, Cursor's changes are merged
4. **If Cursor fails 10+ times**: `cursor-fix.yaml` escalates to human
   - `needs-human-review` label added
   - Comment posted requesting manual intervention

### Proactive Help Request (Jules Gets Stuck)

Jules is instructed to **never stop working without creating a PR**. If Jules encounters difficulties:

1. **Jules creates PR** with current progress (even if incomplete)
2. **Jules adds `jules-needs-help` label** to the PR
3. **Jules comments** with structured help request:

```markdown
## 🆘 Jules Needs Cursor Help

**Where I Got Stuck:**
<Describe the specific problem>

**What I've Tried:**
<List approaches attempted>

**Current Progress:**
<What's done vs remaining>

**Files Changed:**
<Key files modified>

**Suggested Next Steps:**
<What Cursor should try>
```

4. **`jules-needs-help.yaml` triggers** and:

   - Extracts context from Jules' help comment
   - Gathers CI error logs if available
   - Lists files Jules modified
   - Invokes Cursor with full context
   - Changes label to `cursor-reviewing`

5. **Cursor continues from Jules' progress**:
   - Pushes fixes to the same Jules branch
   - CI runs on the updated code
   - `cursor-fix.yaml` handles subsequent CI results

This ensures work is **never lost** when Jules gets stuck. Cursor receives:

- Original issue requirements
- Jules' progress and code changes
- Specific problems Jules encountered
- CI error logs (if any)

**Important**: Once `cursor-reviewing` label is added, Jules is completely out of the loop. Only Cursor and humans can work on it.

**Note**: Cursor agents automatically fix their own failures and push again. The workflow waits for CI to pass, then auto-merges.

## Agent Protections

To prevent agents from interfering with each other:

1. **Jules skips** if:

   - PR has `cursor-reviewing` label (Cursor has taken over)
   - Branch is `cursor-review/*` (not a Jules PR)

2. **Cursor skips** if:
   - PR already has `cursor-reviewed` label
   - Branch is not `cursor-review/*` (for fix workflow)

---

## GITHUB_TOKEN Limitation

**Important:** GitHub Actions triggered by `GITHUB_TOKEN` do NOT trigger other workflows. This is a security feature to prevent infinite loops.

### Impact

When a workflow adds a label using `GITHUB_TOKEN`:

```bash
gh pr edit <PR#> --add-label "jules-needs-help"  # Won't trigger other workflows!
```

The `pull_request: [labeled]` event won't trigger other workflows.

### Solution: repository_dispatch

We use `repository_dispatch` to directly trigger workflows:

```bash
# This DOES trigger the jules-needs-help workflow
gh api repos/{owner}/{repo}/dispatches \
  --method POST \
  -f event_type='jules-needs-help' \
  -f client_payload[pr_number]='123' \
  -f client_payload[branch]='feature/my-branch' \
  -f client_payload[issue_number]='456'
```

### Workflows Using repository_dispatch

| Workflow                | Event Type         | Triggered By                       |
| ----------------------- | ------------------ | ---------------------------------- |
| `jules-needs-help.yaml` | `jules-needs-help` | `jules-ci-fix.yaml`, Jules prompts |

### Agent Prompts

When telling Jules to hand off to Cursor, the prompt instructs Jules to:

1. Add the label (for visibility): `gh pr edit <PR#> --add-label "jules-needs-help"`
2. Trigger the workflow: `gh api repos/.../dispatches -f event_type='jules-needs-help' ...`

Both are required because the label alone won't trigger the workflow.

## CI Error Handling

Both agents receive detailed CI error information:

```yaml
# Error logs are captured and sent to agents
gh run view "$RUN_ID" --log-failed | tail -300 > ci_errors.txt

# Included in agent prompt:
## CI Error Logs
${CI_ERRORS}
```

## Issue Updates

Both agents update the linked issue with progress:

- When CI starts
- When agent starts fixing
- Each fix attempt with details
- When review completes
- When escalation occurs
- When merged to beta

## Environment

| Setting         | Value                         |
| --------------- | ----------------------------- |
| Python Version  | 3.13.2                        |
| Node Version    | 20                            |
| Package Manager | uv (not pip/requirements.txt) |

### Running Checks

**Use `./run_checks.sh`** to run all checks at once:

```bash
./run_checks.sh
```

This script runs:

1. `uv sync` - Install/sync dependencies
2. `uv run ruff check` - Linting
3. `uv run ruff format --check` - Format check
4. `uv run bandit` - Security check
5. `uv run mypy` - Type checking
6. `uv run pytest` - Tests

**Or run individually:**

```bash
uv run ruff check --fix .     # Fix linting issues
uv run ruff format .          # Fix formatting
uv run mypy custom_components/meraki_ha/ tests/
uv run pytest -x              # Stop on first failure
```

**Frontend (if changed):**

```bash
cd custom_components/meraki_ha/www && npm run build
```

## Testing Notes

**IMPORTANT**: Home Assistant is NOT installed in the CI/test environment.

Tests use `pytest-homeassistant-custom-component` which provides:

- Mock `hass` fixture for Home Assistant core
- Mock `mock_config_entry` for configuration entries
- Proper async event loop handling

### Common Import Error

```text
ImportError while loading conftest '/app/tests/conftest.py'.
tests/conftest.py:8: in <module>
    from tests.const import MOCK_ALL_DATA
tests/const.py:7: in <module>
    from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork
custom_components/meraki_ha/__init__.py:7: in <module>
    from homeassistant.config_entries import ConfigEntry
E   ModuleNotFoundError: No module named 'homeassistant'
```

**Cause**: Importing from `custom_components/meraki_ha/` triggers `__init__.py` which imports `homeassistant`.

**Import chain**:

```text
tests/conftest.py → tests/const.py → custom_components/meraki_ha/types.py
                                      ↓ (triggers __init__.py)
                    custom_components/meraki_ha/__init__.py → homeassistant ❌
```

**Solutions** (in order of preference):

1. Ensure `uv sync` was run - this installs `pytest-homeassistant-custom-component`
2. Use `TYPE_CHECKING` for type-only imports:

   ```python
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from custom_components.meraki_ha.types import MerakiDevice
   ```

3. Move type imports inside functions if only needed there
4. Define mock types in `tests/const.py` instead of importing from integration

## Secrets Required

| Secret           | Used By                           | Purpose                           |
| ---------------- | --------------------------------- | --------------------------------- |
| `JULES_API_KEY`  | jules-issue-handler, jules-ci-fix | Authenticate with Jules API       |
| `CURSOR_API_KEY` | cursor-launcher, cursor-fix       | Authenticate with Cursor API      |
| `GH_PAT`         | All Cursor workflows              | GitHub access for Cursor agents   |
| `GITHUB_TOKEN`   | All workflows                     | GitHub API access (auto-provided) |

### GH_PAT Setup

Cursor cloud agents run in their own environment and may not have GitHub access.
The `GH_PAT` secret allows Cursor to comment on issues, update PRs, etc.

**Note:** GitHub doesn't allow secrets starting with `GITHUB_`, so we use `GH_PAT`.

**To create:**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with these scopes:
   - `repo` (full control of private repositories)
3. Copy the token
4. Add to repository: Settings → Secrets → Actions → New repository secret
   - Name: `GH_PAT`
   - Value: Your token

The Cursor prompts include instructions to use this token if permission errors occur.

---

## Cursor Cloud Agent API

The workflows use Cursor's Cloud Agent API to launch and manage agents.

### API Documentation

- **Cloud Agent API:** <https://cursor.com/docs/cloud-agent/api/endpoints>

### How Agent Completion is Detected

We do NOT use external webhooks. Instead:

1. Cursor agents are launched with `autoCreatePr: true`
2. When the agent completes, it creates a PR
3. The PR creation triggers `jules-pr-linker.yaml` (handles both Jules and Cursor)
4. The workflow links the PR to the issue and updates labels

This approach requires no external services or webhook forwarding.

## Manual Triggers

### Cursor Launcher

Can be manually triggered to review any open PR:

```yaml
workflow_dispatch:
  inputs:
    pr_number:
      description: 'PR number to review'
      required: true
```

## Concurrency Groups

Each workflow uses concurrency groups to prevent duplicate runs:

| Workflow                  | Concurrency Group             |
| ------------------------- | ----------------------------- |
| `jules-issue-handler`     | `jules-issue-{issue_number}`  |
| `cursor-issue-handler`    | `cursor-issue-{issue_number}` |
| `jules-ci-fix`            | `jules-fix-{branch}`          |
| `jules-needs-help`        | `jules-help-{pr_number}`      |
| `cursor-launcher`         | `cursor-review-{branch}`      |
| `cursor-fix`              | `cursor-fix-{branch}`         |
| `ready-for-review-merger` | `ready-merger-{branch}`       |

---

## Agent Prompt Best Practices

The prompts sent to agents include explicit completion checklists to ensure tasks are fully completed.

### Key Elements in Every Prompt

1. **Task Context**: Issue number, repository, branch
2. **Requirements**: The actual task from the issue
3. **Step-by-Step Checklist**: Numbered steps with checkboxes
4. **Verification Command**: `./run_checks.sh`
5. **Issue Update Template**: Exact command to comment on issue
6. **PR Requirements**: What the PR must include
7. **Constraints**: What NOT to do
8. **Definition of Done**: Explicit completion criteria

### Example Prompt Structure

```text
═══════════════════════════════════════════════════════════
TASK: <title>
ISSUE: #<number>
═══════════════════════════════════════════════════════════

REQUIREMENTS:
<issue body>

═══════════════════════════════════════════════════════════
MANDATORY STEPS (Complete ALL):
═══════════════════════════════════════════════════════════

□ STEP 1: <action>
□ STEP 2: <action>
□ STEP 3: VERIFY (./run_checks.sh must pass)
□ STEP 4: UPDATE ISSUE (gh issue comment ...)
□ STEP 5: CREATE PR

═══════════════════════════════════════════════════════════
CONSTRAINTS:
- Don't skip any steps
- All tests must pass
═══════════════════════════════════════════════════════════

COMPLETION DEFINITION:
You are DONE when: <explicit criteria>
═══════════════════════════════════════════════════════════
```

### Why This Matters

Without explicit completion criteria, agents may:

- Skip running quality checks
- Not link PRs to issues
- Not comment on issues with progress
- Leave tasks partially complete

The structured prompts ensure consistent, complete task execution.
