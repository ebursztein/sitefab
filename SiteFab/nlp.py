import numpy as np
from perfcounters import PerfCounters
from tabulate import tabulate
from textacy import TextStats, keyterms, make_spacy_doc, preprocessing
from textacy.ke.yake import yake

from sitefab.utils import create_objdict

# FIXME: use the config
NUM_TERMS = 50
SPACY_MODEL = 'en_core_web_sm'  # 'en_core_web_lg'
TERM_EXTRACTOR_ALGO = 'yake'  # yake, sgrank, textrank


def softmax(results, reverse=False):
    """Normalize results values via softmax.

    Args:
        results (array): term extraction results.
        reverse (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    x = np.array([i[1] for i in results])

    if reverse:
        x = 1 - x

    e_x = np.exp(x - np.max(x))
    scores = e_x / e_x.sum()

    normalized_terms = []
    for idx, s in enumerate(scores):
        normalized_terms.append([results[idx][0], float(s)])
    return normalized_terms


def extract_key_terms(doc, num_terms=50, algo='yake'):
    """Compute post most important terms

    This is particularly useful for the search and related posts

    Args:
        num_terms (int, optional): How many terms to return. Defaults to 100.
        algo (str, optional): which algorithm to use to find key terms
    """
    if algo == 'textrank':
        return softmax(keyterms.textrank(doc, n_keyterms=NUM_TERMS))
    elif algo == 'yake':
        return softmax(yake(doc, ngrams=(1), topn=NUM_TERMS, window_size=3),
                       reverse=True)
    # elif algo == 'scake':
    #    results = scake(doc, topn=NUM_TERMS)
    elif algo == 'sgrank':
        return softmax(keyterms.sgrank(doc, ngrams=(1), n_keyterms=NUM_TERMS))
    else:
        err = 'Unknown key term extraction method:%s' % algo
        raise Exception(err)


def text_cleanup(text):
    "cleanup our text"

    text = preprocessing.replace_emails(text, replace_with='')
    text = preprocessing.replace_urls(text, replace_with='')
    text = preprocessing.replace_hashtags(text, replace_with='')
    text = preprocessing.replace_phone_numbers(text, replace_with='')
    text = preprocessing.replace_numbers(text, replace_with='')

    text = preprocessing.remove_accents(text)
    text = preprocessing.remove_punctuation(text)

    text = preprocessing.normalize_quotation_marks(text)
    text = preprocessing.normalize_hyphenated_words(text)
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = text.lower()

    text = preprocessing.normalize_whitespace(text)
    return text


def generate_clean_fields(post):
    "Generate a cleaned up version of the post and its metadata"
    clean_fields = create_objdict()

    # cleaned up fields
    clean_fields.title = ''
    if post.meta.title:
        clean_fields.title = text_cleanup(post.meta.title)

    clean_fields.abstract = ""
    if post.meta.abstract:
        clean_fields.abstract = text_cleanup(post.meta.abstract)

    clean_fields.authors = []
    if post.meta.authors:
        for author in post.meta.authors:
            clean_fields.authors.append(text_cleanup(author))

    # conference
    clean_fields.conference_name = []
    if post.meta.conference_name:
            clean_fields.conference_name = text_cleanup(
                post.meta.conference_name)

    clean_fields.conference_short_name = ""
    if post.meta.conference_short_name:
        clean_fields.conference_short_name = text_cleanup(
            post.meta.conference_short_name)

    # category, tags, etc
    clean_fields.category = ""
    if post.meta.category:
        clean_fields.category = text_cleanup(post.meta.category)

    clean_fields.tags = []
    if post.meta.tags:
        for tag in post.meta.tags:
            clean_fields.tags.append(text_cleanup(tag))

    # text
    clean_fields.text = ''
    if post.text:
        # !make sure to use post html and clean it to avoid markup keywords.
        clean_fields.text = text_cleanup(post.text)

    return clean_fields


def benchmark_term_extractor(doc, counters):
    "benchmark various term extractor algorithms"
    # TL;DR: yake is probably the best. Feel free to experiment
    # scake is not usable as is
    # sgrank is really really slow
    results = []
    methods = ['textrank', 'yake', 'sgrank']  # 'cake',     results = []
    for method in methods:
        counters.start(method)
        results.append(extract_key_terms(doc, algo=method))
        counters.stop(method)

    counters.report()
    table = []
    for idx in range(20):
        row = []
        for aidx in range(len(methods)):
            row.append(results[aidx][idx])
        table.append(row)

    print(tabulate(table, headers=methods))
    return counters


def compute_stats(doc):
    ts = TextStats(doc)
    stats = create_objdict()
    stats.readability = create_objdict(ts.readability_stats)

    fields = {'n_sents': 'sentences',
              'n_words': 'words',
              'n_unique_words': 'unique_words',
              'n_chars': 'chars',
              'n_long_words': 'long_words',
              'n_syllables': 'syllables',
              'n_monosyllable_words': 'monsyllable_words',
              'n_polysyllable_words': 'pollysyllable_words'
              }

    stats.counts = create_objdict()
    for src, dst in fields.items():
        if src in ts.basic_counts:
            stats.counts[dst] = ts.basic_counts[src]
        else:
            stats.counts[dst] = 0

    return stats


def analyze_post(post, debug=False):
    "Perform NLP analysis"

    counters = PerfCounters()
    nlp = create_objdict()

    # clean fields
    counters.start('cleanup')
    clean_fields = generate_clean_fields(post)
    nlp.clean_fields = clean_fields
    counters.stop('cleanup')

    # creating spacy docs
    counters.start('spacy_cleaned_doc')
    all_cleaned_content = ' '.join([clean_fields.title, clean_fields.category,
                                    " ".join(clean_fields.tags),
                                    clean_fields.abstract, clean_fields.text])

    # for term extraction
    cleaned_doc = make_spacy_doc(all_cleaned_content, lang=SPACY_MODEL)
    counters.stop('spacy_cleaned_doc')

    counters.start('spacy_text_doc')
    # for statistics
    text_doc = make_spacy_doc(post.text, lang=SPACY_MODEL)
    counters.stop('spacy_text_doc')

    # terms extraction
    counters.start('extract_key_terms')
    nlp.terms = extract_key_terms(cleaned_doc, num_terms=NUM_TERMS,
                                  algo=TERM_EXTRACTOR_ALGO)
    counters.stop('extract_key_terms')

    # text stats
    counters.start('text_stats')
    nlp.stats = compute_stats(text_doc)
    counters.stop('text_stats')
    if debug:
        counters.report()
    return nlp
