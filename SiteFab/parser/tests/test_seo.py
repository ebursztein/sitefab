import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)

sys.path.insert(0,parentdir2)
import makepost

def error_is_reported(errors, error_id):
    """Check is a given error code is reported"""
    for e in errors:
        if e[0] == error_id:
            return True
    return False

def assert_frontmatter_error_presence(mds, error_id, debug=False):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, config_file="linter_config.yaml")
        if debug:
            print md
            print lr
        msg = "Linting failed. %s not triggered. Got %s" % (error_id, lr.seo)
        assert error_is_reported(lr.seo, error_id), msg

def assert_frontmatter_error_absence(mds, error_id, debug=False):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, config_file="linter_config.yaml")
        if debug:
            print md
            print lr
        msg = "Linting failed. %s triggered. Got %s" % (error_id, lr.seo)
        assert error_is_reported(lr.seo, error_id) == False, msg

def test_E401_trigger():
    mds = []
    mds.append('''
    ---
    banner: "cat/test-match"
    permanent_url: "test-mismatch"
    ---
    ''')

    error_id = "E401"
    assert_frontmatter_error_presence(mds, error_id)

def test_E401_not_trigger():
    mds = []
    mds.append('''
    ---
    banner: "cat/test-match"
    permanent_url: "test-match"
    ---
    ''')
    error_id = "E401"
    assert_frontmatter_error_absence(mds, error_id)

def test_W402_trigger():
    mds = []
    mds.append('''
    ---
    title: "this is too short"
    ---
    ''')

    error_id = "W402"
    assert_frontmatter_error_presence(mds, error_id)

def test_W402_not_trigger():
    mds = []
    mds.append('''
    ---
    title: "this is the appropriate length for a post title!"
    ---
    ''')
    error_id = "W402"
    assert_frontmatter_error_absence(mds, error_id)

def test_W403_trigger():
    mds = []
    mds.append('''
    ---
    title: "this is waaaaaaaaaaaaaaaaaaayyyyyyyyyyyyyyyyyyyyyyyyyyyy toooooooooooooooooo longgggggggggg"
    ---
    ''')

    error_id = "W403"
    assert_frontmatter_error_presence(mds, error_id)

def test_W403_not_trigger():
    mds = []
    mds.append('''
    ---
    title: "this is the appropriate length for a post title!"
    ---
    ''')
    error_id = "W403"
    assert_frontmatter_error_absence(mds, error_id)

def test_W404_trigger():
    mds = []
    mds.append('''
    ---
    abstract: "this is waaaaaaaaaaaaaaaaaaayyyyyyyyyyyyyyyyyyyyyyyyyyyy toooooooooooooooooo longgggggggggg foooooooorrrrrrrrrrrrrrrrrrrrr a pooooooooooooooostttttttttttttttttt abstracttttttttttttttt ooooorrrr  atttttttttt leastttttttttttttt thaaaaaaaattttttt is whattttttttttt SEO says!"
    ---
    ''')

    error_id = "W404"
    assert_frontmatter_error_presence(mds, error_id)

def test_W404_not_trigger():
    mds = []
    mds.append('''
    ---
    abstract: "this is the appropriate length for a post abstract or at least that is what SEO says!"
    ---
    ''')
    error_id = "W404"
    assert_frontmatter_error_absence(mds, error_id)