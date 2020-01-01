class SiteRendering():
    """Plugins that render additional pages after processing.
    Plugin only called once"""

    def process(self, unused, site, config):
        """ Generate additional page or file after site is rendered

        Args:
            post (post): post to process.
            site (SiteFab): instanciated site object.
            config (objectdict): plugin configuration.
        """
