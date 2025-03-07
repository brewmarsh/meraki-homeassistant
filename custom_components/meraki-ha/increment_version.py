import json
import semver
import sys

def increment_version(manifest_path, increment_type):
    """Increments the version number in manifest.json."""
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        current_version = manifest.get('version', '0.0.1')  # Default if not set
        parsed_version = semver.VersionInfo.parse(current_version)

        if increment_type == 'major':
            new_version = parsed_version.bump_major()
        elif increment_type == 'minor':
            new_version = parsed_version.bump_minor()
        elif increment_type == 'patch':
            new_version = parsed_version.bump_patch()
        else:
            raise ValueError("Invalid increment type. Must be 'major', 'minor', or 'patch'.")

        manifest['version'] = str(new_version)

        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"Version incremented to {new_version}")

    except Exception as e:
        print(f"Error incrementing version: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python increment_version.py <major|minor|patch>")
        sys.exit(1)

    increment_type = sys.argv[1].lower()
    manifest_path = "custom_components/meraki_ha/manifest.json"  # Adjust path if necessary
    increment_version(manifest_path, increment_type)