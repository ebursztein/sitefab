import re
from stop_words import get_stop_words

re_clean_text = re.compile('[^a-z \']')
re_duplicate_space = re.compile(' +')

def clean_text(txt):
    "cleanup text to make easy to process for NLP task"
    txt = txt.lower().replace("\n", " ").replace("\r", " ")
    txt = remove_duplicate_space(txt)
    return re_clean_text.sub('', txt)


def remove_words_by_length(words, min_letters, max_letters=16):
    "Remove words that are too short or to long"
    cleaned = []
    for w in words:
        l = len(w)
        if l < min_letters:
            continue
        if l > max_letters:
            continue

        cleaned.append(w)
    return cleaned

def remove_duplicate_space(txt):
    "Remove duplicate space"
    return re_duplicate_space.sub(' ', txt)

def remove_stop_words(slug, stop_words):
    """ Remove stops words from a list or a text.

    Args:
        words (str or list): text or array of word
        stop_words (set): set of stop words to remove
    
    Returns:
        str or list: cleaned up data
    
    Sanitize using intersection and list.remove()
    Pro:
        Fastest method
    Downsides:
        - Looping over list while removing from it?http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
    """

    return_str = False
    if isinstance(slug, str) or isinstance(slug, unicode):
        words = slug.split(" ")
        return_str = True
    else:
        words = slug

    for sw in stop_words.intersection(words):
        while sw in words:
            words.remove(sw)
    
    if return_str:
        return " ".join(words)
    return words

def build_stop_words(lang='en'):
    stop_words = get_stop_words(lang)
    ### adding additional stop words
    stop_words += ['can', 'will', 'use', 'one', 'using', 'used', 'also', 'see', 'first', 'like']
    stop_words += ['page', 'get', 'new', 'two', 'site', 'blog', 'many', "don't", 'dont', 'way']
    stop_words += ['last', 'best', 'able', 'even', 'next', 'last', 'let', "none", 'every', 'three']
    stop_words += ['lot', 'well', 'chart', 'much', 'based', 'important', 'posts', 'reads', 'least']
    stop_words += ['still', 'follow']
    return set(stop_words)