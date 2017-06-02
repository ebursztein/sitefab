# Getting Started

Here is how to get up and running with Site Fab. Creating a website is done in three easy steps:

1. install Site Fab and a web server
2. Initialize your site and add content
3. Generate  your pages

## Installing SiteFab

Currently the only way to install SiteFab is to install it from the source.

### Clone the sources
Clone Site Fab into the directory of your choice

```bash
git clone https://github.com/ebursztein/SiteFab.git sitefab
```

### install the required python packages
install the need python packages by using the requirements file

```bash
pip install -r requirements.txt
```

Note if you have a modern CPU you might want to enable the avx2 optimization for Pillow by running:

```bash
sudo -H CC="cc -mavx2" pip install -U --force-reinstall pillow-simd
```

## Creating your site

The easiest way to get started is to use the demo site which is located in the the **demo_site/** directory

1. Copy it to the directory of you choice:  `cp -r demo_site my_site`
2. Change directory to the newly created one: `cd my_site`
3. Generate the site: `python ../sitefab.py -c config/sitefab.yaml generate`
4. The rendered site is in the **generated/** directory. You can visualize the rendered files either by opening the index file in your browser or via a local server.

## Configuring your site

copy the default configuration to a personalize one:

```bash
cp config/demo_site.yaml config/mysite.yaml
```

Configuration files are written in [YAML](http://docs.ansible.com/ansible/YAMLSyntax.html). 
Don't forget to use your new configuration while generating :)

`python ../sitefab.py -c config/mysite.yaml generate`


## Writing pages

All is left is to write your pages:

- **Page content** is written in [Markdown format](https://guides.github.com/features/mastering-markdown/) and embedded a [front matter](/documentation/content.md#frontmatter) that is used to configure the output (e.g stipulates the template to use) and specify meta information. To create a page simply add a file in the `content/` directory of  your project

- **Page template** are written in Jinja2 and have access to environement variables that give you access to the page content as HTML, the post information and many more useful data. See the [template documentation](/documentation/template.md) for more information on how to write templates.

- **Collections** are special page generated for each categories / tags that your page have. See the [template documentation](/documentation/template.md) for more information.

## Serving your site

### For viewing a specifc file
FIXME: use python simple server

### For production
See our [nginx installation guide](/documentation/nginx_install.md) to learn how to install nginx and get the pretty print URLs working.

