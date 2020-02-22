import jsonlines
from utils import primary_term, GIEntry
from pydantic import ValidationError

import pandas as pd

spreadsheet_url = "http://www.wjh.harvard.edu/~inquirer/inquirerbasic.xls"

d = pd.read_excel(spreadsheet_url).fillna(value={"Othtags": "", "Defined": ""})

keep_cols = ["Entry", "Source", "Othtags", "Defined"]
category_cols = [col for col in d.columns if col not in keep_cols]

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

with jsonlines.open("../assets/inquirer.jsonl", mode="w") as writer:
    writer.write_all(data)
