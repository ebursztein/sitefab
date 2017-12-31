# Responsive Images

Create responsive images by using the `<picture>` element and generating the various
images at different size

## Usage

Specify the various resolutions and format to use and the plugin will generate the images 
for those size and format. It will then replace the `<img>` template with a custom one that
make use of the use of the multi resolutions/format images.

**Important** the plugin depends on the [picture polyfill](https://github.com/scottjehl/picturefill) 
to work on older browsers so make sure to incluse the picture.js in your template. 

**Webp** Webp is not supported by default by Pillow so make sure you install the library if you need to. See the [dependencies](#dependencies) section for more information.




## Configuration

### Configuration file

```yaml
input_dir: "generated/static/images/"
output_dir: "generated/static/images/resized/"

additional_formats: [".webp"]
thumbnail_size: [300, 400, 500, 600, 700, 800, 900, 1000]

cache_min_image_width: 500  # Minimal size for image to be cached
cache_name: "responsive_images" # name of the cache directory 
```

Where

- **input_dir**: is where the images are located
- **output_dir**: is where the thumbnails will be written. **DO NOT** use the input_dir or a sub-directory of it as it will create an ever expanding list of thumbnails
- **additional_formats**: list additional formats on top of the one from the original images that the thumbnails need to be outputed.
- **cache_min_image_width** specify what the minimal width for the images thumbnails to be cached. Caching small images actually cause a slow down. This need to be experimented with but on a medium site 500px with about 6 thumbnails per images seems to work out okay.
- **cache_name**: this is the name of the sub-directory where thumbnails are cached. It leave under the cache directory which is specified in the config file.


## Dependencies

- This plugin requires the [Pillow python package](https://python-pillow.org/).
- WEBP thumbnails requires the webp library. Either use your package system or get it from [this page](https://developers.google.com/speed/webp/download). Don't forget to reinstall Pillow afterward.
- Use the [picture polyfill team](https://raw.githubusercontent.com/scottjehl/picturefill/master/Authors.txt) to get the responsive images compatible with old browser.


## Changlog
- 02/20/17
    - Improved documentation
    - Caching system added
    - Multithread added
    - Multiformat support added
    - Various bugs corrected
- 02/18/17
    - initial version

## Credit
Plugin by Elie Bursztein. Javascript polyfill by the [picture polyfill team](https://raw.githubusercontent.com/scottjehl/picturefill/master/Authors.txt)