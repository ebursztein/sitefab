# SiteFab data structure description

## main structures list

SiteFab main structures are:

- Site: Object representation of the entire Site
- Post: Site basic unit. Mostly created from the .md files and potentially by plugin. Each .md has its own post Object
- Collection: A collection of posts that share the same topic

## Post object

A post is the basic element of the site. It is the parsed version of a file. It contains the main following elements:

- *post.md*: the md version of the post
- *post.html*: the html version of the post
- *post.meta*: the meta information related to the post. Come from the frontmatter data and the various plugins
- *post.info*: information about the body, e.g the list of images. Generated during the parsing.

### Post.info

Here is an example of what is contained in post.info:

```python
{'images': ['https://www.elie.net/image/..',
            '..'
            ],
 'links': ['https://www.elie.net/blog/hearth...',
           '...'
           ],
 'stats': {
     'num_images': 7, 
     'num_links': 14, 
     'num_videos': 0
     },
 'toc': [
     ('Edwin VanCleef is a steal', 2, 0),
     ('Twilight drake', 2, 1),
     ('Twilight drake before the nerf', 2, 2)],
 'videos': []}
```

#### toc structure
The post.info.toc is a **list** that represents the post table of content. The field of each list element are:

- Field [0] The name of the section
- Field [1] The level of section. Basically 1 == H1, 2 == H2, ...
- Field [2] The auto-increment id associated with the section. Mainly useful to generate unique anchor in the template.



## Collection

A collection is structured as follow

```python
collection:
    posts (list)
    meta (object)
```
The posts contains a list of post object. Meta contains the collection meta information.

