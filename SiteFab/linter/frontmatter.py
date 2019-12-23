# encoding: utf-8
from collections import Counter
import re
import os

# from https://mathiasbynens.be/demo/url-regex diego's one
VALID_URL = re.compile(r"^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\\x{00a1}\-\\x{ffff}0-9]+-?)*[a-z\\x{00a1}\-\\x{ffff}0-9]+)(?:\.(?:[a-z\\x{00a1}\-\\x{ffff}0-9]+-?)*[a-z\\x{00a1}\-\\x{ffff}0-9]+)*(?:\.(?:[a-z\\x{00a1}\-\\x{ffff}]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$")  # noqa

VALID_LOCAL_URL = re.compile(r"^/?[a-z0-9\/_\.\-=\?]+$")

VALID_FILENAME = re.compile(r'^[a-z\/][a-z0-9_\-/\.]+\.[a-z]{1,5}$')


def lint(post, test_info, config):
    "Check the frontmatter of a given post for potential errors"

    results = []

    # Testing is meta exists otherwise bailout
    if not post.meta:
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
        e116_value_not_null,
        e117_e118_e119_permanent_url_is_properly_formated,
        e120_valid_permanent_url_prefix,
        e121_file_properly_named,
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
        for field in config.frontmatter_mandatory_fields_by_templates[post.meta.template]:  # noqa
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
                info = test_info['E103'] % (
                    field, post.meta[field],
                    config.frontmatter_fields_value[field])
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
                except:  # noqa
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

        if post.meta.tags and post.meta.category in post.meta.tags:
            info = test_info['E105'] % (
                post.meta.category, " ,".join(post.meta.tags))
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
                extra_space = re.search(" {2,}", elt)
                if extra_space:
                    info = test_info['E106'] % (field, elt)
                    results.append(['E106', info])
    return results


def e107_e108_e109_authors_formating(post, test_info, config):
    "Check if the authors list is properly formatted"
    results = []

    if "authors" not in post.meta:
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
        else:
            firstname, lastname = author.replace(' ', '').split(',')
            if not firstname[0].isupper() or not lastname[0].isupper():
                info = test_info['E109'] % firstname
                results.append(['E109', info])
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

        for fname, fpath in post.meta.files.items():
            if fpath[0] == '/':
                full_path = os.path.join(site_dir, fpath[1:])
                if not os.path.isfile(full_path):
                    info = test_info['E111'] % (fname, full_path)
                    results.append(['E111', info])
    return results


def e113_e114_e115_banner_properly_formated(post, test_info, config):
    "Ensure the banner is properly formated"
    results = []

    if "banner" not in post.meta:
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
    WHITELIST = ['toc', 'statistics', 'elements']  # those are generated
    results = []
    for field in post.meta:
        if field in WHITELIST:
            continue
        if not post.meta[field]:
            info = test_info['E116'] % (field)
            results.append(['E116', info])
    return results


def e117_e118_e119_permanent_url_is_properly_formated(post, test_info, config):
    results = []

    if "permanent_url" not in post.meta:
        return results

    url = post.meta.permanent_url
    if not isinstance(url, str):
        info = test_info['E117'] % (type(url))
        results.append(['E117', info])
        return results

    if ((url != "" and not VALID_URL.match(url)) and
            (not VALID_LOCAL_URL.match(url))):
        info = test_info['E118'] % (url)
        results.append(['E118', info])

    if len(url) and url[0] != '/':
        info = test_info['E119'] % (url)
        results.append(['E119', info])

    return results


def e120_valid_permanent_url_prefix(post, test_info, config):
    "Check if the permanent url has a valid template based of its prefix"
    results = []

    if "template" not in post.meta or "permanent_url" not in post.meta:
        return results

    tlp = post.meta.template
    if tlp not in config.permanent_url_valid_prefixes_by_template:
        return results

    prefix = config.permanent_url_valid_prefixes_by_template[tlp]
    permanent_url = str(post.meta.permanent_url)
    if not permanent_url.startswith(prefix):
        info = test_info['E120'] % (permanent_url, prefix)
        results.append(['E120', info])

    return results


def e121_file_properly_named(post, test_info, config):
    "Check if the files are properly named"
    results = []
    # test if it contains -slides.pdf or -paper.pdf
    # test it contains the name of the short url (see rename tools)
    if "files" not in post.meta or not isinstance(post.meta.files, dict):
        return results

    for t, f in post.meta.files.items():
        # valid type
        if t not in config.files.valid_types:
            info = test_info['E121'] % (t)
            results.append(['E121', info])

        # valid characters
        if not VALID_URL.match(f) and not VALID_LOCAL_URL.match(f):
            info = test_info['E122'] % (f)
            results.append(['E122', info])

        # valid prefix
        valid = False
        for prefix in config.files.valid_prefixes:
            if f.startswith(prefix):
                valid = True
        if not valid:
            info = test_info['E123'] % (
                f, " ,".join(config.files.valid_prefixes))
            results.append(['E123', info])

        # valid suffix
        valid = False
        for suffix in config.files.valid_suffixes:
            if f.endswith(suffix):
                valid = True
        if not valid and not f.startswith("http"):
            info = test_info['E124'] % (
                f, " ,".join(config.files.valid_suffixes))
            results.append(['E124', info])

    return results
