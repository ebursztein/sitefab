from SiteFab.Plugins import PostProcessor
from SiteFab import parser
from SiteFab.SiteFab import SiteFab
from SiteFab import files
import os

class PostLinter(PostProcessor):
    #FIMXE load the config in the init?

    def process(self, post, site, config):
        config_file = os.path.join(files.get_site_path(), config.config_file)
        online_check = config.online_check
        check_content = config.check_content
        errors = parser.lint(post, config_file=config_file, online_checks=online_check, check_content=check_content)
        if errors:
            formatted_errors = parser.format_errors(errors, config_file)
            return (SiteFab.ERROR, post.meta.title, formatted_errors)
        else:
            return (SiteFab.OK, post.meta.title, "")