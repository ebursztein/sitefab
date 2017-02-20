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
    
    try:
        stream = open(config_file, 'r')
    except:
        st  = "%s does not exist" % config_file
        utils.warning(st)
        return None

    try:
        config_yaml = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        return None
    
    # Making it a nice object
    config = utils.dict_to_objdict(config_yaml)    
    return config

cached_files = {}
def read_file(filename, cache=True):
    """Read a file and return its content. Use cached version unless specified.
    Args:
        filename (str): the filename to read from
        cache (bool): wether or not to read result from cache?
    
    Returns
        str: the content of the file

    """
    
    if cache and filename in cached_files:
        return cached_files[filename]
    
    if os.path.isfile(filename):
        with codecs.open(filename, "r", "utf-8-sig") as f:
            content = f.read().encode("utf-8")
        if cache:
            cached_files[filename] = content
        return content 
    else:
        utils.warning("file:%s don't exist" % filename)
        return ""

def write_file(path, filename, content, binary=False):
    """ Write a file at a given path. Create directory if necessary

    Args:
    binary (bool): write a binary file? default False.

    Returns
    """
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, filename)
    if not binary:
        with codecs.open(file_path, "w", "utf-8-sig") as f:
            f.write(content)
    else:
        f = open(file_path, "wb")
        f.write(content)
        f.close()

def get_files_list(content_dir, extensions="*.md"):
    """ Return the list of files in a directory and its sub directories that match a set of extensions.
       Args:
        content_dir (str): file path where content is located.
        extensions(str or list): single extension like "*.md" or array of extensions ["*.jpg", "*.png"]
    Return:
        list: list of content filename.

    Note: matching is done the Usenix file matching way much like ls 
    """

    # normalize the input
    if type(extensions) == str:
        extensions = [extensions]

    for ext in extensions:
        if "*." not in ext:
            utils.warning("extension: %s will not match as it is missing .* somewhere" % ext)

    matches = []
    for root, dirnames, filenames in os.walk(content_dir):
        for extension in extensions:
            for filename in fnmatch.filter(filenames, extension):
                matches.append(os.path.join(root, filename))
    return matches

def clean_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory) 