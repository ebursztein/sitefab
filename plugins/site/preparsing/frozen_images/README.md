# Frozen Images

Inspired by Facebook frozen banner generate small thumbnails that look frozen. Used to make preloading 
more bearable for users.

## Configuration
For example
```yaml
input_dir: "generated/static/images/"
output_dir: "generated/static/images_frozen/"
```

*Important*: don't output frozen images in the base `input dir` to avoid overloading other images plugins with extra images to process.

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
- v1.1
    - Improved performance (~10x):
        -  Cache issue fixed! Now frozen_images use cache corectly
        - Refactored to use image_info data to avoid duplicate computation
        - Lazy image loading for further increase performance
    - Simplified code and fixed a few bugs
- v1
    - initial version

## Credit
Plugin by Elie Bursztein. Javascript polyfill by the [picture polyfill team](https://raw.githubusercontent.com/scottjehl/picturefill/master/Authors.txt)