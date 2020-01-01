from collections import Counter

def lint(post, test_info, config, image_info):
    """Check images for potential errors - Error E2xx
    
    Additional test ideas: image height (but already test ratio)
    """
    results = []

    images = post.elements.images
    if not images or not len(images):
        images = []

    # image_info plugin based test
    if image_info != None:
        results += e201_local_img_file_exist(images, test_info, image_info)
        results += e204_banner_width(post, test_info, image_info, config)
        results += e205_image_width(images, test_info, image_info, config)
        results += e206_banner_local_img_file_exist(post, test_info, image_info)
        results += e207_banner_ratio(post, test_info, image_info, config)
    
    results += e202_img_origin(images, test_info, config)
    results += e203_duplicate_image(images, test_info)
    return results

def e201_local_img_file_exist(images, test_info, image_info): # unit_tested: yes
    "Check if all the relative images urls have a coresponding image"
    results = []
    for image in images:
        if image[:4] != "http":
            if not image in image_info:
                results.append(['E201', test_info['E201'] % image])
    return results

def e202_img_origin(images, test_info, config):
    "Check that external images come from an whitelisted source"
    # FIXME lot's of case here for unit tests
    results = []
    for image in images:
        if image[:4] == "http":
            if not config.allowed_image_sources or not len(config.allowed_image_sources):
                results.append(['E202', test_info['E202'] % image])
            else:
                for site in config.allowed_image_sources:
                    if site in image:
                        continue
                    else:
                        results.append(['E202', test_info['E202'] % image]) 
    return results

def e203_duplicate_image(images, test_info): # unit_tested:yes
    "Test if an image is used multiple time"
    results = []
    cnt = Counter(images)
    for img in cnt.most_common():
        if img[1] > 1:
            results.append(['E203', test_info['E203'] % (img[0], img[1])])
    return results

def e204_banner_width(post, test_info, image_info, config):
    "Test if a banner width is above a certain size"
    results = []

    if  not post.meta or not "banner" in post.meta or not post.meta.banner:
        results.append(["no banner in meta", ""])
        return results
    
    if post.meta.banner not in image_info:
        results.append(["banner not in image_info", ""])
        return results

    banner_width = image_info[post.meta.banner]['width']
    if banner_width <  config.min_banner_width:
        results.append(['E204', test_info['E204'] % (post.meta.banner, banner_width)])

    return results

def e205_image_width(images, test_info, image_info, config):
    "Test if the width of images is above a certain size"
    results = []

    for image in images:
        if image in image_info and "width" in image_info[image]:
            width = image_info[image]['width']
            if width <  config.min_image_width:
                results.append(['E205', test_info['E205'] % (image, width)])

    return results

def e206_banner_local_img_file_exist(post, test_info, image_info): # unit_tested: yes
    "Check if banner local file exist"
    results = []
    if post.meta and "banner" in post.meta and post.meta.banner != None and post.meta.banner[:4] != "http":
            if not post.meta.banner in image_info:
                results.append(['E206', test_info['E206'] % post.meta.banner])
    return results

def e207_banner_ratio(post, test_info, image_info, config): # unit_tested: yes
    "Check banner ratio"
    results = []
    expected_ratio = config.banner_size_ratio
    if post.meta and "banner" in post.meta and post.meta.banner[:4] != "http" and post.meta.banner in image_info and expected_ratio > 0:
            ratio = round(float(image_info[post.meta.banner]['width']) / image_info[post.meta.banner]['height'], 1)
            if ratio != expected_ratio:
                results.append(['E207', test_info['E207'] % (post.meta.banner, ratio)])
    return results