import json
from collections import Counter, defaultdict
from itertools import chain
from pathlib import Path


import jsonlines
from utils import GIEntry, gi_data_to_match_rules, gi_term_to_lemma

_input = []
output = []
excluded = []
term_rule_cache = defaultdict(list)
matcher_loookup = {}
with jsonlines.open("../assets/inquirer.jsonl") as reader:
    for entry in reader:
        GIEntry(**entry)
        _input.append(entry)

for entry in _input:
    categories = entry["categories"]
    if categories:
        lemma = gi_term_to_lemma(entry["term"])
        match_rules = gi_data_to_match_rules(entry)
        if match_rules in term_rule_cache[lemma]:
            excluded.append(entry)
        else:
            term_rule_cache[lemma].append(match_rules)
            _id = f"gi.{entry['term']}"
            matcher_loookup[_id] = {
                "match_rules": match_rules,
                "categories": categories,
            }
            data = {
                "id": f"gi.{entry['term']}",
                "match_rules": match_rules,
                "categories": categories,
            }
            output.append(data)
    else:
        excluded.append(entry)


# with jsonlines.open(
#     "../assets/inquirer_spacy-matcher_inclusions.jsonl", mode="w"
# ) as writer:
#     writer.write_all(output)

# with jsonlines.open(
#     "../assets/inquirer_spacy-matcher_exclusions.jsonl", mode="w"
# ) as writer:
#     writer.write_all(excluded)

Path("../assets/matcher-lookup.json").write_text(json.dumps(matcher_loookup, indent=4))

## Statistics


input_category_counts = Counter(chain.from_iterable(e["categories"] for e in _input))
output_category_counts = Counter(chain.from_iterable(e["categories"] for e in output))
excluded_category_counts = Counter(
    chain.from_iterable(e["categories"] for e in excluded)
)
categories = json.loads(Path("../categories.json").read_text())

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

with jsonlines.open("../assets/category_statistics.jsonl", mode="w") as writer:
    writer.write_all(category_statistics)
