import os
import re


def fix_file(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Fix botched from ... import ( ..., ), )
    # This specifically targets the cases where we have:
    #     SOME_CONST,
    #     ),
    # )
    new_content = re.sub(r",\s*\),\s*\)", r"\n)", content)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {file_path}")


files_to_fix = [
    "custom_components/meraki_ha/schemas.py",
    "custom_components/meraki_ha/core/coordinator_helpers/config_helper.py",
    "custom_components/meraki_ha/helpers/schema.py",
    "custom_components/meraki_ha/discovery/handlers/network.py",
    "custom_components/meraki_ha/discovery/handlers/universal.py",
    "custom_components/meraki_ha/discovery/handlers/wireless.py",
    "custom_components/meraki_ha/discovery/service.py",
    "tests/api/test_websocket.py",
    "tests/discovery/handlers/test_network.py",
]

for f in files_to_fix:
    fix_file(f)
