import json

from sitefab.Plugins import CollectionProcessor
from sitefab.SiteFab import SiteFab


class JsonldCollection(CollectionProcessor):
    """
    Write microdata jsonld_collection

    """
    def process(self, collection, site, config):
        pre_txt = '<script type="application/ld+json">'
        post_txt = '</script>'

        jsonld_data = {"@context": "http://schema.org",
                       "@type": "CollectionPage",
                       "url": collection.meta.full_url,
                       "name": collection.meta.name,
                       "inLanguage": "English",
                       "description": "List of blog posts and publications\
                        about % s" % collection.meta.name
                       }

        jsonld_text = "%s%s%s" % (pre_txt, json.dumps(jsonld_data), post_txt)

        collection.meta.jsonld = jsonld_text

        return SiteFab.OK, collection.meta.name, collection.meta.jsonld
