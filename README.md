# SiteFa: state of the art static website generator for humans

[![Linux Status](https://github.com/ebursztein/sitefab/workflows/Linux/badge.svg)](https://github.com/ebursztein/sitefab/actions)
[![macOS Status](https://github.com/ebursztein/sitefab/workflows/macOS/badge.svg)](https://github.com/ebursztein/sitefab/actions)
[![Code coverage](https://codecov.io/gh/ebursztein/sitefab/branch/master/graph/badge.svg)](https://codecov.io/gh/ebursztein/sitefab)

## Getting Started in 30 seconds

Here is how to install SiteFab, Create a new site and compile it in less than
30 seconds:

```bash

# install the main package
pip install sitefab

# clone the site template as base
git clone https://github.com/ebursztein/sitefab-template.git mysite/

# clone the plugins in your site directory
git clone https://github.com/ebursztein/sitefab-plugins.git mysite/plugins

# generate your shiny new site
sitefab -c mysite/config/sitefab.yaml generate
```

Et voila! you know have a fully fonctional site that can be statically compiled.
As the next step you should add your content, customize the html templates and
tweak the plugins configuration to your liking!

## Key Features

Here are some of the key highlevel functionalities that makes SiteFab the static generator of choice for modern websites:

- **State of the art images processing stack**: The images stack generate out of the box all you need to use image in optimal fashion including: reactive images for the `<picture>` element, webp versions for the browsers who support it, frozen thumbnail for the loading and cropped thumbnails for previews.
- **Bleeding edge natural language processing stack**: Leveraging the latest advance in NLP Sitefab offers: An accurate list of related posts (LSI algorithm), a client side faceted search and a smart client-side autocompletion
- **Fully customizable**: Its [flexible plugin system](/documentation/plugins.md) and [templatized parser](/documentation/parser.md) make it easy and fast to customize SiteFab to your needs.

## Design principles

Beside its technical features what separates SiteFab from other site generators
is its guiding principles:

- **Configuration over convention**: Every behavior is explictly specified.
    There are no special files or directories. SiteFab only do what the
    site configuration say. Nothing more, nothing less.

- **Content Agnostic**: There is only one type of content called post.
    SiteFab makes no assumption about the content stored in the .md files. Its
    job is to apply the configuration specified in the frontmatter to render
    the specificied files and ensure that the enabled plugins are properly
    executed.

- **Atomicity**: Each piece of content is self contained by having its own
    configuration in its frontmatter including which template to use.
    This allows to accomodate both complex sites with per page configuration
    and very simple ones that reuse the same template again and again.

- **Orthogonality**: Site configuration, plugins and plugins configuration
    are independent of the core engine so you can use as many configurations
    and tweaked plugins you want. Additionally you can check those alongside
    with your site content to have reproducible build, safe rollbacks and
    concurrent version of the build pipeline (e.g alpha versus stable).

## Alternatives

Here are some popular alternatives if SiteFab is not what you are looking for:

- [Jekyll](https://jekyllrb.com/): The most popular site generate, written in
`Ruby`.

- [Hugo](https://gohugo.io/): A popular site generator, written in `Go` that
focuses on speed.

- [Pelican](https://blog.getpelican.com/): Another site generator written
in `Python`.
