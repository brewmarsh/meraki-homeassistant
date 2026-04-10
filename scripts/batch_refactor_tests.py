import os
import re

root_dir = "tests"

# Patterns
import_pattern = re.compile(
    r"from custom_components\.meraki_ha\.core\.api\.client import MerakiAPIClient"
)
type_pattern = re.compile(r"(?<!\.)MerakiAPIClient\b")


def replace_content(content):
    # Replace import
    content = import_pattern.sub(
        "from custom_components.meraki_ha.core.api import MerakiApiClientProtocol, create_api_client",
        content,
    )
    # Replace type usage
    content = type_pattern.sub("MerakiApiClientProtocol", content)
    # Replace instantiation
    content = content.replace(
        "MerakiApiClientProtocol(hass=", "create_api_client(hass="
    )
    content = content.replace("MerakiApiClientProtocol(", "create_api_client(")
    return content


for root, _dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(file_path, encoding="utf-8") as f:
                try:
                    content = f.read()
                except UnicodeDecodeError:
                    continue

            new_content = replace_content(content)

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
