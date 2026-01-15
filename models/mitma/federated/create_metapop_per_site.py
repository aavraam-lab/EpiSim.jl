from pathlib import Path
import pandas as pd
import re

# ======================
# CONFIG
# ======================
REGIONS_FILE = "regions_site_3.txt"
INPUT_CSV = "metapopulation_data_test.csv"
OUTPUT_CSV = "metapopulation_data_3.csv"

# ======================
# PATHS (script-relative)
# ======================
BASE_DIR = Path(__file__).resolve().parent
regions_path = BASE_DIR / REGIONS_FILE
csv_path = BASE_DIR / INPUT_CSV
out_path = BASE_DIR / OUTPUT_CSV

# ======================
# LOAD REGIONS FROM TXT
# ======================
text = regions_path.read_text()
region_ids = set(re.findall(r'"([^"]+)"', text))

if not region_ids:
    raise ValueError("No region IDs found in regions.txt")

# ======================
# LOAD & FILTER CSV
# ======================
df = pd.read_csv(csv_path)

filtered_df = df[df["id"].isin(region_ids)]

# ======================
# SAFETY CHECKS
# ======================
missing = region_ids - set(filtered_df["id"])
if missing:
    print("⚠️ Warning: these region IDs were not found in CSV:")
    for r in sorted(missing):
        print("  ", r)

# ======================
# WRITE OUTPUT
# ======================
filtered_df.to_csv(out_path, index=False)

print(f"Created {out_path}")
print(f"Rows kept: {len(filtered_df)} / {len(df)}")
