import json

from sitefab.Plugins import SitePreparsing
from sitefab.SiteFab import SiteFab
from sitefab import files


class Press(SitePreparsing):
    """
    build press list
    """

    def process(self, unused, site, config):
        log = ""
        errors = False
        plugin_name = "press"
        article_list = config.article_list

        try:
            articles = files.load_config(article_list)
        except:
            errors = True
            log += "can't open %s" % article_list
            return (SiteFab.ERROR, plugin_name, log)

        # reading from the yaml it self does not work and crash the soft.
        # forcing a serialization/deserialization
        site.plugin_data['press'] = json.loads(json.dumps(articles))
        log += "loaded %s press articles" % (len(articles))
        return (SiteFab.OK, plugin_name, log)
