import inspect
from collections import defaultdict
import os
import math
import re

from SiteFab.Plugins import ExtraRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files

class Search(ExtraRendering):
    def process(self, unused, site):
        plugin_name = "search"
        output_path = site.config.plugins.search.output_path
        num_tfidf_keywords = site.config.plugins.search.num_tfidf_keywords
        base_js_filename = "search.js" 
        
        #get the search basic javascript
        script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        js_file = os.path.join(script_dir, base_js_filename)
        
        js = files.read_file(js_file) 
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "base javascript not found or too small. Check:%s" % js_file)
        

        ## TF-IDF to select the most important words in the text of the page
        
        # compute df and tf
        df = defaultdict(float) # document frequency
        tf = defaultdict(lambda : defaultdict(float))
        num_doc = len(site.posts)
        for post in site.posts:
            txt = post.md.lower().replace("\n", " ").replace("-", " ").replace("\r", " ")
            txt = re.sub('[^a-z ]', '', txt)
            for tok in set(txt.split(" ")): #using set to get a count of document a token appears
                if len(tok) > 2:
                    df[tok] += 1
            for tok in txt.split(" "): #term frequency per document
                if len(tok) > 2:
                    tf[post.meta.permanent_url][tok] += 1

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

            authors = " ".join(post.meta.authors).replace(",", "")
            
            conference = ""
            if post.meta.conference_name:
                conference = "%s %s" % (post.meta.conference_name, post.meta.conference_short_name)
            
            keywords = ""
            if post.meta.category:
                keywords += "%s " % post.meta.category
            if post.meta.tags:
                keywords += " ".join(post.meta.tags)

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
                    "image_url": "%s"
                },
            """ % (count, count, post.meta.title, post.meta.abstract, keywords, tfidf_keywords, authors, conference, post.meta.permanent_url, post.meta.banner)
            count += 1
        docs_string += "}"

        js = js.replace("SEARCH_DOC_PLUGIN_REPLACE", docs_string)

        # output
        path = os.path.join(site.get_output_dir(), output_path)
        files.write_file(path, 'search.js', js)
        log_info = "base javascript: %s<br>ouput:%ssearch.js" % (js_file, path)
        return (SiteFab.OK, plugin_name, log_info)