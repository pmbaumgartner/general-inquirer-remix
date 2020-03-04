from collections import Counter, defaultdict
from itertools import chain
from pathlib import Path
import json
import pandas as pd

import jsonlines

from slugify import slugify

from artifacts.category_defs import category_definitions

file_path = Path(__file__).parent
artifacts = file_path / "artifacts"
docs_path = file_path.parent.parent / "docs"
category_docs_path = docs_path / "categories"

inquirer = []
complete = []
incomplete = []
with jsonlines.open(artifacts / "inquirer.jsonl") as reader:
    for entry in reader:
        inquirer.append(entry)

with jsonlines.open(artifacts / "complete.jsonl") as reader:
    for entry in reader:
        complete.append(entry)

with jsonlines.open(artifacts / "incomplete.jsonl") as reader:
    for entry in reader:
        incomplete.append(entry)

## Statistics

input_category_counts = Counter(chain.from_iterable(e["categories"] for e in inquirer))
output_category_counts = Counter(chain.from_iterable(e["categories"] for e in complete))
excluded_category_counts = Counter(
    chain.from_iterable(e["categories"] for e in incomplete)
)
categories = json.loads((artifacts / "categories.json").read_text())

category_statistics = []
for category in categories:
    category_data = {
        "category": category,
        "input_category_counts": input_category_counts.get(category, 0),
        "output_category_counts": output_category_counts.get(category, 0),
        "excluded_category_counts": excluded_category_counts.get(category, 0),
    }
    pct_included = (
        category_data["output_category_counts"] / category_data["input_category_counts"]
    )
    category_data["percent_included"] = f"{pct_included:.2f}"
    category_statistics.append(category_data)

with jsonlines.open(artifacts / "category_statistics.jsonl", mode="w") as writer:
    writer.write_all(category_statistics)


# Markdown

category_slugs = {}
slug_appearances = defaultdict(int)
for category in categories:
    slug = slugify(category)
    if slug in category_slugs.values():
        slug += str(slug_appearances[category] + 1)
    category_slugs[category] = slug
    slug_appearances[category] += 1


for category, slug in category_slugs.items():
    completed_items = [e for e in complete if category in e["categories"]]
    incomplete_items = [e for e in incomplete if category in e["categories"]]

    complete_df = (
        pd.DataFrame(completed_items)
        .set_index("id")
        .loc[:, ["term", "source", "defined"]]
        .assign(defined=lambda d: d["defined"].str.replace("|", "").str.strip())
    )
    if incomplete_items:
        incomplete_df = (
            pd.DataFrame(incomplete_items)
            .set_index("id")
            .loc[:, ["term", "source", "defined"]]
            .assign(defined=lambda d: d["defined"].str.replace("|", "").str.strip())
        )
        incomplete_md = incomplete_df.to_markdown()
    else:
        incomplete_md = ""

    complete_md = complete_df.to_markdown()

    md_title = f"# {category}"
    description = category_definitions[category]
    complete_title = "## Completed"
    incomplete_title = "## Incomplete"

    category_md = "\n\n".join(
        [
            md_title,
            description,
            complete_title,
            complete_md,
            incomplete_title,
            incomplete_md,
        ]
    )

    Path(category_docs_path / f"{slug}.md").write_text(category_md)


category_statistics = []
with jsonlines.open(artifacts / "category_statistics.jsonl") as reader:
    for entry in reader:
        category_statistics.append(entry)

rename_cols = {
    "category": "Category",
    "input_category_counts": "Total",
    "output_category_counts": "Complete",
    "excluded_category_counts": "Incomplete",
    "percent_included": "Percent Complete",
}


def category_link(category):
    slug = category_slugs[category]
    return f"[{category}](categories/{slug}.md)"


category_statistics_df = (
    pd.DataFrame(category_statistics)
    .assign(category=lambda d: d["category"].apply(category_link))
    .rename(columns=rename_cols)
    .set_index("Category")
)

completed_ct = category_statistics_df["Complete"].sum()
incomplete_ct = category_statistics_df["Incomplete"].sum()
pct_completed = (completed_ct / (completed_ct + incomplete_ct)) * 100

output_md = f"""# Category Porting Statistics

**Original Terms Completed:** `{completed_ct}`

**Original Terms Incomplete:** `{incomplete_ct}`

**Percent Completed:** `{pct_completed:.1f}%`

"""

output_md += category_statistics_df.to_markdown()

(docs_path / "category-statistics-table.md").write_text(output_md)

