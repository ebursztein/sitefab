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
        

        log_info = "base javascript: %s<br>ouput:%s%s<br>" % (js_filename, output_path, js_filename)

        #Reading the base JS
        plugin_dir = os.path.dirname(__file__)
        js_file = os.path.join(plugin_dir, js_filename)
        js = files.read_file(js_file) 
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "Base Javascript:%s not found or too small." % js_file)
        

        ## TF-IDF to select the most important words in the text of the page
        
        idx = 1
        docs_string = "{"
        log_info += "<table><tr><th>Title</th><th>Keywords</th><th>Keywords TF-IDF</th><th>Abstract</th></tr>"
        for post in site.posts:

            nlp = site.plugin_data['nlp'][post.filename]
            
            keywords = "%s %s" % (nlp.category, " ".join(nlp.tags))
            tfidf_keywords = " ".join(sorted(nlp.grams[1], key=nlp.grams[1].get, reverse=True)[:num_tfidf_keywords])
            authors = " ".join(nlp.authors)
            conference = "%s %s" % (nlp.conference_short_name, nlp.conference_name)


            plugins = ""
            if 'responsive_images' in site.plugin_data:
                if post.meta.banner in site.plugin_data['responsive_images']:
                    plugins += '"srcsets":%s,' % site.plugin_data['responsive_images'][post.meta.banner]['srcsets']


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
                    "type": "%s",
                    %s
                },
            """ % (idx, idx, nlp.title, nlp.abstract, keywords, tfidf_keywords, authors, conference, post.meta.permanent_url, post.meta.banner, post.meta.template, plugins)
            idx += 1
            log_info += "<tr><td>%s</td>%s<td>%s</td><td>%s</td></tr>" % (nlp.title, nlp.keywords, tfidf_keywords, nlp.abstract)
        docs_string += "}"
        log_info += "</table>"

        ##output
        js = js.replace("SEARCH_DOC_PLUGIN_REPLACE", docs_string)
        path = os.path.join(site.get_output_dir(), output_path)
        files.write_file(path, js_filename, js)
        return (SiteFab.OK, plugin_name, log_info)