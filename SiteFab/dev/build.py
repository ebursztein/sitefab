def sitefab_build(site):
    "Build the documentation and the default configuration"

    documentation = """
    # plugins list
    List of available plugins

    """

    plugins = site.plugins.get_plugins()
    for plugin in plugins:
        name = plugin.name
        description = plugin.description
        dependencies = site.plugins.get_plugin_dependencies(plugin)
        doc =  site.plugins.get_plugin_documentation_filename(plugin)
        config = site.plugins.get_plugin_default_configuration_filename(plugin)
        print "%s, %s : %s -- %s " % (name, description, doc, config)