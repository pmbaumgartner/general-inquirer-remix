import spacy
from general_inquirer import GICategories

nlp_v = spacy.load("en_core_web_sm")
gi_cats = GICategories(nlp_v)
nlp_v.add_pipe(gi_cats, last=True)  # Add component to the pipeline
doc = nlp_v(
    "Content analysis is one of the most popular and rapidly expanding techniques for quantitative research. Advances in computer applications and in digital media have made the organized study of messages quicker and easier but not automatically better. This book explores the current options for quantitative analyses of messages."
)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token._.gi_cats, sep="\t")
print(doc._.gi_cats)
