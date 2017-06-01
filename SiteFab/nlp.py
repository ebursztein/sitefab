import re
from stop_words import get_stop_words

re_clean_text = re.compile('[^a-z -\']')
re_duplicate_space = re.compile(' +')

def get_normalized_list_of_words(txt, stop_words, word_min_letters=3, word_max_letters=16):
    """ Perform all the normalization steps in one pass
    Args:
        txt (str): text to normalize
        stop_words (set): set of stop words to remove
        word_min_letters (int): How many letter a word should be have at least  (usually 3 or 4)
        word_max_letters (int): How many letter a word should have at most (usually 16 to 18)
    Returns:
        list: normalized list of words
    
    """
    
    txt = clean_text(txt)
    words = txt.split(" ")
    words = remove_stop_words(words,stop_words)
    words = remove_words_by_length(words, word_min_letters, word_max_letters)
    return words


def clean_text(txt):
    "cleanup text to make easy to process for NLP task"
    txt = txt.lower().replace("\n", " ").replace("\r", " ")
    txt = txt.strip()
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
    # set lookup complexity is O(1)
    return set(stop_words)