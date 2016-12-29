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
        if debug:
            print md
        post = makepost.parse(md)
        lr = makepost.lint(post, config_file="linter_config.yaml")
        msg = "Linting failed. %s not triggered. Got %s" % (error_id, lr.frontmatter)
        assert error_is_reported(lr.frontmatter, error_id), msg

def assert_frontmatter_error_absence(mds, error_id, debug=False):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, config_file="linter_config.yaml")
        if debug:
            print md
            print lr.frontmatter
        msg = "Linting failed. %s triggered. Got %s" % (error_id, lr.frontmatter)
        assert error_is_reported(lr.frontmatter, error_id) == False, msg

def test_trying_to_confuse_parser():
    mds = []
    # field with a typo
    mds.append('''
    ---
        title: title
    ---
    ---
    ''')

    mds.append('''
    ---
        title: ---title
    ---
    test ---
    ''')
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, config_file="linter_config.yaml")
        msg = "frontmatter not correctly parsed. Post.meta empty"
        assert post.meta != None, msg
        msg = "title is not present in frontmater"
        assert "title" in post.meta, msg

def test_E103():
    mds = []
    # field with a typo
    mds.append('''
    ---
        title: ""
    ---
    ''')

    mds.append('''
    ---
        title:
    ---
    ''')

    mds.append('''
    ---
        abstract:
    ---
    ''')

    error_id = "E103"
    assert_frontmatter_error_presence(mds, error_id)

def test_E104():
    mds = []
    # field with a typo
    mds.append('''
    ---
        title: "at"
    ---
    ''')
    error_id = "E104"
    assert_frontmatter_error_presence(mds, error_id)


def test_E105():
    mds = []
    # Month error
    mds.append('''
    ---
        creation_date: 6 July 2016 08:15
    ---
    ''')

    # Missing hour
    mds.append('''
    ---
        creation_date: 6 Jul 2016
    ---
    ''')
    
    error_id = "E105"
    assert_frontmatter_error_presence(mds, error_id)

def test_E106():
    mds = []
    # field with a typo
    mds.append('''
    ---
        titlez: this field has a typo!
    ---
    ''')
    
    error_id = "E106"
    assert_frontmatter_error_presence(mds, error_id)

def test_E106_not_trigger_by_optional_fields():
    mds = []
    mds.append('''
    ---
    update_date: 04 Jun 2011 03:13
    ---
    ''')
    
    error_id = "E106"
    assert_frontmatter_error_absence(mds, error_id)

def test_E107():
    mds = []
    # field with a typo
    mds.append('''
    ---
        tags: this is not a list
    ---
    ''')
    
    error_id = "E107"
    assert_frontmatter_error_presence(mds, error_id)

def test_E108():
    mds = []
    mds.append('''
    ---
        seo_keywords: this, is not, a list
    ---
    ''')
    
    error_id = "E108"
    assert_frontmatter_error_presence(mds, error_id)

def test_E109():
    mds = []
    mds.append('''
    ---
        tags: 
            - tag in lower case
            - Tag with a cap
    ---
    ''')
    
    error_id = "E109"
    assert_frontmatter_error_presence(mds, error_id)

def test_E110():
    mds = []
    mds.append('''
    ''')
    
    error_id = "E110"
    assert_frontmatter_error_presence(mds, error_id)

def test_E111():
    mds = []
    mds.append('''
    ---
        seo_keywords: 
            - tag in lower case
            - Tag with a cap
    ---
    ''')
    
    error_id = "E111"
    assert_frontmatter_error_presence(mds, error_id)

def test_E112_trigger():
    mds = []
    mds.append('''
    ---
    banner: https://not-okay
    ---
    ''')
    
    error_id = "E112"
    assert_frontmatter_error_presence(mds, error_id)

def test_E112_not_trigger():
    mds = []
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg
    ---
    ''')
    
    error_id = "E112"
    assert_frontmatter_error_absence(mds, error_id)

def test_E114_trigger():
    mds = []
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg?param=1
    ---
    ''')
    # encoded value
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg%3Fparam=1
    ---
    ''')
    
    error_id = "E114"
    assert_frontmatter_error_presence(mds, error_id)

def test_E114_not_trigger():
    mds = []
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg
    ---
    ''')
    
    error_id = "E114"
    assert_frontmatter_error_absence(mds, error_id)

def test_E115_trigger():
    mds = []
    # a space
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter .jpg
    ---
    ''')
    # encoded space
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1468375524/credit%20-card-shared-on-twitter.jpg
    ---
    ''')
    
    error_id = "E115"
    assert_frontmatter_error_presence(mds, error_id)

def test_E115_not_trigger():
    mds = []
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg
    ---
    ''')
    
    error_id = "E115"
    assert_frontmatter_error_absence(mds, error_id)

def test_E116_trigger():
    mds = []
    mds.append('''
    ---
    permanent_url: bla%-bla-bla
    ---
    ''')

    mds.append('''
    ---
    permanent_url: bla -bla-bla
    ---
    ''')

    mds.append('''
    ---
    permanent_url: Bla-Bla-bla
    ---
    ''')
    
    mds.append('''
    ---
    permanent_url: http://www.elie.net/blog/cat/bla-bla-bla
    ---
    ''')
    error_id = "E116"
    assert_frontmatter_error_presence(mds, error_id)

def test_E116_not_trigger():
    mds = []
    mds.append('''
    ---
    permanent_url: bla-bla-bla
    ---
    ''')
    
    error_id = "E116"
    assert_frontmatter_error_absence(mds, error_id)

def test_E117_trigger():
    mds = []
    mds.append('''
    ---
    type: post
    category: security
    permanent_url: bla-bla-bla
    ---
    ''')

    error_id = "E117"
    assert_frontmatter_error_presence(mds, error_id)

def test_E117_not_trigger():
    mds = []
    mds.append('''
    ---
    type: post
    category: security
    permanent_url: security/bla-bla-bla
    ---
    ''')
    
    error_id = "E117"
    assert_frontmatter_error_absence(mds, error_id)

def test_E118_trigger():
    mds = []
    mds.append('''
    ---
    authors:
        - Elie Bursztein
    ---
    ''')
    
    error_id = "E118"
    assert_frontmatter_error_presence(mds, error_id)

def test_E118_not_trigger():
    mds = []
    mds.append('''
    ---
    authors:
        - Elie, Bursztein
    ---
    ''')
    
    error_id = "E118"
    assert_frontmatter_error_absence(mds, error_id)

def test_E119_trigger():
    mds = []
    mds.append('''
    ---
    authors:
        - Elie, bursztein
    ---
    ''')
    
    error_id = "E119"
    assert_frontmatter_error_presence(mds, error_id)

def test_E119_not_trigger():
    mds = []
    mds.append('''
    ---
    authors:
        - Elie, Bursztein
    ---
    ''')
    
    error_id = "E119"
    assert_frontmatter_error_absence(mds, error_id)

def test_E120_trigger():
    mds = []
    mds.append('''
    ---
    files:
        - paper: https://cdn.elie.net/publications/i-am-a-legend--hacking-hearthstone-using-statistical-learning-methods.pdf
    ---
    ''')

    mds.append('''
    ---
    files: https://cdn.elie.net/publications/i-am-a-legend--hacking-hearthstone-using-statistical-learning-methods.pdf
    ---
    ''')
    
    error_id = "E120"
    assert_frontmatter_error_presence(mds, error_id)

def test_E120_not_trigger():
    mds = []
    mds.append('''
    ---
    files:
        paper: https://cdn.elie.net/publications/i-am-a-legend--hacking-hearthstone-using-statistical-learning-methods.pdf
    ---
    ''')
    
    error_id = "E120"
    assert_frontmatter_error_absence(mds, error_id)

def test_E121_trigger():
    mds = []
    mds.append('''
    ---
    files:
        paper: https://cdn.elie.net/publications/i-am-a-legend?hacking-hearthstone-using-statistical-learning-methods.pdf
    ---
    ''')

    mds.append('''
    ---
    files:
        paper: https://cdn.elie.net/publications/i-am-a-legend  hacking-hearthstone-using-statistical-learning-methods.pdf
    ---
    ''')
    

    mds.append('''
    ---
    files:
        paper: https://cdn.elie.net/publications/i-am-a-legend%hacking-hearthstone-using-statistical-learning-methods.pdf
    ---
    ''')

    error_id = "E121"
    assert_frontmatter_error_presence(mds, error_id)

def test_E121_not_trigger():
    mds = []
    mds.append('''
    ---
    files:
        paper: https://cdn.elie.net/publications/i-am-a-legend--hacking-hearthstone-using-statistical-learning-methods.pdf
    ---
    ''')
    
    error_id = "E121"
    assert_frontmatter_error_absence(mds, error_id)

def test_E122_trigger():
    mds = []
    mds.append('''
    ---
    abstract: "<p>test</p>"
    ---
    ''')

    mds.append('''
    ---
    abstract: "test &nbsp;"
    ---
    ''')

    error_id = "E122"
    assert_frontmatter_error_presence(mds, error_id)

def test_E122_not_trigger():
    mds = []
    mds.append('''
    ---
    abstract: "test abstract, just to be sure."
    ---
    ''')

    mds.append('''
    ---
    abstract:
    ---
    ''')
    
    error_id = "E122"
    assert_frontmatter_error_absence(mds, error_id)

def test_E123_trigger():
    mds = []
    mds.append('''
    ---
    title: "<p>test</p>"
    ---
    ''')

    mds.append('''
    ---
    title: "test &nbsp;"
    ---
    ''')

    error_id = "E123"
    assert_frontmatter_error_presence(mds, error_id)

def test_E123_not_trigger():
    mds = []
    mds.append('''
    ---
    title: "test title"
    ---
    ''')
    
    error_id = "E122"
    assert_frontmatter_error_absence(mds, error_id)