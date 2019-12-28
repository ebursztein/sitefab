from sitefab import nlp
from sitefab.nlp import SPACY_MODEL
from textacy import make_spacy_doc


def test_text_cleanup():
    snips = [
                """@test@""",
                " test  ",
                " TeSt ",
                "-#, test, "
    ]

    for snip in snips:
        assert nlp.text_cleanup(snip) == 'test'


def test_stats():
    text = "the quick fox and the cat. The turtle and the rabbit."
    doc = make_spacy_doc(text, lang=SPACY_MODEL)
    stats = nlp.compute_stats(doc)
    assert stats.counts.sentences == 2
    assert stats.counts.words == 11


def test_terms():
    text = "the quick fox and the cat. The turtle and the rabbit."
    doc = make_spacy_doc(text, lang=SPACY_MODEL)
    terms = nlp.extract_key_terms(doc, num_terms=5)
    terms = [t[0] for t in terms]  # remove scores
    assert 'fox' in terms
    assert 'cat' in terms
    assert 'turtle' in terms
    assert 'rabbit' in terms
