from sitefab.Plugins import CollectionProcessor
from sitefab.SiteFab import SiteFab


class SortCollection(CollectionProcessor):
    """
    Sort Collection
    """

    def process(self, collection, site, config):

        if config.criteria == "udpate_date":
            k = lambda x: x.meta.update_date_ts
        else:
            k = lambda x: x.meta.creation_date_ts

        # note: recall sort do sorting in place!
        collection.posts.sort(key=k, reverse=True)

        return (SiteFab.OK, collection.meta.name, "")
