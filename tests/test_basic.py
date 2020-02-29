from general_inquirer import GICategories


def test_basic_sm(spacy_en_core_web_sm):
    nlp = spacy_en_core_web_sm
    text = (
        "Content analysis is one of the most popular"
        " and rapidly expanding techniques for quantitative research."
        " Advances in computer applications and in digital media"
        " have made the organized study of messages quicker"
        " and easier... but not automatically better. "
    )

    gi_tags = GICategories(nlp)
    nlp.add_pipe(gi_tags, last=True)
    doc = nlp(text)

    assert doc._.gi_tags != {}


def test_basic_lg(spacy_en_core_web_lg):
    nlp = spacy_en_core_web_lg
    text = (
        "Content analysis is one of the most popular"
        " and rapidly expanding techniques for quantitative research."
        " Advances in computer applications and in digital media"
        " have made the organized study of messages quicker"
        " and easier... but not automatically better. "
    )

    gi_tags = GICategories(nlp)
    nlp.add_pipe(gi_tags, last=True)
    doc = nlp(text)

    assert doc._.gi_tags != {}


def test_explain(spacy_en_core_web_sm):
    nlp = spacy_en_core_web_sm
    gi_tags = GICategories(nlp)

    assert (
        gi_tags.explain("Positiv") == "1,915 words of positive outlook."
        " (It does not contain words for yes,"
        " which has been made a separate category of 20 entries.)"
    )


def test_explain_not_found(spacy_en_core_web_sm):
    nlp = spacy_en_core_web_sm
    gi_tags = GICategories(nlp)

    bad_category = "FAKE CATEGORY 12345"

    assert (
        gi_tags.explain(bad_category)
        == f"No definition for category given: {bad_category}"
    )
