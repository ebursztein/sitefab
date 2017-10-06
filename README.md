# SiteFab

A flexible yet simple website static generator.

## Getting Started
Follow our [Getting Started Guide](/documentation/getting_started.md) to get up and runnning in less than 10 minutes.

## Key Features

Here are some of the key highlevel functionalities that makes SiteFab the static generator of choice for modern websites: 

- **State of the art images processing stack**: The images stack generate out of the box all you need to use image in optimal fashion including: reactive images for the `<picture>` element, webp versions for the browsers who support it, frozen thumbnail for the loading and cropped thumbnails for previews.
- **Bleeding edge natural language processing stack**: Leveraging the latest advance in NLP Sitefab offers: An accurate list of related posts (LSI algorithm), a client side faceted search and a smart client-side autocompletion
- **Fully customizable**: Its [flexible plugin system](/documentation/plugins.md) and [templatized parser](/documentation/parser.md) make it easy and fast to customize SiteFab to you need.

## Diving in

### Getting started

- Have a  [basic site up and running](/documentation/getting_started.md)  in less than 10 minutes.
- Learn how to [write a page](/documentation/page.md)
- Get [answers](/documentation/faq.md) for the most frequent questions.

### Customizating the generation

- Explore all the [available plugins](/documentation/plugin_list.md)
- Discover how to [customize your templates](/documentation/templates.md)
- Understand how to [personalize the parser](/documentation/parser.md) to suite your need such as adding a CSS class to the `<img>` tag.

### Serving and maintainig your site

- [Configure Nginx](/documentation/nginx_install.md) to serve your site and use pretty urls.
- [Upgrade](/documentation/upgrade.md) SiteFab to the latest version to benefits from new plugins and options.

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
