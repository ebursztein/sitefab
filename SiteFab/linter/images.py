def lint(post, test_info, config, image_info):
    "Check images for potential errors - Error E2xx"
    results = []
    # Run metas tests
    if image_info:
        results += e201_local_img_file_exist(post, test_info, image_info)
    results += e202_img_origin(post, test_info, config)
    return results

def e201_local_img_file_exist(post, test_info, image_info):
    "Check if all the relative images urls have a coresponding image"
    results = []
    for image in post.elements.images:
        if image[:4] != "http":
            if not image in image_info:
                results.append(['E201', test_info['E201'] % image])
    return results

def e202_img_origin(post, test_info, config):
    "Check that external images come from an whitelisted source"
    # FIXME lot's of case here for unit tests
    results = []
    for image in post.elements.images:
        if image[:4] == "http":
            if not config.allowed_image_sources or not len(allowed_image_sources):
                results.append(['E202', test_info['E202'] % image])
            else:
                for site in config.allowed_image_sources:
                    if site in image:
                        continue
                    else:
                        results.append(['E202', test_info['E202'] % image]) 
    return results
