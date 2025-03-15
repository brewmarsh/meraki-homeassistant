import json
import sys
import os

import semver

manifest_path = "custom_components/meraki-ha/manifest.json"  # Corrected path

try:
    print(f"Current working directory: {os.getcwd()}")  # Added debug

    print(f"Attempting to read manifest file from: {manifest_path}")  # Added debug

    with open(manifest_path, "r") as f:
        data = json.load(f)
    print(f"Manifest file contents: {data}")  # Added debug
    version = data["version"]

    print(f"Current version: {version}")  # Added debug

    increment_type = sys.argv[1]  # Get increment type from command-line argument

    print(f"Increment type: {increment_type}")  # Added debug

    # Corrected semver usage
    semver_obj = semver.Version(version)
    new_version = semver_obj.bump(increment_type)

    print(f"New version: {new_version}")  # Added debug

    data["version"] = str(new_version)  # convert to string

    print(f"Modified manifest data: {data}")  # Added debug

    with open(manifest_path, "w") as f:
        json.dump(data, f, indent=4)

    print("Manifest file updated successfully.")  # Added debug

except FileNotFoundError:
    print(f"Error: Manifest file not found at {manifest_path}")
    sys.exit(1)  # Exit with error code

except json.JSONDecodeError:
    print(f"Error: Invalid JSON in manifest file at {manifest_path}")
    sys.exit(1)  # Exit with error code

except IndexError:
    print("Error: Increment type not provided as a command-line argument.")
    sys.exit(1)  # Exit with error code

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)  # Exit with error code
