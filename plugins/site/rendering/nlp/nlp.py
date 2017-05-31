from collections import Counter, defaultdict
import os
import math
import json
import re

from SiteFab.Plugins import SiteRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files
from SiteFab import utils
from SiteFab import nlp


class NLP(SiteRendering):

    #@profile
    def process(self, unused, site, config):
        plugin_name = "nlp"

        # configuration
        min_word_letters = 3 #config.min_word_letters
        max_word_letters = 16 #config.max_word_letters
        #num_tfidf_keywords_per_post = config.num_tfidf_keywords_per_post

        # init
        
        stop_words = nlp.build_stop_words(lang='en')
        ngrams_frequencies = Counter()
        post_frequencies = Counter()
        post_taboo = {} #ensure it is only ocnunted once.
        num_doc = len(site.posts)
        df = defaultdict(float) # document frequency
        tf = defaultdict(lambda : defaultdict(float))
        num_doc = len(site.posts)
        log_info = ""
        
        # Article content TF-IDF
        for post in site.posts:
            words = nlp.get_normalized_list_of_words(post.md, stop_words, min_word_letters, max_word_letters)

            # Term frequency
            for word in words: 
                tf[post.meta.permanent_url][word] += 1
            
            # Document frequency
            for word in set(words): 
                df[word] += 1

        # Compute df - idf
        for slug, tokens in tf.iteritems():
            for tok, freq in tokens.iteritems():
                # Recommended formula 3 according to wikepedia
                tf[slug][tok] = (1 + math.log(freq)) * math.log((num_doc/df[tok]))



        
        # Building NLP version of the post by normalizing all the fields
        nlp_data = {}
        log_info += "<table><tr><th>post</th><th>nlp title</th><th>nlp abstract</th><th>top tf-idf keywords</th></tr>"
        for post in site.posts:
            post_nlp = utils.create_objdict() 

            tokens = tf[post.meta.permanent_url]
            post_nlp.txt_tfidf = sorted(tokens, key=tokens.get, reverse=True)

            post_nlp.title = ""
            if post.meta.title:
                post_nlp.title = " ".join(nlp.get_normalized_list_of_words(post.meta.title, stop_words, min_word_letters, max_word_letters))

            post_nlp.abstract = ""
            if post.meta.abstract:
                post_nlp.abstract = " ".join(nlp.get_normalized_list_of_words(post.meta.abstract, stop_words, min_word_letters, max_word_letters))

            post_nlp.authors = []
            if post.meta.authors:
                for author in post.meta.authors:
                    author = author.strip().lower().replace(",", '')
                    post_nlp.authors.append(nlp.remove_duplicate_space(author))

            post_nlp.conference_name = ""
            if post.meta.conference_name:
                post_nlp.conference_name = nlp.remove_duplicate_space(post.meta.conference_name.lower().strip())
                
            post_nlp.conference_short_name = ""
            if post.meta.conference_short_name:
                post_nlp.conference_short_name = nlp.remove_duplicate_space(post.meta.conference_short_name.lower().strip())
            
            post_nlp.category = ""
            if post.meta.category:
                post_nlp.category = nlp.remove_duplicate_space(post.meta.category.lower().strip())

            post_nlp.tags = []
            if post.meta.tags:
                for tag in post.meta.tags:
                    post_nlp.tags.append(nlp.remove_duplicate_space(tag.lower().strip()))
            
            nlp_data[post.meta.permanent_url] = post_nlp
            log_info += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (post.meta.permanent_url, post_nlp.title, post_nlp.abstract, post_nlp.txt_tfidf[:10])
        log_info += "</table>"
         
        site.plugin_data['nlp'] = nlp_data
        return (SiteFab.OK, plugin_name, log_info)