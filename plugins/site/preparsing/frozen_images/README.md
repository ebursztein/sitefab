# Frozen Images

Inspired by Facebook frozen banner generate small thumbnails that look frozen. Used to make preloading.

## Usage
.

## Configuration
For example
```yaml
fixme:
```

## Usage

To load the frozen image from its url:

```jinja2
<img src="{{ plugin_data.frozen_images[src].url }}"/>
```

To inline the image using a base64 representation:

```jinja2
<img src="{{ plugin_data.frozen_images[src].base64 }}"/>
```

## Changlog
- 06/14/17
    - initial version

## Credit
Plugin by Elie Bursztein. Javascript polyfill by the [picture polyfill team](https://raw.githubusercontent.com/scottjehl/picturefill/master/Authors.txt)