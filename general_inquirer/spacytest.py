import spacy
from general_inquirer import GICategories

text = (
    "Content analysis is one of the most popular"
    " and rapidly expanding techniques for quantitative research."
    " Advances in computer applications and in digital media"
    " have made the organized study of messages quicker"
    " and easier... but not automatically better. "
)
# Krippendorff, K. (2019). Content analysis : an introduction to its methodology.

nlp = spacy.load("en")
gi_cats = GICategories(nlp)
nlp.add_pipe(gi_cats, last=True)
doc = nlp(text)

# Counter of categories per document
print(doc._.gi_cats)

# categories per token also available
for token in next(doc.sents):
    print(token.text, token._.gi_cats)
