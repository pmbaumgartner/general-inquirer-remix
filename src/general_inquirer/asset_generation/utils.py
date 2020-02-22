from typing import List, Optional, Dict
from pydantic.dataclasses import dataclass


@dataclass
class GIEntry:
    id: int
    term: str
    source: str
    othtags: List[str]
    defined: str
    categories: List[str]
    redundant: bool
    idiom: bool
    multiple: bool
    primary: bool


def primary_term(term: str) -> bool:
    """Determines if a term is the first or only term.
    
    Arguments:
        term {str} -- The term from GI (WORD#N)
    
    Returns:
        bool -- True if the term is the primary one.
    """
    if "#" in term:
        return term.endswith("#1")
    else:
        return True


def gi_term_to_lemma(term: str) -> str:
    """Converts the GI term to the
    lemma by removing the # and lowercasing.
    
    Arguments:
        term {str} -- [description]
    
    Returns:
        str -- [description]
    """
    return term.split("#")[0].lower()


def gi_tags_to_spacy_pos(tags: List[str]) -> Optional[Dict[str, str]]:
    """Detects relevant `othtags` from GI and converts to
    a single spacy `POS`.
    
    Arguments:
        tags {List[str]} -- A list of `othtags` from GI.
    
    Returns:
        Optional[Dict[str, str]] -- A Dictionary of {'POS' : POS}. `None` if no mapping.
    """
    if "Noun" in tags:
        return {"POS": "NOUN"}
    elif "MODIF" in tags:
        return {"POS": "ADJ"}
    elif "SUPV" in tags:
        return {"POS": "VERB"}
    elif "LY" in tags:
        return {"POS": "ADV"}
    else:
        return None


def data2rules(entry: GIEntry) -> Dict[str, str]:
    lemma = {"LEMMA": gi_term_to_lemma(entry["term"])}
    pos = gi_tags_to_spacy_pos(entry["othtags"])
    if pos:
        return {**lemma, **pos}
    else:
        return lemma
