from SiteFab.Plugins import PostProcessor
from SiteFab.SiteFab import SiteFab

class FullUrl(PostProcessor):
    def process(self, post, site):
        if post.meta.permanent_url:
            post.meta.full_url = "%s/%s" % (site.config.url, post.meta.permanent_url)
            log_info = "full url:%s" % (post.meta.full_url)
            return (SiteFab.OK, post.meta.title, "")
        else:
            return (SiteFab.SKIPPED, post.meta.title, "")