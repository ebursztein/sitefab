import sys
import operator
import re
import hashlib
import xxhash
from stop_words import get_stop_words

from objdict import objdict
from termcolor import colored, cprint


# hashing
def hexdigest(w):
    return xxhash.xxh64(w).hexdigest()
    #return hashlib.md5(w).hexdigest() < too slow was like 3x to 5x what xxhash is

# image
def get_img_extension_alternative_naming(extension):
    "Return extensions naming for PIL and Mime/type"
    web_extension = None
    pil_extension_codename = None

    if extension.lower() == ".jpg" or extension.lower() == ".jpeg":
        pil_extension_codename = "JPEG"
        web_extension = "image/jpeg"

    elif extension.lower() == ".png":
        pil_extension_codename = "PNG"
        web_extension = "image/png"

    elif extension.lower() == ".gif":
        pil_extension_codename = "GIF"
        web_extension = "image/gif"

    elif extension.lower() == ".webp":
        pil_extension_codename = "WEBP"
        web_extension = "image/webp"

    return [pil_extension_codename, web_extension]


### colored output ###
def warning(txt):
    cprint("\n[Warning] %s\n" % txt, 'yellow')

def error(error_msg):
    cprint("\n[Error] %s" % error_msg, 'red')
    sys.exit(-1)

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
    cprint ("\n[%s]" % val, 'yellow')

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

### Object dict ###
def create_objdict():
    "Create a an empty objdict object"
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
        for k, v in dictionnary.iteritems():
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
        for k, v in objdict.iteritems():
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
        cprint('''              -= https://github.com/ebursztein/SiteFab =-
        ''', "cyan")