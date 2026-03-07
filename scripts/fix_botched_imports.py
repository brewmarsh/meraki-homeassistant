
import os
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix from ... import (, ...)
    # Pattern: from custom_components.meraki_ha.const.integration import ( (, ...) )
    content = re.sub(r'from custom_components\.meraki_ha\.const\.integration import\s*\(\s*\(\s*,', 'from custom_components.meraki_ha.const.integration import (', content)
    
    # Fix from custom_components.meraki_ha.const.integration import from custom_components.meraki_ha.const.integration import DOMAIN
    content = re.sub(r'from custom_components\.meraki_ha\.const\.integration import from custom_components\.meraki_ha\.const\.integration import DOMAIN', 'from custom_components.meraki_ha.const.integration import DOMAIN', content)
    
    # Fix duplicate/nested from statements
    content = re.sub(r'from custom_components\.meraki_ha\.const\.integration import from custom_components\.meraki_ha\.const\.websocket import', 'from custom_components.meraki_ha.const.websocket import', content)

    # Clean up double closing parens if any
    content = content.replace('), )', ')')
    
    # Fix specific botched import in integration setup if any
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# List of files identified with SyntaxErrors in ruff output
files = [
    'custom_components/meraki_ha/api/commands_network.py',
    'custom_components/meraki_ha/api/utils.py',
    'custom_components/meraki_ha/core/coordinator_helpers/config_helper.py',
    'custom_components/meraki_ha/core/helpers/device_registry.py',
    'custom_components/meraki_ha/discovery/handlers/network.py',
    'custom_components/meraki_ha/discovery/handlers/universal.py',
    'custom_components/meraki_ha/discovery/handlers/wireless.py',
    'custom_components/meraki_ha/discovery/service.py',
    'custom_components/meraki_ha/helpers/schema.py',
    'custom_components/meraki_ha/meraki_select/__init__.py',
    'custom_components/meraki_ha/schemas.py',
    'custom_components/meraki_ha/services/ipsk_manager.py',
    'tests/api/test_websocket.py',
    'tests/discovery/handlers/test_network.py',
    'tests/test_e2e_ipsk.py',
    'tests/test_ipsk_manager.py'
]

for f in files:
    if os.path.exists(f):
        fix_file(f)
        print(f"Fixed {f}")
