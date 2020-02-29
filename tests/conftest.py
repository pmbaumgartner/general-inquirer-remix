# content of ./test_smtpsimple.py
import pytest
import spacy


@pytest.fixture(scope="module")
def spacy_en_core_web_sm():
    nlp = spacy.load("en_core_web_sm")
    return nlp


@pytest.fixture(scope="module")
def spacy_en_core_web_lg():
    nlp = spacy.load("en_core_web_lg")
    return nlp
