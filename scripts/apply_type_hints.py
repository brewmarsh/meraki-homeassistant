"""Script to apply type hints to files using Gemini API."""

import json
import os
import re
import time

try:
    from google import genai
except ImportError:
    print(
        "Error: google-genai package is not installed. Please run 'pip install google-genai'."
    )
    genai = None


def apply_type_hints() -> None:
    """Read typing_tasks.json and apply type hints using Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    if genai is None:
        return

    client = genai.Client(api_key=api_key)

    tasks_file = "typing_tasks.json"
    if not os.path.exists(tasks_file):
        print(f"Error: {tasks_file} not found.")
        return

    try:
        with open(tasks_file, encoding="utf-8") as f:
            tasks = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding {tasks_file}: {e}")
        return

    for task in tasks:
        file_path = task.get("file")
        if not file_path or not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found. Skipping.")
            continue

        print(f"Processing {file_path}...")
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            prompt = (
                "Add strict PEP 484 type hints to all function signatures in the following Python code. "
                "Use types like '-> None', 'list[dict[str, Any]]', etc. Do not alter any core logic. "
                "Ensure all necessary imports for typing (from typing import Any, etc.) are included. "
                "Return ONLY the complete refactored code wrapped in ```python and ``` tags.\n\n"
                f"Code:\n{content}"
            )

            # gemini-2.5-flash as requested, though it might be 2.0-flash in reality.
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            if not response or not response.text:
                print(f"Error: Received empty response for {file_path}.")
                continue

            # Extract refactored code using regex
            refactored_code_match = re.search(
                r"```python\s+(.*?)\s+```", response.text, re.DOTALL
            )
            if not refactored_code_match:
                # Fallback to general code block if python tag is missing
                refactored_code_match = re.search(
                    r"```\s+(.*?)\s+```", response.text, re.DOTALL
                )

            if refactored_code_match:
                refactored_code = refactored_code_match.group(1).strip()
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(refactored_code)
                print(f"Successfully updated {file_path}.")
            else:
                print(
                    f"Error: Could not extract code from Gemini response for {file_path}."
                )

        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                print(
                    f"Rate limit reached (429) for {file_path}. Waiting 60 seconds..."
                )
                time.sleep(60)
                # We could retry here, but for simplicity we'll just move on or rely on next run.
            else:
                print(f"An error occurred while processing {file_path}: {e}")

        # Gracefully manage free-tier rate limits
        time.sleep(10)


if __name__ == "__main__":
    apply_type_hints()
