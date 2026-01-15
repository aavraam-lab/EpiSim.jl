import pandas as pd
from pathlib import Path

"'' "
"Create R_mobility_matrix.csv with region IDs instead of indices"
""
""
"'"



BASE_DIR = Path(__file__).resolve().parent

map_df = pd.read_csv(BASE_DIR / "rosetta.csv")
values_df = pd.read_csv(BASE_DIR / "R_mobility_matrix.csv")    # columns: idx1, idx2, number


# Build idx -> id mapping
idx_to_id = dict(zip(map_df["idx"], map_df["id"]))

# Replace idx with id
values_df["id1"] = values_df["source_idx"].map(idx_to_id)
values_df["id2"] = values_df["target_idx"].map(idx_to_id)

# Select final columns
output_df = values_df[["id1", "id2", "ratio"]]

# Save result
output_df.to_csv("R_matrix_test.csv", index=False)

print("R_matrix_test.csv created successfully")
