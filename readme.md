# General Inquirer

This is a version of the [General Inquirer](http://www.wjh.harvard.edu/~inquirer/) (GI) that operates as a [spaCy](https://spacy.io/) extension.

## Example

```python
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
```

```
{'Know': 2, 'Active': 6, 'Abs@': 1, 'ABS': 1, 'EnlOth': 5, 'EnlTot': 5, 'Strong': 7, 'Ovrst': 2, 'Quan': 2, 'Positiv': 5, 'Pstv': 5, 'Virtue': 4, 'AffOth': 1, 'AffTot': 1, 'Increas': 1, 'IAV': 2, 'EndsLw': 2, 'Means': 4, 'SklOth': 1, 'SklTot': 1, 'Academ': 2, 'ECON': 1, 'Object': 1, 'Tool': 1, 'Submit': 1, 'ComForm': 2, 'COM': 2, 'FormLw': 2, 'Solve': 1, 'Work': 1, 'PowCoop': 1, 'PowTot': 1, 'EVAL': 2, 'Undrst': 1, 'Compare': 1, 'PosAff': 1}
```

```python
# categories per token also available
for token in next(doc.sents):
    print(token.text, token._.gi_cats)
```

```
Content ['Know']
analysis ['Active', 'Know', 'Abs@', 'ABS', 'EnlOth', 'EnlTot']
is []
one []
of []
the []
most ['Strong', 'Ovrst', 'Quan']
popular ['Positiv', 'Pstv', 'Strong', 'Virtue', 'AffOth', 'AffTot']
and []
rapidly []
expanding ['Strong', 'Active', 'Increas', 'IAV', 'EndsLw']
techniques ['Means', 'SklOth', 'SklTot']
for []
quantitative []
research ['Active', 'Academ', 'Means', 'EnlOth', 'EnlTot']
. []
```
## License

Still figuring this out...

Please note the unclear copyright status for commercial use. From the [original spreadsheet documentation](http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm):

> **General Inquirer Categories as Intellectual Property.**
>
> The development of the General Inquirer has been supported by grants from American, British and Australian government science foundations and by industry. Those who developed and contributed categories have done so with the understanding that they could be used by others for academic research. Many categories have a long and complicated history and may be copyrighted at one point or another. Persons who would like to use any category for any commercial use should first send an email to inquirer@wjh.harvard.edu describing its intended use and arrange a permission for that application.