"Post parser"
import jinja2
import mistune
from pygments.formatters import html

from sitefab import files, utils
from sitefab.parser import frontmatter
from sitefab.parser.html2text import html2text
from sitefab.parser.markdown import HTMLRenderer


class Parser():

    def __init__(self, config, site):
        """ Initialize a new parser for a given type of parsing

        Args:
            config (obj_dict): the parser config. It is explicitly defined to
            allows  different conf
            site (dictobj): sitefab instantiated object
        Return:
            None

        note: one parser is instanciated by thread. potentially batching more
        than one post per thread might help with performance.
        """

        # verify that the config exist
        self.config = config
        self.site = site

        # NOTE: Might seems weird to do this but templates is what allows
        # to have different rendering for each plugins. So we keep it explict
        # in the code as this got messed up countless time :(
        self.templates = self.config.templates

        # templates are not compiled yet, they will be when parsing will be
        # called the first time
        self.jinja2 = None

        # markdown parser
        self.renderer = HTMLRenderer()
        self.md_parser = mistune.Markdown(renderer=self.renderer)

        # code higlighterr
        if self.config.code_display_line_num:
            linenos = 'table'
        else:
            linenos = False

        self.code_formatter = html.HtmlFormatter(
            style=self.config.code_highlighting_theme,
            nobackground=False, linenos=linenos)

    @staticmethod
    def make_config(config):
        """ Initialize a parser config with all the needed variables

        Args:
            config (obj_dict): the uninitialized configuration with basic
            variables
        Returns:
            obj_dict: The initialized configuration
        """

        if not config:
            utils.detailed_error("Parser", 'make_config',
                                 'supplied config is empty')

        if 'template_dir' not in config:
            utils.detailed_error("Parser", 'make_config',
                                 'template_dir not found')

        config.templates = {}
        for fname in files.get_files_list(config.templates_path, "*.html"):
            template = files.read_file(fname)
            config.templates[fname.stem] = template
        return config

    def list_templates(self):
        "Return the list of available templates"
        return self.templates.keys()

    def parse(self, md_file):
        """ Parse a md file into a post object
        """

        # compile the templates when we parse the first post. This is needed
        # to ensure that plugins get a chance to modify the templates before
        # we compile them.
        if not self.jinja2:
            self.jinja2 = jinja2.Environment(loader=jinja2.DictLoader(
                                             self.templates))

        parsed_post = utils.dict_to_objdict()

        # parsing frontmatter and getting the md
        parsed_post.meta, parsed_post.md = frontmatter.parse(md_file)

        # parsing markdown and extractring info
        # NOTE: this must called before every parsing
        self.renderer.init(self.jinja2, self.code_formatter, self.site,
                           parsed_post.meta)

        parsed_post.html = self.md_parser.parse(parsed_post.md)
        parsed_post.text = html2text(parsed_post.html)  # used by NLP
        parsed_post.meta.statistics = self.renderer.get_stats()
        parsed_post.meta.toc = self.renderer.get_json_toc()
        parsed_post.elements = self.renderer.get_info()
        return parsed_post
