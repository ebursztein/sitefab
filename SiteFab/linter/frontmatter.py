def lint(post, test_info, config):
    "Check the frontmatter of a given post for potential errors"
    results = []

    # Testing is meta exists otherwise bailout
    if post.meta == None:
        results.append(['E100', test_info['E100']])
        return results
    # Run metas tests
    results += e101_mandatory_fields(post, test_info, config)

    return results

def e101_mandatory_fields(post, test_info, config):
    "Check for the presence of mandatory fields in the meta"
    results = []
    for field in config.frontmatter_mandatory_fields:
        if field not in post.meta:
            results.append(['E101', test_info['E101']  % field])

    return results
