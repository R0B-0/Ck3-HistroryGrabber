import re
import os

# Input and output file paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(SCRIPT_DIR, "00_Input.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "00_Output.txt")

# Read the input
if not os.path.exists(INPUT_FILE):
    print(f"Missing {INPUT_FILE}! Please put it in the same folder as this script.")
    input("Press Enter to exit...")
    exit()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

current_kingdom = None
current_duchy = None
current_barony = None
duchy_entries = {}
kingdom_entries = {}
kingdom_order = []

# Parse landed titles
for line in lines:
    kingdom_match = re.match(r'\s*k_([\w-]+)\s*=\s*{', line)
    duchy_match   = re.match(r'\s*d_([\w-]+)\s*=\s*{', line)
    barony_match  = re.match(r'\s*b_([\w-]+)\s*=\s*{', line)
    province_match= re.match(r'\s*province\s*=\s*(\d+)', line)

    if kingdom_match:
        current_kingdom = kingdom_match.group(1)
        if current_kingdom not in kingdom_entries:
            kingdom_entries[current_kingdom] = []
            kingdom_order.append(current_kingdom)

    if duchy_match:
        current_duchy = duchy_match.group(1)
        if current_duchy not in duchy_entries:
            duchy_entries[current_duchy] = []
            if current_kingdom:
                kingdom_entries[current_kingdom].append(current_duchy)

    if barony_match:
        current_barony = barony_match.group(1)

    if province_match and current_duchy and current_barony:
        province_id = province_match.group(1)
        duchy_entries[current_duchy].append(
            f"#{current_barony.replace('_', ' ').replace('-', ' ').title()}\n"
            f"{province_id} = {{\n\n}}\n"
        )

# Write the output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for kingdom in kingdom_order:
        kingdom_name = kingdom.replace('_', ' ').replace('-', ' ').title()
        f.write(f"\n{'#'*49}\n# {kingdom_name}\n{'#'*49}\n")

        for duchy in kingdom_entries[kingdom]:
            f.write(f"\n####### {duchy.replace('_', ' ').replace('-', ' ').title()}\n\n")
            f.writelines(duchy_entries[duchy])
            f.write("\n")

print(f"Done! Output saved to {OUTPUT_FILE}")
input("Press Enter to exit...")
