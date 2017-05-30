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
class Autocomplete(SiteRendering):

    #@profile
    def process(self, unused, site, config):
        plugin_name = "autocomplete"
        js_filename = "autocomplete.js"
        AUTHOR_COEFF = 100
        CATEGORY_COEFF = 100
        TAG_COEFF = 50
        CONFERENCE_COEFF = 100
        # configuration
        output_path = config.output_path
        num_suggestions = config.num_suggestions
        min_words = config.min_words
        max_words = config.max_words
        min_word_letters = config.min_word_letters
        
        log_info = "base javascript: %s<br>ouput:%s%s" % (js_filename, output_path, js_filename)

        stop_words = nlp.build_stop_words(lang='en')

        #Reading the base JS
        plugin_dir = os.path.dirname(__file__)
        js_file = os.path.join(plugin_dir, js_filename)
        js = files.read_file(js_file) 
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "Base Javascript:%s not found or too small." % js_file)
                
        # Extracting ngram frequencies
        ngrams_frequencies = Counter()
        post_frequencies = Counter()
        post_taboo = {} #ensure it is only ocnunted once.
        num_doc = len(site.posts)
        
        for post in site.posts:
            info = []
            info.append(post.md)
            info.append(post.meta.title)
            #print info
            txt = " ".join(info)
            txt = nlp.clean_text(txt)
            words = txt.split()
            #remove stop words
            words = nlp.remove_stop_words(words, stop_words)
            words = nlp.remove_words_by_length(words, min_word_letters)
            
            #extracting ngrams
            #max_words += 1  # range requires +1
            title = post.meta.title # prevent slow lookup
            num_words = len(words)
            for i in xrange(num_words):
                start = i + min_words
                stop = min(num_words, i +  max_words) + 1
                for j in xrange(start, stop):
                    n = " ".join(words[i:j]).strip()
                    ngrams_frequencies[n] += 1
                    idx = "%s-%s" % (title, n)
                    if idx not in post_taboo:
                        post_frequencies[n] += 1
                        post_taboo[idx] = 1
        
            #other field
            if "authors" in post.meta:
                for author in post.meta.authors:
                    author = author.strip().lower().replace(",", '')
                    author = nlp.remove_duplicate_space(author)
                    ngrams_frequencies[author] += AUTHOR_COEFF
                    post_frequencies[author] += 1
            
            if post.meta.conference_name:
                conf = post.meta.conference_name.lower().strip()
                conf = nlp.remove_duplicate_space(conf)
                ngrams_frequencies[conf] += CONFERENCE_COEFF
                post_frequencies[conf] += 1
           
            if post.meta.conference_short_name:
                short = post.meta.conference_short_name.lower().strip()
                short = nlp.remove_duplicate_space(short)
                ngrams_frequencies[short] += CONFERENCE_COEFF
                post_frequencies[short] += 1
            
            if post.meta.category:
                category = post.meta.category.lower().strip()
                category = nlp.remove_duplicate_space(category)
                ngrams_frequencies[category] += CATEGORY_COEFF
                post_frequencies[category] += 1

            if post.meta.tags:
                for tag in post.meta.tags:
                    tag = tag.lower().strip()
                    tag = nlp.remove_duplicate_space(tag)
                    ngrams_frequencies[tag] += TAG_COEFF
                    post_frequencies[tag] += 1

        # weigth by frequency and blog post
        max_grams = num_suggestions * 10
        scored_ngrams = Counter()
        for ngram in ngrams_frequencies.most_common(max_grams):
            word = ngram[0]
            ngram_freq = int(ngram[1]) + 1 # avoid the case of the word being there only once
            post_freq = post_frequencies[word]
            score = ngram_freq* post_freq * 5
            #score = pow(ngram_freq, post_freq),
            scored_ngrams[word] = min(score, 100000)

        
        output = []
        log_info += "num of ngram considered: %s<br>" % len(ngrams_frequencies)
        log_info += "<table><tr><th>ngram</th><th>score</th><th>post frequency</th><th>total frequency</th></tr>"
        for info in scored_ngrams.most_common(num_suggestions):
            word = info[0]
            score = info[1]
            post_freq = post_frequencies[word]
            ngram_freq = ngrams_frequencies[word]
            log_info += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (word, score, post_freq, ngram_freq)
            output.append([word, post_freq, score])
        log_info += "</table>"
        
        # replacing placeholder with computation result
        output_string = json.dumps(output)
        js = js.replace("AUTOCOMPLETE_PLUGIN_REPLACE", output_string)

        # output
        path = os.path.join(site.get_output_dir(), output_path)
        files.write_file(path, js_filename, js)
 
        return (SiteFab.OK, plugin_name, log_info)