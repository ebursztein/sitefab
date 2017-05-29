from collections import defaultdict
import os
import math
import json

from SiteFab.Plugins import SiteRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files
from SiteFab import utils

class Autocomplete(SiteRendering):

    
    def process(self, unused, site, config):
        plugin_name = "autocomplete"
        js_filename = "autocomplete.js"
        output_path = config.output_path

        # configuration
        num_suggestions = config.num_suggestions
        min_words = config.min_words
        max_words = config.max_words
        min_word_letters = config.min_word_letters

        log_info = "base javascript: %s<br>ouput:%s%s" % (js_filename, output_path, js_filename)



        #Reading the base JS
        plugin_dir = os.path.dirname(__file__)
        js_file = os.path.join(plugin_dir, js_filename)
        js = files.read_file(js_file) 
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "Base Javascript:%s not found or too small." % js_file)
                
        # Extracting ngram frequencies
        ngrams_frequencies = defaultdict(int) # ngrams frequency
        post_frequencies = defaultdict(dict)
        num_doc = len(site.posts)
        info = []
        for post in site.posts:
            info.append(post.md)
            info.append(post.meta.title)

            if "authors" in post.meta:
                info.append(" ".join(post.meta.authors).replace(",", " "))

            if post.meta.conference_name:
                info.append("%s %s" % (post.meta.conference_name, post.meta.conference_short_name))
            
            if post.meta.category:
                info.append("%s " % post.meta.category)

            if post.meta.tags:
                info.append(" ".join(post.meta.tags))

            txt = " ".join(info)
            txt = utils.cleaned_txt(txt)
            txt = utils.remove_stop_words(txt)
            words = txt.split()
            
            #extracting ngrams
            #max_words += 1  # range requires +1 
            for n in range(min_words, max_words):
                for gram in utils.find_ngrams(words, n):
                    
                    # check that each word in the ngram meet minimal size requirements
                    for w in gram:
                        if len(w) < min_word_letters:
                            continue
                    
                    s = " ".join(gram)
                    ngrams_frequencies[s] += 1
                    if post.meta.title not in post_frequencies[s]:
                        post_frequencies[s][post.meta.title] = 1
        
        suggestions  = sorted(ngrams_frequencies, key=ngrams_frequencies.get, reverse=True)[:num_suggestions]
        output = []
        log_info += "<table><tr><th>ngram</th><th>frequency</th><th>post frequency</th></tr>"
        for suggestion in suggestions:
            freq = ngrams_frequencies[suggestion]
            post_freq = len(post_frequencies[suggestion])
            log_info += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (suggestion, freq, post_freq)
            output.append([suggestion,post_freq])
        log_info += "</table>"
        
        # replacing placeholder with computation result
        output_string = json.dumps(output)
        js = js.replace("AUTOCOMPLETE_PLUGIN_REPLACE", output_string)

        # output
        path = os.path.join(site.get_output_dir(), output_path)
        files.write_file(path, js_filename, js)
 
        return (SiteFab.OK, plugin_name, log_info)