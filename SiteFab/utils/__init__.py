import operator
from objdict import objdict
from termcolor import colored, cprint

### colored output ###
def warning(txt):
    cprint("\nWarning:%s\n" % txt, 'red')

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
### Dict to objet ###

def create_objdict(dictionnary=None):
    """ Convert a dict struct into a objdict structure 
    
    Args:
        dictionnary (dict): the dictionnary to convert

    return objdict: the dictionnary converted in objdict
    """
    o = objdict()
    if dictionnary:
        for k, v in dictionnary.iteritems():
            if type(v) == dict:
                o[k] = create_objdict(v)
            else:
                o[k] = v
    return o