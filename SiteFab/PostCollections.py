import os
from tqdm import tqdm

from . import utils, files


class PostCollections():
    "Handle posts collections"

    def __init__(self, site, template=None, output_path=None, web_path=None,
                 min_posts=0):
        """Init the collections

            Args:
                site (SiteFab): current instance of SiteFab
                template (Template): the jinja2 template used to render the collections. If none can't be rendered (optional)
                path (str): directory where to render the collections. If none can't be rendered (optional)
                min_posts (int): minimal number of posts to render the category (optional)
        """

        self.site = site
        self.collections = {}
        self.template = template
        self.output_path = output_path
        self.web_path = web_path
        self.min_posts = min_posts

    def add(self, name, post):
        """Create a Collection

        Args:
            name (str): name of the Collection.
            post (Post): post to add to the collection
        Return:
            None
        """

        if name not in self.collections:
            collection = utils.dict_to_objdict()
            collection.posts = []

            collection.meta = utils.dict_to_objdict()
            collection.meta.name = name
            collection.meta.num_posts = 0
            if self.web_path:
                url = "/%s%s" % (self.web_path, name)
                url = url.replace(" ", "-").lower()
                collection.meta.url  = url
            self.collections[name] = collection
        self.collections[name].meta.num_posts += 1
        self.collections[name].posts.append(post)

    def render(self):
        "Render collections pages."

        for collection in tqdm(self.get_as_list(), unit=' collections', miniters=1, desc="Collections"):
                collection.meta.slug = collection.meta.name.replace(" ", "-").lower()
                if collection.meta.num_posts >= self.min_posts:
                    filename = "%s.html" % (collection.meta.slug)
                    rv = self.template.render(posts=collection.posts, meta=collection.meta, plugin_data=self.site.plugin_data, config=self.site.config)
                    new_path = os.path.join(self.output_path, collection.meta.slug)
                    files.write_file(new_path, "index.html", rv)

    def get_as_list(self):
        """Returns the collections as lists
        Return:
            list: collections as list
        """
        return self.collections.values()

    def get_as_dict(self):
        """ return the collections as dict
        Return:
            dict: collections as dict
        """

        return self.collections

    def get_num_collections(self):
        """ return the number of collections
        Return:
            int: number of collections
        """
        return len(self.collections)
