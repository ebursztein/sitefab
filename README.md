# SiteFab

A flexible yet simple website static generator.

## Getting Started
Follow our [Getting Started Guide](/documentation/getting_started.md) to get up and runnning in less than 10 minutes.

## Features

Here are some of the key features offered by SiteFab

- **Related posts**: Compute the list of related post using the LSI algorithm thanks to [GenSim](https://radimrehurek.com/gensim/)
- **Client side search**: Search through posts localy using javascript thanks to [ElasticLunr](http://elasticlunr.com/)
- **Flexible plugins system**: Easily extend SiteFab to suit your need.

## Diving in

- Learn how to [write a page](/documentation/page.md)
- Get a list of [available plugins](/documentation/plugins.md)
- [Configure Nginx](/documentation/nginx_install.md) to serve your site and use pretty urls.
- Discover how to [customize your templates](/documentation/templates.md)


## Philosophy

More than its technical features what separates SiteFab from the other site generators is its philosophy.
Namely SiteFab is about favoring configuration over convention, be content agnostic and to treat 
content as atomic elements.

Concretly it mean the following:

- **Configuration over convention**: Every behavior is explictly specified. There is no special files or directory. SiteFab only
 do what the configuration say nothing more, nothing less. Post configuration are located in the content file itself and site wide
 option is centralized in a single file that must be specified when sitefab is invoked.

- **Agnostic**: There is only one type of content called post. Site Fab makes no assumption about the content stored 
    in the .md file. Its job is to apply the configuration specified in the frontmatter to render the file and ensure that
    the plugins specified in the site configuration are properly executed.

- **Content as atomic elements**: Each piece of content is self contained by having its its own configuration in its frontmatter. For
 example if the post need to be output in the RSS feed then it need to be specified frontmatter. Similarly the template to use 
 and where the file should be written is specified in the post frontmatter. This allows to accomodate both complex sites with per page
 configuration and very simple site that reuse the same template again and again.

## Alternatives
