
import os

files_to_fix = [
    'custom_components/meraki_ha/core/repositories/camera_repository.py',
    'custom_components/meraki_ha/core/repository.py',
    'custom_components/meraki_ha/core/fetch_strategies/base.py',
    'custom_components/meraki_ha/core/coordinator_helpers/client_fetcher.py'
]

for file_path in files_to_fix:
    if not os.path.exists(file_path):
        continue

    with open(file_path, encoding='utf-8') as f:
        content = f.read()

    # Replace from ..api.client import MerakiApiClientProtocol with from ..api import MerakiApiClientProtocol
    new_content = content.replace('from ..api.client import MerakiApiClientProtocol', 'from ..api import MerakiApiClientProtocol')
    new_content = new_content.replace('from .api.client import MerakiApiClientProtocol', 'from .api import MerakiApiClientProtocol')

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
