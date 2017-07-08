import os
from PIL import Image, ImageFilter
from tqdm import tqdm
import time
import base64
from diskcache import Cache as dc
from StringIO import StringIO

from SiteFab.Plugins import SitePreparsing
from SiteFab.SiteFab import SiteFab
from SiteFab import files
from SiteFab import utils

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
        additional_formats = config.additional_formats
        site_output_dir = site.config.dir.output
        blur_value = 2

        # creating output directory
        if not output_dir:
            return (SiteFab.ERROR, plugin_name, "no output_dir specified")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # reading images list
        if not input_dir:
            return (SiteFab.ERROR, plugin_name, "no input_dir specified")
        
        images  =  files.get_files_list(input_dir, ["*.jpg", "*.jpeg", "*.png", "*.gif"])
        num_images = len(images)

        if num_images == 0:
            return (SiteFab.ERROR, plugin_name, "no images found")
        
        # opening cache
        start = time.time()
        cache = dc(cache_file)
        cache_timing = {
            'opening': time.time() - start,
            'fetching': 0,
             'writing': 0
        }


        # processing images
        frozen_images = {}
        progress_bar = tqdm(total=num_images, unit=' frozen thumb', desc="Generating frozen images", leave=False)
        for image_full_path in images:
            log += "<br><br><h2>%s</h2>" % (image_full_path)
            # Creating needed directories
            img_path, img_filename = os.path.split(image_full_path)
            sub_path = img_path.replace(input_dir, "") # preserve the directory structure under the input dir
            img_output_path = os.path.join(output_dir, sub_path)
            if not os.path.exists(img_output_path):
                os.makedirs(img_output_path)
            
            # File info extraction
            img_path, img_filename = os.path.split(image_full_path)
            img_name, img_extension = os.path.splitext(img_filename)
            pil_extension_codename, web_extension = utils.get_img_extension_alternative_naming(img_extension)            


            # directories
            sub_path = img_path.replace(input_dir, "") # preserve the directory structure under the input dir
            img_output_path = os.path.join(output_dir, sub_path)
            web_path = image_full_path.replace('\\', '/' ).replace(site_output_dir, "/") # base image url
            output_filename = "%s.frozen%s" % (img_name, img_extension)
            output_full_path = os.path.join(img_output_path, output_filename)
            output_web_path = output_full_path.replace("\\", "/").replace(site_output_dir, "/") #frozen image  url

            # loading
            start = time.time()
            raw_image = open(image_full_path, 'rb').read() #we need the raw bytes to do the hashing. Asking PIL for is 10x slower.
            img = Image.open(StringIO(raw_image))
            log += "Image loading time:<i>%s</i><br>" % (round(time.time() - start, 3))
            
            # hashing
            start = time.time()
            img_hash = utils.hexdigest(raw_image)
            log += "Hashing time:<i>%s</i><br>" % (round(time.time() - start, 3))
            log += "hash: %s<br>" % (img_hash)

            # width and height
            width, height = img.size
            ratio = float(frozen_width) / width
            frozen_height = int(height * ratio)  # preserve the ratio
            log += "size: %sx%s<br>"  % (width, height)
            log += "frozen width:%sx%s<br>"

            # cache fetch
            start = time.time()
            cached_value = cache.get(img_hash)
            cache_timing['fetching'] += time.time() - start
            if not cached_value: # cache miss!
                log += "Cache status: MISS<br>"
            else:
                log += "Cache status: HIT<br>"
        
            # generating image
            start = time.time()
            if cached_value:
               stringio_file = cached_value
            else:
                resized_img = img.resize((frozen_width, frozen_height), Image.ANTIALIAS)
                if resized_img.mode != "RGBA":
                    resized_img = resized_img.convert('RGBA')
                resized_img = resized_img.filter(ImageFilter.GaussianBlur(blur_value))
                stringio_file = StringIO()
                resized_img.save(stringio_file, 'JPEG', optimize=True)

            #cache storing
            start_set = time.time()
            cache.set(img_hash, stringio_file)
            cache_timing["writing"] += time.time() - start_set

            "IMG manipulation:%ss<br>" % (time.time() - start)


            #writing to disk
            start = time.time() 
            f = open(output_full_path, "wb+")
            f.write(stringio_file.getvalue())
            f.close()

            s =  base64.b64encode(stringio_file.getvalue())
            img_base64 = "data:image/jpg;base64,%s" % s

            "Write to disk:%ss<br>" % (time.time() - start)

            frozen_images[web_path] = {
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