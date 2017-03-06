from tqdm import tqdm
from collections import defaultdict

import utils
import files

class PostCollections():
    "Handle posts collections"

    def __init__(self, template=None, path=None, min_posts=0):
        """Init the collections 

            Args:
                template (Template): the jinja2 template used to render the collections (optional)
                path (str): directory where to render the collections (optional)
                min_posts (int): minimal number of posts to render the category (optional)
        """
        self.collections = {}
        self.template = template
        self.path = path
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
            self.collections[name] = collection

        self.collections[name].posts.append(post)

    def render(self):
        "Render collections pages."

        for collection in tqdm(self.get_as_list(), unit=' collections', miniters=1, desc="Collections"):
                collection.meta.slug = collection.meta.name.replace(" ", "-").lower()
                collection.meta.num_posts = len(collection.posts)
                if collection.meta.num_posts >= self.min_posts:
                    filename = "%s.html" % (collection.meta.slug)
                    rv = self.template.render(collection=collection.posts, meta=collection.meta)
                    files.write_file(self.path, filename, rv)
    
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