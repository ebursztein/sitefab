class SiteProcessor():
    "Plugins that process the whole site once during processing stage"

    def process(self, unused, site, config):
        """ Process the content of the site once during processing stage.

        Args:
            unused (None): not used.
            site (SiteFab): instanciated site object.
            config (objectdict): plugin configuration.
        """
