import pandas as pd
import jsonlines
from pathlib import Path

file_path = Path(__file__).parent
artifacts = file_path / "artifacts"

category_statistics = []
with jsonlines.open(artifacts / "category_statistics.jsonl") as reader:
    for entry in reader:
        category_statistics.append(entry)

category_statistics_df = pd.DataFrame(category_statistics).set_index("category")

completed_ct = category_statistics_df["output_category_counts"].sum()
incomplete_ct = category_statistics_df["excluded_category_counts"].sum()
pct_completed = (completed_ct / (completed_ct + incomplete_ct)) * 100

output_md = f"""# Category Porting Statistics

**Original Terms Completed:** `{completed_ct}`

**Original Terms Incomplete:** `{incomplete_ct}`

**Percent Completed:** `{pct_completed:.2f}`

"""

output_md += category_statistics_df.to_markdown()

(file_path / "category_statistics_table.md").write_text(output_md)
