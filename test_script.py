def get_active_keys(active_keys, config_entry_id=None, network_id=None):
    keys = active_keys
    if config_entry_id:
        keys = [k for k in keys if k["config_entry_id"] == config_entry_id]
    if network_id:
        keys = [k for k in keys if k["network_id"] == network_id]
    return keys

def get_active_keys_opt(active_keys, config_entry_id=None, network_id=None):
    if not config_entry_id and not network_id:
        return active_keys

    return [
        k for k in active_keys
        if (not config_entry_id or k["config_entry_id"] == config_entry_id)
        and (not network_id or k["network_id"] == network_id)
    ]

keys = [
    {"config_entry_id": "c1", "network_id": "n1"},
    {"config_entry_id": "c1", "network_id": "n2"},
    {"config_entry_id": "c2", "network_id": "n1"},
]

print("Original:")
print(get_active_keys(keys, "c1", "n1"))
print("Optimized:")
print(get_active_keys_opt(keys, "c1", "n1"))
