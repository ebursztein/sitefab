import os
import json

from SiteFab.Plugins import SiteRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files

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
        
        docs_string = "{"
        js_posts = {}
        log_info += "<table><tr><th>Title</th><th>Keywords</th><th>Keywords TF-IDF</th><th>Abstract</th></tr>"
        for post in site.posts:
            nlp = site.plugin_data['nlp'][post.filename]
            terms = []
            terms.append(nlp.category)
            terms.extend(nlp.tags)
            terms.extend(sorted(nlp.grams[1], key=nlp.grams[1].get, reverse=True)[:num_tfidf_keywords])
            terms = " ".join(set(terms))
            terms = terms.replace('"', '')

            js_post = {
                "id": post.id,
                "title": nlp.title,
                "authors": " ".join(nlp.authors),
                "conference": "%s %s" % (nlp.conference_short_name, nlp.conference_name),
                "terms": terms
            }
            js_posts[post.id] = js_post
            log_info += "<tr><td>%s</td><td>%s</td></tr>" % (nlp.title, terms)

        log_info += "</table>"

        ##output
        output_string = json.dumps(js_posts)
        output_string = output_string.replace('"', '\\"').replace('\\\\"', '\\"')
        js = js.replace("SEARCH_DOC_PLUGIN_REPLACE", output_string)
        path = os.path.join(site.get_output_dir(), output_path)
        files.write_file(path, js_filename, js)
        return (SiteFab.OK, plugin_name, log_info)