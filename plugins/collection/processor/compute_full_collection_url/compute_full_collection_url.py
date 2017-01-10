from SiteFab.Plugins import CollectionProcessor
from SiteFab.SiteFab import SiteFab


class FullUrl(CollectionProcessor):
    def process(self, collection, site):
        safe = collection.meta.name.replace(" ", "-")
        url = "%s%s%s" % (site.config.url, site.config.collections.output_dir, safe)
        collection.meta.full_url = url
        return SiteFab.OK, collection.meta.name, url
