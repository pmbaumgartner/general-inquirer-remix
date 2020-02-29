import pandas as pd
import jsonlines
from pathlib import Path

file_path = Path(__file__).parent
assets_path = file_path / ".." / "assets"

category_statistics = []
with jsonlines.open(assets_path / "category_statistics.jsonl") as reader:
    for entry in reader:
        category_statistics.append(entry)

category_statistics_df = pd.DataFrame(category_statistics).set_index("category")

(assets_path / "category_statistics_table.md").write_text(
    category_statistics_df.to_markdown()
)
