# SiteFab data structures

SiteFab have three main data structures:

1. Site: Object representation of the entire Site
2. [Post](/documentation/post.md): Site basic unit. Mostly created from the .md files and potentially by plugin. Each .md has its own post Object
3. Collection: A collection of posts that share the same topic

## Collection

A collection is structured as follow

```python
collection:
    posts (list)
    meta (object)
```
The posts contains a list of post object. Meta contains the collection meta information.

