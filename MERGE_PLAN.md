# Pull Request Merge Plan

This document outlines the analysis and proposed merge sequence for the open pull requests targeting the `beta` branch.

**Blocker:** The repository currently has the `node_modules` directory committed to its history. This prevents `git` operations like `rebase` from completing successfully. Before this plan can be executed, a repository administrator must remove this directory from the git history.

**Recommended Action to Unblock:**

1. A user with push access to the repository needs to run the following command:
   ```bash
   git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch node_modules' --prune-empty --tag-name-filter cat -- --all
   ```
2. After running the command, the user will need to force-push the changes to the repository to update all branches.

---

## Preliminary Merge Status Report

### High-Conflict Groups (Require Manual Intervention)

- **Dataclass Refactoring:**

  - **PR #328: `Refactor: Transition to Meraki* Dataclasses`**
  - **PR #342: `Refactor: Modernize MerakiDevice and MerakiNetwork to Dataclasses`**
  - **Analysis:** These two PRs appear to be working on the same core refactoring. They will almost certainly conflict.
  - **Recommendation:** These PRs should be combined into a single PR. One should be chosen as the base, and the other should be closed after its unique changes have been cherry-picked.

- **Frontend UI:**
  - **PR #338: `Fix: Address XSS Vulnerability in Web Panel`**
  - **PR #339: `Fix: Stabilize UI by Caching Pre-Connect Data`**
  - **Analysis:** Both of these PRs likely modify the same frontend file (`meraki-panel.js`).
  - **Recommendation:** These PRs should be rebased and merged sequentially, with the conflicts resolved manually.

### Moderate-Conflict Group (Dependent on Dataclass Refactor)

- **PR #335: `Feat: Centralize Device Info Resolution with New Helper`**
- **PR #336: `Fix: Resolve TypeErrors with a Serialization Helper`**
- **PR #340: `Fix: Prevent KeyError in MerakiNetwork Instantiation`**
- **PR #341: `Fix: Gracefully Handle Missing lanIp in Device Payloads`**
- **Analysis:** These PRs were likely written against the old dictionary-based data model. They will need to be significantly updated to work with the new dataclass model.
- **Recommendation:** These PRs should be rebased on top of the combined dataclass PR and updated to use the new data structures.

### Low-Conflict Group (Likely to Merge Cleanly After Rebase)

- **PR #332: `Fix: Restore Organization-level Client Sensors`**
- **PR #333: `Fix: Correct Device Name Resolution for Unnamed Devices`**
- **PR #337: `Fix: Ensure Immediate UI Updates with an Initial WebSocket Push`**
- **Analysis:** These PRs appear to touch isolated parts of the codebase. They will still need to be rebased on top of the dataclass PR and updated to use the new data structures, but the logic changes are unlikely to conflict with other PRs.

### Documentation

- **PR #334: `Docs: Adhere to Home Assistant Sentence Case Standards`**
- **Analysis:** This PR will likely have many small conflicts with the other PRs, but they should all be straightforward to resolve.
- **Recommendation:** This PR should be merged last.
