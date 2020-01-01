import sys
import xxhash

from .objdict import objdict
from termcolor import cprint


# hashing
def hexdigest(w):
    # xxhash is 3x/5x faster than md5
    return xxhash.xxh64(w).hexdigest()


# [colored output] #
def warning(txt):
    cprint("\n[Warning] %s\n" % txt, 'yellow')


def error(error_msg):
    cprint("\n[Error] %s" % error_msg, 'red')
    raise Exception(error_msg)


def detailed_error(module, function, error_msg):
    """ Display detail error and exit

    Args:
        module (str): the module where the error occured
        function (str): the function that triggred the errror message
        error_msg (str): the error message to display

    Return:
        None
    """
    msg = "\n[Error] %s:%s: %s\n" % (module, function, error_msg)
    cprint(msg)
    sys.exit(-42)


def section(val):
    cprint("\n[%s]" % val, 'yellow')


def print_color_list(lst, prefix='|-'):
    count = 0
    for i in lst:
        if count % 2:
            color = 'blue'
        else:
            color = 'cyan'
        st = "%s%s" % (prefix, i)
        cprint(st, color)
        count += 1


# [Object dict]
def create_objdict(dictionnary=None):
    "Create a an empty objdict object"
    if dictionnary:
        return dict_to_objdict(dictionnary)
    else:
        return objdict()


def dict_to_objdict(dictionnary=None):
    """ Convert a dict struct into a objdict structure

    Args:
        dictionnary (dict): the dictionnary to convert

    Returns:
        objdict: the dictionnary converted in objdict
    """
    o = objdict()
    if dictionnary:
        for k, v in dictionnary.items():
            if type(v) == dict:
                o[k] = dict_to_objdict(v)
            else:
                o[k] = v
    return o


def objdict_to_dict(objdict):
    """ Convert an objdict structure into a dict structure

    Args:
        obj (objdict): the objdict to convert

    Returns:
        dict: the objdict as standard dictionnary
    """
    d = {}
    if objdict:
        for k, v in objdict.items():
            if type(v) == dict:
                d[k] = objdict_to_dict(v)
            else:
                d[k] = v
    return d


def print_header(version):
        cprint('''
 ad88888ba   88                      88888888888          88
d8"     "8b  ""    ,d                88                   88
Y8,                88                88                   88
`Y8aaaaa,    88  MM88MMM  ,adPPYba,  88aaaaa  ,adPPYYba,  88,dPPYba,
  `"""""8b,  88    88    a8P_____88  88"""""  ""     `Y8  88P'    "8a
        `8b  88    88    8PP"""""""  88       ,adPPPPP88  88       d8
Y8a     a8P  88    88,   "8b,   ,aa  88       88,    ,88  88b,   ,a8"
 "Y88888P"   88    "Y888  `"Ybbd8"'  88       `"8bbdP"Y8  8Y"Ybbd8"'   v: %s
        ''' % version, "blue")
        cprint('''              -= https://github.com/ebursztein/sitefab =-
        ''', "cyan")
