### **1. Test Server Requirements Document**

#### **Objective**

To achieve an autonomous, observability-driven testing loop that validates integration health through live deployment, real-time log analysis, and automated self-correction.

#### **Autonomous Infrastructure**

- **Test Server:** A Home Assistant instance (OS or Docker) reachable via SSH.
- **Log Shipper:** **Fluent Bit** installed as a service or Docker container on the test server.
- **Observability Platform:** **Better Stack** (Logs) with an HTTP source.
- **Secrets Management:**
- `SMOKE_TEST_SERVER_IP`: The address of the test box.
- `SMOKE_TEST_SSH_KEY`: Private key for deployment.
- `BETTER_STACK_SOURCE_TOKEN`: The unique token from your Better Stack HTTP source.
- `BETTER_STACK_API_TOKEN`: Used by Jules to query logs programmatically.
- `HA_TEST_TOKEN`: Long-lived access token for HA API/CLI.

---

### **2. Detailed Implementation Plan**

#### **Phase 1: Log Forwarding Setup**

Jules will generate and deploy a `fluent-bit.conf` to the test server. This configuration monitors the `home-assistant.log` and ships it to Better Stack.

- **Input:** `tail` plugin pointing to `/config/home-assistant.log`.
- **Output:** `http` plugin pointing to `in.logs.betterstack.com` using your source token.

#### **Phase 2: Deployment & Orchestration**

- **Sync:** Workflow uses `rsync` to push code to `/config/custom_components/meraki_ha/`.
- **Reboot:** Workflow triggers `hass-cli service call homeassistant.restart`.
- **Wait:** Polling loop monitors the `/api/config` endpoint until the state is `RUNNING`.

#### **Phase 3: The Multi-Vector Audit**

1. **State Audit:** `scripts/smoke_test_probe.py` connects via WebSockets to verify that the `meraki_ha` domain is loaded and entities are not `unavailable`.
2. **Log Audit:** A new script `scripts/check_better_stack.py` queries the Better Stack API for any `ERROR` level logs containing "meraki_ha" that occurred in the 5 minutes post-deployment.

#### **Phase 4: Autonomous Bug Reporting**

If either audit fails:

- Jules extracts the **Traceback** and **Entity State** data.
- Jules creates a GitHub issue titled **"Smoke Test Failure: [Commit ID]"**.
- The issue description serves as the "Fix It" prompt for the next Healer cycle.

---

### **4. Fluent Bit Configuration (For Jules to Deploy)**

Jules should use this configuration to set up the log shipping:

```ini
[SERVICE]
    Flush        1
    Daemon       Off
    Log_Level    info

[INPUT]
    Name         tail
    Path         /config/home-assistant.log
    Tag          ha.logs
    DB           /tmp/fluent-bit.db

[FILTER]
    Name         grep
    Match        ha.logs
    Regex        log .*meraki_ha.*

[OUTPUT]
    Name         http
    Match        ha.logs
    Host         in.logs.betterstack.com
    Port         443
    URI          /
    Header       Authorization Bearer ${{ secrets.BETTER_STACK_SOURCE_TOKEN }}
    Format       json
    tls          On

```
