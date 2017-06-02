# Format_ts filter plugin

Add a custom filter called `format_ts` to jinja template that allows to format timestamp using standard
strftime() syntax.

## Usage

You can use this custom filter in your templates to format the timestamp as follows:

```jinja2
{{ meta.creation_ts | format_ts("%d-%m-%Y") }
```

## Changelog

- 04/14/17 initial version

## Credits

**Author**: Elie Bursztein
