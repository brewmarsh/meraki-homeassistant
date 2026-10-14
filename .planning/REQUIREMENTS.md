# Requirements

## v1.0 - v3.0 Milestones: (Complete)

All core functional and platform requirements (FND, MON, WEB, CTRL, STB, UP, SVC, BP, CAM) have been satisfied.

## v3.1 Milestone: Staging Infrastructure Refactoring (New)

### 8. Staging & DevOps (STG)

| ID     | Requirement                                                                   | Status  |
| ------ | ----------------------------------------------------------------------------- | ------- |
| STG-01 | Consolidate `staging_test_entities.py` and `staging_test_probe.py`.           | Planned |
| STG-02 | Standardize all health checks to use the Home Assistant WebSocket API.        | Planned |
| STG-03 | Implement fingerprinting/hashing for failure deduplication in GitHub issues.  | Planned |
| STG-04 | Filter expected warnings (unknown/unavailable) from critical failure reports. | Planned |
| STG-05 | Add issue commenting for repeat failures instead of new issue creation.       | Planned |

## Traceability

| Requirement | Phase   | Status   |
| ----------- | ------- | -------- |
| FND/MON/WEB | P1-P3   | Complete |
| CTRL/STB/UP | P4-P6   | Complete |
| CAM-01-04   | Phase 7 | Complete |
| STG-01      | Phase 8 | Pending  |
| STG-02      | Phase 8 | Pending  |
| STG-03      | Phase 8 | Pending  |
| STG-04      | Phase 8 | Pending  |
| STG-05      | Phase 8 | Pending  |
