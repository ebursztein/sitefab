import os
import json
from PIL import Image
from tqdm import tqdm
import random
import pprint
import time
from multiprocessing import Pool as ThreadPool
from itertools import repeat
from diskcache import Cache as dc
from io import StringIO

from sitefab.Plugins import SitePreparsing
from sitefab.SiteFab import SiteFab
from sitefab import files
from sitefab import utils


def generate_thumbnails(images, params):
    "generate thumbnails for a given image"
    total_time = time.time()
    num_errors = 0

    # minimal width that make sense to cache.
    MIN_CACHED_SIZE = params['min_image_width']

    JPEG_QUALITY = 85
    WEBP_QUALITY = 85

    start = time.time()
    cache = dc(params['cache_file'])
    cache_timing = {
        'opening': time.time() - start,
        'fetching': 0,
        'writing': 0
    }

    results = []  # returned info
    for image_full_path in images:
        resize_list = {}
        log = "<br><br><h2>%s</h2>" % (image_full_path)

        # File info extraction
        img_path, img_filename = os.path.split(image_full_path)
        # preserve the directory structure under the input dir
        img_name, img_extension = os.path.splitext(img_filename)
        sub_path = img_path.replace(params['input_dir'], "")
        img_output_path = os.path.join(params['output_dir'], sub_path)
        web_path = image_full_path.replace('\\', '/' ).replace(params['site_output_dir'], "/") #replace the root for output by / as it is what the webserver sees.
        log += "MIN_CACHED_SIZE:%s<br>" % MIN_CACHED_SIZE
        log += "img_path:%s<br>img_filename:%s<br>img_name:%s<br>img_extention:%s<br>img_output_path:%s<br>" % (img_path, img_filename, img_name, img_extension, img_output_path)

        # extensions
        requested_extensions = []
        for f in params['requested_format_list']:
            requested_extensions.append(f)
        requested_extensions.append(img_extension)

        # loading image in memory
        start = time.time()
        f = open(image_full_path, 'rb')
        raw_image = f.read()
        f.close()
        img = Image.open(StringIO(raw_image))
        log += "Opening time:<i>%s</i><br>" % (round(time.time() - start, 3))

        # hashing
        start = time.time()
        img_hash = utils.hexdigest(raw_image) # we use the hash of the content to make sure we regnerate if the image is different
        log += "Hashing time:<i>%s</i><br>" % (round(time.time() - start, 3))

        # width and height
        width, height = img.size
        log += "hash: %s<br>" % (img_hash)
        log += "size: %sx%s<br>" % (width, height)
        log += "</br>"


        # cache loading

        if width >= MIN_CACHED_SIZE:
            start = time.time()
            cached_value = cache.get(img_hash)
            cache_timing['fetching'] += time.time() - start
            if not cached_value: # cache miss!
                log += "Cache status: MISS<br>"
                cached_value = {}
            else:
                log += "Cache status: HIT<br>"
        else:
            cached_value = {}
            log += "Cache status: Image too small, not using cache<br>"



        # add default images
        s = "%s %sw" % (web_path, width)
        pil_extension_codename, web_extension = utils.get_img_extension_alternative_naming(img_extension)
        resize_list[web_extension] = []
        resize_list[web_extension].append(s)

        log += "<table><tr><th>Status</th><th>size</th><th>extension</th><th>gen time</th><th>write time</th><th>msg</th></tr>"
        for requested_width in params['requested_width_list']:
            if requested_width > width:
                log += '<tr><td class="error">Skipped</td><td>%spx</td><td>all</td><td>N/A</td><td>N/A</td><td>Image too small (%spx) to generate %spx thumbnail</td></tr>' % (requested_width, width, requested_width)
                continue

            ratio = float(requested_width) / width
            requested_height = int(height * ratio)  # preserve the ratio

            for extension in requested_extensions:
                pil_extension_codename, web_extension = utils.get_img_extension_alternative_naming(extension)
                if not pil_extension_codename:
                    # unknown extension marking the image as errors and skipping
                    log += '<tr><td class="error">ERROR</td><td>%spx</td><td>%s</td><td>N/A</td><td>N/A</td><td>Unkown extension: %s</td></tr>' % (requested_width, extension, extension)
                    num_errors += 1
                    continue

                if web_extension not in resize_list:
                    resize_list[web_extension] = []

                # filename for the resized image
                output_filename = "%s.%s%s" % (img_name, requested_width, extension)
                output_full_path = os.path.join(img_output_path, output_filename)
                output_web_path = output_full_path.replace("\\", "/").replace(params['site_output_dir'], "/")
                cache_secondary_key = "%s-%s" % (pil_extension_codename, requested_width)
                if cache_secondary_key in cached_value:
                    start = time.time()
                    stringio_file = cached_value[cache_secondary_key]
                    resize_time = time.time() - start
                    log += '<tr><td class="cached">cached</td>'
                #log += "[Cached] %spx thumbnail - generation time: %s" % (requested_width, round(resize_time, 2))
                else:
                    # do the real work
                    # print("cache key:%s --  available keys:%s" % (cache_secondary_key, cached_value.keys()))
                    start = time.time()

                    stringio_file = StringIO()
                    resized_img = img.resize((requested_width,
                                              requested_height), Image.LANCZOS)
                    # print("image:%s, image mode:%s resized image mode:%s" % (image_full_path, img.mode, resized_img.mode))
                    if pil_extension_codename == 'PNG':
                        resized_img.save(stringio_file, pil_extension_codename,
                                         optimize=True, compress_level=9)
                    elif pil_extension_codename == 'WEBP':
                        if resized_img.mode == "P":
                            resized_img = img.convert('RGBA')
                        if resized_img.mode == "L":
                            resized_img = img.convert('RGB')
                        resized_img.save(stringio_file, pil_extension_codename,
                                         optimize=True, compress_level=9,
                                         quality=WEBP_QUALITY)
                    elif pil_extension_codename == "JPEG":
                        if resized_img.mode != "RGB":
                            resized_img = resized_img.convert('RGB')
                        resized_img.save(stringio_file, pil_extension_codename,
                                         optimize=True, quality=JPEG_QUALITY)
                    elif pil_extension_codename == "GIF":
                        resized_img.save(stringio_file, pil_extension_codename,
                                         optimize=True)
                    else:
                        print("Unknown: %s" % image_full_path)

                    resize_time = time.time() - start
                    log += '<tr><td class="generated">generated</td>'
                    # log += "[GENERATED] %spx thumbnail - generation time: %s" % (requested_width, round(resize_time, 2))
                    cached_value[cache_secondary_key] = stringio_file

                # writing to disk
                start = time.time()
                f = open(output_full_path, "wb+")
                f.write(stringio_file.getvalue())
                f.close()
                write_time = time.time() - start
                log += '<td>%spx</td><td>%s</td><td>%ss</td><td>%ss</td><td></td></tr>' % (requested_width, extension, round(resize_time, 3), round(write_time, 4))

                s = "%s %sw" % (output_web_path, requested_width)
                resize_list[web_extension].append(s)

        log += "</table>"

        # log += "Cache: opening time: %s<br>" % (round(cache_open_time, 3))

        if width > MIN_CACHED_SIZE:  # is there anyhthing to cache?
            start = time.time()
            cache.set(img_hash, cached_value)
            # print("cache_key:%s - width:%s - writing keys:%s" % (img_hash, width, sorted(cached_value)))
            cache_timing["writing"] += time.time() - start

        if 'opening' in cache_timing:
            log += "<h3>Cache stats</h3>"
            log += '<table><tr><th>Action</th><th>Timing</th></tr><tr><td>Open</td><td>%s</td></tr><tr><td>Fetch</td><td>%s</td></tr><tr><td>Write</td><td>%s</td></tr></table>' % (cache_timing['opening'], cache_timing['fetching'], cache_timing['writing'])

        results.append([web_path, resize_list, width, log, num_errors, img_hash])

    log += "Total time:%s<br>" % (round(time.time() - total_time, 3))
    if cache:
        cache.close()
    return results
    # (output_web_path, requested_width)


class ResponsiveImages(SitePreparsing):
    """
    Create responsive images
    """

    def process(self, unused, site, config):
        log = ""
        errors = False
        plugin_name = "responsive_images"
        input_dir = config.input_dir
        output_dir = config.output_dir
        multithreading = config.multithreading
        cache_file = os.path.join(site.config.dir.cache, plugin_name)

        # creating output directory
        if not output_dir:
            return (SiteFab.ERROR, plugin_name, "no output_dir specified")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # reading images list
        if not input_dir:
            return (SiteFab.ERROR, plugin_name, "no input_dir specified")


        images = files.get_files_list(input_dir, ["*.jpg","*.jpeg", "*.png", "*.gif"])

        if len(images) == 0:
            return (SiteFab.ERROR, plugin_name, "no images found")

        if config.additional_formats:
            requested_format_list = config.additional_formats
        else:
            requested_format_list = []

        params = {
            "input_dir": input_dir,
            "output_dir": output_dir,
            "site_output_dir": site.config.dir.output,
            "requested_width_list": config.thumbnail_size,
            "requested_format_list": requested_format_list,
            "cache_file": cache_file,  # According to the doc, cache need to be open in different thread
            "min_image_width": config.cache_min_image_width
        }

        # creating needed directories
        for image_full_path in images:
            img_path, img_filename = os.path.split(image_full_path)
            sub_path = img_path.replace(params['input_dir'], "") # preserve the directory structure under the input dir
            img_output_path = os.path.join(params['output_dir'], sub_path)
            if not os.path.exists(img_output_path):
                os.makedirs(img_output_path)


        resize_images = {} # store the results
        num_images = len(images)
        progress_bar = tqdm(total=num_images, unit=' images', desc="Generating responsive_images", leave=False)

        # batching images to reduce cache operation cost.
        random.shuffle(images) # ensuring that the load will be uniformly split among the threads

        batch_size =  20
        #batch_size = num_images / (site.config.threads)
        batches =  [images[x: x + batch_size] for x in xrange(0, len(images), batch_size)]

        bundles = zip(batches, repeat(params))
        results = []

        # allows non-multithread for windows.
        if multithreading:
            log += "Using multithreading: %s threads<br>" % (site.config.threads)
            tpool = ThreadPool(processes=site.config.threads)
            for data in tpool.imap_unordered(generate_thumbnails, bundles):
                results.extend(data)
                progress_bar.update(batch_size)
            tpool.close()
            tpool.join()
        else:
            for bundle in bundles:
                results.extend(generate_thumbnails(bundle))
                progress_bar.update(batch_size)

        for result in results:
            web_path = result[0].replace("\\", "/") #be extra sure that windows path don't messup the thing
            resize_list = result[1]
            width = result[2]
            log += result[3]
            num_errors = result[4]
            img_hash = result[5]
            if num_errors:
                errors = True

            #store all the resized images info
            srcsets = {}
            for webformat, srcset in resize_list.items():
                if webformat == "image/webp":
                    key = 'webp'
                else:
                    key = 'original'
                srcsets[key] = {
                    'srcset': ", ".join(srcset),
                    'format': webformat
                }

            resize_images[web_path] = {"srcsets": srcsets,
                                    "media": '(max_width: %spx)' % width,
                                    "sizes": '(max_width: %spx)' % width,
                                    "hash": img_hash,

            }

        log += pprint.pformat(resize_images)
        # configuring the parser to make use of the resize images
        site.plugin_data['responsive_images'] = resize_images # expose the list of resized images
        if errors:
            return (SiteFab.ERROR, plugin_name, log)
        else:
            return (SiteFab.OK, plugin_name, log)
