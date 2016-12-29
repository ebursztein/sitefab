""" 
SiteFab Plugin system
"""

from termcolor import colored, cprint
import utils
from tqdm import tqdm
from yapsy.PluginManager import PluginManager
import logging 


### Plugin type classes ###
class ContentPreparsing():
    "Plugins that process content files before the parsing"

    def process(self, filename, site):
        """ Process a parsed post to add extra meta or change its HTML  
            :param str filename: the filename of the content file process
            :param FabSite site: the site object 
        """

class PostProcessor():
    "Plugins that process each post between the parsing and the rendering"

    def process(self, post, site):
        """ Process a parsed post to add extra meta or change its HTML  
            :param post post: the post to process
            :param FabSite site: the site object 
        """

class CollectionProcessor():
    "Plugins that process each collection between the parsing and the rendering"
    
    def process(self, post, site):
        """ Process a parsed post to add extra meta or change its HTML  
            :param collection collection: the collection to process
            :param FabSite site: the site object 
        """

class SiteProcessor():
    "Plugins that process the whole site once"

    def process(self, unused, site):
        """ Process the content of the site once  
            :param FabSite site: the site object 
        """

class ExtraRendering():
    "Plugins that render additional pages"

    def process(self, unused, site):
        """ Generate additional page or file  
            :param FabSite site: the site object 
        """

### Plugin management ###
class Plugins():
    """ 
    Class responsible to manage the plugins

    """
    def __init__(self, plugin_directory, debug_log_fname):
        "Load plugins"
        self.plugins = PluginManager(plugin_info_ext='sitefab-plugin', categories_filter={ 
            "ContentPreparsing": ContentPreparsing,
            "PostProcessor": PostProcessor,
            "CollectionProcessor": CollectionProcessor,
            "SiteProcessor": SiteProcessor,
            "ExtraRendering": ExtraRendering
            })
        self.plugins.setPluginPlaces([plugin_directory])
        self.plugins.locatePlugins()
        self.plugins.loadPlugins()
        # FIXME: make sure it is working
        logging.basicConfig(filename=debug_log_fname, level=logging.DEBUG)

    def get_plugins(self, category=None):
        """Return the list of plugins
        
        :param str category: restrict to plugins that belong to a given category
        
        :rtype: list(iPlugin)
        :return: list of plugins
        """
        if category:
            return self.plugins.getPluginsOfCategory(category)
        else:
            return self.plugins.getAllPlugins()

    def get_num_plugins(self, category=None):
        """Return the number of plugins available
        
        :param str category: restrict to plugins that belong to a given category
        
        :rtype: int
        :return: number of plugins
        """
        plugins = self.get_plugins(category)
        return len(plugins)

    def get_plugin_info(self, category=None):
        """Return the list of plugins available with their type
        
        :param str category: restrict to plugins that belong to a given category
        
        :rtype: list(str)
        :return: list of plugins name
        """

        pl = []
        if category:
            categories = [category] 
        else:
            categories = self.plugins.getCategories()
        for cat in categories:
            for plugin in self.plugins.getPluginsOfCategory(cat):
                s = [cat, plugin.name, plugin.description]
                pl.append(s)
        return pl

    def display_execution_results(self, results, site):
        """ Display execution summary
        """
        cprint("|-Execution result", "magenta")
        count = 0
        for plugin, stats in results.iteritems():
            if count % 2:
                c = "blue"
            else:
                c = "cyan"

            name = colored("  |-%15s" % plugin, c)
            ok = colored("ok:%s"% stats[site.OK], "green")
            skip = colored("skip:%s" % stats[site.SKIPPED], "yellow")
            err = colored("error:%s" % stats[site.ERROR], "red")
            print "%s\t%s\t%s\t%s" % (name, ok, skip, err)
            count += 1

    def run_plugins(self, items, plugin_class, unit, site):
        """Execute a set of plugins on a given list of items

        :param list items: list of items to process
        :param str plugin_type: the plugin_class to use
        :param str unit: the unit to use in the display
        :param SiteFab site: pointer to the site object to be passed to the plugins

        :rtype: dict(dict(list))
        :return: plugins execution statistics
        """
        results = {}
        import pprint
        desc = colored("|-Execution", "magenta")
        plugins = self.plugins.getPluginsOfCategory(plugin_class)
        for plugin in tqdm(plugins, unit=' plugin', desc=desc, leave=True):
            
            
            module = plugin.details.get("Core", "Module").split("/")[-1]
            pclass = plugin_class.lower()

            filename = "%s.%s.html" % (pclass, module)
            log_id = site.logger.create_log(pclass, plugin.name, filename)

            plugin_results = utils.create_objdict({
                site.OK: 0,
                site.SKIPPED: 0,
                site.ERROR: 0
            })

            for item in tqdm(items, unit=unit, desc=plugin.name, leave=False):
                result = plugin.plugin_object.process(item, site)
                plugin_results[result[0]] += 1
                
                severity = result[0]
                name = result[1]
                details = result[2]
                site.logger.record_event(log_id, name, severity, details)
            

            results[plugin.name] = plugin_results
            site.logger.write_log(log_id)
        return results