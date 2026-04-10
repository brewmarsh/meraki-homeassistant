import re

# IGNORE_PATTERNS defines the list of regexes for log lines that should be ignored during CI/CD auditing.
IGNORE_PATTERNS = [
    re.compile(r"entity_registry is logging too frequently", re.I),
    re.compile(
        r"(Network traffic analysis|Vlan tracking|Appliance port tracking) is not enabled",
        re.I,
    ),
    re.compile(r"Meraki API Informational Error.*Status 400", re.I),
]


def is_fatal_error(log_line: str) -> bool:
    """
    Determines if a log line represents a fatal error that should fail a test run.
    It returns True if the line contains [WARNING] or [ERROR] and does NOT match
    any of the IGNORE_PATTERNS.
    """
    if "[WARNING]" not in log_line and "[ERROR]" not in log_line:
        return False

    # Ignore all errors or warnings not related to the meraki_ha integration
    if "meraki" not in log_line.lower():
        return False

    return not any(pattern.search(log_line) for pattern in IGNORE_PATTERNS)


def filter_logs(log_lines: list[str]) -> list[str]:
    """
    Filters a list of log lines, returning only those that are considered fatal errors.
    """
    return [line for line in log_lines if is_fatal_error(line)]
