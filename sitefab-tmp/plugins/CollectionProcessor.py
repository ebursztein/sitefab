class CollectionProcessor():
    "Plugins that process each collection between parsing and rendering"

    def process(self, post, site, config):
        """ Process a parsed post to add extra meta or change its HTML.

        Args:
            post (post): post to process.
            site (SiteFab): instanciated site object.
            config (objectdict): plugin configuration.
        """
