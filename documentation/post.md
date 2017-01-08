# Post object

The post object is the basic element of the site. It is the parsed version of a file and contains the following elements:

- *post.md*: the md version of the post
- *post.html*: the html version of the post
- *post.meta*: the meta information related to the post. Meta come from the frontmatter data and the various plugins
- *post.elements*: List of elements contained in the post. For example the list of images. This is generated during the parsing.

## Accessing post elements from the template

Each of the element is directly available in the template by there name. 

For example to get the title of the post in a template one will write:

```python
Title: {{ meta.title }}
```

Similarly to get the table of content (toc) and list the section of the page in the template:

```python
{%  for elt in toc %}
    {{elt[0]}}<br>
{%endfor%}
```

## post.meta details
FIXME

## post.toc details
Here is an example of the toc array:
 ```python
[
     ('Edwin VanCleef is a steal', 2, 0),
     ('Twilight drake', 2, 1),
     ('Twilight drake before the nerf', 2, 2)
]
```

The post.info.toc is a **list** that represents the post table of content. The field of each list element are:

- Field [0] The name of the section
- Field [1] The level of section. Basically 1 == H1, 2 == H2, ...
- Field [2] The auto-increment id associated with the section. Mainly useful to generate unique anchor in the template.


## post.elements details

Here is an example of what is contained in post.elements:

```python
{'images': ['https://www.elie.net/image/..',
            '..'
            ],
 'links': ['https://www.elie.net/blog/hearth...',
           '...'
           ],
 'videos': []}
```