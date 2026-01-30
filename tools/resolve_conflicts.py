#!/usr/bin/env python3
"""Resolve git merge conflict markers by keeping the incoming (theirs) sections.

Usage: python tools/resolve_conflicts.py

This scans the repository for files containing conflict markers and replaces
each conflict region with the incoming section (the text between ======= and
"""

import os
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
changed = []

for dirpath, _dirnames, filenames in os.walk(root):
    # skip .git and node_modules to avoid large binary trees
    if ".git" in dirpath.split(os.sep) or "node_modules" in dirpath.split(os.sep):
        continue
    for fname in filenames:
        path = os.path.join(dirpath, fname)
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception:  # nosec
            continue
        if "<<<<<<<" not in text:
            continue
        lines = text.splitlines(keepends=True)
        out_lines = []
        i = 0
        changed_file = False
        # Robust handling:
        # - Keep the incoming section when a well-formed conflict is found.
        # - Strip stray marker lines when only separators/end markers remain.
        while i < len(lines):
            line = lines[i]
            if line.lstrip().startswith("<<<<<<<"):
                # Found start of conflict. Advance to the separator.
                i += 1
                while i < len(lines) and not lines[i].lstrip().startswith("======="):
                    i += 1
                # If EOF reached, break to avoid infinite loop
                if i >= len(lines):
                    break
                # Skip the ======= line
                i += 1
                # Collect incoming until >>>>>>> or EOF
                incoming = []
                while i < len(lines) and not lines[i].lstrip().startswith(">>>>>>>"):
                    incoming.append(lines[i])
                    i += 1
                # Append the incoming section
                out_lines.extend(incoming)
                # Skip the >>>>>>> line if present
                if i < len(lines) and lines[i].lstrip().startswith(">>>>>>>"):
                    i += 1
                changed_file = True
            elif line.lstrip().startswith("=======") or line.lstrip().startswith(
                ">>>>>>>"
            ):
                # Stray separator or end marker: drop it.
                i += 1
                changed_file = True
            else:
                out_lines.append(line)
                i += 1
        if changed_file:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(out_lines)
                changed.append(path)
                print("Resolved:", path)
            except Exception as e:
                print("Failed to write", path, e)

print(f"Total files changed: {len(changed)}")
if len(changed) == 0:
    print("No conflict markers found.")
else:
    print("Please review changes and run linters/tests as needed.")

sys.exit(0)
