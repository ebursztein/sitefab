# Related posts

Use LSI to generate related posts. Related posts are added to the post object in **post.meta.related** which a list of related posts ordered by relevance

## Usage

Add the following code into the template to list related posts:

```jinja2
{% for related_post in meta.related_posts %}
    {{ related_post.meta.title }} ({{ related_post.score}})<br>
{% endfor%}
```

## Requirements

The plugin use the [gensim](https://radimrehurek.com/gensim/) python package.

## Changelog

- 06/29/17 Refactored code to make the list of related post easier to work with by making them look like normal post objects.
- 12/27/16 Initial version released

## Credits

**Author**: Elie Bursztein

Inpired by [Pelican LSI plugin](http://www.datasciencebytes.com/bytes/2014/11/20/using-topic-modeling-to-find-related-blog-posts/)