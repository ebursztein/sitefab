# How to write post template

This page describe how to create template to render your site content. See [how to write a post](post_content.md) to learn how to write the post files that hold your site contnet.
For the templating of the collection page which are generate for a group of post see the [collection template documentation](collection_template.md).

## Specifying which template to apply to which post

The template used to render a given post file is specified in the frontmatter under the `template` variable. When specficying the template filename in the frontmatter omit the `.html` at the end. You instruct SiteFab where to fetch the templates from by specifying the following variable in the site configuration:

```yaml
dir:
    templates: "templates/" # where to fetch the templates used to render the various posts
```

## Accessing meta data

All meta information specified in the content file *frontmatter* are directly available from the **meta** variable. For example to get the title of the post in a template one will write:

```python
Title: {{ meta.title }}
```

### commonly available meta

While most variables are optional, usually the frontmatter contains a few common variables:
- *meta.title* : title of the page
- *meta.language*: language of the page

## TOC

Getting the table of content (toc) and list the section of the page in the template:

```jinja2
<ul>
{%  for elt in meta.toc %}
    <li class="headline-{{elt[1]}}"><a href="#toc-{{elt[2]}}">{{elt[0]}}</a></li>
{%endfor%}
</ul>
```

Each elt in the toc contains the following information:
- **elt[0]**: headline value. For example "my headline"
- **elt[1]**: headline size. For example: *2* for a H2, *3* for a H3
- **elt[2]**: headline id. This is a sequential count that allows to jump to the headline in the text using
anchor href. For example the second headline will have the id *2*. See example above

## Content

Getting the .md content rendered as HTML is accesible in the template as follow:

```jinja2
{{content}}
```

### code hilighting

Sitefab uses [pygments](http://pygments.org/) to perform code hilighting. During the parsing phase
the code blocks are automatically processed and the needed annotation are added. Parsing option are configured
in the config under the parser category:
```yaml
parser:
    code_highlighting_theme: "monokai" # Template to apply, choose from https://help.farbox.com/pygments.html
    code_display_line_num: True # display line number?
```

**important**: while the parser do add the needed HTML and CSS classname, the CSS is **not** included in the page for obvious reason. It is your responsability to embed the CSS of the template of your choice directly into your CSS file. You can get them [here on github](https://github.com/richleland/pygments-css)

### Date manipulation

FIXME

### Plugin data

#### how to get image size

Getting the image width for an image for which the url is `src`:
```python
plugin_data['image_info'][src]['width']
```

## Related posts
if the related_post plugin is activated, related posts are available as follow:

```jinja2
{% for related_post in meta.related_posts %}
    {{ related_post.meta.title }} ({{ related_post.score}})<br>
{% endfor%}
```

## Collections

Collections are list of posts grouped by a given criteria. The following collections are available in the post template (for the collection page see below):

* **categories**: regroup post by categories as specified in post frontmatter
* **tags**: regroup post by tags as specified in post frontmatter
* **templates**: regroup posts that share the same rendering template (e.g blog_post)
* **microdata**: regroup posts that share the same microformat (e.g BlogPosting)

### Examples

#### Getting the url of the category or tags

If you want to url of the post category you can do:

```jinja2
<a href="{{categories[meta.category].meta.url}}">{{ meta.category }}</a>
```

Same works for the tags. Assuming you have the tag you are interested in the `tag` variable:

```jinja2
<a href="{{tags[tag].meta.url}}">{{ tag }}</a>
```


#### Listing all the post related to security in the footer

To list all the post related to security in yout footer you can do:

```jinja2
<ul>
{% for post in categories.security.posts %}
  {# the if is used to filter out pages which are not blog articles #}
  {% if post.meta.template == "blog_post" %}
    <li><a href="{{ post.meta.permanent_url }}">{{ post.meta.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>
```

#### Listing the five most recent posts that belongs to a category

To list the five most recent post that use the blog_post template:

```jinja2
<ul>
{% for post in templates.blog_post.posts[:10] %}
    <li><a href="{{ post.meta.permanent_url }}">{{ post.meta.title }}</a></li>
{% endfor %}
</ul>
```

### Listing all the blog posts by categories

```jinga2
{% for category, data in categories.items() %}
    <h3>{{ category }} </h3>
    <ul>
        {% for post in data.posts %}
            {# the if is used to filter out pages which are not blog articles #}
            {% if post.meta.template == "blog_post" %}
                <li><a href="{{ post.meta.permanent_url }}">{{ post.meta.title }}</a></li>
            {% endif %}
        {% endfor %}
    </ul>
{% endfor %}
```

### Format




{% for related_post in meta.related_posts %}
    {{ related_post.meta.title }} ({{ related_post.score}})<br>
{% endfor%}

### Using template inheritance

FIXME