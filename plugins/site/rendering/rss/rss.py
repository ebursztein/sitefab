from datetime import datetime

from sitefab.Plugins import SiteRendering
from sitefab.SiteFab import SiteFab
from sitefab import files
from sitefab.parser.parser import Parser


class Rss(SiteRendering):

    def process(self, unused, site, config):
        template_name = config.template
        parser_config = config.parser_config

        config.banner = "%s%s" % (site.config.url, config.banner)
        config.icon = "%s%s" % (site.config.url, config.icon)
        config.logo_svg = "%s%s" % (site.config.url, config.logo_svg)

        # Loading
        try:
            template = site.jinja2.get_template(template_name)
        except:
            return SiteFab.ERROR, "rss", "can't find template:%s" % template_name

        cfg = Parser.make_config(parser_config) # initialize the parser config
        parser = Parser(cfg, site)

        rss_items = []
        count = 0
        posts = []
        for post in site.posts:
            posts.append(post)

        # sort posts from newer to older
        k = lambda x: x.meta.creation_date_ts
        posts.sort(key=k, reverse=True)

        for post in posts:
            if post.meta.hidden or (post.meta.microdata_type != "BlogPosting" and post.meta.microdata_type != "ScholarlyArticle" and post.meta.microdata_type != "PublicationEvent"):
                continue

            # parse the post with a customized parser
            file_content = files.read_file(post.filename)
            parsed_post = parser.parse(file_content)
            post.rss = parsed_post.html # adding the newly generated HTML as RSS

            formatted_rss_creation_date = datetime.fromtimestamp(int(post.meta.creation_date_ts)).strftime('%Y-%m-%dT%H:%M:%SZ')
            if post.meta.update_date_ts:
                formatted_rss_update_date = datetime.fromtimestamp(int(post.meta.update_date_ts)).strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                formatted_rss_update_date = formatted_rss_creation_date

            post.meta.formatted_creation = formatted_rss_creation_date
            post.meta.formatted_update = formatted_rss_update_date

            post.meta.author = post.meta.authors[0].replace(",", "")
            rss_items.append(post)
            count += 1
            if count == config.num_posts:
                break
        if not len(rss_items):
            return (SiteFab.ERROR, "rss", 'no RSS items')

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

