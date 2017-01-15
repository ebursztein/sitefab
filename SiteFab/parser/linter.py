import yaml
import re

import frontmatter
from collections import defaultdict
from SiteFab import utils
from SiteFab import files

VALID_URL_CHARS = '[^a-z0-9_\-:/\.]'
VALID_PERMA_CHARS = '[^a-z0-9-\/\.]'
VALID_TEXT_CHARS = '[^a-zA-Z0-9,;\. ]'

def _url_exist(url):

    ## for unit test
    if "mock_url_exist" in url:
        return True
    if "mock_url_not_exist" in url:
        return False

    import requests

    request = requests.get(url)
    if request.status_code == 200:
        return True
    return False

def _is_publication(post):
    if post.meta and "type" in post.meta and post.meta.type == "publication":
        return True
    return False

def _is_blogpost(post):
    if post.meta and "type" in post.meta and post.meta.type == "post":
        return True
    return False


def count_errors(errors):
    """ Return the number of errors found"""
    count = 0
    for k,v in errors.iteritems():
        if v:
            count += len(v)
    return count


def has_errors(post, config_file):
    """ Validate that the post structure and meta is okay
    
    This function is used at upload time as a mini lint that
    ensure that at least all the fields are corrects and no 
    site breaking content would be uploaded.

    used check_meta and check_structure

    @return: True is valid, return array of errors
    """

    errors = objdict()
    config = load_config(config_file)
    if not config:
        errors['config']["config file not found"]
        return errors

    errors = objdict()
    errors.frontmatter = check_frontmatter(post, config)
    errors.structure = check_structure(post, config)

    if count_errors(errors):
        return errors
    return None
    
    

def lint(post, config_file="linter_config.yaml", online_checks=False, check_content=False):
    """ Check the post for various errors.
    @param online_check: perform online check. E.g test for URL existence. Off by default
    @param check_content: use language tool to check the content against common mistake. Off by default
    @return None if no errors, errors object otherwise
    """
    config = load_config(config_file)
    if not config:
        return None
    
    errors = utils.dict_to_objdict()
    errors.frontmatter = check_frontmatter(post, config)
    errors.structure = check_structure(post, config)
    errors.seo = check_seo(post, config)    
    
    if online_checks:
        errors.links = check_links(post, config)
    else:
        errors.links = []
    if check_content:
        check_post_content(post, config)
   
    if count_errors(errors):
        return errors
    return None


def check_frontmatter(post, config):
    """ Ensure that every mandatory fields are set"""
    errors = []
    IS_PUBLICATION = _is_publication(post)
    IS_BLOGPOST = _is_blogpost(post)

    if post.meta == None:
        errors.append(['E110',()])
        return errors
    
    # mandatory fields checking
    mandatory_fields = config['frontmatter_mandatory_fields']
    # adding the publication fields if needed
    if "type" in post.meta and post.meta.type == "publication":
        mandatory_fields.update(config['publication_mandatory_field'])
    optional_fields = config['frontmatter_optional_fields']
    authorized_fields = mandatory_fields.copy() 
    authorized_fields.update(optional_fields)

    for field_name, field_value in post.meta.iteritems():
        # date format
        if field_name == "creation_date" or field_name == "update_date":
            ts = frontmatter.parse_date_to_ts(field_value)
            if not ts:
                errors.append(['E105',(field_name, field_value)])
        # check for unspecified fields
        if field_name not in authorized_fields:
            errors.append(['E106', (field_name)])
        
        ### Tags related tests ###
        if field_name == "tags":
            # tags are an array
            if type(field_value) != list:
                errors.append(['E107', (field_value, type(field_value))])
            else:
                for v in field_value:
                    if not v.islower():
                       errors.append(['E109', (v)]) 

        if field_name == "seo_keywords":
            if type(field_value) != list:
                errors.append(['E108', (field_value, type(field_value))])
            else:
                for v in field_value:
                    if not v.islower():
                       errors.append(['E111', (v)]) 

        if field_name == 'banner':
            if "https://www.elie.net/image/public/" not in field_value:
                errors.append(['E112', (field_value)])
            if "?" in field_value or "%3F" in field_value:
                errors.append(['E114', (field_value)])
            if re.search(VALID_URL_CHARS, field_value):
                errors.append(['E115', (field_value)])
    
        if field_name == "permanent_url":
            if re.search(VALID_PERMA_CHARS, field_value):
                errors.append(['E116', (field_value)])
            if IS_BLOGPOST and post.meta.category not in field_value:
                errors.append(['E117', (field_value)])

        if field_name == "authors":
            for author in field_value:
                if ',' not in author:
                    errors.append(['E118', (author)])
                for t in author.split(","):
                    t = t.strip()
                    if not t[0].strip().isupper():
                        errors.append(['E119', (author)])
        
        if field_name == "files":
            if type(field_value) != dict:
                errors.append(['E120', (type(field_value))])
            else:
                for url in field_value.itervalues():
                    if re.search(VALID_URL_CHARS, url):
                        errors.append(['E121', (url)])
        
        if field_name == "abstract":
            if  field_value and re.search(VALID_TEXT_CHARS, field_value):
                errors.append(['E122', (field_value)])
        
        if field_name == "title":
            if field_value and re.search(VALID_TEXT_CHARS, field_value):
                errors.append(['E123', (field_value)])

    # check for mandatory fields
    for field_name, field_expected_values in mandatory_fields.iteritems():        
        if field_name not in post.meta:
            errors.append(['E101', (field_name)])
        else:
            field_value = post.meta[field_name]
            if field_expected_values: #testing the value
                if field_value not in field_expected_values:
                    errors.append(['E102', (field_name, field_value)])
            else:
                if not field_value:
                    errors.append(['E103', (field_name)]) 
                elif type(field_value) == str and len(field_value) < 3:
                    errors.append(['E104', (field_name, field_value)])
    
    #FIXME: Test that the abstract end with a period and is capitalized.
    return errors

def check_structure(post, config):
    """Check that the structure of the post is correct"""
    errors = []
    IS_PUBLICATION = _is_publication(post)

    ### TOC analysis ###
    toc = post.info.toc
    toc_per_level = defaultdict(list)
    for elt in post.info.toc:
        txt, level, index = elt
        toc_per_level[level].append(txt.lower())
    
    # H1 present
    if 1 in toc_per_level:
        errors.append(['E201',(toc_per_level[1])])

    # no H2 present in the structure
    if 2 not in toc_per_level and not IS_PUBLICATION:
        errors.append(['E204', ()])

    # check for duplicate
    for level, headers in toc_per_level.iteritems():
        if len(headers) != len(set(headers)):
            errors.append(['E205', (level, headers)])
    
    for img in post.info.images:
        if "https://www.elie.net/image/public/" not in img:
            errors.append(['E206', (img)])
        if "?" in img or "%3F" in img:
            errors.append(['E207', (img)])
        if re.search(VALID_URL_CHARS, img):
            errors.append(['E208', (img)])



    return errors

def check_links(post, config):
    """perform check on the links"""
    errors = []
    
    #print post.info

    CATEGORIES = {
        'links':  ['E301', 'W304'],
        'images': ['E302', 'W305'],
        'videos': ['E303', 'W306'],
    }

    ''' Testing if the link exists '''
    for cat, error_ids in CATEGORIES.iteritems():
        error_id = error_ids[0]
        for link in set(post.info[cat]):
            exist = _url_exist(link)
            if not exist:
                errors.append([error_id, (link)])

    '''Check if the links are duplicated'''
    for cat, error_ids in CATEGORIES.iteritems():
        error_id = error_ids[1]
        lst = post.info[cat]
        if len(lst) != len(set(lst)):
            errors.append([error_id, (link)])

    '''Checking files URL if needed'''
    if post.meta and "files" in post.meta:
        if type(post.meta.files) == dict:
            for link in post.meta.files.itervalues():
                exist = _url_exist(link)
                if not exist:
                    errors.append(['E307', (link)])

    '''Check  files URL if needed'''
    if post.meta and "banner" in post.meta:
        exist = _url_exist(post.meta.banner)
        if not exist:
            errors.append(['E308', (post.meta.banner)])

    #FIXME check for link, video, images existence  - check banner as well

    return errors

def check_post_content(post, config, language='en-US'):
    """Check content for style potential errors """
    errors = []
    #FIXME check abstract content as well

    import language_check
    lc = language_check.LanguageTool(language)
    txt = unicode(post.md, "utf-8")
    results = lc.check(txt)
    if len(results):
        # online display
        print "=== Content ==="
        
        for e in results:
            start = e.offset
            stop = start + e.errorlength
            word = txt[start:stop]
            #print word
            if word not in config['word_whitelist']:
                try:
                    print e
                except:
                    continue
    return errors
def check_seo(post, config):
    errors = []
    # FIXME: check abstract length

    if post.meta and "permanent_url" in post.meta and "banner" in post.meta:
        if "/" in post.meta.permanent_url:
            stub = post.meta.permanent_url.split('/')[1]
        else:
            stub = post.meta.permanent_url
        img = post.meta.banner.split('/')[-1].replace(".png", '').replace('.jpg', '')
        if stub != img:
                 errors.append(['E401', (stub, img)])

    if post.meta and "title" in post.meta and post.meta.title:
        l = len(post.meta.title)
        if l < 40:
            errors.append(['W402',(l, post.meta.title) ])
        if l > 70:
            errors.append(['W403',(l, post.meta.title) ])

    if post.meta and "abstract" in post.meta and post.meta.abstract:
        l = len(post.meta.abstract)
        if l > 156:
            errors.append(['W404',(l, post.meta.abstract) ])

    return errors


def load_config(config_file):
    """ Load linter configuration """
    config = None
    stream = files.read_file(config_file)
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
    return config

def format_errors(results, config_file):
    config = load_config(config_file)
    if not config:
        return None
    buffer = ""
    for cat, errors in results.iteritems():
        if not errors:
            continue
        buffer += '<div><div class="details_section"> %s</div>' % cat
        buffer += "<table><tr><th>Severity</th><th>ErrID</th><th>Description</th></tr>"
        for error in errors:
            idx = error[0]
            params = error[1]
            description = config['errors'][idx]['description'] % (params)
            fix = config['errors'][idx]['fix']
            if idx[0] == 'E':
                severity = "Error"
            elif idx[0] == "W":
                severity = "Warning"
            elif idx[0] == "I":
                severity = "Info" 
            else:
                severity = "Unknown"
            #idx_n = int(id[1])
            #category = config['error_categories'][idx_n]
            s = "<tr><td>%s</td><td>%s</td><td>%s - %s</td></tr>" % (severity, idx, description, fix)
            buffer += s
        buffer += "</table></div>"
    return buffer