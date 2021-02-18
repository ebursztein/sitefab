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


def test_empty_stats():
    text = ""
    doc = make_spacy_doc(text, lang=SPACY_MODEL)
    stats = nlp.compute_stats(doc)
    assert stats.counts.sentences == 0
    assert stats.counts.words == 0
    assert stats.readibility == None


def test_terms():
    text = "the quick fox and the cat. The turtle and the rabbit."
    doc = make_spacy_doc(text, lang=SPACY_MODEL)
    terms = nlp.extract_key_terms(doc, num_terms=5)
    terms = [t[0] for t in terms]  # remove scores
    assert 'fox' in terms
    assert 'cat' in terms
    assert 'turtle' in terms
    assert 'rabbit' in terms


def test_empty_terms():
    text = ""
    doc = make_spacy_doc(text, lang=SPACY_MODEL)
    terms = nlp.extract_key_terms(doc, num_terms=5)
    assert terms == []


def test_single_term():
    text = "elie"
    doc = make_spacy_doc(text, lang=SPACY_MODEL)
    terms = nlp.extract_key_terms(doc, num_terms=5)
    assert terms[0][0] == 'elie'
    assert terms[0][1] == 1.0


def test_two_term_behavhior():
    """Case when there is less than 3 words and rank algo can't be used.
    """
    text = "search page"
    doc = make_spacy_doc(text, lang=SPACY_MODEL)
    terms = nlp.extract_key_terms(doc, num_terms=5)
    assert 'search' == terms[0][0]
    assert 0.5 == terms[0][1]
    assert 'page' == terms[1][0]
    assert 0.5 == terms[1][1]


def test_analyze_post(empty_post):
    empty_post.text = """
    Protecting accounts from credential stuffing attacks remains burdensome
    due to an asymmetry of knowledge: attackers have wide-scale access to
    billions of stolen usernames and passwords, while users and identity
    providers remain in the dark as to which accounts require remediation.
    In this paper, we propose a privacy-preserving protocol whereby a
    client can query a centralized breach repository to determine whether
    a specific username and password combination is publicly exposed,
    but without revealing the information queried. Here, a client can be an
    end user, a password manager, or an identity provider. To demonstrate the
    feasibility of our protocol, we implement a cloud service that mediates
    access to over 4 billion credentials found in breaches and a Chrome
    extension serving as an initial client. Based on anonymous telemetry
    from nearly 670,000 users and 21 million logins, we find that 1.5% of
    logins on the web involve breached credentials. By alerting users to this
    breach status, 26% of our warnings result in users migrating to a new
    password, at least as strong as the original. Our study illustrates how
    secure, democratized access to password breach alerting can help
    mitigate one dimension of account hijacking."""

    empty_post.meta.title = 'Protecting accounts from credential stuffing with\
                             password breach alerting'

    post_nlp = nlp.analyze_post(empty_post)
    assert post_nlp.stats.counts.words > 0
    assert post_nlp.stats.readability.flesch_kincaid_grade_level > 0
    assert 'password' in [t[0] for t in post_nlp.title_terms]
    assert 'password' in [t[0] for t in post_nlp.terms]
