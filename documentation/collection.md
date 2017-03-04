# Collection

A collection is an object that as its name imply a list of posts that are regrouped by logical entity (e.g category, tag, template) along side with 
some meta data.

## type of collections

The following type of collections are available:
**collections**: regroup post by tags and category as specified in post frontmatter
**posts_by_templates**: regroup posts that share the same rendering template (e.g blog_post)
**posts_by_microdata**: regroup posts that share the same microformat (e.g BlogPosting)

## collection structure

Here is how a collection object is structure

```python
collection:
    posts (list) # list of posts. Usually sorted from most recent to oldest.
    meta (object):
        name # name of the collection. E.g Web Security
        slug(str)   #slug used for the url. E.g for Web Security the slug is web-security
        num_posts(int)  #number of posts in the collection
```

## Usage in Jinja2 template

To list all the post related to security:
```jinja2
<ul>
{% for post in collections.security.posts %}
    <li><a href="{{ post.meta.permanent_url }}">{{ post.meta.title }}</a></li>
{% endfor %}
</ul>
```

To list the five most recent post that use the blog_post template:
```jinja2
<ul>
{% for post in posts_by_templates.blog_post.posts[:10] %}
    <li><a href="{{ post.meta.permanent_url }}">{{ post.meta.title }}</a></li>
{% endfor %}
</ul>
```