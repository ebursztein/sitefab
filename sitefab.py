#!/usr/bin/python  
""" 
SiteFab take content in, output static site
"""
import sys
import getopt

from SiteFab.SiteFab import SiteFab
from termcolor import colored, cprint
from SiteFab.utils import print_color_list, section, print_header

def print_plugins_list(site, only_enable=True):
    "Output the list of plugins"
    lst = []
    for pl in site.plugins.get_plugin_info():
        if only_enable:
            if pl[3]:
                lst.append("%s/%s: %s"% (pl[0], pl[1], pl[2]))
        else:
            if pl[3]:
                status = colored("enable", 'green')
            else:
                status = colored("disable", 'red')

            lst.append("[%s] %s/%s: %s"% (status, pl[0], pl[1], pl[2]))
    lst.sort()
    print_color_list(lst)

def generate(config):
    "generate command main function"
    section("Init")
    # initializing site
    site = SiteFab(config)

    cprint("Directories", 'magenta')
    dirs = []
    dirs.append("Ouput:\t%s" % site.get_output_dir())
    dirs.append("Logs:\t\t%s" % site.get_logs_dir())
    dirs.append("Content:\t%s" % site.get_content_dir())
    dirs.append("Template:\t%s" % site.get_template_dir())
    dirs.append("Plugins:\t%s" % site.get_plugins_dir())
    print_color_list(dirs)
    print "\n"
    cprint("Active plugins", 'magenta')
    print_plugins_list(site)

    section("Parsing")
    # loading up the posts
    site.parse()

    #FIXME all the data processing -- Image, Related blog post etc
    section("Processing")
    site.process()

    section("Rendering")
    site.render()
    # Generate auxiliary files (sitemap, facebook_instant etc)
    #FIXME Cleanup the output
    section("Summary")
    site.finale()

def print_help():
    "Display help and exist"
    
    cmds = [
        "generate: generate the site", 
        "deploy: deploy generated site to remote server",
        "plugins: list available plugins"
        ]

    cprint("usage: SiteFab -c <config_file> -s <site_vars_file> command", 'yellow')
    cprint("commands", 'magenta')
    print_color_list(cmds)
    sys.exit(2)

if __name__ == '__main__':
    config = "sitefab.yaml"

    print_header()

    # args parsing
    short_options = "c:h"
    long_options = ["config=","help"]
    try:
        options, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError:
        displat_help()

    # options
    for opt, arg in options:
        if opt in ('-c', '--config'):
            config = arg
        elif opt in ('-h', '--help'):
            print_help()
    
    # arguments
    if len(args):
        cmd = args[0]
        if cmd == "generate":
            generate(config)
        elif cmd == "plugins":
            site = SiteFab(config)
            cprint("Plugins status", 'magenta')
            print_plugins_list(site, only_enable=False)
        else:
            print_help()
    else:
        print_help()