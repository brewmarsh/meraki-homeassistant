
import os
import re

root_dir = 'custom_components/meraki_ha'

# Patterns
import_pattern = re.compile(r'from \.{1,3}core\.api\.client import MerakiAPIClient(?: as ApiClient)?')
type_pattern = re.compile(r'(?<!\.)MerakiAPIClient\b')

# Replacement functions
def replace_imports(content, file_path):
    # Determine the relative path to core/api
    rel_path = os.path.relpath('custom_components/meraki_ha/core/api', os.path.dirname(file_path))
    rel_path_dots = rel_path.replace('\\', '/').replace('custom_components/meraki_ha/', '').replace('.', '')
    # Since we're usually in custom_components/meraki_ha, relative imports are best
    
    # Simpler: just use absolute imports for the core package if possible, 
    # but the project seems to prefer relative.
    
    # Calculate dots based on depth
    depth = len(os.path.relpath(file_path, 'custom_components/meraki_ha').split(os.sep)) - 1
    dots = '.' * (depth + 1)
    
    # Replace the import
    def sub_import(match):
        if 'as ApiClient' in match.group(0):
            return f'from {dots}core.api import MerakiApiClientProtocol as ApiClient'
        return f'from {dots}core.api import MerakiApiClientProtocol'

    return import_pattern.sub(sub_import, content)

def replace_types(content):
    return type_pattern.sub('MerakiApiClientProtocol', content)

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    content = f.read()
                except UnicodeDecodeError:
                    continue
            
            new_content = replace_imports(content, file_path)
            new_content = replace_types(new_content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
