# encoding: utf-8
from collections import Counter
import re
import os.path

#from https://mathiasbynens.be/demo/url-regex diego's one
VALID_URL= re.compile(r"^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\\x{00a1}\-\\x{ffff}0-9]+-?)*[a-z\\x{00a1}\-\\x{ffff}0-9]+)(?:\.(?:[a-z\\x{00a1}\-\\x{ffff}0-9]+-?)*[a-z\\x{00a1}\-\\x{ffff}0-9]+)*(?:\.(?:[a-z\\x{00a1}\-\\x{ffff}]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$")

VALID_FILENAME = re.compile(r'^[a-z\/][a-z0-9_\-/\.]+\.[a-z]{1,5}$')

def lint(post, test_info, config):
    "Check the frontmatter of a given post for potential errors"
    
    results = []

    # Testing is meta exists otherwise bailout
    if post.meta == None:
        results.append(['E100', test_info['E100']])
        return results
    # Run metas tests
    tests = [
        e101_mandatory_fields,
        e102_mandatory_fields_for_specific_templates,
        e103_field_value,
        e104_duplicate_value,
        e105_category_in_tags,
        e106_duplicate_spaces,
        e107_e108_e109_authors_formating,
        e110_lowercase_fields,
        e111_e112_local_files_exists,
        e113_e114_e115_banner_properly_formated,
        e116_value_not_null
    ]
    for test in tests:
        results += test(post, test_info, config)

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
            info = test_info['E105'] %  (post.meta.category, " ,".join(post.meta.tags))
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
                    info = test_info['E106'] %  (field, elt)
                    results.append(['E106', info])
    return results

def e107_e108_e109_authors_formating(post, test_info, config):
    "Check if the authors list is properly formatted"
    results = []
    
    if not "authors" in post.meta:
        return results
    
    authors = post.meta.authors
    if not isinstance(authors, list):
        info = test_info['E107'] % authors
        results.append(['E107', authors])
        return results

    for author in authors:
        if ',' not in author:
            info = test_info['E108'] % authors
            results.append(['E108', info])
        if not author.istitle():
            info = test_info['E109'] % authors
            results.append(['E109', author])
    return results

def e110_lowercase_fields(post, test_info, config):
    "Check that field values are indeed lowercase"
    results = []
    for field in config.frontmatter_field_values_must_be_lowercase:
        if field in post.meta:
            value = post.meta[field]
            if not isinstance(value, list):
                value = [value]
            for elt in value:
                if isinstance(elt, str):
                    if not elt.islower():
                        info = test_info['E110'] % (field, elt)
                        results.append(['E110', info])
    return results

def e111_e112_local_files_exists(post, test_info, config):
    "check if local files exists"
    results = []
    site_dir = config.site_output_dir
    if "files" in post.meta:
        if not isinstance(post.meta.files, dict):
            info = test_info['E112'] % (type(post.meta.files))
            results.append(['E112', info])
            return results

        for fname, fpath  in post.meta.files.items():
            if fpath[0] == '/':
                full_path = os.path.join(site_dir, fpath[1:])
                if not os.path.isfile(full_path):
                    info = test_info['E111'] % (fname, full_path)
                    results.append(['E111', info])
    return results

def e113_e114_e115_banner_properly_formated(post, test_info, config):
    "Ensure the banner is properly formated"
    results = []

    if not "banner" in post.meta:
        return results
    
    banner = post.meta.banner
    if not isinstance(banner, str):
        info = test_info['E113'] % (type(banner))
        results.append(['E113', info])
        return results
    
    if "http" in banner[:6]:
        if not VALID_URL.match(banner):
            info = test_info['E114'] % (banner)
            results.append(['E114', info])
    else:
        if not VALID_FILENAME.match(banner):
            info = test_info['E115'] % (banner)
            results.append(['E115', info])
    
    return results

def e116_value_not_null(post, test_info, config):
    "Ensure the field value are not null"
    results = []
    for field in post.meta:
        if post.meta[field] == None:
            info = test_info['E116'] % (field)
            results.append(['E116', info])
    return results
# URL validity