from sitefab.Plugins import CollectionProcessor
from sitefab.SiteFab import SiteFab


class FullUrl(CollectionProcessor):

    def process(self, collection, site, config):
        safe = collection.meta.name.replace(" ", "-").lower()
        url = "%s/%s%s" % (site.config.url, site.config.collections.output_dir, safe)
        collection.meta.full_url = url
        return SiteFab.OK, collection.meta.name, url
