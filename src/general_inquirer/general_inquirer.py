from spacy.matcher import Matcher
from spacy.tokens import Token, Doc
from collections import Counter
from pathlib import Path
import json


class GICategories(object):
    def __init__(self, nlp):
        Token.set_extension("gi_cats", default=[])
        Doc.set_extension("gi_cats", default={})
        self.matcher_lookup = json.loads(Path("assets/matcher-lookup.json").read_text())
        self.matcher = Matcher(nlp.vocab)
        for _id, match_data in self.matcher_lookup.items():
            self.matcher.add(_id, None, [match_data["match_rules"]])

    def __call__(self, doc):
        matches = self.matcher(doc)
        doc_gi_categories = []
        for match_id, start, end in matches:
            match_name = doc.vocab.strings[match_id]
            match_span = doc[start:end]
            gi_cats = self.matcher_lookup[match_name]["categories"]
            for token in match_span:
                token._.gi_cats = gi_cats
            doc_gi_categories.extend(gi_cats)
        doc._.gi_cats = dict(Counter(doc_gi_categories))
        return doc

