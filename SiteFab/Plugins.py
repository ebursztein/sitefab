""" 
SiteFab Plugin system
"""

import os
from termcolor import colored, cprint
import utils
from tqdm import tqdm
from yapsy.PluginManager import PluginManager
import logging 
from toposort import toposort, toposort_flatten
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
### Plugin type classes ###
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

class  SitePreparsing():
    "Site wide plugins that execute before the parsing start. Plugin are called only once."

    def process(self, unused, site):
        """ Process the content of the site once  
        :param FabSite site: the site object 
        """

class SiteProcessor():
    "Plugins that process the whole site once"

    def process(self, unused, site):
        """ Process the content of the site once  
            :param FabSite site: the site object 
        """

class SiteRendering():
    "Plugins that render additional pages. Plugin only called once"

    def process(self, unused, site):
        """ Generate additional page or file  
            :param FabSite site: the site object 
        """

### Plugin management ###
class Plugins():
    """ 
    Class responsible to manage the plugins

    """

    # for plugin info structure
    PLUGIN_CAT = 0
    PLUGIN_NAME = 1
    PLUGIN_DESC = 2
    PLUGIN_ENABLE = 3
    PLUGIN_MODULE_NAME = 4


    def __init__(self, plugin_directory, debug_log_fname, plugins_config):
        "Load plugins"
        self.plugins = PluginManager(plugin_info_ext='sitefab-plugin', categories_filter={ 
            
            "PostProcessor": PostProcessor,
            "CollectionProcessor": CollectionProcessor,
            
            "SitePreparsing": SitePreparsing,
            "SiteProcessor": SiteProcessor,
            "SiteRendering": SiteRendering
            })
        self.plugins.setPluginPlaces([plugin_directory])
        self.plugins.locatePlugins()
        self.plugins.loadPlugins()
        self.plugins_config = plugins_config

        # List of enabled plugins
        self.plugins_enabled = {}
        for pl in self.get_plugins_info():
            if pl[self.PLUGIN_ENABLE]:
                self.plugins_enabled[pl[self.PLUGIN_MODULE_NAME]] = 1
        
        print "== Plugins =="
        print self.plugins_enabled
        # FIXME: make sure it is working
        #logging.basicConfig(filename=debug_log_fname, level=logging.DEBUG)

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
        """ Return the number of plugins available.
        
        :param str category: restrict to plugins that belong to a given category
        
        :rtype: int
        :return: number of plugins
        """
        plugins = self.get_plugins(category)
        return len(plugins)

    def get_plugin_module_name(self, plugin):
        """ Return the module name of a given plugin

        :param iPlugin plugin: the plugin requested

        :rtype: str
        :return: the module name
        """
        module_path = plugin.details.get("Core", "module")
        path, filename = os.path.split(module_path)
        return filename

    def get_plugin_dependencies(self, plugin):
        """ Return the dependency of a given plugin

        :param iPlugin plugin: the plugin requested

        :rtype: list
        :return: list of plugins name the plugin depend on
        """

        # No dependencies
        if not plugin.details.has_option("Core", "Dependencies"):
            return set()

        dependencies = set()
        st = plugin.details.get("Core", "Dependencies")
        if "," in st:
            elts = st.split(",")
            for elt in elts:
                dependencies.add(dep.strip())
        else:
            dependencies.add(st)
        return dependencies

    def is_plugin_enabled(self, plugin):
        module_name = self.get_plugin_module_name(plugin)
        if module_name in self.plugins_config and self.plugins_config[module_name].enable:
            return True
        else:
            return False
        

    def get_plugins_info(self, category=None):
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
                enabled = self.is_plugin_enabled(plugin)
                module_name = self.get_plugin_module_name(plugin)
                s = [cat, plugin.name, plugin.description, enabled, module_name]
                pl.append(s)
        return pl

    def display_execution_results(self, results, site):
        """ Display execution summary
        """
        cprint("|-Execution result", "magenta")
        count = 0
        for result in results:
            plugin_name, stats = result  
            if count % 2:
                c = "blue"
            else:
                c = "cyan"

            name = colored("  |-%15s" % plugin_name, c)
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
        module_name_to_plugin = {} # used to get back from the module name to the plugin
        
        # computing plugin dependencies
        dependencie_map = {}
        plugins = self.plugins.getPluginsOfCategory(plugin_class)
        for plugin in plugins:
            if self.is_plugin_enabled(plugin):
                module_name = self.get_plugin_module_name(plugin)
                module_name_to_plugin[module_name] = plugin
                dependencies = self.get_plugin_dependencies(plugin)
                for dep_mod_name in dependencies:
                    if dep_mod_name not in self.plugins_enabled:
                        utils.error("Plugin:%s can't be executed because plugin %s is not enable" % (module_name, dep_mod_name))
                dependencie_map[module_name] = dependencies

        # Toplogical sorting
        try:
            plugins_to_process = toposort_flatten(dependencie_map)
        except Exception as e:
            utils.error("Circular dependencies between plugins. Can't execute plugins:%s" % s)



        desc = colored("|-Execution", "magenta")
        results = []
        for module_name in tqdm(plugins_to_process, unit=' plugin', desc=desc, leave=True):
            if module_name in module_name_to_plugin:
                plugin = module_name_to_plugin[module_name]
            else:
                raise Exception("The following plugin module name listed in dependencies don't exist %s " % module_name)
        
            pclass = plugin_class.lower()
            filename = "%s.%s.html" % (pclass, module_name)
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
            

            results.append([plugin.name, plugin_results])
            site.logger.write_log(log_id)
        return results