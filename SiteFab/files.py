import yaml
import fnmatch
import codecs
import os
import shutil

#from utils.objdict import objdict
import utils as utils

def get_code_path():
    "Get SiteFab base directory path"
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def get_site_path():
    "Get website base path"
    return os.getcwd()

def load_config(config_file):
    """ Load yaml configuration 
    
    Args:
        config_file (str): The path to the config file to load.

    Return:
        objdict: configuration file parsed as dict or empty if parsing fail
    """
    with open(config_file, 'r') as stream:
        try:
            config_yaml = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
    
    # Making it a nice object
    config = utils.create_objdict(config_yaml)    
    return config

cached_files = {}
def read_file(filename, cache=True):
    """Read a file and return its content. Use cached version unless specified.
    
    :params str filename: the filename to read from
    :params book cache: caching/reading result from cache?
    
    """
    
    if cache and filename in cached_files:
        return cached_files[filename]
    
    if os.path.isfile(filename):
        content = open(filename).read()
        if cache:
            cached_files[filename] = content
        return content 
    else:
        utils.warning("file:%s don't exist" % filename)
        return ""

def write_file(path, filename, content):
    """ Write a file at a given path. Create directory if necessary

    Args:

    Returns
    """
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, filename)
    with codecs.open(file_path, "w", "utf-8-sig") as f:
        f.write(content)

def get_content_files_list(content_dir):
    """ Return the list of content file available in a directory.
       Args:
        content_dir (str): file path where content is located.
    Return:
        list: list of content filename.
    """
    matches = []
    for root, dirnames, filenames in os.walk(content_dir):
        for filename in fnmatch.filter(filenames, '*.md'):
            matches.append(os.path.join(root, filename))
    return matches

def clean_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory) 