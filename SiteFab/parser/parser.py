import jinja2
import  os

import fb
import frontmatter
import linter
import markdown
from markdown import HTMLRenderer
import mistune
from mistune import Renderer

from SiteFab import utils
from SiteFab import files

class Parser():
    
    def __init__(self, templates_dir, linter_config=None):
        """ Initialize a new parser for a given type of parsing

        Args:
            templates_dir (str): path where the templates for the token emissions are stored.
            linter_config (str): The path to the linter config file. Can be None if no linting
        
        Return:
            None

        note: moving to an object was needed for perfomance reasons. You don't want to 
        reinitialize all the templating system for every post.

        """

        #FIXME verify the linter config exist
        self.linter_config = linter_config

        #Loadings template strings in memory so we can manipulate them
        self.templates = {}
        for fname in files.get_files_list(templates_dir, "*.html"):
            template_name = os.path.basename(fname).replace(".html", "")
            template = files.read_file(fname)
            #print "%s -> %s" % (template_name, template)
            self.templates[template_name] = template

        # templates are not compiled yet, they will be when parsing will be called the first time to
        # allows pluging to modify them before hand if needed.
        self.jinja2 = None 

        # markdown parser
        self.renderer = HTMLRenderer()
        self.md_parser = mistune.Markdown(renderer=self.renderer)
    
    def lint(self, post, online_checks=False, check_content=False):
        """ Lint post for various errors.

        Args:
            post (str): The post object to lint.
            online_check (bool): perform online check. E.g test for URL existence. Off by default
            check_content (bool): use language tool to check the content against common mistake. Off by default
        
        Return:
            Object: None if no errors, errors object otherwise
        """

        result = linter.lint(post, self.linter_config, online_checks, check_content)
        return result

    def has_errors(self, post, config_file):
        """Validate that post has basic no errors.

        Args:
            post (str): The post object to lint.
            config_file (str): The path to the linter config file.

        Return:
            bool: True if there is error False otherwise
        """
        
        return linter.has_errors(post, self.linter_config)

    def format_errors(self, errors):
        """ Format errors """
        return linter.format_errors(errors, self.linter_config)
        

    def parse(self, md_file):
        """ Parse a md file into a post object
        """
        
        # compile the templates when we parse the first post. This is needed to ensure that
        # plugins get a chance to modify the templates before we compile them. 
        if not self.jinja2:
            self.jinja2 = jinja2.Environment(loader=jinja2.DictLoader(self.templates))

        parsed_post = utils.create_objdict()

        # parsing frontmatter and getting the md
        parsed_post.meta, parsed_post.md = frontmatter.parse(md_file)

        # parsing markdown and extractring info
        self.renderer.init(self.jinja2) # reset all the needed counters
        parsed_post.html = self.md_parser.parse(parsed_post.md)
        parsed_post.info = self.renderer.get_info()
        parsed_post.info.toc = self.renderer.get_json_toc()

        return parsed_post