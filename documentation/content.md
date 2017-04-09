# Writing content

To generate a page, two files are required:

- a *Content file*: Written in [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) the content file contains the content of the page, its meta data and its configuration. The meta data and configuration are stored in the frontmatter in the [YAML format](http://docs.ansible.com/ansible/YAMLSyntax.html). The meta data are made accessible to the template in the [meta object](/documentation/post.md)

- a *Template file*: Written in Jinga2 format the template file is used to specify how the page is rendered.

## Content file

Here is how a content file is structured

### Frontmatter

The front matter is used to store the page configuration and meta data. It is written in the YAML format.

The meta data stored in the front matter are made available to template file during the generation process under the meta object. for example the title specified in the 
meta data can be accessed in the template page as follow:

```Python
{% meta.title %}
```

#### available fields


| Field        		  | Type        | Needed?    | Description                                   | Example           |
| -------------       |-----------  | ---------  | -----------                                   | ------------------- |
| **title**      	  | string 		| Mandatory  | Title of the page                             | Hacking IoT devices |
| **author**      	  | string 		| Mandatory  | author of the page                            | Elie, Bursztein |
| **creation_date**   | string 		| Mandatory  | When was the post created.                    | 2 Jan 2017 17:23|
| **update_date**     | string 		| Optional  | When was the post was last updated. Used by search engine as hint.                   | 5 Jan 2017 22:23|
| **permanent_url**   | URL 		| Mandatory  | The url of the page, relative to the hostname | /blog/security/hacking-iot-devices|
| **category**        | string 		| Mandatory  | Category of the post                          | security | 
| **tags**      	  | list 		| Optional  | List of tags associated with the page         | |
| **abstract**        | string 		| Mandatory  | short description of the page. used in meta and search| this is how to hack iot device|
| **template**        | filename 	| Mandatory  | which template to use to render the page (without the *.html* extension) | post |
| **lang**      	  | ISO code (default:site lang)	| Optional  | language of the page used for i18n | en |
| **hidden**         | bool         | Optional (default:false)  | Don't list the post in collections or RSS or any other list| true |


#### Example

Here is an example of a frontmatter. It is the one I used to generate the publication page for one of my paper on my [site](https://www.elie.net/publication/i-am-a-legend-hacking-hearthstone-using-statistical-learning-method)
```YAML
---
template: publication
title: I am a legend hacking Hearthstone using statistical learning methods
banner: https://www.elie.net/image/public/1476002309/i-am-a-legend-hacking-hearthstone-using-statistical-learning-methods.jpg
permanent_url: publication/i-am-a-legend-hacking-hearthstone-using-statistical-learning-method
lang: en

creation_date: 18 oct 2016 13:29

category: video game

tags: 
 - hearthstone
 - offensive technologies
 - machine learning

seo_keywords: 
 - hearthstone
 - hearthstone card game
 - hearthstone bot
 - hearthstone cards 
 - ccg
 - tgc

authors:
  - Elie, Bursztein

conference_name: Computational Intelligence and Games conference
conference_short_name: CIG
conference_location: Santorini, Greece
conference_publisher: IEEE

files:
  paper: https://cdn.elie.net/publications/i-am-a-legend-hacking-hearthstone-using-statistical-learning-methods.pdf

abstract: this paper demonstrate how to apply machine learning to Hearthstone to predict opponent future plays and game outcome.

---
```

#### Custom fields

On top of the specific field, any additional field can be added to the frontmatter and will be accessible by the template as part of the meta object.
For example the easiest way to have a banner image for each post is too add a meta banner:

```
banner: /static/images/iot-device-banner.jpg
```

which then can be used in the template page as follow:

```python
<img src="{% meta.banner %}"/>
```