from typing import List, Optional, Dict
from pydantic.dataclasses import dataclass
import re


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
        term {str} -- Entry from GI spreadsheet (TERM#N)

    Returns:
        str -- "Lemma" - term with no pound or number
    """
    return term.split("#")[0].lower()


adj_re = re.compile(r'\% adj: "(\S+)"')
adv_re = re.compile(r'\% adv: "(\S+)"')


def gi_tags_to_spacy_pos(entry: GIEntry) -> Optional[Dict[str, str]]:
    """Detects relevant `othtags` from GI and converts to
    a single spacy `POS`.
    
    Arguments:
        tags {List[str]} -- A list of `othtags` from GI.
    
    Returns:
        Optional[Dict[str, str]] -- A Dictionary of {'POS' : POS}. `None` if no mapping.
    """
    tags = entry["othtags"]
    if "Noun" in tags:
        return {"POS": "NOUN"}
    elif "Modif" in tags:
        adv_described = re.search(adv_re, entry["defined"])
        if adv_described:  # CONTINUAL#2
            return {"POS": "ADV"}
        else:
            return {"POS": "ADJ"}
    elif "SUPV" in tags:
        return {"POS": "VERB"}
    elif "LY" in tags:
        return {"POS": "ADV"}
    else:
        return None


def parse_lemma(entry: GIEntry) -> str:
    if "Modif" in entry["othtags"]:
        adj_described = re.search(adj_re, entry["defined"])
        if adj_described:
            return adj_described.group(1).lower()
        adv_described = re.search(adv_re, entry["defined"])
        if adv_described:  # CONTINUAL#2
            return adv_described.group(1).lower()
    return gi_term_to_lemma(entry["term"])


def gi_data_to_match_rules(entry: GIEntry) -> Dict[str, str]:
    lemma = {"LEMMA": parse_lemma(entry)}
    pos = gi_tags_to_spacy_pos(entry)
    if pos:
        return {**lemma, **pos}
    else:
        return lemma
