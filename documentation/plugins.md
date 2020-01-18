# Writing a SiteFab plugin

This document describe how to write a plugin for SiteFab. A list of available plugins is available [here](/documentation/plugin_list.md)

Writing a plugin is easy. First you have to decide whether what type of plugins you
want as it change where to put it. Then you need to use the correct plugin class
so SiteFab knows when to run it and call it with the information you need. Plugins
are dynamically loaded everytime you run SiteFab so once you have the code and
the config in place they will be called automatically without any additional
changes.


## Plugin type

For the plugin type you have two options:

1. **For private plugins**: you create a directory in your site project and then
in the *sitefab.yaml* you declare it as plugin dir. This allows you to have SiteFab
to run your custom code and revise it as you please.

2. **Public plugins**: If your plugin can benefit the community you can simply
do a pull request to add it to the [Plugin repo](https://github.com/ebursztein/sitefab-plugins).
Make sure to document it properly so people know how to use and who wrote it.


## Workflow

FIXME: add a diagram of how th
e plugins are called

## Plugins directory structure

Typically Plugins are stored in the **Plugins/** directory which is organized
as follow:

- The first level represent the entity the plugin apply to
- The 2nd level represent the phase in which the plugin is to be applied

*Note*: Like everything with SiteFab the directory organization is just here for readability and don't influence when plugins are called or with which data. What do define which data the plugin get and when it is called is its configuration and its class.

```bash
plugins/
  collection/
        processor/
        pendering/
        ..
  posts/
        preparsing/
        processor/
        rendering/
        ..
  site/
        ..
  ..
```

## Plugin structure

Plugins use the [YAPSY framework](http://yapsy.sourceforge.net/) and is composed of the following four files:

1. **.sitefab-plugin** description file which describes the plugin.
2. **.py** file which contains the actual code of the plugin.
3. **.md** markdown file which the document the plugin.
4. **.yaml** yaml file that contains the plugin default configuration.

## Basic Example

Here is a basic plugin that add the fully qualified URL to each post meta information right after the post were parsed.

### plugin meta information file

The meta information are located in the file named: **your_plugin_module_name.sitefab-plugin**

```ini
[Core]
Name = Copy directories
Module = copy_dir
Version = 1
Dependencies = module_x

[Documentation]
Filename = README.md
Description = Copy a set of directory from one place to another.

[Configuration]
Filename = config.yaml
```

Where

- The *Name* and *Description* are used to inform the users what the plugin do. Those information are returned by the site.get_plugin_info() method.
- The *Module* variable must be exactly the name of the python file that contains the code with the *.py* removed.
- *Version* allows to track change and when to notify the users when a plugin was changed.
- *Dependencies* is optional and is used to ensure that plugins are executed in the proper order and the needed one are activated. Not the ordering working for plugins of the same classes. Activation check works accross all class of plugins.
- The type of plugin **is not** defined in the description. It is defined by the class the plugin inherit from.
- The *Documentation* file prefered name is README.md so it show-up automatically on github. However you can use another filename if you want.
To know what to include in the documentation file refers to the [documentation](#Documentation) section below.
- The *configuration* file is used to provide the default configuration for the various plugin option. See the [configuration](#Configuration) section below.

### plugin code

The code file for the plugin is named: ****compute_full_post_url.sitefab-plugin**

```python
from SiteFab.Plugins import PostProcessor

class FullUrl(PostProcessor):
    def process(self, post, site, config):
        if post.meta.permanent_url:
            post.meta.full_url = "%s/%s" % (site.vars.url, post.meta.permanent_url)
            return True
        return False
```

Each plugin only implements the function **process()** which return True if executed, False otherwise.

As visible in the import, plugins must inherit from one of the plugin class available in SiteFab/plugins.py.
The class is used to define at which stage of the pipeline the plugin will be executed and the information passed to it. See below for the list of plugin class available and their process function prototype.

**Important**: While every plugin has access to the full site object to get the information it need, the site object should not be manipulated directly except if it is a site plugin. Choosing the most specific plugin type possible.

### Configuration
Each plugin must come with a default configuration. It is used to generate the default "plugins.yaml" file so users know what to configure.

Here is for example the configuration of the read_time plugin:
```yaml
wpm: 260 # avg number of words read per minute
```

This configuration is reflected in the plugins.yaml as follow:
```yaml
read_time:
    enable: False
    wpm: 260 # avg number of words read per minute
```

In the plugin code you simply access the various parameters you specified via the `config` variable.

In our read_time plugin example, to get the average number of word per minutes (wpm), the plugin will do:
```python
wpm = config.wpm
```

Notes:
- All plugins are disable by default to not suprise the user.
- The plugin.yaml default file is constructed from the plugin default configurations using the command `sitefab.py -c config/sitefab.yaml sitefab_build`.
- Plugins new options are reflected to the site configuration files by calling `sitefab.py -c config/sitefab.yaml upgrade`

### Exposing plugin data to the templates and parser

To expose some data to the templates and potentially the parser (if the plugin is ran before) add your data to the `site.plugin_data` dict as follow:

```python
# dictionary of values
site.plugin_data[plugin_name] = {}
site.plugin_data[plugin_name]['key1'] = 'val1'

# Array
site.plugin_data[plugin_name] = [1,2,3,4]

# or any other structure you need
site.plugin_data[plugin_name] = "https://example.com"
```

### Documentation

Plugin documentation are written in standard markdown format. They are collected to create an index of available plugin when the code is released.
Each plugin documentation follows the following template:

```markdown
# Plugin name
A description of what the plugin do.

## Usage

How to use the plugin. Preferably with a full template code example
and a description of the options

### Usage example

### Configuration

## Changlog

A simple list that list what changed. Something like:

- 12/23/16
 - Documentation updated to reflect how the plugin work

## Credit
Who wrote the plugin, which library it use, who got the idea etc.

```

## Type of plugins

**FIXME** Reorder the description to fit the directory hierachy

### Pre Parsing

### Site wide

Plugins that are used to initialize the structure and set global variable. For example copying assets to the release directory.

### content

These plugins execute before the parsing

```python
class ContentPreparsing():
    "Plugins that process content files before the parsing"

    def process(self, filename, site, config):
        """ Process a parsed post to add extra meta or change its HTML
            :param str filename: the filename of the content file process
            :param FabSite site: the site object
        """
```

### Processing

#### Post Processor

Used to manipulate the content of post. Run between parsing and rendering.

```python
class PostProcessor():
    "Plugins that process each post between the parsing and the rendering"

    def process(self, post, site, config):
        """ Process a parsed post to add extra meta or change its HTML
            :param post post: the post to process
            :param FabSite site: the site object
        """
```

#### Collection Processor

Used to manipulate the content of a collection (e.g adding meta data like statistics). Run between parsing and rendering.

```python
class CollectionProcessor():
    "Plugins that process each collection between the parsing and the rendering"

    def process(self, post, site, config):
        """ Process a parsed post to add extra meta or change its HTML
            :param collection collection: the collection to process
            :param FabSite site: the site object
        """
```

#### Site processor

For example related posts

### Rendering

#### Site Rendering

** Warning:** When accessing Collections via site object be aware that collections are a dict. To get their content make
sure to use `site.collections.values()`

#### Extra rendering

After the posts and collections are rendered, these plugins are invoked to generate extra-pages, javascript file etc...
For example both the sitemap and the search.js generation are done as ExtraRendering plugins.

```python
class ExtraRendering():
    "Plugins that render additional pages"

    def process(self, unused, site, config):
        """ Generate additional page or file
            :param FabSite site: the site object
        """
```

## Useful functions

### Modifying the HTML rendering of a given HTML element

To modify how a given element will be rendered by the parser a plugin can override its jinja template as follow:

```python
site.inject_parser_html_template("plugin_name", "html_elt", "template")
```

Where:

- **plugin name** is the name of the plugin.
- **html_elt** is the HTML element to override. For example `img`
- **template** is the new HTML template that will be used for rendering the targeted HTML element

FIXME: add a concrete example

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