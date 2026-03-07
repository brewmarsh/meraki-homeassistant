import os
import sys
import ast

def check_file(filepath):
    with open(filepath, 'r') as f:
        try:
            ast.parse(f.read())
        except SyntaxError as e:
            print(f"SYNTAX ERROR in {filepath}: {e}")
            return False
    return True

all_ok = True
for root, dirs, files in os.walk('custom_components/meraki_ha'):
    for file in files:
        if file.endswith('.py'):
            if not check_file(os.path.join(root, file)):
                all_ok = False

for root, dirs, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py'):
            if not check_file(os.path.join(root, file)):
                all_ok = False

if all_ok:
    print("All files parsed successfully (no syntax errors)")
else:
    sys.exit(1)
