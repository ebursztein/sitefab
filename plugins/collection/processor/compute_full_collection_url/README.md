# Compute Full URl for collections plugin

Compute the full url of a collection

## Usage

Add the following snippet to your template to get the full url.

```html
{% if collection.meta.full_url %}
{{ collection.meta.full_url}}
{% endif %}
```

## Changelog
- 03/02/17 ensured the collections are in lower case.
- 12/27/16 initial version

## Credits

**Author**: Celine Bursztein
