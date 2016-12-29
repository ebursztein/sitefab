from SiteFab.Plugins import CollectionProcessor
from SiteFab.SiteFab import SiteFab

class SortCollection(CollectionProcessor):
    def process(self, collection, site):
        collection.posts = site.sort_posts(collection.posts, SiteFab.SORT_BY_CREATION_DATE_DESC)
        return (SiteFab.OK, collection.meta.name, "")