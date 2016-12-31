from SiteFab.Plugins import SiteRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files

class Sitemap(SiteRendering):
    def process(self, unused, site):
        template_name = site.config.plugins.sitemap.template
        
        # Loading
        try:
            template = site.jinja2.get_template(template_name)
        except:
            return (SiteFab.ERROR, "sitemap", "can't find template:%s" % template_name)
        
        # Rendering
        try:
            rv = template.render(posts=site.posts, collections=site.collections, site_vars=site.vars)
        except Exception as e:
            return (SiteFab.ERROR, "sitemap", e)

        # output
        path = site.get_output_dir()
        files.write_file(path, 'sitemap.xml', rv)

        log_info = "template used:%s<br>ouput:%ssitemap.xml" % (template_name, path)
        return (SiteFab.OK, "sitemap", log_info)