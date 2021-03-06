import json
from pathlib import Path

import pandas as pd

import jsonlines
from pydantic import ValidationError
from utils import GIEntry, primary_term

file_path = Path(__file__).parent
artifacts = file_path / "artifacts"

spreadsheet_url = "http://www.wjh.harvard.edu/~inquirer/inquirerbasic.xls"

d = pd.read_excel(spreadsheet_url).fillna(value={"Othtags": "", "Defined": ""})

keep_cols = ["Entry", "Source", "Othtags", "Defined"]
category_cols = [col for col in d.columns if col not in keep_cols]
(artifacts / "categories.json").write_text(json.dumps(category_cols, indent=4))

data = []
for i in range(len(d)):
    row = d.loc[i, :]
    term = str(row["Entry"])
    source = row["Source"]
    othtags = row["Othtags"].split()
    defined = row["Defined"]
    redundant = "handled" in defined
    idiom = "idiom" in defined
    multiple = "#" in term
    primary = primary_term(term)
    categories = list(row[category_cols][row[category_cols].notnull()].index)
    rdata = {
        "id": i,
        "term": term,
        "source": source,
        "othtags": othtags,
        "defined": defined,
        "categories": categories,
        "redundant": redundant,
        "idiom": idiom,
        "multiple": multiple,
        "primary": primary,
    }
    try:
        GIEntry(**rdata)
        data.append(rdata)
    except ValidationError as e:
        print(e)

file_path = Path(__file__).parent

with jsonlines.open(str(artifacts / "inquirer.jsonl"), mode="w") as writer:
    writer.write_all(data)
