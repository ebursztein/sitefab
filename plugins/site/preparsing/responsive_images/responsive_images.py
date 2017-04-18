import os
import json
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool as ThreadPool
from itertools import repeat
from diskcache import Cache as dc
import hashlib
from StringIO import StringIO

from SiteFab.Plugins import SitePreparsing
from SiteFab.SiteFab import SiteFab
from SiteFab import files
import time

def get_extension_alternative_naming(extension):
    "Return extensions naming for PIL and Mime/type"
    web_extension = None
    pil_extension_codename  = None

    if extension.lower() == ".jpg" or extension.lower() == ".jpeg":
        pil_extension_codename = "JPEG"
        web_extension = "image/jpeg"
    
    elif extension.lower() == ".png":
        pil_extension_codename = "PNG"
        web_extension = "image/png"
    
    elif extension.lower() == ".gif":
        pil_extension_codename = "GIF"
        web_extension = "image/gif"

    elif extension.lower() == ".webp":
        pil_extension_codename = "WEBP"
        web_extension = "image/webp"
    return [pil_extension_codename, web_extension]

def generate_thumbnails((image_full_path, params)):
    "generate thumbnails for a given image"
    total_time = time.time()
    resize_list = {} # record all the generated images
    num_errors = 0
    MIN_CACHED_SIZE = params['min_image_width']  #minimal width where it make sense to cache.
    
    log = "<br><br><h2>%s</h2>" % (image_full_path)
    
    # File info extraction
    img_path, img_filename = os.path.split(image_full_path)
    img_name, img_extension = os.path.splitext(img_filename)            
    sub_path = img_path.replace(params['input_dir'], "") # preserve the directory structure under the input dir
    img_output_path = os.path.join(params['output_dir'], sub_path)
    
    # loading image in memory
    start = time.time()
    img = Image.open(image_full_path)
    opening_time = time.time() - start
    img_hash = hashlib.sha256(img.tobytes()).hexdigest()  # we use the hash of the content to make sure we regnerate if the image is different 

    width, height = img.size
    web_path = image_full_path.replace('\\', '/' ).replace(params['site_output_dir'], "/") #replace the root for output by / as it is what the webserver sees.

    log += "opening time:%s<br>" % (round(opening_time, 3))
    log += "hash: %s<br>" % (img_hash)
    log += "size: %sx%s<br>"  % (width, height)
    log += "</br>"


    # add default images
    s = "%s %sw" % (web_path, width)
    pil_extension_codename, web_extension = get_extension_alternative_naming(img_extension)
    resize_list[web_extension] = []
    resize_list[web_extension].append(s)
   

    cache = None
    cached_value = {}
    cache_timing = {}    
    requested_extensions = []
    for f in params['requested_format_list']:
        requested_extensions.append(f)
    requested_extensions.append(img_extension)
    #print "\n\n%s\n%s\n\n" % ( params['requested_format_list'], requested_extensions)

    log += "<table><tr><th>Status</th><th>size</th><th>extension</th><th>gen time</th><th>write time</th><th>msg</th></tr>"
    for requested_width in params['requested_width_list']:
        if requested_width >= width:
            log += '<tr><td class="error">Skipped</td><td>%spx</td><td>all</td><td>N/A</td><td>N/A</td><td>Image too small (%spx) to generate %spx thumbnail</td></tr>' % (requested_width, width, requested_width)
            continue

        ratio = float(requested_width) / width
        requested_height = int(height * ratio)  # preserve the ratio
        
        for extension in requested_extensions:
            pil_extension_codename, web_extension = get_extension_alternative_naming(extension)
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
            
            # loading cache only when needed.
            if not cache and requested_width > MIN_CACHED_SIZE:
                start = time.time()
                cache = dc(params['cache_file'])
                cache_timing['opening'] = time.time() - start
                start = time.time()
                cache_key = "%s" % (img_hash)
                try:
                    cached_value = cache.get(cache_key)
                except:
                    cached_value = {}
                    cache_timing['loading'] = time.time() - start
                    log += "<b>ERROR</b>: can't open cache<br>"
                if not cached_value:
                    cache_timing['loading'] = time.time() - start 
                    cached_value = {}
                else:
                    cache_timing['loading'] = time.time() - start
            else:
                log += "INFO: Image too small, not using cache<br>"
  


            cache_secondary_key = "%s-%s" % (pil_extension_codename, requested_width)
            if cache_secondary_key in cached_value:   
                start = time.time()
                stringio_file = cached_value[cache_secondary_key]
                resize_time = time.time() - start
                log += '<tr><td class="cached">cached</td>'
                #log += "[Cached] %spx thumbnail - generation time: %s" % (requested_width, round(resize_time, 2))
            else:
                # do the real work
                start = time.time()
                resized_img = img.resize((requested_width, requested_height), Image.ANTIALIAS)
                stringio_file = StringIO()
                if resized_img.mode != "RGBA":
                    resized_img = resized_img.convert('RGBA')
                resized_img.save(stringio_file, pil_extension_codename)
                resize_time = time.time() - start
                log += '<tr><td class="generated">generated</td>'
                #log += "[GENERATED] %spx thumbnail - generation time: %s" % (requested_width, round(resize_time, 2))
                cached_value[cache_secondary_key] = stringio_file
            
            start = time.time() 
            f = open(output_full_path, "wb+")
            f.write(stringio_file.getvalue())
            f.close()
            write_time = time.time() - start
            log += '<td>%spx</td><td>%s</td><td>%ss</td><td>%ss</td><td></td></tr>' % (requested_width, extension, round(resize_time, 3), round(write_time, 3))

            s = "%s %sw" % (output_web_path, requested_width)
            resize_list[web_extension].append(s)

    log += "</table>" 

    #        log += "Cache: opening time: %s<br>" % (round(cache_open_time, 3))
      
    if cache and width > MIN_CACHED_SIZE:
        start = time.time()
        cache.set(cache_key, cached_value)
        cache.close()
        cache_timing["writing"] = time.time() - start
    else:
        cache_timing["writing"] = -1
    
    if 'opening' in cache_timing:
        log += "<h3>Cache stats</h3>"
        log += '<table><tr><th>Action</th><th>Timing</th></tr><tr><td>Open</td><td>%s</td></tr><tr><td>Load</td><td>%s</td></tr><tr><td>Write</td><td>%s</td></tr></table>' % (cache_timing['opening'], cache_timing['loading'], cache_timing['writing'])
   
    
    log += "Total time:%s<br>" % (round(time.time() - total_time, 3))
    
    return [web_path, resize_list, width, log, num_errors]
    #(output_web_path, requested_width)

class ResponsiveImages(SitePreparsing):
    """
    Create responsive images
    """

    def process(self, unused, site, config):
        log = ""
        errors = False


        input_dir = config.input_dir
        output_dir = config.output_dir
        cache_file = os.path.join(site.config.dir.cache, config.cache_name)

        #loading HTML template
        fname = os.path.join(files.get_site_path(), config.template_file)
        html_template = files.read_file(fname)

        if len(html_template) == "":
            return (SiteFab.ERROR, "ResponsiveImages", log)

        # creating output directory
        if not output_dir:
            return (SiteFab.ERROR, "ResponsiveImages", "no output_dir specified")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # reading images list
        if not input_dir:
            return (SiteFab.ERROR, "ResponsiveImages", "no input_dir specified")
        
        
        images  =  files.get_files_list(input_dir, ["*.jpg","*.jpeg", "*.png", "*.gif"])
        
        if len(images) == 0:
            return (SiteFab.ERROR, "ResponsiveImages", "no images found")
        
        params = {
            "input_dir": input_dir,
            "output_dir": output_dir,
            "site_output_dir": site.config.dir.output,
            "requested_width_list": config.thumbnail_size,
            "requested_format_list": config.additional_formats,
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
        num_resize = len(params['requested_width_list'])
        num_format = 1 + len(params['requested_format_list'])
        total_thumbnails = len(images)* num_resize * num_format
        progress_bar = tqdm(total=total_thumbnails, unit=' thumbnails', desc="Generating thumbnails", leave=False)

        bundles = zip(images, repeat(params)) 
        tpool = ThreadPool(processes=site.config.threads)        
        #chunksize = (len(images) / (self.config.threads * 2)) < don't seems to make a huge difference
        for result in tpool.imap_unordered(generate_thumbnails, bundles, chunksize=1):           
        #for bundle in bundles:
        #    result = generate_thumbnails(bundle)
            progress_bar.update(num_resize)
            web_path = result[0].replace("\\", "/") #be extra sure that windows path don't messup the thing
            resize_list = result[1]
            width = result[2]
            log += result[3]
            num_errors = result[4]
            if num_errors:
                errors = True

            #store all the resized images info
            srcsets = {}
            for webformat, srcset in resize_list.iteritems():
                srcsets[webformat] = ", ".join(srcset)

            resize_images[web_path] = {"srcsets": srcsets,
                                       "media": '(max_width: %spx)' % width,
                                       "sizes": '(max_width: %spx)' % width
            }


                
        tpool.close()
        tpool.join()
        # configuring the parser to make use of the resize images
        site.config.parser.plugin_data['responsive_images'] = resize_images # pass the list of images to the parser
        site.inject_parser_html_template("reponsive_images", "img", html_template) # modify the template used to render images

        if errors:
            return (SiteFab.ERROR, "ResponsiveImages", log)
        else:
            return (SiteFab.OK, "ResponsiveImages", log)