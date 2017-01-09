import os

from SiteFab import files


def sitefab_build(site):
    "Build the documentation and the default configuration"

    doc_filename = os.path.join(files.get_code_path(), "documentation")
    print doc_filename
    plugin_list_md = "# plugins list\n"
    plugin_list_md += "List of available plugins\n\n"
    plugin_list_md += "|Name | Description | dependencies|\n"
    plugin_list_md += "|----:|------------:|------------:|\n"

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