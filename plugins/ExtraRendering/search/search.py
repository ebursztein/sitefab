import inspect
import os

from SiteFab.Plugins import ExtraRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files

class Search(ExtraRendering):
    def process(self, unused, site):
        plugin_name = "search"
        output_path = site.config.plugins.search.output_path
        base_js_filename = "search.js" 
        
        #get the search basic javascript
        script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        js_file = os.path.join(script_dir, base_js_filename)
        
        js = files.read_file(js_file) 
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "base javascript not found or too small. Check:%s" % js_file)
        
        #generate posts data and adding it to the javascript
        count = 1
        docs_string = "{"
        for post in site.posts:
            docs_string += """
                "%s": {
                    "id": "%s",
                    "title": "%s",
                    "abstract": "%s"
                },
            """ % (count, count, post.meta.title, post.meta.abstract)
            count += 1
        docs_string += "}"

        js = js.replace("SEARCH_DOC_PLUGIN_REPLACE", docs_string)

        # output
        path = os.path.join(site.get_output_dir(), output_path)
        files.write_file(path, 'search.js', js)
        log_info = "base javascript: %s<br>ouput:%ssearch.js" % (js_file, path)
        return (SiteFab.OK, plugin_name, log_info)