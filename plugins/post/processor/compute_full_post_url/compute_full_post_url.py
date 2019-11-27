from sitefab.Plugins import PostProcessor
from sitefab.SiteFab import SiteFab


class FullUrl(PostProcessor):
    def process(self, post, site, config):
        if post.meta.permanent_url:
            permanent_url = post.meta.permanent_url.strip()

            if site.config.url[-1] != "/" and permanent_url[0] != "/":
                post.meta.full_url = "%s/%s" % (site.config.url, permanent_url)
            elif site.config.url[-1] == "/" and permanent_url[0] == "/":
                post.meta.full_url = "%s%s" % (site.config.url[:1],
                                               permanent_url)
            else:
                post.meta.full_url = "%s%s" % (site.config.url, permanent_url)

            return SiteFab.OK, post.meta.title, post.meta.full_url
        else:
            post.meta.full_url = site.config.url
            return SiteFab.OK, post.meta.title, post.meta.full_url
