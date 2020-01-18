# Frequently asked questions

## Configuration

### How to configure the parser output for basic HTML elements?

See the [parser documentation](/documentation/parser.md).

**TL;DR**: It is easy and there are two ways: the first one is to edit the
templates used to emit the html elements the second is to programatically
change the templates using the Parser object API.

## Plugins

### How do I create my own plugin?

This is super easy see: 



### Why plugins configurations are in the config directory?

The decision to make the plugins configuration part of the site configuration
was made to allows you to have the flexibility to have different build
configuration with different plugin configuration.

This allows for example to a dev configuration with fewer plugins to speed up
the rendering or experiment with a new config as you develop a new version with
added functionality.

## Windows specific Installation issues

If you get the error message *"cannot be loaded because the execution of scripts is disabled on this system"*,
you need to change your Windows policy as follow using **powershell as admin**:

```bash
Set-ExecutionPolicy Unrestricted -Force
```
