# How to write post template

This page describe how to create a template for a post page. SiteFab post page 
are generated for each `.md` file. The template used to render a given file is 
specified in the frontmatter under the `template` variable. Directory for where to fetch
the templates from is specified in the site configuration.

See the [how to format your markdown documentation](content.md) to learn how to write your markdown file that hold your site contnet.
For the templating of the collection page which are generate for a group of post see the [collection template documentation](collection_template.md).

## Meta data

All meta information specified in the content file *frontmatter* are directly available from the **meta** variable. For example to get the title of the post in a template one will write:

```python
Title: {{ meta.title }}
```

## TOC

Getting the table of content (toc) and list the section of the page in the template:

```jinja2
{%  for elt in toc %}
    {{elt[0]}}<br>
{%endfor%}
```

## Content

Getting the .md content rendered as HTML is accesible in the template as follow:

```jinja2
{{content}}
```

## Collections

Collections are list of posts grouped by a given criteria. The following collections are available in the post template (for the collection page see below):

* **categories**: regroup post by categories as specified in post frontmatter
* **tags**: regroup post by tags as specified in post frontmatter
* **templates**: regroup posts that share the same rendering template (e.g blog_post)
* **microdata**: regroup posts that share the same microformat (e.g BlogPosting)

### Examples

#### Getting the url of the category of a given post

If you want to link to the category of the post

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
{% for category, data in categories.iteritems() %}
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


### Variable available

*meta.title* : title of the page
*meta.language*: language of the page

### Using template inheritance

FIXME