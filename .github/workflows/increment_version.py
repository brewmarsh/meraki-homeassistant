import json
import sys
import semver

manifest_path = "custom_components/meraki-ha/manifest.json" #full path to manifest.

# ... (rest of your script)

with open(manifest_path, "r") as f:
    data = json.load(f)

# ... (version increment logic)

with open(manifest_path, "w") as f:
    json.dump(data, f, indent=4)