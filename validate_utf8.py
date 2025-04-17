# validate_utf8.py
import os
import sys

ERRORS = []


def check_utf8(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError as e:
        ERRORS.append((filepath, str(e)))


def scan_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                check_utf8(full_path)


if __name__ == "__main__":
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_directory(base_dir)

    if ERRORS:
        print("\n[!] Non-UTF8 Python files found:\n")
        for path, err in ERRORS:
            print(f" - {path}: {err}")
        sys.exit(1)
    else:
        print("? All .py files are valid UTF-8.")
        sys.exit(0)
