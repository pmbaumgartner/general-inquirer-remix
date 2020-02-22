import jsonlines
from utils import GIEntry, gi_tags_to_spacy_pos

output = []
with jsonlines.open("../assets/inquirer.jsonl") as reader:
    for obj in reader:
        GIEntry(**obj)
        if obj["primary"] and obj["categories"]:
            match_rules = gi_tags_to_spacy_pos(obj)
            categories = obj["categories"]
            data = {"match_rules": match_rules, "categories": categories}
            output.append(data)

with jsonlines.open("../assets/inquirer_spacy-matcher.jsonl", mode="w") as writer:
    writer.write_all(output)
