import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(SCRIPT_DIR, "00_Input.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "00_Output.txt")


def humanize(tag: str) -> str:
    # turn k_byzantium -> Byzantium ; c_county-of_ork -> County Of Ork
    return tag.replace('_', ' ').replace('-', ' ').strip().title()

def block(title_tag: str) -> str:
    return f"{title_tag} = {{\n\n}}\n"

# --- read input ---
if not os.path.exists(INPUT_FILE):
    print(f"Missing {INPUT_FILE}! Put it next to this script.")
    input("Press Enter to exit...")
    raise SystemExit(1)

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# --- parse hierarchy: kingdom -> duchies -> counties ---
current_kingdom = None
current_duchy = None

kingdom_order = []               # preserve order of appearance
duchies_by_kingdom = {}          # k -> [d...]
counties_by_duchy = {}           # d -> [c...]

seen_kingdoms = set()
seen_duchies = set()
seen_counties = set()

for raw in lines:
    line = raw.strip()

    m_k = re.match(r'k_([\w-]+)\s*=\s*{', line)
    m_d = re.match(r'd_([\w-]+)\s*=\s*{', line)
    m_c = re.match(r'c_([\w-]+)\s*=\s*{', line)

    if m_k:
        current_kingdom = f"k_{m_k.group(1)}"
        current_duchy = None
        if current_kingdom not in seen_kingdoms:
            seen_kingdoms.add(current_kingdom)
            kingdom_order.append(current_kingdom)
            duchies_by_kingdom.setdefault(current_kingdom, [])
        continue

    if m_d:
        current_duchy = f"d_{m_d.group(1)}"
        if current_kingdom:
            if current_duchy not in seen_duchies:
                seen_duchies.add(current_duchy)
                duchies_by_kingdom.setdefault(current_kingdom, []).append(current_duchy)
                counties_by_duchy.setdefault(current_duchy, [])
        continue

    if m_c:
        county = f"c_{m_c.group(1)}"
        if current_duchy:
            if county not in seen_counties:
                seen_counties.add(county)
                counties_by_duchy.setdefault(current_duchy, []).append(county)
        continue

# --- build output text ---
out_lines = []

for k in kingdom_order:
    # Kingdom block
    out_lines.append(f"# {humanize(k)}\n")
    out_lines.append(block(k))
    out_lines.append("\n")

    # Duchies under the kingdom
    for d in duchies_by_kingdom.get(k, []):
        out_lines.append(f"# {humanize(d)}\n")
        out_lines.append(block(d))
        out_lines.append("\n")

        # Counties under the duchy
        for c in counties_by_duchy.get(d, []):
            out_lines.append(f"# {humanize(c)}\n")
            out_lines.append(block(c))
            out_lines.append("\n")

# --- write output ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print(f"Done! Title history written to {OUTPUT_FILE}")
input("Press Enter to exit...")
