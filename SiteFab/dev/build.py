import os
import yaml
from tqdm import tqdm

from SiteFab import files


def sitefab_build(site):
    "Sitefab_build command"

    # plugin site configuration
    upgrade_plugin_configuration_file(site)

    # Pluging documentation
    build_plugin_documentation(site)

def upgrade_plugin_configuration_file(site):
    "Collect plugins configuration and create the configuration file"

    cats_description = {
        "CollectionProcessor"
    }

    plugin_config_filename = os.path.join(files.get_code_path(), "demo_site", "config", "plugins.yaml")

    configuration = {}
    descriptions = {} # add description in the documentation
     
    categories = site.plugins.plugins.getCategories()
    for cat in categories:
        configuration[cat] = {}
        for plugin in site.plugins.plugins.getPluginsOfCategory(cat):
            new_config = {}            
            
            module_name = site.plugins.get_plugin_module_name(plugin)
            current_config = site.plugins.get_plugin_config(plugin)
            
            #doc
            descriptions[module_name] = plugin.description
            


            # enable?
            if current_config.get('enable'):
                new_config['enable'] = True
            else:
                new_config['enable'] = False

            # comparing current configuration with plugin default configuration to see if there are new / removed options 
            default_config_filename = site.plugins.get_plugin_default_configuration_filename(plugin)
            if default_config_filename:
                default_config = files.load_config(default_config_filename)
                
                # iterating over the default config to only keep the options relevant to current plugin version
                for k in default_config.iterkeys():
                    # already existing keep current value
                    if k in current_config:
                        new_config[k] = current_config[k]
                    # new option adding default value
                    else:
                        new_config[k] = default_config[k]

            configuration[cat][module_name] = new_config

    # Getting the YAML formated dump
    dump = yaml.dump(configuration, default_flow_style = False, allow_unicode = True, encoding = None)
    
    # Adding plugins description as comments
    for module_name, description in descriptions.iteritems():
        new_str = "\n  # %s\n  %s" % (description, module_name)
        dump = dump.replace(module_name, new_str)

    # adding categorie description
    for cat in site.plugins.categories:
        c = cat[0]
        description  = cat[2]
        new_str = "\n##########################\n# %s\n# %s\n##########################\###\n%s" % (c, description, c)
        dump = dump.replace(c, new_str)

    # writing configuration
    with open(plugin_config_filename, 'w') as yaml_file:
        yaml_file.write( dump )


def build_plugin_documentation(site):
    "Build the plugins documentation"

    doc_filename = os.path.join(files.get_code_path(), "documentation")
    plugin_list_md = "# plugins list\n"
    plugin_list_md += "List of available plugins\n\n"
    plugin_list_md += "|Name | Description | dependencies|\n"
    plugin_list_md += "|-----|:------------|:------------|\n"

    plugins = site.plugins.get_plugins()
    for plugin in plugins:
        name = plugin.name
        description = plugin.description
        dependencies = site.plugins.get_plugin_dependencies(plugin)
        if not len(dependencies):
            dependencies = ""
        else:
            dependencies = ", ".join(dependencies)
        doc =  site.plugins.get_plugin_documentation_filename(plugin)
        if "SiteFab" in doc:
            doc = doc.split("SiteFab")[1]
        config = site.plugins.get_plugin_default_configuration_filename(plugin)
        plugin_list_md += "| [%s](%s) | %s | %s |\n" % (name, doc, description, dependencies)
    
    files.write_file(doc_filename, "plugin_list.md", plugin_list_md)