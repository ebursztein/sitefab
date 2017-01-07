# Frequently asked questions

## How to configure the parser output?

See the [parser documentation](/documentation/parser.md).

**TL;DR**: It is easy and there are two ways: the first one is to edit the templates used to emit the html elements
the second is to programatically change the templates using the Parser object API. 

## Why plugins are configured in the config.yaml file?

The decision to make the plugins enable or disable from the config file was made
to allows the flexibility to have different configuration with different plugin configuration.

This allows for example to a dev configuration with fewer plugins to speed up the rendering.

The downside of course is that every plugin must be reflected in the config file and increase
coupling between the engine the plugins. However in that specific case, this cost seemed worthwhile.
