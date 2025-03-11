import json
import sys
import semver

manifest_path = "../../custom_components/meraki-ha/manifest.json" # Corrected path

try:
    with open(manifest_path, "r") as f:
        data = json.load(f)
    version = data["version"]

    increment_type = sys.argv[1] # Get increment type from command-line argument

    new_version = semver.bump_version(version, increment_type)

    data["version"] = new_version

    with open(manifest_path, "w") as f:
        json.dump(data, f, indent=4)

except Exception as e:
    print(f"Error: {e}")