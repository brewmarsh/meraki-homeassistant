1. **Analyze target:** Find a suitable, small performance improvement within the `<50 lines` limit and with a measurable performance impact. In `custom_components/meraki_ha/sensor/network/ssid_client_count.py` and `custom_components/meraki_ha/sensor/device/connected_clients.py`, the counts of `all_clients` are calculated using `sum(1 for ...)` or list comprehensions, which are perfectly fine as they process lists in O(N).
2. However, inside `custom_components/meraki_ha/sensor/device/connected_clients.py` line 72, a list comprehension is used just to get the length (`network_clients = [c for c in all_clients if ...]; self._attr_native_value = len(network_clients)`). This creates an intermediate list which allocates memory. We can optimize this by changing it to `sum(1 for c in all_clients if ...)` which runs in O(N) but uses O(1) memory, just like the `Bolt` persona's guiding principles state.
3. Wait, is there any other place doing `[x for x ...]` and taking `len()`? Let's check `grep -rn "len(" custom_components/meraki_ha/ | grep "\["`. Wait, I did that and found nothing. I can optimize `custom_components/meraki_ha/sensor/device/connected_clients.py`.
4. Let's look at `custom_components/meraki_ha/core/utils/network_utils.py`, `calculate_network_health` function. It has `online_devices = sum(1 for d in devices if d.get("status") == "online")` and `healthy_clients = sum(1 for c in clients if c.get("status") == "healthy")`. That's already optimized.
5. In `custom_components/meraki_ha/sensor/device/connected_clients.py`:
   ```python
            network_clients = [
                c
                for c in all_clients
                if isinstance(c, dict)
                and c.get("networkId") == network_id
                and c.get("status") == "Online"
            ]
            self._attr_native_value = len(network_clients)
   ```
   Can be optimized to:
   ```python
            # Bolt Performance: Use sum with a generator expression instead of a list comprehension
            # to avoid allocating an intermediate list in memory just to count elements.
            self._attr_native_value = sum(
                1
                for c in all_clients
                if isinstance(c, dict)
                and c.get("networkId") == network_id
                and c.get("status") == "Online"
            )
   ```
6. **Pre-commit checks**: Run `run_checks.sh` or `pytest`.
7. **Submit changes**: Commit with PR Title `⚡ Bolt: [performance improvement]`.
