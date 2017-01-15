from SiteFab.Plugins import SiteRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files


class Sitemap(SiteRendering):

    def process(self, unused, site):
        template_name = site.config.plugins.rss.template

        # Loading
        try:
            template = site.jinja2.get_template(template_name)
        except:
            return SiteFab.ERROR, "sitemap", "can't find template:%s" % template_name

