import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
import makepost
from makepost import linter
from makepost import objdict

def test_error_count_errors_return_a_number_on_invalid_post():
    mds = []
    mds.append('''
    ---
        title: ""
    ---
    ''')
    for md in mds:
        post = makepost.parse(md)
        errors = makepost.lint(post, "linter_config.yaml")
        msg = "has_error should return a number > 0. got %s"  % errors
        v = linter.count_errors(errors)
        assert v > 0, msg


def test_linter_return_none_on_valid_blog():
    mds = []
    md = open("tests/files/post.md").read()
    mds.append(md)   
    for md in mds:
        post = makepost.parse(md)
        errors = makepost.lint(post, "linter_config.yaml")
        msg = "Linting failed, should have returned none but got %s" % errors
        assert errors == None, msg

def test_linter_return_none_on_valid_publication():
    mds = []
    md = open("tests/files/publication.md").read()
    mds.append(md)   
    for md in mds:
        post = makepost.parse(md)
        errors = makepost.lint(post, "linter_config.yaml")
        msg = "Linting failed, should have returned none but got %s" % errors
        assert errors == None, msg

def test_linter_return_proper_errors_structure_on_invalid_md():
    mds = []
    mds.append('''
    ---
        title: ""
    ---
    ''')
    for md in mds:

        #valid structure?
        post = makepost.parse(md)
        errors = makepost.lint(post, "linter_config.yaml")
        msg = "Linter shoud have returned an objdict but got:%s" % (type(errors))
        assert type(errors) == objdict, msg

        # all fields?
        for f in ["frontmatter", "structure", "links", "seo"]:
            msg = "%s not in linter results" % f
            assert f in errors, msg
            
            # all fields are array?
            msg = "%s expected value is array. got %s" % (f, type(errors[f]))
            assert(type(errors[f]) == list)


def test_has_error_return_none_on_valid_blog():
    mds = []
    md = open("tests/files/post.md").read()
    mds.append(md)   
    for md in mds:
        post = makepost.parse(md)
        errors = makepost.has_errors(post, "linter_config.yaml")
        msg = "Validation failed. Should have returned True"
        assert errors == None, msg

def test_has_error_return_none_on_valid_publication():
    mds = []
    md = open("tests/files/publication.md").read()
    mds.append(md)   
    for md in mds:
        post = makepost.parse(md)
        errors = makepost.has_errors(post, "linter_config.yaml")
        msg = "Validation failed. Should have returned True"
        assert errors == None, msg