def lint(post, test_info, config):
    "Check the frontmatter of a given post for potential errors"
    results = []

    # Testing is meta exists otherwise bailout
    if post.meta == None:
        results.append(['E100', test_info['E100']])
        return results
    # Run metas tests
    results += e101_mandatory_fields(post, test_info, config)
    results += e102_mandatory_fields_for_specific_templates(post, test_info, config)
    results += e103_field_value(post, test_info, config)
    return results

def e101_mandatory_fields(post, test_info, config):
    "Check for the presence of mandatory fields in the meta"
    results = []
    for field in config.frontmatter_mandatory_fields:
        if field not in post.meta:
            results.append(['E101', test_info['E101'] % field])
    return results

def e102_mandatory_fields_for_specific_templates(post, test_info, config):
    "Check for the presense of mandatory field for specific template"
    
    results = []

    if "template" not in post.meta:
        return results

    if post.meta.template in config.frontmatter_mandatory_fields_by_templates:
        for field in config.frontmatter_mandatory_fields_by_templates[post.meta.template]:
            if field not in post.meta:
                info = test_info['E102'] % (field, post.meta.template)
                results.append(['E102', info])
    return results

def e103_field_value(post, test_info, config):
    "Check if the value for specific fields match the list"
    
    results = []
    for field in config.frontmatter_fields_value:
        if field in post.meta:
            if post.meta[field] not in config.frontmatter_fields_value[field]:
                info = test_info['E103'] % (field, post.meta[field], config.frontmatter_fields_value[field])
                results.append(['E103', info])
    return results
