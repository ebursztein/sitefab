import os
from PIL import Image
from tqdm import tqdm
import time
from StringIO import StringIO

from SiteFab.Plugins import SitePreparsing
from SiteFab.SiteFab import SiteFab
from SiteFab import files
from SiteFab import utils

class ImageInfo(SitePreparsing):
    """
    Gather image info
    """

    def process(self, unused, site, config):
        log = ""
        errors = False
        plugin_name = "image_info"
        input_dir = config.input_dir
        site_output_dir = site.config.dir.output

        # reading images list
        if not input_dir:
            return (SiteFab.ERROR, plugin_name, "no input_dir specified")
        
        images  =  files.get_files_list(input_dir, ["*.jpg", "*.jpeg", "*.png", "*.gif"])
        num_images = len(images)

        if num_images == 0:
            return (SiteFab.ERROR, plugin_name, "no images found")


        # processing images
        image_info = {}
        progress_bar = tqdm(total=num_images, unit=' frozen thumb', desc="Generating frozen images", leave=False)
        for image_full_path in images:
            log += "<br><br><h2>%s</h2>" % (image_full_path)
            # Creating needed directories
            img_path, img_filename = os.path.split(image_full_path)
            sub_path = img_path.replace(input_dir, "") # preserve the directory structure under the input dir
              
            # File info extraction
            img_path, img_filename = os.path.split(image_full_path)
            img_name, img_extension = os.path.splitext(img_filename)
            pil_extension_codename, web_extension = utils.get_img_extension_alternative_naming(img_extension)            

            # directories
            web_path = image_full_path.replace('\\', '/' ).replace(site_output_dir, "/") # base image url

            # loading
            start = time.time()
            raw_image = open(image_full_path, 'rb').read() #we need the raw bytes to do the hashing. Asking PIL for is 10x slower.
            img = Image.open(StringIO(raw_image))
            log += "Image loading time:<i>%s</i><br>" % (round(time.time() - start, 3))
            
            # width and height
            width, height = img.size
            log += "size: %sx%s<br>"  % (width, height)
            
            # FIXME dominante colors


            image_info[web_path] = {
                "extension": img_extension,
                "filename": img_filename,
                "width": width,
                "height": height 
            }
            progress_bar.update(1)

    
        # reporting data
        site.plugin_data['image_info'] = image_info # expose images info

        if errors:
            return (SiteFab.ERROR, plugin_name, log)
        else:
            return (SiteFab.OK, plugin_name, log)