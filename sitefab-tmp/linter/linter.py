from pathlib import Path
from jinja2 import Template

from sitefab import utils
from sitefab import files
from . import frontmatter, images, structure


class Linter:

    def __init__(self, config):
        current_dir = Path(__file__).parent
        test_file = current_dir / 'tests.yaml'
        self.test_info = files.load_config(test_file)
        if not self.test_info:
            utils.error("Can't load linter tests")

        self.config = config
        self.results = {}
        template_content = files.read_file(self.config.report_template_file)
        self.jinja2_template = Template(str(template_content))

    def render_report(self):
        "Create a linting report for all posts"
        report = self.jinja2_template.render(results=self.results)
        files.write_file(self.config.output_dir, "linter.html", report)

    def num_post_with_errors(self):
        "Return number of posts that have errors"
        cnt = 0
        for p in self.results.values():
            cnt += p.has_errors
        return cnt

    def num_post_with_warnings(self):
        "Return the numbers of posts that have warnings but no errors"
        cnt = 0
        for p in self.results.values():
            if not p.has_errors:
                cnt += p.has_warnings
        return cnt

    def num_post_ok(self):
        "num post with no wrror or warnings"
        cnt = 0

        for p in self.results.values():
            if not p.has_errors and not p.has_warnings:
                cnt += 1
        return cnt

    def lint(self, post, rendered_post, site):
        """ Load yaml configuration

        Args:
            post (Post): the post to analyze
            rendered_post (str): the html version of the post
            site (Sitefab): the site object mainly used to get access
            to plugin data
        Return:
            dict: linting results
        """
        results = utils.create_objdict()
        results.has_errors = 0
        results.has_warnings = 0

        # frontmatter
        results.info = frontmatter.lint(post, self.test_info, self.config)

        # images
        if 'image_info' in site.plugin_data:
            image_info = site.plugin_data['image_info']
        else:
            image_info = None

        img_results = images.lint(post, self.test_info, self.config,
                                  image_info)
        results.info.extend(img_results)
        stucture_results = structure.lint(post, self.test_info, self.config)
        results.info.extend(stucture_results)

        for d in results.info:
            if d[0][0] == "E":
                results.has_errors += 1
            if d[0][1] == "W":
                results.has_warnings += 1

        if results.has_errors or results.has_warnings:
            self.results[post.filename] = results

        return results
