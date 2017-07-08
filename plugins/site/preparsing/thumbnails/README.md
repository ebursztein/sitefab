# Image Thumbnails

Generated thumbnails hard-croped to the specified size. If you want to have images resized (soft-cropped) then use the reactive_images plugin

## Configuration

```yaml
input_dir: "generated/static/images/"
output_dir: "generated/static/thumbnails/" #don't output under input dir to avoid overloading other images plugins
thumbnail_sizes: #thumbnails size.
  - [120,120]
  - [96, 56]
```

## Usage

Assuming you have generated a 120x120 thumbnail you can access it as follow:

```jinja2
<img src="{{ plugin_data.thumbnails[src]['120x120'] }}"/>
```

## Changlog
- v1
    - initial version

## Credit

Plugin by Elie Bursztein.