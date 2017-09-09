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

### install the needed package

Image processing (Pillow) requires a few packages.
#### OSX

```bash
brew install libtiff libjpeg webp little-cms2
```

### install the required python packages
install the need python packages by using the requirements file

```bash
pip install -r requirements.txt
```

Note if you have a modern CPU you might want to enable the avx2 optimization for Pillow by running:

```bash
CC="cc -mavx2" pip install -U --force-reinstall pillow-simd
```
add sudo -H for version below Sierra.

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

### plugins
FIXME

## Writing content

All is left is to write your content :)

This is done by creating two files:

- A **post file** which contains your content and its meta data. This is the core of your site. See [the post file documentation](/documentation/post_file.md) to learn how to write it.

- A **template file** which is used to specify how you would like to render your content in HTML/CSS/Javascript. Usually many posts use the same templates but you can create as many as you wish. See the [template documentation](/documentation/post_template.md) for more information on how to write templates.

Remember in SiteFab terminology everything is a post even if you treat it as a page so if you would like for example to create an about page, you will write a post called `about.md` which contains which ever information you want and an `about.html` template that will render it. While it might seems confusing at first, treating each page the same way will makes it easier and more fool proof on the long run.

Note that SiteFab also generate **Collections** pages for each categories and tags that your posts have. See the [collection documentation](/documentation/collection_template.md) for more information.

## Serving your site

### For viewing a specifc file
FIXME: use python simple server

### For production
See our [nginx installation guide](/documentation/nginx_install.md) to learn how to install nginx and get the pretty print URLs working.

