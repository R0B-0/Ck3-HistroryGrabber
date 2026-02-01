import re
import os
import sys
from collections import OrderedDict

def read_text_safely(path):
    # Try a few common encodings CK3 mod files often use
    encodings = ["utf-8-sig", "utf-8", "utf-16-le", "utf-16-be", "cp1252"]
    last_err = None
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeError as e:
            last_err = e
            continue
        except FileNotFoundError:
            raise
    # Fallback: binary read then decode ignoring errors
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="ignore")

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "00_Input.txt"
    output_file = "00_Output.txt"

    if not os.path.exists(input_file):
        print(f"Missing {input_file}! Put it next to this script or pass a path as the first argument.")
        input("Press Enter to exit...")
        raise SystemExit(1)

    text = read_text_safely(input_file)

    # Strip inline comments beginning with # (CK3 uses # for comments)
    text_nocomments = re.sub(r'(?m)#.*$', '', text)

    # Regex: match 'province = 1234' with any spacing/casing
    # Use a left "non-word" guard to avoid matching part of longer identifiers
    pattern = re.compile(r'(?i)(?<!\w)province\s*=\s*(\d+)\b')
    province_ids = OrderedDict()

    for m in pattern.finditer(text_nocomments):
        pid = m.group(1)
        if pid not in province_ids:
            province_ids[pid] = None

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        for pid in province_ids.keys():
            f.write(f"{pid}=\n")

    print(f"Scanned: {input_file}")
    print(f"Found {len(province_ids)} unique province ids.")
    if province_ids:
        # Show a tiny preview
        sample = list(province_ids.keys())[:10]
        print("Preview:", ", ".join(pid + "=" for pid in sample))

    print(f"Saved: {output_file}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
