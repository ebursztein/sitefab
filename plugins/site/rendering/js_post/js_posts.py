import os
import json

from sitefab.Plugins import SiteRendering
from sitefab.SiteFab import SiteFab
from sitefab import files


class JSPosts(SiteRendering):

    #@profile
    def process(self, unused, site, config):
        plugin_name = "js_posts"
        js_filename = "js_posts.js"

        # configuration
        output_path = config.output_path
        meta_fields_to_output = config.meta_fields_to_output
        plugin_data_to_output = config.plugin_data_to_output

        log_info = "base javascript: %s<br>ouput:%s%s<br>" % (js_filename, output_path, js_filename)
        log_info = "meta fields to outputs:%s" % (", ".join(meta_fields_to_output))

        # Reading the base JS
        plugin_dir = os.path.dirname(__file__)
        js_file = os.path.join(plugin_dir, js_filename)
        js = files.read_file(js_file)
        if not js or len(js) < 10:
            return (SiteFab.ERROR, plugin_name, "Base Javascript:%s not found or too small." % js_file)

        js_posts = {}
        for post in site.posts:
            js_post = {}
            js_post['id'] = post.id
            for field in meta_fields_to_output:
                if field in post.meta:
                    js_post[field]  = post.meta[field]
            if 'responsive_banner' in plugin_data_to_output and 'responsive_images' in site.plugin_data:
                if post.meta.banner in site.plugin_data['responsive_images']:
                    js_post['banner_srcsets'] = site.plugin_data['responsive_images'][post.meta.banner]['srcsets']
            if 'thumbnail_banner' in plugin_data_to_output and 'thumbnails' in site.plugin_data:
                if post.meta.banner in site.plugin_data['thumbnails']:
                    js_post['thumbnails'] = site.plugin_data['thumbnails'][post.meta.banner]

            js_posts[post.id] = js_post

        # replacing placeholder with post data
        output_string = json.dumps(js_posts)
        log_info += "output string:<br>%s" % output_string
        js = str(js)
        js = js.replace("JS_POSTS_PLUGIN_REPLACE", output_string)

        # output
        path = os.path.join(site.get_output_dir(), output_path)
        log_info += "output directory: %s" % path
        files.write_file(path, js_filename, js)

        return (SiteFab.OK, plugin_name, log_info)