from collections import defaultdict
import os
import math
import re

from SiteFab.Plugins import SiteRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files
from SiteFab import nlp

class Search(SiteRendering):
    def process(self, unused, site, config):
        plugin_name = "search"
        js_filename = "search.js" 
        output_path = config.output_path
        num_tfidf_keywords = config.num_tfidf_keywords
        
        stop_words = nlp.build_stop_words('en')


        log_info = "base javascript: %s<br>ouput:%s%s<br>" % (js_filename, output_path, js_filename)

        #Reading the base JS
        plugin_dir = os.path.dirname(__file__)
        js_file = os.path.join(plugin_dir, js_filename)
        js = files.read_file(js_file) 
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "Base Javascript:%s not found or too small." % js_file)
        

        ## TF-IDF to select the most important words in the text of the page
        
        # compute df and tf
        df = defaultdict(float) # document frequency
        tf = defaultdict(lambda : defaultdict(float))
        num_doc = len(site.posts)
        for post in site.posts:
            txt = nlp.clean_text(post.md)
            words = txt.split(" ")
            words = nlp.remove_stop_words(words, stop_words)
            words = nlp.remove_words_by_length(words, 3)
            
            # term frequency
            for word in words: 
                tf[post.meta.permanent_url][word] += 1
            
            # document frequency
            for word in set(words): 
                df[word] += 1

        # compute df - idf
        for slug, tokens in tf.iteritems():
            for tok, freq in tokens.iteritems():
                # Recommended formula 3 according to wikepedia
                tf[slug][tok] = (1 + math.log(freq)) * math.log((num_doc/df[tok]))

        #generate posts data and adding it to the javascript
        count = 1
        docs_string = "{"
        for post in site.posts:
            tokens = tf[post.meta.permanent_url]
            tfidf_keywords = " ".join(sorted(tokens, key=tokens.get, reverse=True)[:num_tfidf_keywords])

            authors = nlp.clean_text(" ".join(post.meta.authors))
            authors = nlp.remove_duplicate_space(authors)

            conference = ""
            if post.meta.conference_name:
                conference = "%s %s" % (post.meta.conference_name, post.meta.conference_short_name)
                conference = nlp.clean_text(conference)

            keywords = ""
            if post.meta.category:
                keywords += "%s " % post.meta.category
            if post.meta.tags:
                keywords += " ".join(post.meta.tags)
            keywords = nlp.clean_text(keywords)

            abstract = nlp.clean_text(post.meta.abstract)
            abstract = nlp.remove_stop_words(abstract, stop_words)
            title = nlp.clean_text(post.meta.title)
            title = nlp.remove_stop_words(title, stop_words)

            # add additional informations based of plugins
            plugins = ""
            if 'responsive_images' in site.plugin_data:
                if post.meta.banner in site.plugin_data['responsive_images']:
                    log_info += "found srcset for %s<br>" % post.meta.banner
                    plugins += '"srcsets":%s,' % site.plugin_data['responsive_images'][post.meta.banner]['srcsets']
                else:
                    log_info += "no_srcset for %s<br>" % post.meta.banner

            docs_string += """
                "%s": {
                    "id": "%s",
                    "title": "%s",
                    "abstract": "%s",
                    "keywords": "%s",
                    "tfidf": "%s",
                    "authors": "%s",
                    "conference": "%s",
                    "permanent_url": "%s",
                    "image_url": "%s",
                    %s
                },
            """ % (count, count, title, abstract, keywords, tfidf_keywords, authors, conference, post.meta.permanent_url, post.meta.banner, plugins)
            count += 1
        docs_string += "}"

        js = js.replace("SEARCH_DOC_PLUGIN_REPLACE", docs_string)

        # output
        path = os.path.join(site.get_output_dir(), output_path)
        files.write_file(path, js_filename, js)
        return (SiteFab.OK, plugin_name, log_info)