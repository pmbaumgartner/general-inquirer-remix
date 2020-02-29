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
