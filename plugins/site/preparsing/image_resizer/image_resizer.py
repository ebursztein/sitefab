import os
from PIL import Image
from tqdm import tqdm
import time
from diskcache import Cache as dc
from io import StringIO

from sitefab.Plugins import SitePreparsing
from sitefab.SiteFab import SiteFab


class ImageResizer(SitePreparsing):
    "Resize images"

    def process(self, unused, site, config):
        log = ""
        errors = False
        plugin_name = "image_resizer"
        input_dir = config.input_dir
        max_width = config.max_width
        quality = config.quality
        cache_file = os.path.join(site.config.dir.cache, plugin_name)
        site_output_dir = site.config.dir.output

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
        progress_bar = tqdm(total=len(images), unit=' image', desc="Resizing images", leave=False)
        for img_info in images:
            thumb = {}
            log += "<br><br><h2>%s</h2>" % (img_info['full_path'])

            if img_info['width'] < max_width:
                log += "Image width %s < max_width: %s skipping" % (img_info['width'], max_width)
                continue

            # cache fetch
            start = time.time()
            cached_version = cache.get(img_info['hash'])
            cache_timing['fetching'] += time.time() - start

            #Do we have a cached version else creating it
            if cached_version:
                raw_image = cached_version['raw_image']
            else:
                start = time.time()
                f = open(img_info['full_path'], 'rb')
                raw_image = f.read()
                f.close()

                log += "Image loading time:<i>%s</i><br>" % (round(time.time() - start, 5))
                cached_version = {}
                cached_version['raw_image'] = raw_image
                cached_version['max_width'] = -1

            # Is the cached version have the right size?
            if cached_version['max_width'] == max_width:
                log += "Cache status: HIT<br>"
                stringio = cached_version['resized_img']
                resized_img = Image.open(stringio)
            else:
                log += "Cache status: MISS<br>"

                img = Image.open(StringIO(raw_image))
                img_width, img_height = img.size
                log += "img size: %sx%s<br>" % (img_width, img_height)

                ratio = max_width / float(img_width)
                new_height = int(img_height * ratio)
                resized_img = img.resize((max_width, new_height), Image.LANCZOS)
                log += "Image resized to %sx%s<br>" % (max_width, new_height)

                stringio = StringIO()
                pil_extension_codename =  img_info['pil_extension']
                if pil_extension_codename == 'PNG':
                    resized_img.save(stringio, pil_extension_codename, optimize=True, compress_level=9)#
                elif pil_extension_codename == 'WEBP':
                    if resized_img.mode != "RGBA":
                        resized_img = resized_img.convert('RGBA')
                    resized_img.save(stringio, pil_extension_codename, optimize=True, compress_level=9, quality=quality)#
                else: #jpg
                    if resized_img.mode != "RGB":
                        resized_img = resized_img.convert('RGB')
                    resized_img.save(stringio, pil_extension_codename, optimize=True, quality=quality, compress_level=9)
                img.close()

                cached_version['max_width'] = max_width
                cached_version['resized_img'] = stringio
                log += "resize time:%ss<br>" % (round(time.time() - start, 5))


            # writing to disk
            start = time.time()
            f = open(img_info['full_path'], "wb+")
            f.write(stringio.getvalue())
            f.close()
            progress_bar.update(1)

            # update image info to reflect new size
            width, height = resized_img.size
            site.plugin_data['image_info'][img_info['web_path']]['width'] = width
            site.plugin_data['image_info'][img_info['web_path']]['height'] = height

            # cache storing
            start_set = time.time()
            cache.set(img_info['hash'], cached_version)
            cache_timing["writing"] += time.time() - start_set

        cache.close()
        #FIXME: add counter output

        if errors:
            return (SiteFab.ERROR, plugin_name, log)
        else:
            return (SiteFab.OK, plugin_name, log)