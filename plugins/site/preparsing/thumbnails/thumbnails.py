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


class Thumbnails(SitePreparsing):
    "Generate thumbnail images"

    def process(self, unused, site, config):
        log = ""
        errors = False
        plugin_name = "thumbnails"
        input_dir = config.input_dir
        output_dir = config.output_dir
        thumbnail_sizes = config.thumbnail_sizes
        cache_file = os.path.join(site.config.dir.cache, plugin_name)
        site_output_dir = site.config.dir.output

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
        thumbs = {}
        num_thumbs = len(images) * len(thumbnail_sizes)
        progress_bar = tqdm(total=num_thumbs, unit=' thumbnails', desc="Generating thumbnails", leave=False)
        for img_info in images:
            thumb = {}
            log += "<br><br><h2>%s</h2>" % (img_info['full_path'])

            sub_path = img_info['path']
            if sub_path[-1] != "/": # not ideal as it might crash on windwos. FIXME:more testing
                sub_path += "/"
            sub_path = sub_path.replace(input_dir[:-1], "") # preserve the directory structure under the input dir


            if sub_path[0] == "/" or sub_path[0] == "\\": # startingv with / or \ on the 2nd arg mess-up os.path.join
                sub_path = sub_path[1:]

            img_output_path = os.path.join(output_dir, sub_path)
            log += "img_output_path: %s<br>" % img_output_path
            log += "output_dir: %s<br>" % output_dir
            log += "sub_path: %s<br>" % sub_path
            log += "input_dir: %s<br>" % input_dir

            # Creating needed directories
            if not os.path.exists(img_output_path):
                os.makedirs(img_output_path)

            # cache fetch
            start = time.time()
            cached_version = cache.get(img_info['hash'])
            cache_timing['fetching'] += time.time() - start

            #Do we have a cached version else creating it
            if cached_version:
                raw_image = cached_version['raw_image']
            else:
                start = time.time()
                raw_image = open(img_info['full_path'], 'rb').read()
                log += "Image loading time:<i>%s</i><br>" % (round(time.time() - start, 5))
                cached_version = {}
                cached_version['raw_image'] = raw_image

            img = None
            for thumb_width, thumb_height in thumbnail_sizes:
                thumb_key = "%sx%s" % (thumb_width, thumb_height)
                log += "<h3>%s</h3>" % (thumb_key)
                output_filename = "%s-thumb-%s%s" % (img_info['name'], thumb_key, img_info['extension'])
                output_full_path = os.path.join(img_output_path, output_filename)
                output_web_path = output_full_path.replace("\\", "/").replace(site_output_dir, "/")
                thumb[thumb_key] = output_web_path
                log += "output_filename: %s<br>" % output_filename
                log += "output_full_path: %s<br>" % output_full_path
                log += "output_web_path: %s<br>" % output_web_path

                # generating image
                start = time.time()
                if thumb_key in cached_version:
                    log += "Cache status: HIT<br>"
                    thumb_stringio = cached_version[thumb_key]
                else:
                    log += "Cache status: MISS<br>"

                    # parsing image if needed
                    if not img:
                        img = Image.open(StringIO(raw_image))
                        img_width, img_height = img.size
                        log += "img size: %sx%s<br>" % (img_width, img_height)

                    #scale on the smallest side to maximize quality
                    if img_width < img_height:
                        ratio = img_height  / float(img_width)
                        if thumb_width  * ratio >  thumb_height: #take into account thumb requested ratio
                            ratio2 = thumb_width / float(img_width)
                            tmp_height = int(img_height * ratio2)
                            thumb_img = img.resize((thumb_width, tmp_height), Image.LANCZOS)
                        else:
                            ratio2 = thumb_height / float(img_height)
                            tmp_width = int(img_width * ratio2)
                            thumb_img = img.resize((tmp_width, thumb_height), Image.LANCZOS)
                    else:
                        ratio = float(img_width) / img_height
                        if thumb_height * ratio > thumb_width:
                            ratio2 = thumb_height / float(img_height)
                            tmp_width = int(img_width * ratio2)
                            thumb_img = img.resize((tmp_width, thumb_height), Image.LANCZOS)
                        else:
                            ratio2 = thumb_width / float(img_width)
                            tmp_height = int(img_height * ratio2)
                            thumb_img = img.resize((thumb_width, tmp_height), Image.LANCZOS)


                    scaled_width = thumb_img.width
                    scaled_height = thumb_img.height
                    log += "Image scaled to %sx%s<br>" % (scaled_width, scaled_height)

                    ### cropping ###
                    top = 0.0
                    bottom = 1.0
                    left = 0.0
                    right = 1.0

                    #cutting the width if needed
                    ratio_width = thumb_width / float(scaled_width)
                    if ratio_width < 1:
                        reduction_factor = 1 - ratio_width
                        baricenter = 0.5 #FIXME: potentially compute using interest points
                        center = float(scaled_width) * baricenter
                        left = (center - thumb_width / 2) / float(scaled_width)
                        right = left + ratio_width

                        # correcting potential overflow
                        if left < 0:
                            log += "correcting overflow on the left<br>"
                            right -= left
                            left = 0.0

                        if right > 1:
                            log += "correcting overflwo on the right<br>"
                            left -= (right - 1.0)
                            right = 1.0

                        log += "baricenter:%s, reduction_factor:%s, center:%s, left:%s, right:%s<br>" % (baricenter, reduction_factor, center, left, right)

                    # cut height
                    ratio_height = thumb_height / float(scaled_height)
                    if ratio_height < 1:
                        reduction_factor = 1 - ratio_height
                        baricenter = 0.5
                        center = float(scaled_height) * baricenter  # center as weight by the baricenter
                        top = (center - thumb_height / 2) / float(scaled_height)
                        bottom = top + ratio_height

                        # correcting for overflow
                        if top < 0:
                            log += "correcting overflow on the top<br>"
                            bottom -= top
                            top = 0.0

                        if bottom > 1:
                            log += "correcting overflow on the bottom<br>"
                            top -= (bottom - 1.0)
                            bottom = 1.0

                    log += "bounding box left: %s, top: %s, right: %s, bottom: %s<br>" % (left, top, right, bottom)
                    left_pixel = int(scaled_width * left)
                    top_pixel = int(scaled_height * top)
                    right_pixel = int(scaled_width * right)
                    bottom_pixel = int(scaled_height * bottom)

                    if right_pixel - left_pixel != thumb_width: #happen when both are at .5
                        right_pixel += thumb_width - (right_pixel - left_pixel)

                    if bottom_pixel - top_pixel != thumb_height: #happen when both are at .5
                        bottom_pixel += thumb_height - (bottom_pixel - top_pixel)

                    log += "crop pixel box: left %s, top: %s, right: %s, bottom: %s<br>" % (left_pixel, top_pixel, right_pixel, bottom_pixel)

                    thumb_img = thumb_img.crop([left_pixel, top_pixel, right_pixel, bottom_pixel])
                    log += "thumbnail size: %sx%s<br>" % (thumb_img.width, thumb_img.height)

                    if thumb_img.mode == "P":
                        thumb_img = thumb_img.convert('RGBA')
                    thumb_img = thumb_img.convert('RGB')

                    thumb_stringio = StringIO()
                    thumb_img.save(thumb_stringio, 'JPEG', optimize=True, quality=90) #FIXME support webp and tune parameters
                    cached_version[thumb_key] = thumb_stringio

                    log += "thumbnail generation:%ss<br>" % (round(time.time() - start, 5))


                #writing to disk
                start = time.time()
                f = open(output_full_path, "wb+")
                f.write(thumb_stringio.getvalue())
                f.close()
                progress_bar.update(1)


            #cache storing
            start_set = time.time()
            cache.set(img_info['hash'], cached_version)
            cache_timing["writing"] += time.time() - start_set

            thumbs[img_info['web_path']] = thumb

        site.plugin_data['thumbnails'] = thumbs # expose the list of resized images
        cache.close()
        #FIXME: add counter output

        if errors:
            return (SiteFab.ERROR, plugin_name, log)
        else:
            return (SiteFab.OK, plugin_name, log)