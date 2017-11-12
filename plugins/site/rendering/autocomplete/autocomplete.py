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

        # configuration
        output_path = config.output_path
        num_suggestions = config.num_suggestions
        terms_to_exclude = config.excluded_terms
        
        log_info = "base javascript: %s<br>ouput:%s%s" % (js_filename, output_path, js_filename)

        #Reading the base JS
        plugin_dir = os.path.dirname(__file__)
        js_file = os.path.join(plugin_dir, js_filename)
        js = files.read_file(js_file) 
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "Base Javascript:%s not found or too small." % js_file)
        
        ngrams_frequencies = Counter()
        post_frequencies = Counter()
        total_score = 0
        total_doc = 0.0
        other_fields = Counter()
        for post in site.posts:
            post_filename = post.filename
            nlp = site.plugin_data['nlp'][post.filename]
            for gram_len, grams in nlp.grams.iteritems():
                for gram, score in grams.iteritems():
                    if gram in terms_to_exclude:
                        continue
                    ngrams_frequencies[gram] += score
                    total_score += score
                    post_frequencies[gram] += 1
                    total_doc += 1
        
        avg_score =  total_score / total_doc
        boost_score = avg_score * 1.3
        #print "%s %s %s" % (total_doc, total_score, avg_score)
        for post in site.posts:
            post_filename = post.filename
            nlp = site.plugin_data['nlp'][post.filename]  
            #other field
            for author in nlp.authors:
                other_fields[author] += boost_score
                post_frequencies[author] += 1
                # make sure autocomplete work on first and last name
                for tok in author.split(" "):
                    if len(tok) > 2: 
                        other_fields[tok] += boost_score
                        post_frequencies[tok] += 1
                         
            other_fields[nlp.conference_name] += boost_score
            post_frequencies[nlp.conference_name] += 1

            other_fields[nlp.conference_short_name] += boost_score
            post_frequencies[nlp.conference_short_name] += 1

            other_fields[nlp.category] += boost_score
            post_frequencies[nlp.category] += 1
            
            for tag in nlp.tags:
                other_fields[tag] += boost_score
                post_frequencies[tag] += 1

        del post_frequencies[""]
        del other_fields[""]
        
        # combining all the fields into a global list
        suggestions = Counter()
        ngram_num = num_suggestions - len(other_fields)
        for ngram in ngrams_frequencies.most_common(ngram_num):
            #score = ngram_freq* post_freq * 5
            #score = pow(ngram_freq, post_freq),
            suggestions[ngram[0]] = int(ngram[1])

        for val, score in other_fields.iteritems():
            suggestions[val] = score

        output = []
        log_info += "num of ngram considered: %s<br>" % len(ngrams_frequencies)
        log_info += "<table><tr><th>ngram</th><th>score</th><th>post frequency</th><th>tf-idf score</th></tr>"
        for info in suggestions.most_common(num_suggestions):
            word = info[0]
            score = int(info[1])
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
        log_info += "output directory: %s" % path
        files.write_file(path, js_filename, js)
 
        return (SiteFab.OK, plugin_name, log_info)