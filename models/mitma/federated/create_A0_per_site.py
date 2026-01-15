from pathlib import Path
import pandas as pd
import re

# ======================
# CONFIG
# ======================
REGIONS_FILE = "regions_site_3.txt"
INPUT_CSV = "A0_initial_conditions_seeds_test.csv"          # name,id,idx,Y,M,O
OUTPUT_CSV = "A0_initial_conditions_seeds_3.csv"

# ======================
# PATHS (script-relative)
# ======================
BASE_DIR = Path(__file__).resolve().parent
regions_path = BASE_DIR / REGIONS_FILE
input_path = BASE_DIR / INPUT_CSV
output_path = BASE_DIR / OUTPUT_CSV

# ======================
# LOAD REGION IDS FROM TXT
# ======================
text = regions_path.read_text()
region_ids = set(re.findall(r'"([^"]+)"', text))

if not region_ids:
    raise ValueError("No region IDs found in regions.txt")

# ======================
# LOAD & FILTER CSV
# ======================
df = pd.read_csv(input_path)

filtered_df = df[df["id"].isin(region_ids)]

# ======================
# SAFETY CHECKS
# ======================
missing = region_ids - set(df["id"])
if missing:
    print("⚠️ Warning: these region IDs are in regions.txt but not in the CSV:")
    for r in sorted(missing):
        print("  ", r)

if filtered_df.empty:
    raise ValueError("Filtered CSV is empty — check ID consistency")

# ======================
# WRITE OUTPUT
# ======================
filtered_df.to_csv(output_path, index=False)

print(f"Created {output_path}")
print(f"Rows kept: {len(filtered_df)} / {len(df)}")
