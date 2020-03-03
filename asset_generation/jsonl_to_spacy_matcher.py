import json
from collections import defaultdict
from pathlib import Path


import jsonlines
from utils import GIEntry, gi_data_to_match_rules, gi_term_to_lemma

file_path = Path(__file__).parent
artifacts = file_path / "artifacts"
repo_root = Path.cwd()
gi_assets = repo_root / "general_inquirer" / "assets"

_input = []
complete = []
incomplete = []
term_rule_cache = defaultdict(list)
matcher_loookup = {}
with jsonlines.open(artifacts / "inquirer.jsonl") as reader:
    for entry in reader:
        GIEntry(**entry)
        _input.append(entry)

for entry in _input:
    categories = entry["categories"]
    if categories:
        # lemma = gi_term_to_lemma(entry["term"])
        match_rules = gi_data_to_match_rules(entry)
        lemma = match_rules["LEMMA"]
        if match_rules in term_rule_cache[lemma]:
            incomplete.append(entry)
        else:
            term_rule_cache[lemma].append(match_rules)
            _id = f"gi.{entry['term']}"
            matcher_loookup[_id] = {
                "match_rules": match_rules,
                "categories": categories,
            }
            complete.append(entry)
    else:
        incomplete.append(entry)


with jsonlines.open(artifacts / "complete.jsonl", mode="w") as writer:
    writer.write_all(complete)

with jsonlines.open(artifacts / "incomplete.jsonl", mode="w") as writer:
    writer.write_all(incomplete)

(gi_assets / "gi-matcher-rules.json").write_text(json.dumps(matcher_loookup, indent=4))

