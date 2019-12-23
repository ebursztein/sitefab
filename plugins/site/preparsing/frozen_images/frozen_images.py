import os
from PIL import Image, ImageFilter
from tqdm import tqdm
import time
import base64
from diskcache import Cache as dc
from io import StringIO

from sitefab.Plugins import SitePreparsing
from sitefab.SiteFab import SiteFab
from sitefab import files
from sitefab import utils

class FrozenImages(SitePreparsing):
    """
    Create frozen images
    """

    def process(self, unused, site, config):
        log = ""
        errors = False
        plugin_name = "frozen_images"
        frozen_width = 42
        input_dir = config.input_dir
        output_dir = config.output_dir
        cache_file = os.path.join(site.config.dir.cache, plugin_name)
        site_output_dir = site.config.dir.output
        blur_value = 2

        # creating output directory
        if not output_dir:
            return (SiteFab.ERROR, plugin_name, "no output_dir specified")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # opening cache
        start = time.time()
        cache = dc(cache_file)
        cache_timing = {
            'opening': time.time() - start,
            'fetching': 0,
             'writing': 0
        }

        # using the list of images from image_info
        if 'image_info' not in site.plugin_data:
            log += 'image_info not found in plugin_data. No images?'
            return (SiteFab.ERROR, plugin_name, log)
        images = site.plugin_data['image_info'].values()

        # processing images
        frozen_images = {}
        progress_bar = tqdm(total=len(images), unit=' frozen thumb',
                            desc="Generating frozen images", leave=False)
        for img_info in images:
            log += "<br><br><h2>%s</h2>" % (img_info['full_path'])
            # Creating needed directories
            # preserve the directory structure under the input dir
            sub_path = img_info['path'].replace(input_dir, "")
            img_output_path = os.path.join(output_dir, sub_path)
            if not os.path.exists(img_output_path):
                os.makedirs(img_output_path)

            img_output_path = os.path.join(output_dir, sub_path)
            output_filename = "%s.frozen%s" % (img_info['name'], img_info['extension'])
            output_full_path = os.path.join(img_output_path, output_filename)
            output_web_path = output_full_path.replace("\\", "/").replace(site_output_dir, "/") #frozen

            # cache fetch
            start = time.time()
            cached_value = cache.get(img_info['hash'])
            cache_timing['fetching'] += time.time() - start

            # generating image
            start = time.time()
            if cached_value:
                log += "Cache status: HIT<br>"
                stringio_file = cached_value
            else:
                log += "Cache status: MISS<br>"
                # loading
                start = time.time()
                f = open(img_info['full_path'], 'rb')
                raw_image = f.read()
                f.close()
                log += "Image loading time:<i>%s</i><br>" % (round(time.time() - start, 3))
                img = Image.open(StringIO(raw_image))

                # width and height
                width, height = img.size
                ratio = float(frozen_width) / width
                frozen_height = int(height * ratio)  # preserve the ratio
                log += "size: %sx%s<br>"  % (width, height)
                log += "frozen width:%sx%s<br>"
                resized_img = img.resize((frozen_width, frozen_height), Image.LANCZOS)
                if resized_img.mode == "P": # PIL complain if we don't force the conversion first
                    resized_img = img.convert('RGBA')
                resized_img = resized_img.convert('RGB')
                resized_img = resized_img.filter(ImageFilter.GaussianBlur(blur_value))
                stringio_file = StringIO()
                resized_img.save(stringio_file, 'JPEG', optimize=True)

            # cache storing
            start_set = time.time()
            cache.set(img_info['hash'], stringio_file)
            cache_timing["writing"] += time.time() - start_set

            "IMG manipulation:%ss<br>" % (time.time() - start)

            # writing to disk
            start = time.time()
            f = open(output_full_path, "wb+")
            f.write(stringio_file.getvalue())
            f.close()

            s = base64.b64encode(stringio_file.getvalue())
            img_base64 = "data:image/jpg;base64,%s" % s

            "Write to disk:%ss<br>" % (time.time() - start)

            frozen_images[img_info['web_path']] = {
                "url": output_web_path,
                "base64": img_base64,
            }
            log += 'Img result (from base64): <img src="%s">' % img_base64
            progress_bar.update(1)


        # reporting data
        site.plugin_data['frozen_images'] = frozen_images # expose the list of resized images
        cache.close()

        #FIXME: add counter output

        if errors:
            return (SiteFab.ERROR, plugin_name, log)
        else:
            return (SiteFab.OK, plugin_name, log)
