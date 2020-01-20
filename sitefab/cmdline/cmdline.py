# coding: utf-8
"""
SiteFab: content > sitefab > static site
"""
import sys
import getopt
from collections import defaultdict

from sitefab import __version__ as version
from sitefab.SiteFab import SiteFab
from termcolor import colored, cprint
from sitefab.utils import print_color_list, section, print_header
from sitefab.docs.plugins import generate_plugins_readme


def print_plugins_list(site, only_enable=True):
    "Output the list of plugins"
    info = defaultdict(lambda: defaultdict(list))
    categories = ['Collection', 'Post', 'Site']
    phases = ['Preparsing', 'Parsing', 'Processor', 'Rendering']

    for pl in site.plugins.get_plugins_info():
        cat = pl[0]
        name = pl[1]
        status = pl[3]
        desc = pl[2]
        version = pl[5]

        if only_enable:
            if not status:
                continue
            status = ""
        else:
            if status:
                status = colored("[enable]  ", 'green')
            else:
                status = colored("[disable] ", 'red')

        s = "%-20s (%s):\t %s" % (name, version, desc)

        for category in categories:
            if category in cat:
                phase = cat.replace(category, "")
                info[category][phase].append([status, s])

    for category, data in info.items():
        print(colored("[%s]" % category, 'yellow'))
        for phase in phases:
            if len(data[phase]):
                print(colored("  %s" % phase, 'magenta'))
                count = 0
                for plugin in data[phase]:
                    if count % 2:
                        plugin[1] = colored(plugin[1], 'blue')
                    else:
                        plugin[1] = colored(plugin[1], 'cyan')
                    print("    |-%s%s" % (plugin[0], plugin[1]))
                    count += 1
        print("\n")


def generate(config, version):
    "generate command main function"
    section("Init")
    # initializing site
    site = SiteFab(config, version)
    cprint("Directories", 'magenta')
    dirs = []
    dirs.append("Ouput:\t%s" % site.get_output_dir())
    dirs.append("Logs:\t\t%s" % site.get_logs_dir())
    dirs.append("Content:\t%s" % site.get_content_dir())
    dirs.append("Template:\t%s" % site.get_template_dir())
    dirs.append("Plugins:\t%s" % site.get_plugins_dirs())
    dirs.append("Cache:\t%s" % site.get_cache_dir())
    print_color_list(dirs)
    print("\n")
    cprint("Active plugins", 'magenta')
    print_plugins_list(site)

    section("Pre processing")
    site.preprocessing()
    # parsing content into post objects
    section("Parsing")
    site.parse()

    # processing posts and collections to add extra info
    section("Processing")
    site.process()

    section("Rendering")
    site.render()
    # Generate auxiliary files (sitemap, facebook_instant etc)
    # FIXME Cleanup the output
    section("Summary")
    site.finale()


def print_help():
    "Display help and exist"

    cprint("Usage: sitefab -c <config_file> command", 'yellow')

    # end user
    cmds = [
        "generate: generate the site",
        "plugins: list available plugins",
        ]

    cprint("Available Commands", 'magenta')
    print_color_list(cmds, prefix="\t")

    # dev
    #  dev_cmds = [
    #     "gen_plugins_readme: generate plugins README.md from plugins infos",
    # ]
    # cprint("Developper command", 'blue')
    # print_color_list(dev_cmds, prefix="\t")

    sys.exit(2)


def main():
    config = None
    short_options = "c:h:o:"
    long_options = ["config=", "help", "output_file="]

    # pretty banner
    print_header(version)

    # parsing
    try:
        options, args = getopt.getopt(sys.argv[1:], short_options,
                                      long_options)
    except getopt.GetoptError:
        print_help()

    # options
    for opt, arg in options:
        if opt in ('-c', '--config'):
            config = arg
        elif opt in ('-h', '--help'):
            print_help()
        elif opt in ('-o', '--output_file'):
            # used for documentation generation
            output_fname = arg
    # arguments
    if len(args):
        cmd = args[0]

        if not config:
            cprint('[ERROR] Please provide a config file via the -c option',
                   'red')
            print_help()

        if cmd == "generate":
            generate(config, version)

        elif cmd == "plugins":
            site = SiteFab(config)
            cprint("Plugins status", 'magenta')
            print_plugins_list(site, only_enable=False)

        # doc command
        elif cmd == "gen_plugins_readme":
            # this function rebuild the plugin readme
            site = SiteFab(config, version)
            generate_plugins_readme(site, output_fname)

        else:
            print_help()
    else:
        print_help()


if __name__ == '__main__':
    main()
