"files manipulation utilities"
import codecs
import shutil
from pathlib import Path
from time import sleep

import yaml

from . import utils as utils


def get_code_path():
    """Get SiteFab base directory path

    Note:
        code path is the dir where we have: sitefab, plugins... it's not
        the package root
    """
    path = Path(__file__)
    return(path.parents[1])


def load_config(config_file):
    """ Load yaml configuration

    Args:
        config_file (str): The path to the config file to load.

    Returns:
        objdict: configuration file parsed as dict or empty if parsing fail
    """

    # open file
    config_file = Path(config_file)
    if not config_file.exists:
        st = "%s does not exist" % config_file
        utils.warning(st)
        return None
    stream = open(config_file, 'r')

    # parse  yaml
    try:
        config_yaml = yaml.load(stream, Loader=yaml.SafeLoader)
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

    filename = Path(filename)
    if filename.is_file():
        f = codecs.open(filename, "r", "utf-8-sig")
        content = f.read()
        return content
    else:
        utils.warning("file:%s don't exist" % filename)
        return ""


def write_file(target_path, filename, content, binary=False):
    """ Write a file at a given path. Create directory if necessary

    Args:
        target_path (str): path where to write.
        filename (str): filename to write to.
        content (str or bytes): Content to write
        binary (bool, optional): Write as binary?. Defaults to False.

    Returns:
        None: no returns
    """
    target_path = Path(target_path)

    if not target_path.exists():
        target_path.mkdir(parents=True)

    file_path = target_path / filename
    if not binary:
        f = codecs.open(file_path, "w", "utf-8-sig")
        f.write(content)
        f.close()
    else:
        f = open(file_path, "wb")
        f.write(content)
        f.close()


def get_files_list(content_dir, extensions="*.md", recursive=True):
    """ Return the list of files in a directory and its sub directories that
    match a set of extensions.

    Args:
        content_dir (str): file path where content is located.
        extensions(str or list): single extension like "*.md" or array of
        extensions ["*.jpg", "*.png"]
        rescursive (bool): perform recursive listing

    Returns:
        list: list of content filename.

    Notes:
        matching is done the Usenix file matching way much like ls
    """

    # normalize the input
    if type(extensions) == str:
        extensions = [extensions]

    matches = []
    content_dir = Path(content_dir)
    for extension in extensions:
        if "*." not in extension:
            utils.warning("extension: %s won't match missing '*.'" % extension)
            continue
        if recursive:
            flist = list(content_dir.rglob(extension))
        else:
            flist = list(content_dir.glob(extension))
        matches.extend(flist)

    return matches


def clean_dir(directory):
    """Clean by deleting and recreating the directory

    Args:
        directory (str): Directory to clean.
    """
    directory = Path(directory)
    if directory.exists:
        shutil.rmtree(directory, ignore_errors=True)
        sleep(0.2)  # need time for the filesystem to register deletion
    if directory.exists():
        utils.error("%s not deleted." % directory)
    directory.mkdir()
