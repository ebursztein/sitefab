from sitefab import files


def generate_plugins_readme(site, output_fname):
    "Generate plugins readme"

    plugin_list_md = "# SiteFab plugins\n"
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
        doc_path = site.plugins.get_plugin_documentation_filename(plugin)
        doc_path = str(doc_path)
        if 'plugins' in doc_path:
            doc_path = doc_path.replace('\\', '/').split('plugins')[1]
            name = "[%s](tree/master%s)" % (name, doc_path)
        plugin_list_md += "| %s | %s | %s |\n" % (name, description,
                                                  dependencies)

    files.write_file('', output_fname, plugin_list_md)
