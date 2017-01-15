# Related posts

Use LSI to generate related posts. Related posts are added to the post object in **post.meta.related** which a list of related posts ordered by relevance

## Usage

Add the following code into the template to list related posts:

```jinja2
{% for p in post.meta.related_posts %}
{% endfor %}
```

## Requirements

The plugin use the [gensim](https://radimrehurek.com/gensim/) python package.


## Changelog

- 12/27/16 Initial version released

## Credits

**Author**: Elie Bursztein

Inpired by [Pelican LSI plugin](http://www.datasciencebytes.com/bytes/2014/11/20/using-topic-modeling-to-find-related-blog-posts/)