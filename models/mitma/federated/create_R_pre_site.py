from pathlib import Path
import pandas as pd
import re

# ======================
# CONFIG
# ======================
REGIONS_FILE = "regions_site_3.txt"
INPUT_CSV = "R_mobility_matrix_test.csv"          # id1,id2,ratio
OUTPUT_CSV = "R_mobility_matrix_3.csv"

# ======================
# PATHS (script-relative)
# ======================
BASE_DIR = Path(__file__).resolve().parent
regions_path = BASE_DIR / REGIONS_FILE
input_path = BASE_DIR / INPUT_CSV
output_path = BASE_DIR / OUTPUT_CSV

# ======================
# LOAD REGION IDS
# ======================
text = regions_path.read_text()
site_regions = set(re.findall(r'"([^"]+)"', text))

if not site_regions:
    raise ValueError("No region IDs found in regions.txt")

# ======================
# LOAD CSV
# ======================
df = pd.read_csv(input_path)

# ======================
# FILTER: id1 OR id2
# ======================
site_df = df[
    df["id1"].isin(site_regions) |
    df["id2"].isin(site_regions)
]

# ======================
# OPTIONAL SANITY CHECKS
# ======================
if site_df.empty:
    raise ValueError("Filtered CSV is empty — check regions.txt vs CSV IDs")

missing_id1 = site_regions - set(df["id1"])
missing_id2 = site_regions - set(df["id2"])

if missing_id1:
    print("⚠️ Regions never appearing as id1:")
    for r in sorted(missing_id1):
        print("  ", r)

if missing_id2:
    print("⚠️ Regions never appearing as id2:")
    for r in sorted(missing_id2):
        print("  ", r)

# ======================
# WRITE OUTPUT
# ======================
site_df.to_csv(output_path, index=False)

print(f"Created {output_path}")
print(f"Rows kept: {len(site_df)} / {len(df)}")
