import sys
import shutil

print("sys.path:")
for p in sys.path:
    print(p)

print("\npytest executable:")
print(shutil.which("pytest"))

print("\npip executable:")
print(shutil.which("pip"))
