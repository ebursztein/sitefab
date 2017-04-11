# How to write templates

## Meta data information

All meta information specified in the content file frontmatter are directly available from the **meta** variable. For example to get the title of the post in a template one will write:

```python
Title: {{ meta.title }}
```

### Examples

Getting the table of content (toc) and list the section of the page in the template:

```python
{%  for elt in toc %}
    {{elt[0]}}<br>
{%endfor%}
```

### post



## Post collections

Collections are list of posts grouped by a given criteria. The following collections are available in the template:

* **categories**: regroup post by categories as specified in post frontmatter
* **tags**: regroup post by tags as specified in post frontmatter
* **templates**: regroup posts that share the same rendering template (e.g blog_post)
* **microdata**: regroup posts that share the same microformat (e.g BlogPosting)


### Usage examples

#### Listing all the posts that belong to a category

To list all the post related to security:

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

### Listing the five most recent posts that belongs to a category

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

#### post page


#### collection page



### Basic example


### Using template inheritance
