from pathlib import Path
import math
import re

# ======================
# CONFIG
# ======================
NUM_OF_SITES = 3
INPUT_FILE = "regions.txt"
OUTPUT_PREFIX = "regions_site"

# ======================
# PATH HANDLING (FIX)
# ======================
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / INPUT_FILE

# ======================
# LOAD & PARSE
# ======================
text = INPUT_PATH.read_text()

regions = re.findall(r'"([^"]+)"', text)

if NUM_OF_SITES > len(regions):
    raise ValueError("NUM_OF_SITES cannot exceed number of regions")

# ======================
# SPLIT
# ======================
chunk_size = math.ceil(len(regions) / NUM_OF_SITES)
chunks = [
    regions[i * chunk_size : (i + 1) * chunk_size]
    for i in range(NUM_OF_SITES)
]

# ======================
# WRITE OUTPUT
# ======================
for i, chunk in enumerate(chunks, start=1):
    lines = []
    for j, region in enumerate(chunk):
        prefix = "M = " if j == 0 else "    "
        comma = "," if j < len(chunk) - 1 else ";"
        lines.append(f'{prefix}"{region}"{comma}')

    out_path = BASE_DIR / f"{OUTPUT_PREFIX}_{i}.txt"
    out_path.write_text("\n".join(lines) + "\n")

    print(f"Created {out_path}")
