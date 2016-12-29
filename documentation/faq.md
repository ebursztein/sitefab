# Frequently asked questions


## Why plugins are configured in the config.yaml file?

The decision to make the plugins enable or disable from the config file was made
to allows the flexibility to have different configuration with different plugin configuration.

This allows for example to a dev configuration with fewer plugins to speed up the rendering.

The downside of course is that every plugin must be reflected in the config file and increase
coupling between the engine the plugins. However in that specific case, this cost seemed worthwhile.
