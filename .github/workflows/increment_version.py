import json
import sys
import os

import semver

manifest_path = "custom_components/meraki-ha/manifest.json"

try:
    print(f"Current working directory: {os.getcwd()}")
    print(f"Attempting to read manifest file from: {manifest_path}")

    with open(manifest_path, "r") as f:
        data = json.load(f)
    print(f"Manifest file contents: {data}")
    version = data["version"]

    print(f"Current version: {version}")
    increment_type = sys.argv[1]
    print(f"Increment type: {increment_type}")

    # Parse and create semver.Version
    version_info = semver.VersionInfo.parse(version)
    semver_obj = semver.Version(
        str(version_info)
    )  # create version object from version info

    new_version = semver_obj.bump(increment_type)

    print(f"New version: {new_version}")
    data["version"] = str(new_version)
    print(f"Modified manifest data: {data}")

    with open(manifest_path, "w") as f:
        json.dump(data, f, indent=4)

    print("Manifest file updated successfully.")

except FileNotFoundError:
    print(f"Error: Manifest file not found at {manifest_path}")
    sys.exit(1)

except json.JSONDecodeError:
    print(f"Error: Invalid JSON in manifest file at {manifest_path}")
    sys.exit(1)

except IndexError:
    print("Error: Increment type not provided as a command-line argument.")
    sys.exit(1)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
