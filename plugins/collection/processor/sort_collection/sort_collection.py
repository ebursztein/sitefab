from SiteFab.Plugins import CollectionProcessor
from SiteFab.SiteFab import SiteFab

class SortCollection(CollectionProcessor):
    """
    Sort Collection
    """
    def process(self, collection, site, config):
        collection.posts = site.sort_posts(collection.posts, SiteFab.SORT_BY_CREATION_DATE_DESC)
        return (SiteFab.OK, collection.meta.name, "")