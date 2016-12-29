import os
import operator
from tqdm import tqdm
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from termcolor import colored, cprint

import time
import files
import parser
from Logger import Logger
from Plugins import Plugins

import utils
from utils import warning




class SiteFab(object):
    """ Object representation of the site being built. 
    
    SiteFab main class 
    """

    SORT_BY_CREATION_DATE_DESC  = 1
    SORT_BY_CREATION_DATE = 2
    SORT_BY_UPDATE_DATE_DESC = 3
    SORT_BY_UPDATE_DATE = 4

    OK = 1
    SKIPPED = 2
    ERROR = 3

    def __init__(self, config_filename):
        
        # Timers
        self.timings  = utils.create_objdict()
        self.timings.start = time.time()

        ### Configuring ###
        self.current_dir = os.getcwd()

        # configuration
        if os.path.isfile(config_filename): #absolute path 
            self.config  = files.load_config(config_filename)
        else:
            cfg = os.path.join(files.get_site_path(), config_filename)
            if os.path.isfile(cfg):
                self.config = files.load_config(cfg)
            else:
                raise "can't find configuration: %s" % config_filename

        # template rendering engine init
        self.jinja2 = Environment(loader=FileSystemLoader(self.get_template_dir()))
        
        # plugins
        #fixme no more plugins dir conf
        print files.get_code_path()
        debug_log_fname = os.path.join(self.get_logs_dir(), "debug.log") # where to redirect the standard python log
        self.plugins = Plugins(self.get_plugins_dir(), debug_log_fname)
        self.plugins_results = defaultdict(int)
        
        # logger
        cfg = utils.create_objdict()
        cfg.output_dir = self.get_logs_dir()
        cfg.template_dir = os.path.join(files.get_code_path() + "/templates/") #internal template not the one from the users.
        cfg.log_template = "log.html" #FIXME: put the path into a config dir
        cfg.log_index_template = "log_index.html"
        self.logger = Logger(cfg, self)

        # finding content and assets
        self.filenames = utils.create_objdict()
        self.filenames.posts = files.get_content_files_list(self.get_content_dir())

        # finding assests
        #FIXME add asset here.

        ### Cleanup ###
        files.clean_dir(self.get_output_dir())
        
    ### Engine Stages ###
    def parse(self):
        "parse md content into post objects"

        filenames = self.filenames.posts
        self.posts = []
        self.collections = defaultdict(list)
        self.posts_by_templates = defaultdict(list)

        #Pre-parsing plugin 
        print "\nPre-processing content"
        self.execute_plugins(self.posts, "ContentPreparsing", " posts")

        print "\nParsing posts"
        for filename in tqdm(filenames, unit=' files', desc="Files"):
            file_content = files.read_file(filename)
            post = parser.parse(file_content)
            self.posts.append(post)
            
            # template
            if post.meta.template not in self.posts_by_templates:
                self.posts_by_templates[post.meta.template] = self.create_collection(post.meta.template)
            self.posts_by_templates[post.meta.template].posts.append(post)
            
            ## collections
            cols = []
            if post.meta.category:
                cols.append(post.meta.category)
            if post.meta.tags:
                for tag in post.meta.tags:
                    cols.append(tag)
            for col in cols:
                if col not in self.collections:
                    self.collections[col] = self.create_collection(col)
                self.collections[col].posts.append(post)
      
    def process(self):
        "Processing stage"

        # Posts processing
        print "\nPosts plugins"
        self.execute_plugins(self.posts, "PostProcessor", " posts")
        
        # collection processing
        print "\nCollections plugins"
        self.execute_plugins(self.collections.values(), "CollectionProcessor", " collections")

        # site wide processing
        print "\nSite wide plugins"
        self.execute_plugins([1], "SiteProcessor", " site")

    def render(self):
        "Rendering stage"
        
        print "\nRendering posts"
        self.render_posts()
        
        print "\nRendering collections"
        self.render_collections()
        
        print "\nRendering extra files"
        self.execute_plugins([1], "ExtraRendering", " pages")

    def finale(self):
        "Last stage"
        
        #last thing to do is to output the logs index
        self.logger.write_log_index()
        total_ts = round(time.time() - self.timings.start, 2)
        
        cprint("\nStatistics", 'magenta')
        cprint("|-Generation time: %s sec" % (total_ts), "cyan")
        cprint("|-Num Posts: %s" % len(self.posts), "blue")
        cprint("|-Num Collections: %s" % len(self.collections), "cyan")


        cprint("\nPlugins", 'magenta')
        cprint("|-Num plugins: %s" % (self.plugins.get_num_plugins()), "cyan")
        if self.plugins_results[self.ERROR]:            
            cprint("|-Num Errors:%s (check the logs!)" % self.plugins_results[self.ERROR], 'red')

        if self.plugins_results[self.SKIPPED]:
            cprint("|-Num Skipped:%s " % self.plugins_results[self.SKIPPED], 'yellow' )

    ### Post functions ###

    def get_posts(self, collection=None, template=None, order=1):
        """Return a list of ordered posts

        :param str collection: restrict to posts that belong to a given collection
        :param str template: restict to posts that belongs to a given template type
        :param int order: How to order the returned posts. Default: Inverted sorting date
        
        :rtype: list(post)
        :return: list of post
        """

        if collection:
            if collection in self.collections:
                posts = self.collections[collection]
            else:
                warning("can't find posts for collection:%s", collection)
                return []
        else:
            posts = self.posts
        
        selected_posts = []
        if template:
            for post in posts:
                if template in post.meta and post.meta.template == template:
                    selected_posts.append(post)
        else:
            selected_posts = posts

        selected_posts = self.sort_post(selected_posts, order)
        return selected_posts

    def get_num_posts(self, collection=None, template=None):
        """Return the numbers of posts available
        
        Args:
            collection: restrict count to a given collection
            template: restict to a given template type #FIXME:

        """
        posts = self.get_posts(collection=collection, template=template)
        return len(posts)

    def render_posts(self):
        "Render posts using jinja2 templates."
        
        for post in tqdm(self.posts, unit=' pages', miniters=1, desc="Posts"):
            template_name = "%s.html" % post.meta.template
            template = self.jinja2.get_template(template_name)            
            rv = template.render(content=post.html, meta=post.meta, collections=self.collections, posts_by_templates=self.posts_by_templates)
            path = "%s%s/" % (self.get_output_dir(), post.meta.permanent_url)
            path = path.replace('//', '/')
            files.write_file(path, 'index.html', rv)

    def sort_posts(self, posts, sorting_criteria):
        """ Sort a list of posts by a given field
        
        Args:
            posts (list): collection of post to sort.
            sorting_criteria (int): which field to sort by. See SORT_* macro

        Returns:
            list: ordered list of posts
        """
        if sorting_criteria == self.SORT_BY_CREATION_DATE or sorting_criteria == self.SORT_BY_CREATION_DATE_DESC:
            k = lambda x: x.meta.creation_date_ts
        elif sorting_criteria == self.SORT_BY_UPDATE_DATE or sorting_criteria == self.SORT_BY_UPDATE_DATE_DESC:
            k = lambda x: x.meta.update_date_ts
        else:
            raise "invalid sorting_criteria", sorting_criteria
            return posts

        reverse = False
        if sorting_criteria in [self.SORT_BY_CREATION_DATE_DESC, self.SORT_BY_UPDATE_DATE_DESC]:
            reverse = True
        
        posts.sort(key=k, reverse=reverse)
        return posts

    ### Collection functions ###

    def create_collection(self, name):
        "Create a post structure"
        
        collection = utils.create_objdict()
        collection.posts = []

        collection.meta = utils.create_objdict()
        collection.meta.name = name
        collection.meta.num_posts = 0
        
        return collection
        
    def render_collections(self):
        "Render collections pages."
        
        # Getting the data ready
        cols = self.collections.iterkeys()
        template = self.jinja2.get_template(self.config.collections.template) # load it once.
        path = "%s/%s" % (self.get_output_dir(), self.config.collections.output_dir)
        path = path.replace('//', '/')
        #print path
        #print cols
        min_posts = self.config.collections.min_posts
        rendered = 0

        for col in tqdm(cols, unit=' collections', miniters=1, desc="Collections"):
            if len(self.collections[col].posts) >= min_posts:
                collection = self.collections[col]
                meta = {
                    "collection_name": col,
                    "num_posts": len(collection)
                }
                filename = "%s.html" % (col)
                rv = template.render(collection=collection, meta=meta)
                files.write_file(path, filename, rv)


    ### Templates functions ###

    def get_num_templates(self):
        "Return the number of templates loaded."
        return len(self.jinja2.list_templates())

    def get_template_list(self):
        "Return the list of templates loaded."
        return self.jinja2.list_templates()

    ### Plugins ###
    def execute_plugins(self, items, plugin_class, unit):
        results = self.plugins.run_plugins(items, plugin_class, unit, self)
        self.plugins.display_execution_results(results, self)
        
        # sum all plugins data for recap
        for plugin, values in results.iteritems():
            for k, v in values.iteritems():
                self.plugins_results[k] += v


    ### Files and directories ###
    def get_site_info(self):
        "Return site information."
        return self.site
    
    def get_config(self):
        "Return sitefab config."
        return self.config
    
    def get_output_dir(self):
        "return the absolute path of the ouput dir"
        return os.path.join(files.get_site_path(), self.config.dir.output)

    def get_content_dir(self):
        "return the absolute path of the content dir"
        return os.path.join(files.get_site_path(), self.config.dir.content)
    
    def get_template_dir(self):
        "return the absolute path of the template dir"
        return os.path.join(files.get_site_path(), self.config.dir.templates)
    
    def get_logs_dir(self):
        "return the absolute path of the template dir"
        return os.path.join(files.get_site_path(), self.config.dir.logs)
    
    def get_plugins_dir(self):
        "return the absolute path for the plugins dir"
        return os.path.join(files.get_code_path() + "/plugins/")