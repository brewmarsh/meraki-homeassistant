import subprocess
print(subprocess.run(["uv", "run", "pytest", "tests/sensor/test_network_health.py"]))
