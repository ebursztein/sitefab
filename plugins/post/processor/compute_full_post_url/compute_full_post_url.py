from SiteFab.Plugins import PostProcessor
from SiteFab.SiteFab import SiteFab


class FullUrl(PostProcessor):
    def process(self, post, site, config):
        if post.meta.permanent_url:
            permanent_url = post.meta.permanent_url.strip()
            if site.config.url[-1] == "/":
                post.meta.full_url = "%s%s" % (site.config.url, permanent_url)
            else:
                post.meta.full_url = "%s/%s" % (site.config.url, permanent_url)

            log_info = "full url:%s" % post.meta.full_url

            return SiteFab.OK, post.meta.title, post.meta.full_url
        else:
            post.meta.full_url = site.config.url
            return SiteFab.OK, post.meta.title, post.meta.full_url
