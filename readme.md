# General Inquirer

This is a version of the [General Inquirer](http://www.wjh.harvard.edu/~inquirer/) (GI) that operates as a [spaCy](https://spacy.io/) extension.

## Installation

Install from GitHub. 

```bash
pip install git+https://github.com/pmbaumgartner/general-inquirer-remix
```

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

nlp = spacy.load("en_core_web_lg")
gi_tags = GICategories(nlp)
nlp.add_pipe(gi_tags, last=True)
doc = nlp(text)

# Counter of categories per document
print(doc._.gi_tags)
```

```python
{'ABS': 1,
 'Abs@': 1,
 'Academ': 2,
 'Active': 9,
 'AffOth': 1,
 'AffTot': 1,
 'COM': 2,
 'ComForm': 2,
 'ECON': 1,
 'EVAL': 1,
 'EndsLw': 2,
 'EnlOth': 5,
 'EnlTot': 5,
 'FormLw': 2,
 'IAV': 3,
 'Increas': 1,
 'Intrj': 1,
 'Know': 2,
 'Means': 4,
 'Object': 1,
 'Ovrst': 4,
 'Positiv': 5,
 'PowCoop': 1,
 'PowTot': 1,
 'Power': 1,
 'Pstv': 5,
 'Quan': 2,
 'Rel': 1,
 'SklOth': 1,
 'SklTot': 1,
 'Solve': 1,
 'Strong': 7,
 'Submit': 1,
 'Time@': 2,
 'TimeSpc': 1,
 'Tool': 1,
 'Undrst': 2,
 'Virtue': 3,
 'WlbPhys': 1,
 'WlbTot': 1,
 'Work': 1}
```

```python
# categories per token also available
for token in next(doc.sents):
    print(token.text, token._.gi_tags)
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
rapidly ['Active', 'Ovrst', 'Time@']
expanding ['Strong', 'Active', 'Increas', 'IAV', 'EndsLw']
techniques ['Means', 'SklOth', 'SklTot']
for []
quantitative []
research ['Active', 'Academ', 'Means', 'EnlOth', 'EnlTot']
. []
```
## License

TBD (Unknown)

### From the Spreadsheet Download Page

From the [original spreadsheet documentation](http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm):

> **General Inquirer Categories as Intellectual Property.**
>
> The development of the General Inquirer has been supported by grants from American, British and Australian government science foundations and by industry. Those who developed and contributed categories have done so with the understanding that they could be used by others for academic research. Many categories have a long and complicated history and may be copyrighted at one point or another. Persons who would like to use any category for any commercial use should first send an email to inquirer@wjh.harvard.edu describing its intended use and arrange a permission for that application.

[ref]: Philip J. Stone, Dexter C. Dunphy, Marshall S. Smith, Daniel M. Ogilvie, and associates.
The General Inquirer: A Computer Approach to Content Analysis.
MIT Press, 1966.  