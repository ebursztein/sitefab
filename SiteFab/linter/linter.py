import os
from jinja2 import Template

from SiteFab import utils
from SiteFab import files
import sys

import frontmatter
import images
import structure

class Linter:
    
    def __init__(self, config):
        current_dir = os.path.dirname(__file__)
        test_file = os.path.join(current_dir, 'tests.yaml')
        self.test_info = files.load_config(test_file)
        if self.test_info == None:
            utils.error("Can't load linter tests")

        #FIXME: add/use config
        self.config = config
        self.results = {}
        template_content = files.read_file(self.config.report_template_file)
        self.jinja2_template = Template(template_content)
    
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

    def lint(self, post, rendered_post, site):
        """ Load yaml configuration 
    
        Args:
            post (Post): the post to analyze
            rendered_post (str): the html version of the post
            site (Sitefab): the site object mainly used to get access to plugin data
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

        img_results = images.lint(post, self.test_info, self.config, image_info)
        stucture_results = structure.lint(post, self.test_info, self.config)
        results.info.extend(img_results)

        for d in results.info: 
            if d[0][0] == "E":
                results.has_errors += 1
            if d[0][1] == "W":
                results.has_warnings += 1
        
        if results.has_errors or results.has_warnings:
            self.results[post.filename] = results
        
        return results
