import jinja2
import  os

import fb
import frontmatter
import linter
import markdown
from markdown import HTMLRenderer
import json

import mistune
from mistune import Renderer

from pygments.formatters import html


from SiteFab import utils
from SiteFab import files

def parse_post((filename, parser_config)):
    file_content = files.read_file(filename)
    cfg = utils.dict_to_objdict(parser_config)
    parser = Parser(cfg)
    post = parser.parse(file_content)
    post.filename = filename
    d = utils.objdict_to_dict(post)
    return json.dumps(d)

class Parser():
    
    def __init__(self, config):
        """ Initialize a new parser for a given type of parsing

        Args:
            config (dictobj): parser configuration        
        Return:
            None

        note: one parser is instanciated by thread. potentially batching more than one post per thread might help with performance.

        """
        
        # verify that the config exist
        self.config = config

        #Loadings template strings in memory so we can manipulate them
        self.templates = {}
        for fname in files.get_files_list(self.config.templates_path, "*.html"):
            template_name = os.path.basename(fname).replace(".html", "")
            template = files.read_file(fname)
            #print "%s -> %s" % (template_name, template)
            self.templates[template_name] = template

        # Replacing standard template with the one injected by plugins
        for elt, template in config.injected_html_templates.iteritems():
            self.templates[elt] = template
            
        # templates are not compiled yet, they will be when parsing will be called the first time 
        self.jinja2 = None 

        # markdown parser
        self.renderer = HTMLRenderer()
        self.md_parser = mistune.Markdown(renderer=self.renderer)
    
        #code higlighterr
        if self.config.code_display_line_num:
            linenos = 'table'
        else:
            linenos = False
        
        self.code_formatter = html.HtmlFormatter(style=self.config.code_highlighting_theme, nobackground=False, linenos=linenos)

    @staticmethod
    def make_config(config):
        """ Initialize a parser config with all the needed variables

        Args:
            config (obj_dict): the uninitialized configuration with basic variable
        Returns:
            obj_dict: The initialized configuration
        """

        if config == None:
            utils.detailed_error("Parser", 'make_config', 'supplied config is empty')

        if 'template_dir' not in config:
            utils.detailed_error("Parser", 'make_config', 'template_dir not found')

        config.templates_path =  os.path.join(files.get_site_path(),  config.template_dir)
        config.injected_html_templates = {} # Used to allows plugins to dynamically inject html templates.
        config.injected_html_templates_owner = {} # store who was responsible for the injection
        config.plugin_data = {} # store plugin data that need to be passed to the parser. E.g resized images
        return config

    def list_templates(self):
        "Return the list of available templates"
        return self.templates.keys()

    
    def parse(self, md_file):
        """ Parse a md file into a post object
        """
        
        # compile the templates when we parse the first post. This is needed to ensure that
        # plugins get a chance to modify the templates before we compile them. 
        if not self.jinja2:
            self.jinja2 = jinja2.Environment(loader=jinja2.DictLoader(self.templates))

        parsed_post = utils.dict_to_objdict()

        # parsing frontmatter and getting the md
        parsed_post.meta, parsed_post.md = frontmatter.parse(md_file)

        # parsing markdown and extractring info
        self.renderer.init(self.jinja2, self.code_formatter, self.config.plugin_data)

        parsed_post.html = self.md_parser.parse(parsed_post.md)
        parsed_post.meta.statistics = self.renderer.get_stats()
        parsed_post.meta.toc = self.renderer.get_json_toc()
        parsed_post.elements = self.renderer.get_info()
        return parsed_post