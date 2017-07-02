from collections import Counter, defaultdict

def lint(post, test_info, config):
    "Check the structure of given post for potential errors"
    
    results = []

    if  post.meta == None or "toc" not in post.meta:
        return results
    
    tests = [
        e300_no_h1,
        e301_no_single_headline
    ]

    for test in tests:
        results += test(post, test_info, config)

    return results

def e300_no_h1(post, test_info, config):
    "Check for the absence of H1 in the content of the post"
    results = []
    for item in post.meta.toc:
       if item[1] == 1:
           info = test_info['E300'] % (item[0])
           results.append(['E300', info])
    return results

def e301_no_single_headline(post, test_info, config):
    "Check that there not only one h2, h3, h4"
    results = []
    counter = Counter()
    elts = defaultdict(list)
    for item in post.meta.toc:
        counter[item[1]] += 1
        elts[item[0]]
    
    for val, count in counter.most_common():
        if count == 1:
            info = test_info['E301'] % (val, " ,".join(elts[val]))
            results.append(['E301', info])
    return results