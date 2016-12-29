import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
import makepost

def error_is_reported(errors, error_id):
    """Check is a given error code is reported"""
    for e in errors:
        if e[0] == error_id:
            return True
    return False

def assert_content_error_presence(mds, error_id, debug=False):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, "linter_config.yaml")
        msg = "Linting failed. %s not triggered. Got %s" % (error_id, lr.structure)
        if debug:
            print post.html
            print lr.content
        assert error_is_reported(lr.content, error_id) == True, msg

def assert_content_error_absence(mds, error_id):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, "linter_config.yaml")
        msg = "Linting failed. %s triggered. Got %s" % (error_id, lr.structure)
        assert error_is_reported(lr.content, error_id) == False, msg