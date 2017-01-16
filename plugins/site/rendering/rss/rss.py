from datetime import datetime

from SiteFab.Plugins import SiteRendering
from SiteFab.SiteFab import SiteFab
from SiteFab import files


class Rss(SiteRendering):

    def process(self, unused, site, config):
        template_name = config.template
        rss_url = config.url

        config.url = "%s%s" % (site.config.url, rss_url)
        config.banner = "%s%s" % (site.config.url, config.banner)
        config.icon = "%s%s" % (site.config.url, config.icon)
        config.logo_svg = "%s%s" % (site.config.url, config.logo_svg)
        config.banner = "%s%s" % (site.config.url, config.banner)

        # Loading
        try:
            template = site.jinja2.get_template(template_name)
        except:
            return SiteFab.ERROR, "rss", "can't find template:%s" % template_name

        rss_items = []
        for post in site.posts:
            if post.meta.microdata_type != "BlogPosting" and post.meta.microdata_type != "ScholarlyArticle":
                continue

            formatted_rss_creation_date = datetime.fromtimestamp(int(post.meta.creation_date_ts)).strftime('%Y-%m-%dT%H:%M:%SZ')
            if post.meta.update_date_ts:
                formatted_rss_update_date = datetime.fromtimestamp(int(post.meta.update_date_ts)).strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                formatted_rss_update_date = formatted_rss_creation_date

            post.meta.formatted_creation = formatted_rss_creation_date
            post.meta.formatted_update = formatted_rss_update_date

            post.meta.author = post.meta.authors[0].replace(",", "")
            rss_items.append(post)

        config.formatted_update = rss_items[0].meta.formatted_update

        try:
            rv = template.render(site=site, rss=config, items=rss_items)
        except Exception as e:
            return (SiteFab.ERROR, "rss", e)

        # output
        path = site.get_output_dir()
        files.write_file(path, 'rss.xml', rv)

        log_info = "template used:%s<br>ouput:%srss.xml" % (template_name, path)
        return SiteFab.OK, "rss", log_info

