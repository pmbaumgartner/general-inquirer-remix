import spacy
from spacy.matcher import Matcher
from spacy.tokens import Token
import jsonlines


class GICategories(object):
    def __init__(self, nlp):
        Token.set_extension("gi_cats", default=[])
        self.matcher = Matcher(nlp.vocab)
        with jsonlines.open("spacy.jsonl") as reader:
            match_objects = []
            for obj in reader:
                self.matcher.add(
                    obj["match_rules"]["LEMMA"], None, [obj["match_rules"]]
                )
                match_objects.append(obj)
        self.match_objects = match_objects

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []  # Collect the matched spans here
        #
        for match_id, start, end in matches:
            match_name = doc.vocab.strings[match_id]
            match_span = doc[start:end]
            for token in match_span:
                match_obj = next(
                    obj
                    for obj in self.match_objects
                    if obj["match_rules"]["LEMMA"] == match_name
                )
                gi_cats = match_obj["categories"]
                token._.gi_cats = gi_cats
        return doc


nlp = spacy.load("en_core_web_sm")
gi_cats = GICategories(nlp)
nlp.add_pipe(gi_cats, last=True)  # Add component to the pipeline
doc = nlp("He sustained a 5 day suspension.")
for token in doc:
    print(token.text, token._.gi_cats)
