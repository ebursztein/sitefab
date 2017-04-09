# Responsive Images

Create responsive images by using the `<picture>` element and generating the various
images at different size

## Usage

Specify the various resolutions and format to use and the plugin will generate the images 
for those size and format. It will then replace the `<img>` template with a custom one that
make use of the use of the multi resolutions/format images.

**Important** the plugin depends on the [picture polyfill](https://github.com/scottjehl/picturefill) 
to work so make sure to incluse the picture.js in your template.

## Configuration
For example
```yaml
copy_dir:
    - enable: True
    copy:
        - "assets/js > release/static/js"
```

will copy the content of the directory *assets/js* to  *release/static/js*

## Dependency

This plugin requires the [Pillow python package](https://python-pillow.org/).


## Changlog
- 02/18/17
    - initial version

## Credit
Plugin by Elie Bursztein. Javascript polyfill by the [picture polyfill team](https://raw.githubusercontent.com/scottjehl/picturefill/master/Authors.txt)