# Writing a SiteFab plugin

This document describe how to write a plugin for SiteFab

## Plugins structure

Plugins use the [YAPSY framework](http://yapsy.sourceforge.net/) and require two files:

1. **.sitefab-plugin** which describe the plugin
2. **.py** which contains the actual code of the plugin

## Basic Example

Here is a basic plugin that add the fully qualified URL to each post meta information right after the post were parsed.

### plugin meta information file

The meta information are located in the file named: **compute_full_post_url.sitefab-plugin**

```ini
[Core]
Name = Post full url
Module = compute_full_post_url

[Documentation]
Author = Elie Bursztein
Version = 0.1
Website = https://www.elie.net
Description = Compute the full qualified url for each post and store in the post.meta under full_url
```

A few notes:

- The *Module* variable must be exactly the name of the python file that contains the code with the *.py* removed.
- The *Name* and *Description* are used to inform the users what the plugin do. Those information are returned by the site.get_plugin_info() method.
- The type of plugin **is not** defined in the description. It is defined by the class the plugin inherit from.

### plugin code

The code file for the plugin is named: ****compute_full_post_url.sitefab-plugin**

```python
from SiteFab.Plugins import PostProcessor

class FullUrl(PostProcessor):
    def process(self, post, site):
        if post.meta.permanent_url:
            post.meta.full_url = "%s/%s" % (site.vars.url, post.meta.permanent_url)
            return True
        return False
```

Each plugin only implement the function **process()** which return True if executed, False otherwise.

As visible in the import, plugins must inherit from one of the plugin class available in SiteFab/plugins.py. The class is used to define at which stage
of the pipeline the plugin will be executed and the information passed to it.
See below for the list of plugin class available and their process function prototype.

**Important**: While every plugin has access to the full site object to get the information it need, the site object should not be manipulated directly except
if it is a site plugin. Choosing the most specific plugin type is required.

## Type of plugins

### PostProcessor

Used to manipulate the content of post. Run between parsing and rendering.

```python
class PostProcessor():
    "Plugins that process each post between the parsing and the rendering"

    def process(self, post, site):
        """ Process a parsed post to add extra meta or change its HTML  
            :param post post: the post to process
            :param FabSite site: the site object
        """
```

### CollectionProcessor

Used to manipulate the content of a collection (e.g adding meta data like statistics). Run between parsing and rendering.

```python
class CollectionProcessor():
    "Plugins that process each collection between the parsing and the rendering"

    def process(self, post, site):
        """ Process a parsed post to add extra meta or change its HTML
            :param collection collection: the collection to process
            :param FabSite site: the site object
        """
```

## Logging
Fixme


## FAQ
### Which plugins framework is used?

SiteFab use [YAPSY](https://github.com/tibonihoo/yapsy).

### How to get a variable defined in the plugin description file?

The info from the configuration files are represented as [configParser](https://docs.python.org/2/library/configparser.html) object
This object can be accessed as follow:

```python
# get the value of a given property which is under a given section
plugin.details.get(section, property_name)
```

for example to get the Module info under the section core:

```python
plugin.details.get("Core", "Module")
```

### How to get reliably the config directory and other directories?

Don't try to compute the path yourself, instead use the built-in helpers that do it for you:

```python
site.get_config_dir()
site.get_templates_dir()
site.get_output_dir()
site.get_assets_dir()
```

So for example the post_linter plugin use these helpers to get its configuration files, specified in its option,
as follow:

```python
config_file = site.get_config_dir() + site.config.plugins.post_linter.config_file
```


### How to access all the site information from plugin code

The site variables from the *site_vars.yaml*  and *sitefab.yaml* configs are
accessible as object via the site object. Here are few examples:

```python
### config object ###
pprint.pprint(site.config)

# plugin configuration
var1 = site.config.plugins.myplugin.var1
```