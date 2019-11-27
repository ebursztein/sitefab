import yaml
import fnmatch
import codecs
import os
import shutil

from . import utils as utils


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

    Returns:
        objdict: configuration file parsed as dict or empty if parsing fail
    """

    # open file
    if not os.path.exists(config_file):
        st = "%s does not exist" % config_file
        utils.warning(st)
        return None
    stream = open(config_file, 'r')

    # parse  yaml
    try:
        config_yaml = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        return None

    # Making config a nice object
    config = utils.dict_to_objdict(config_yaml)
    return config


def read_file(filename):
    """Read a file and return its content. Use cached version unless specified.

    Args:
        filename (str): the filename to read from

    Returns:
        str: the content of the file
    """

    if os.path.isfile(filename):
        f = codecs.open(filename, "r", "utf-8-sig")
        content = f.read().encode("utf-8")
        f.close()
        return content
    else:
        utils.warning("file:%s don't exist" % filename)
        return ""


def write_file(path, filename, content, binary=False):
    """ Write a file at a given path. Create directory if necessary

    Args:
        binary (bool): write a binary file? default False.

    Returns:
        None: no returns
    """
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, filename)
    if not binary:
        f = codecs.open(file_path, "w", "utf-8-sig")
        f.write(content)
        f.close()
    else:
        f = open(file_path, "wb")
        f.write(content)
        f.close()


def get_files_list(content_dir, extensions="*.md"):
    """ Return the list of files in a directory and its sub directories that
    match a set of extensions.

    Args:
        content_dir (str): file path where content is located.
        extensions(str or list): single extension like "*.md" or array of
        extensions ["*.jpg", "*.png"]

    Returns:
        list: list of content filename.

    Notes:
        matching is done the Usenix file matching way much like ls
    """

    # normalize the input
    if type(extensions) == str:
        extensions = [extensions]

    for ext in extensions:
        if "*." not in ext:
            utils.warning("extension: %s will not match as it is missing .*\
                          somewhere" % ext)

    matches = []
    for root, unused, filenames in os.walk(content_dir):
        for extension in extensions:
            for filename in fnmatch.filter(filenames, extension):
                matches.append(os.path.join(root, filename))
    return matches


def clean_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)
    if os.path.exists(directory):
        utils.error("%s not deleted." % directory)
    os.mkdir(directory)
