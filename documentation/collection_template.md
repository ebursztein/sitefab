# How to write a collection page template

Sitefab allow you to output a page that list all the posts that 
have a given tag / categrory. Behavior of collection pages is defined
in the collection section of the site config.

To learn how to write template for post see the [post page templating documentation](post_template.md) documentation.

## Available data

In a collection page the template have access to the following information:

- **meta**: collection meta information including name and number of posts
- **posts**: list of posts that belong to the category. Each post is a normal object as used in post page. It contains its content (post.content), meta data (post.meta), toc and info.

## Example

Basic example of collection page that display the collection name and list all the posts that belong to it with their creation date:

```jinja2
<h1>{{meta.collection_name}}</h1>
<ul>
    {% for post in posts %}
    <li>{{post.meta.creation_date}} - {{post.meta.title}}</li>
    {% endfor %}
</ul>
```