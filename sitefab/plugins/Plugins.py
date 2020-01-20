"""
SiteFab Plugin system
"""

import logging
import os
from pathlib import Path

from termcolor import colored, cprint
from terminaltables import SingleTable
from toposort import toposort_flatten
from tqdm import tqdm
from yapsy.PluginManager import PluginManager

from sitefab import utils

from .CollectionProcessor import CollectionProcessor
from .PostProcessor import PostProcessor
from .SitePreparsing import SitePreparsing
from .SiteProcessor import SiteProcessor
from .SiteRendering import SiteRendering
from .TemplateFilter import TemplateFilter

logging.basicConfig(level=logging.INFO)


class Plugins():
    """
    Class responsible to manage the plugins

    """

    categories = [
        ["SitePreparsing", SitePreparsing,
         "Site wide plugins that execute before the parsing start."],

        ["SiteProcessor", SiteProcessor,
         "Plugins that process the whole site once after parsing."],

        ["SiteRendering", SiteRendering,
         "Plugins that render additional pages after the rendering."],

        ["PostProcessor", PostProcessor,
         "Plugins that process each post after they are parsed"],

        ["CollectionProcessor", CollectionProcessor,
         "Plugins that process each collection after posts are parsed"],

        ["TemplateFilter", TemplateFilter,
         "Plugins that define jinja2 filters to be used in templates"],
    ]

    # for plugin info structure
    PLUGIN_CAT = 0
    PLUGIN_NAME = 1
    PLUGIN_DESC = 2
    PLUGIN_ENABLE = 3
    PLUGIN_MODULE_NAME = 4
    PLUGIN_VERSION = 5

    def __init__(self, plugin_directories, debug_log_fname, plugins_config):
        "Load plugins"

        categories_filter = {}
        for cat in self.categories:
            categories_filter[cat[0]] = cat[1]

        # single or multi-directory handling
        if not isinstance(plugin_directories, list):
            plugin_directories = [plugin_directories]

        self.plugins = PluginManager(plugin_info_ext='sitefab-plugin',
                                     categories_filter=categories_filter)
        self.plugins.setPluginPlaces(plugin_directories)

        self.plugins.locatePlugins()
        self.plugins.loadPlugins()

        self.plugins_config = plugins_config

        # List of enabled plugins
        self.plugins_enabled = {}
        for pl in self.get_plugins_info():
            if pl[self.PLUGIN_ENABLE]:
                self.plugins_enabled[pl[self.PLUGIN_MODULE_NAME]] = 1

        # list of plugins already executed. Used for dependencies tracking
        # across stages
        self.plugins_executed = {}

        # FIXME: make sure it is working
        # logging.basicConfig(filename=debug_log_fname, level=logging.DEBUG)

    def get_plugins(self, category=None):
        """Return the list of plugins

        :param str category: restrict to plugins of a given category

        :rtype: list(iPlugin)
        :return: list of plugins
        """
        if category:
            return self.plugins.getPluginsOfCategory(category)
        else:
            return self.plugins.getAllPlugins()

    def get_num_plugins(self, category=None):
        """ Return the number of plugins available.

        :param str category: restrict to plugins of given category

        :rtype: int
        :return: number of plugins
        """
        plugins = self.get_plugins(category)
        return len(plugins)

    def get_plugin_dir(self, plugin):
        """ Return the directory where the plugin is stored

        :param iPlugin plugin: the plugin requested

        :rtype: str
        :return: the module name
        """

        module_path = Path(plugin.details.get("Core", "module"))
        return module_path.parent

    def get_plugin_default_configuration_filename(self, plugin):
        """ Return the path to the plugin default configuration filename
        """
        try:
            fname = plugin.details.get("Configuration", "Filename")
        except: # noqa
            return ""
        fname = fname.replace('"', '')
        path = self.get_plugin_dir(plugin)
        return path / fname

    def get_plugin_documentation_filename(self, plugin):
        """ Return the path to the plugin documentation
        """
        try:
            fname = plugin.details.get("Documentation", "Filename")
        except: # noqa
            return ""
        path = self.get_plugin_dir(plugin)
        return path / fname

    def get_plugin_class_name(self, plugin):
        """ Return the class of a given plugin

        :param iPlugin plugin: the plugin requested

        :rtype: str
        :return: the module classname
        """
        return plugin.categories[0]

    def get_plugin_module_name(self, plugin):
        """ Return the module name of a given plugin

        :param iPlugin plugin: the plugin requested

        :rtype: str
        :return: the module name
        """
        module_path = plugin.details.get("Core", "module")
        path, filename = os.path.split(module_path)
        return filename

    def get_plugin_config(self, plugin):
        """ Return the configuration of a given plugin

        :param iPlugin plugin: the plugin requested

        :rtype: dict
        :return: plugin configuration
        """
        module_name = self.get_plugin_module_name(plugin)
        class_name = self.get_plugin_class_name(plugin)
        try:
            config = self.plugins_config[class_name][module_name]
        except:  # noqa
            config = {}
        return config

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
                dependencies.add(elt.strip())
        else:
            dependencies.add(st)
        return dependencies

    def is_plugin_enabled(self, plugin):
        config = self.get_plugin_config(plugin)
        if config.get('enable'):
            return True
        else:
            return False

    def get_plugins_info(self, category=None):
        """Return the list of plugins available with their type

        :param str category: restrict to plugins of a given category.

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
                try:
                    version = plugin.version
                except: # noqa
                    version = "NA"

                s = [cat, plugin.name, plugin.description, enabled,
                     module_name, version]
                pl.append(s)
        return pl

    def display_execution_results(self, results, site):
        """ Display execution summary
        """
        cprint("|-Execution result", "magenta")
        table_data = [['name', 'ok', 'skipped', 'errors']]
        count = 0
        for result in results:
            row = []
            plugin_name, stats = result

            # plugin name
            c = "cyan"
            if count % 2:
                c = "blue"
            row.append(colored(plugin_name, c))

            # ok
            if stats[site.OK]:
                if stats[site.OK] == 1:
                    val = 'v'
                else:
                    val = stats[site.OK]
                row.append(colored(val, 'green'))
            else:
                row.append(' ')

            # warning
            if stats[site.SKIPPED]:
                row.append(colored(stats[site.SKIPPED], "yellow"))
            else:
                row.append(' ')

            # error
            if stats[site.ERROR]:
                if stats[site.ERROR] == 1:
                    val = 'x'
                else:
                    val = stats[site.ERROR]
                row.append(colored(val, "red"))
            else:
                row.append(' ')

            table_data.append(row)
            count += 1

        print(SingleTable(table_data).table)

    def run_plugins(self, items, plugin_class, unit, site):
        """Execute a set of plugins on a given list of items

        :param list items: list of items to process
        :param str plugin_type: the plugin_class to use
        :param str unit: the unit to use in the display
        :param SiteFab site: pointer to the site object to be passed
        to the plugins

        :rtype: dict(dict(list))
        :return: plugins execution statistics
        """

        # dependencies map
        dependencie_map = {}

        # used to get back from the module name to the plugin
        module_name_to_plugin = {}

        plugins = self.plugins.getPluginsOfCategory(plugin_class)

        # collecting plugins that are to be executed.
        for plugin in plugins:
            if self.is_plugin_enabled(plugin):
                module_name = self.get_plugin_module_name(plugin)
                module_name_to_plugin[module_name] = plugin

        # dependencies computation.
        # Due to  potential dependencies on plugins from previous stage
        # this must be computed after collecting which
        # plugins were executed.
        for plugin in module_name_to_plugin.values():
            all_dependencies = self.get_plugin_dependencies(plugin)
            dependencies = set()  # topological sort requires use of set
            module_name = self.get_plugin_module_name(plugin)

            for dep_module_name in all_dependencies:
                if dep_module_name not in self.plugins_enabled:
                    utils.error("Plugin:%s can't be executed because\
                                plugin %s is not enable" % (module_name,
                                dep_module_name))

                # only add to the dependencies map the plugins
                # that are from the same stage
                if dep_module_name in module_name_to_plugin:
                    dependencies.add(dep_module_name)
                else:
                    # check if already executed
                    if dep_module_name not in self.plugins_executed:
                        utils.error("Plugin:%s can't be executed because\
                                    plugin %s was not executed in previous\
                                    stage" % (module_name, dep_module_name))

            dependencie_map[module_name] = dependencies

        # print dependencie_map

        # Topological sorting
        try:
            plugins_to_process = toposort_flatten(dependencie_map)
        except Exception as e:
            utils.error("Circular dependencies between plugins.\
                Can't execute plugins:%s" % e)

        s = "|-%s plugins" % (unit.strip().capitalize())
        desc = colored(s, "magenta")
        results = []
        for module_name in tqdm(plugins_to_process, unit=' plugin',
                                desc=desc, leave=True):
            if module_name in module_name_to_plugin:
                plugin = module_name_to_plugin[module_name]
            else:
                raise Exception(
                    "The following plugin module name listed in\
                    dependencies don't exist % s " % module_name)

            pclass = plugin_class.lower()
            filename = "%s.%s.html" % (pclass, module_name)
            log_id = site.logger.create_log(pclass, plugin.name, filename)

            plugin_results = utils.dict_to_objdict({
                site.OK: 0,
                site.SKIPPED: 0,
                site.ERROR: 0
            })

            config = self.get_plugin_config(plugin)

            for item in tqdm(items, unit=unit, desc=plugin.name, leave=False):
                result = plugin.plugin_object.process(item, site, config)
                plugin_results[result[0]] += 1

                severity = result[0]
                name = result[1]
                details = result[2]
                site.logger.record_event(log_id, name, severity, details)

            self.plugins_executed[module_name] = True
            results.append([plugin.name, plugin_results])
            site.logger.write_log(log_id)
        return results

    def get_template_filters(self):
        """Load template filters and return a dictionary list

        Return:
            dict: jinja filter functions
        """
        template_filters = {}

        filters = self.plugins.getPluginsOfCategory("TemplateFilter")

        for flt in filters:
            filter_name = self.get_plugin_module_name(flt)
            template_filters[filter_name] = flt.plugin_object.myfilter

        return template_filters
