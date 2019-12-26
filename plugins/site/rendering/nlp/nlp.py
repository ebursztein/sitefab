from collections import defaultdict
import math

from sitefab.Plugins import SiteRendering
from sitefab.SiteFab import SiteFab
from sitefab import utils
from sitefab import nlp


class NLP(SiteRendering):

    # @profile
    def process(self, unused, site, config):
        plugin_name = "nlp"

        # configuration
        min_word_letters = config.min_word_letters
        max_word_letters = config.max_word_letters
        min_gram_len = 1
        max_gram_len = 3

        # init
        stop_words = nlp.build_stop_words(lang='en')
        log_info = ""

        taboo = {}  # ensure it is only occurs once.

        # ngram_len -> gram: frequency
        ngram_post_frequencies = defaultdict(lambda: defaultdict(float))

        # ngram_len -> post -> gram: frequency (ouch ^^)
        ngram_frequencies = defaultdict(lambda:
                                        defaultdict(lambda: defaultdict(float))
                                        )

        # Article content TF-IDF
        for post in site.posts:
            post_filename = post.filename  # minimize get_attr() call
            txt = post.md
            if post.meta.title:
                txt += post.meta.title
            if post.meta.abstract:
                txt += post.meta.abstract

            txt = nlp.clean_text(txt)
            words = txt.split(" ")

            num_words = len(words)

            for i in range(num_words):
                start = i + min_gram_len
                stop = min(num_words, i + max_gram_len) + 1
                for j in range(start, stop):
                    skip = False
                    gram = words[i:j]

                    # reject ngrams with stop words or which are too short/long
                    for w in gram:
                        if w in stop_words:
                            skip = True
                        if len(w) > max_word_letters:
                            skip = True
                        if len(w) < min_word_letters:
                            skip = True
                        if skip:
                            # print "skipping %s" % (" ".join(gram).strip())
                            continue

                    gram_len = len(gram)
                    gram = " ".join(gram).strip()

                    # gram frequency
                    ngram_frequencies[gram_len][post_filename][gram] += 1

                    # doc frequency
                    idx = "%s-%s" % (post_filename, gram)
                    if idx not in taboo:
                        ngram_post_frequencies[gram_len][gram] += 1
                        taboo[idx] = 1
                import pprint
                pprint.pprint(ngram_frequencies)
                quit()

        # Compute df - idf
        num_posts = len(site.posts)
        for gram_len, data in ngram_frequencies.items():
            for slug, grams in data.items():
                for gram, freq in grams.items():
                    global_freq = ngram_post_frequencies[gram_len][gram]
                    # print "gram_len:%s, post:%s\tgram:%s\tdoc freq:%s, \ttotal freq:%s" % (gram_len, slug.split("/")[-1][:20], gram, freq, global_freq)
                    # Recommended formula 3 according to wikepedia
                    ngram_frequencies[gram_len][slug][gram] = (
                        1 + math.log(freq)) * math.log((num_posts/global_freq))

        # Building NLP version of the post by normalizing all the fields
        nlp_data = {}
        log_info += "<table><tr><th>post</th><th>nlp title</th><th>nlp abstract</th><th>top 1-gram</th><th>2-grams</th></tr>"
        for post in site.posts:
            post_nlp = utils.create_objdict()

            post_nlp.grams = {}
            for gram_len in range(min_gram_len, max_gram_len + 1):
                post_nlp.grams[gram_len] = ngram_frequencies[gram_len][post.filename]

            post_nlp.title = ""
            if post.meta.title:
                post_nlp.title = " ".join(nlp.get_normalized_list_of_words(
                    post.meta.title, stop_words, min_word_letters, max_word_letters))

            post_nlp.abstract = ""
            if post.meta.abstract:
                post_nlp.abstract = " ".join(nlp.get_normalized_list_of_words(
                    post.meta.abstract, stop_words, min_word_letters, max_word_letters))

            post_nlp.authors = []
            if post.meta.authors:
                for author in post.meta.authors:
                    author = author.strip().lower().replace(",", '')
                    post_nlp.authors.append(nlp.remove_duplicate_space(author))

            post_nlp.conference_name = ""
            if post.meta.conference_name:
                post_nlp.conference_name = nlp.remove_duplicate_space(
                    post.meta.conference_name.lower().strip())

            post_nlp.conference_short_name = ""
            if post.meta.conference_short_name:
                post_nlp.conference_short_name = nlp.remove_duplicate_space(
                    post.meta.conference_short_name.lower().strip())

            post_nlp.category = ""
            if post.meta.category:
                post_nlp.category = nlp.remove_duplicate_space(
                    post.meta.category.lower().strip())

            post_nlp.tags = []
            if post.meta.tags:
                for tag in post.meta.tags:
                    post_nlp.tags.append(
                        nlp.remove_duplicate_space(tag.lower().strip()))

            nlp_data[post.filename] = post_nlp
            top_1grams = ", ".join(
                sorted(post_nlp.grams[1], key=post_nlp.grams[1].get, reverse=True)[:15])
            top_2grams = ", ".join(
                sorted(post_nlp.grams[2], key=post_nlp.grams[1].get, reverse=True)[:15])
            log_info += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                post.meta.permanent_url, post_nlp.title, post_nlp.abstract, top_1grams, top_2grams)
        log_info += "</table>"

        site.plugin_data['nlp'] = nlp_data
        return (SiteFab.OK, plugin_name, log_info)
