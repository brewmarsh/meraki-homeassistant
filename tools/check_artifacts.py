#!/usr/bin/env python3
"""Check staged files for forbidden artifact patterns.

Used by pre-commit as a local hook to prevent committing agent/debug artifacts.
"""

import re
import subprocess
import sys

FORBIDDEN_PATTERNS = [
    r"(^|/)git-error-",
    r"(^|/)git-output-",
    r"(^|/)message_to_user\.txt$",
    r"(^|/).*~$",
    r"(^|/).*\.tmp$",
    r"(^|/).*\.bak$",
    r"(^|/)tmp(/|$)",
    r"(^|/)archive(/|$)",
]


def get_staged_files():
    """Return a list of staged filenames from `git diff --cached --name-only`.

    Returns an empty list if the git command fails.
    """
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"], text=True
        )
    except subprocess.CalledProcessError:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def main() -> int:
    """Check staged files and return non-zero on forbidden matches."""
    files = get_staged_files()
    if not files:
        return 0

    matches = []
    for f in files:
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, f):
                matches.append((f, pat))
                break

    if matches:
        print("Forbidden artifact files are staged for commit:")
        for f, pat in matches:
            print(f" - {f}  (matches {pat})")
        print(
            "\nPlease remove these from the commit or move them to "
            "`archive/agent-artifacts/`."
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
