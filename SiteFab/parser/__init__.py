import fb
import frontmatter
import linter
import markdown
from SiteFab import utils

def lint(post, config_file="libs/makepost/linter_config.yaml", online_checks=False, check_content=False):
    """ Lint post for various errors.

    Args:
        post (str): The post object to lint.
        config_file (str): The path to the linter config file.
        online_check (bool): perform online check. E.g test for URL existence. Off by default
        check_content (bool): use language tool to check the content against common mistake. Off by default
    
    Return:
        Object: None if no errors, errors object otherwise
    """
    result = linter.lint(post, config_file, online_checks, check_content)
    return result

def has_errors(post, config_file="libs/makepost/linter_config.yaml"):
    """Validate that post has no breaking errors at upload time.

    Args:
        post (str): The post object to lint.
        config_file (str): The path to the linter config file.

    Return:
        bool: True if there is error False otherwise
    """
    return linter.has_errors(post, config_file)

def format_errors(errors, config_file):
    """ Format errors """
    return linter.format_errors(errors, config_file)
    

def parse(md_file):
    """ Parse a md file into a post object
    """
    #FIXME: use frm  utils.objdict import objdict
    parsed_post = utils.create_objdict()

    # parsing frontmatter and getting the md
    parsed_post.meta, parsed_post.md = frontmatter.parse(md_file)

    # parsing markdown and extractring info
    parsed_post.html, parsed_post.info = markdown.parse(parsed_post.md)
    
    #Facebook  instant article
    parsed_post.fb = fb.parse(parsed_post.md)
    
    return parsed_post

if __name__ == '__main__':
    #import pprint
    #cfg = "linter_config.yaml"
    #md = open("tests/files/publication.md").read()
    md = '''
This is a list
 1.  elt1

 2. elt2.1

    elt 2.1

 3. elt3
    '''
    
    post = parse(md)
    print "=== html ===\n"
    print post.html
    print "=== FB ===\n"
    print post.fb
    #errors = lint(post, config_file=cfg, online_checks=True, check_content=True)
    #if errors:
     #  print "\n".join(linter.format_errors(errors, config_file=cfg))

    '''
    if post.meta:
        print post.meta.authors
    print post.info.stats
    print post.html
    '''