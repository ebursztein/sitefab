import numpy as np
from perfcounters import PerfCounters
from tabulate import tabulate
from textacy import TextStats, make_spacy_doc, preprocessing
from textacy.text_stats import readability
from textacy.ke.yake import yake
from textacy.ke.textrank import textrank
from textacy.ke.sgrank import sgrank
from textacy.ke.scake import scake

from sitefab.utils import create_objdict, dict_to_objdict

# FIXME: use the config
NUM_TERMS = 50
SPACY_MODEL = 'en_core_web_sm'  # 'en_core_web_lg'
# python -m spacy download en_core_web_sm
TERM_EXTRACTOR_ALGO = 'yake'  # yake, sgrank, textrank
NGRAMS = (1, 2, 3)  # default


def softmax(results, reverse=False):
    """Normalize results values via softmax.

    Args:
        results (array): term extraction results.
        reverse (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """

    if len(np.asarray(results).shape) == 1:
        # !case when there are less than 3 words as the rank algo won't work
        fill_value = 1 / len(results)
        x = np.full(len(results), fill_value)
        results = [[t, 0] for t in results]
    else:
        x = np.array([i[1] for i in results])

    if reverse:
        x = 1 - x

    e_x = np.exp(x - np.max(x))
    scores = e_x / e_x.sum()

    normalized_terms = []
    for idx, s in enumerate(scores):
        normalized_terms.append([results[idx][0], float(s)])
    return normalized_terms


def extract_key_terms(doc, num_terms=50, ngrams=(1, 2, 3), algo='yake'):
    """Compute post most important terms

    This is particularly useful for the search and related posts

    Args:
        doc (Spacy.doc): Doc to extract terms from.
        num_terms (int, optional): How many terms to return. Defaults to 100.
        ngrams (int, optional): which size of ngrams to consider
        algo (str, optional): which algorithm to use to find key terms
    """
    if not len(doc):
        return []

    # special case
    if len(doc) < 3:
        return softmax(str(doc).split(' '))

    if algo == 'textrank':
        return softmax(textrank(doc, n_keyterms=NUM_TERMS))
    elif algo == 'yake':
        return softmax(yake(doc, ngrams=ngrams, topn=NUM_TERMS),
                       reverse=True)
    elif algo == 'scake':
        return softmax(scake(doc, topn=NUM_TERMS))
    elif algo == 'sgrank':
        return softmax(sgrank(doc, ngrams=ngrams,
                              n_keyterms=NUM_TERMS))
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
    # see https://github.com/LIAAD/yake
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
    counts = {'sentences': ts.n_sents,
              'words': ts.n_words,
              'unique_words': ts.n_unique_words,
              'chars': ts.n_chars,
              'chars_per_word': ts.n_chars_per_word,
              'long_words': ts.n_long_words,
              'syllables': ts.n_syllables,
              'syllables_per_word': ts.n_syllables_per_word,
              'monosyllable_words': ts.n_monosyllable_words,
              'polysyllable_words': ts.n_polysyllable_words
              }
    stats.counts = dict_to_objdict(counts)
    readability = {}
    if stats.counts.words > 0:
        readability = {'flesch_kincaid_grade_level': ts.flesch_kincaid_grade_level,
                       'flesch_reading_ease': ts.flesch_reading_ease,
                       'smog_index': 0,
                       'gunning_fog_index': ts.gunning_fog_index,
                       'coleman_liau_index': ts.coleman_liau_index,
                       'automated_readability_index': ts.automated_readability_index,
                       'lix': ts.lix,
                       }
    if stats.counts.sentences >= 30:
        readability['smog_index'] = ts.smog_index
    stats.readability = dict_to_objdict(readability)
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
    counters.start('make_spacy_docs')
    all_cleaned_content = ' '.join([clean_fields.title, clean_fields.category,
                                    " ".join(clean_fields.tags),
                                    clean_fields.abstract, clean_fields.text])

    # overall terms
    cleaned_doc = make_spacy_doc(all_cleaned_content, lang=SPACY_MODEL)

    # title terms
    title_doc = make_spacy_doc(clean_fields.title, lang=SPACY_MODEL)

    # for statistics
    text_doc = make_spacy_doc(post.text, lang=SPACY_MODEL)

    counters.stop('make_spacy_docs')

    # terms extraction
    counters.start('extract_key_terms')
    nlp.terms = extract_key_terms(cleaned_doc, num_terms=NUM_TERMS,
                                  algo=TERM_EXTRACTOR_ALGO, ngrams=NGRAMS)

    # !note we restrict ngram to one as we only want the lemmized top terms.
    nlp.title_terms = extract_key_terms(title_doc, num_terms=NUM_TERMS,
                                        algo=TERM_EXTRACTOR_ALGO, ngrams=1)

    counters.stop('extract_key_terms')

    # text stats
    counters.start('text_stats')
    nlp.stats = compute_stats(text_doc)
    counters.stop('text_stats')
    if debug:
        counters.report()
    return nlp
