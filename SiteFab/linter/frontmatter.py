from collections import Counter
import re
 
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
    results += e104_duplicate_value(post, test_info, config)
    results += e105_category_in_tags(post, test_info, config)
    results += e106_duplicate_spaces(post, test_info, config)
    results += e107_e108_e109_authors_formating(post, test_info, config)
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


def e104_duplicate_value(post, test_info, config):
    "Check if a value appears twice in a field list"
    results = []
    for field in post.meta:
        value_field = post.meta[field]
        if isinstance(value_field, list):
            count = Counter()
            for elt in value_field:
                try:
                    count[elt] += 1
                except:
                    continue

            duplicates = []
            for elt in count.most_common():
                if elt[1] > 1:
                    duplicates.append(elt[0])
            
            if len(duplicates):
                info = test_info['E104'] % (field, " ,".join(duplicates))
                results.append(['E104', info])
    return results

def e105_category_in_tags(post, test_info, config):
    "Check if the category appears in the tag list"
    results = []
    if "category" in post.meta and "tags" in post.meta:
        if post.meta.category in post.meta.tags:
            info = [post.meta.category, post.meta.tags]
            results.append(['E105', info])
    return results

def e106_duplicate_spaces(post, test_info, config):
    "Check if there are extra spaces"
    results = []
    for field in post.meta:
        value = post.meta[field]
        if not isinstance(value, list):
            value = [value]
        for elt in value:
            if isinstance(elt, str):
                extra_space  = re.search(" {2,}", elt)
                if extra_space:
                    info = [field, elt]
                    results.append(['E106', info])
    return results

def e107_e108_e109_authors_formating(post, test_info, config):
    "Check if the authors list is properly formatted"
    results = []
    
    if not "authors" in post.meta:
        return results
    
    authors = post.meta.authors
    if not isinstance(authors, list):
        results.append(['E107', authors])
        return results

    for author in authors:
        if ',' not in author:
            results.append(['E108', author])
        if not author.istitle():
            results.append(['E109', author])
    return results
# capitalization