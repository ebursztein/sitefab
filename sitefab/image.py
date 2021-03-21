"Image function common to many plugins"
from io import BytesIO
from .utils import hexdigest


def image_hash(raw_image):
    """Compute imgae hash

    Args:
        raw_image (bytes): image raw bytes.

    Returns:
        str: image hash
    """
    return hexdigest(raw_image)


def convert_image(img,
                  extension_codename,
                  jpeg_quality=85,
                  webp_quality=80,
                  return_as_bytesio=True,
                  webp_lossless=False,
                  webp_method=6):
    """Generate an image in the requested format

    Args:
        img (PIL.Image): The image to save.

        extension_codename (PIL extension name): normalize extension name.
        See: get_img_extension_alternative_naming to generate those

        compression_level (int, optional): Png compression level.
        Defaults to 6.

        jpeg_quality (int, optional): Jpeg quality level. Defaults to 85.

        webp_quality (int, optional): Webp quality level. Defaults to 85.

        return_as_bytesio (bool, optional): save image in a byteIO,
        if false return the image it self. Defauls to True.

        webp_lossless (boolean, optional): Default is False,
        only True when saving in webp.

        webp_method (int, optional): Defaults to 6 the best quality to
        save webp images.

    Returns:
        BytesIO or Image: the converted image as byteIO if return_as_bytesio
        is true or as Image otherwise.
    """

    img_io = BytesIO()

    # encoding
    if extension_codename == 'PNG':
        if return_as_bytesio:
            # no need to pass compress_level value as optimize set it to 9
            img.save(img_io,
                     extension_codename,
                     optimize=True)

    elif extension_codename == 'WEBP':

        # if lossless quality == compression effort.
        # ! keep it at 80 as 100 is insanely slow
        if webp_lossless:
            webp_quality = 80

        if img.mode == "P":
            img = img.convert('RGBA')
        if img.mode == "L":
            img = img.convert('RGB')

        img.save(img_io,
                 extension_codename,
                 method=webp_method,
                 quality=webp_quality,
                 lossless=webp_lossless)

    elif extension_codename == "JPEG":
        if img.mode != "RGB":
            img = img.convert('RGB')
        img.save(img_io,
                 extension_codename,
                 optimize=True,
                 quality=jpeg_quality)

    elif extension_codename == "GIF":
        img.save(img_io, extension_codename, optimize=True)

    if return_as_bytesio:
        return img_io
    else:
        return img


def read_image_bytes(path):
    """Read raw image bytes from disk

    we need this because use a lot of bytesIO for manipulation
    and getting the bytes via PIL image API is 10x slower.

    Args:
        path (Path): image path

    Returns:
        bytes: images bytes
    """
    f = open(path, 'rb')
    raw_image = f.read()
    f.close()
    return raw_image


def save_image(img_io, path):
    """Save the image

    Args:
        img_io (BytesIO): The image byteIO representation
        path (Path): Path where to save the image

    Returns:
        int: 1 ok, 0 failed
    """
    # FIXME non-existing path testing

    # writing to disk
    f = open(path, "wb+")
    f.write(img_io.getvalue())
    f.close()
    return 1


def normalize_image_extension(extension):
    """Return extensions naming for PIL and Mime/type.

    Args:
        extension (str): extension to normalize.

    Returns:
        list: [PIL extension codename, mimetye]
    """
    web_extension = None
    extension_codename = None

    if extension.lower() == ".jpg" or extension.lower() == ".jpeg":
        extension_codename = "JPEG"
        web_extension = "image/jpeg"

    elif extension.lower() == ".png":
        extension_codename = "PNG"
        web_extension = "image/png"

    elif extension.lower() == ".gif":
        extension_codename = "GIF"
        web_extension = "image/gif"

    elif extension.lower() == ".webp":
        extension_codename = "WEBP"
        web_extension = "image/webp"

    return [extension_codename, web_extension]
