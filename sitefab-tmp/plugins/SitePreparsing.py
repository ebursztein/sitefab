class SitePreparsing():
    """Site wide plugins that execute before the parsing start.
    Plugin are called only once."""

    def process(self, unused, site, config):
        """ Process the content of the site once before parsing

        Args:
            unused (None): not used.
            site (SiteFab): instanciated site object.
            config (objectdict): plugin configuration.
        """
