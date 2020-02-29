from spacy.matcher import Matcher
from spacy.tokens import Token, Doc
from collections import Counter
from pathlib import Path
import json
from .category_defs import category_definitions

file_path = Path(__file__).parent
assets_dir = file_path / "assets"


class GICategories(object):

    name = "general_inquirer"

    def __init__(self, nlp):
        Token.set_extension("gi_tags", default=[], force=True)
        Doc.set_extension("gi_tags", default={}, force=True)
        self.matcher_lookup = json.loads(
            (Path(assets_dir / "gi-matcher-rules.json")).read_text()
        )
        self.matcher = Matcher(nlp.vocab)
        for _id, match_data in self.matcher_lookup.items():
            self.matcher.add(_id, None, [match_data["match_rules"]])

        self.category_definitions = category_definitions

    def __call__(self, doc):
        matches = self.matcher(doc)
        doc_gi_categories = []
        for match_id, start, end in matches:
            match_name = doc.vocab.strings[match_id]
            match_span = doc[start:end]
            gi_tags = self.matcher_lookup[match_name]["categories"]
            for token in match_span:
                token._.gi_tags = gi_tags
            doc_gi_categories.extend(gi_tags)
        doc._.gi_tags = dict(Counter(doc_gi_categories))
        return doc

    def explain(self, category: str):
        no_def = f"No definition for category given: {category}"
        return self.category_definitions.get(category, no_def)
