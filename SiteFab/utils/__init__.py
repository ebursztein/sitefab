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

def print_header():
        cprint('''
                                                                       
 ad88888ba   88                      88888888888          88           
d8"     "8b  ""    ,d                88                   88           
Y8,                88                88                   88           
`Y8aaaaa,    88  MM88MMM  ,adPPYba,  88aaaaa  ,adPPYYba,  88,dPPYba,   
  `"""""8b,  88    88    a8P_____88  88"""""  ""     `Y8  88P'    "8a  
        `8b  88    88    8PP"""""""  88       ,adPPPPP88  88       d8  
Y8a     a8P  88    88,   "8b,   ,aa  88       88,    ,88  88b,   ,a8"  
 "Y88888P"   88    "Y888  `"Ybbd8"'  88       `"8bbdP"Y8  8Y"Ybbd8"'   
                                                                       
        ''', "blue")
        cprint('''             
                -= https://github.com/ebursztein/SiteFab =-                                                                                     
        ''', "cyan")