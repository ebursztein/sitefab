def lint(post, test_info, config):
    "Check the structure of given post for potential errors"
    
    results = []

    if  post.meta == None or post.meta.toc == None:
        return results
    
    tests = [
        e300_no_h1,
    ]

    for test in tests:
        results += test(post, test_info, config)

    return results

def e300_no_h1(post, test_info, config):
    "Check for the absence of H1 in the content of the post"
    results = []
    return results