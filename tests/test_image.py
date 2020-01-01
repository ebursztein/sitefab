from sitefab import image


def test_img_extensions():
    values = [
        [".png", "PNG", "image/png"],
        [".webp", "WEBP", "image/webp"],
        [".jpeg", "JPEG", "image/jpeg"],
        [".jpg", "JPEG", "image/jpeg"],
        ["unkn", None, None]
    ]
    for value in values:
        codename, extension = image.normalize_image_extension(value[0])
        assert codename == value[1]
        assert extension == value[2]
