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
        lr = makepost.lint(post, "linter_config.yaml", online_checks=True)
        msg = "Linting failed. %s not triggered. Got %s" % (error_id, lr.links)
        if debug:
            print post.html
            print lr.links
        assert error_is_reported(lr.links, error_id) == True, msg

def assert_content_error_absence(mds, error_id, debug=False):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, "linter_config.yaml",  online_checks=True)
        msg = "Linting failed. %s triggered. Got %s" % (error_id, lr.links)
        if debug:
            print post.html
            print lr.links
        assert error_is_reported(lr.links, error_id) == False, msg


def test_E301_trigger():
    mds = []
    mds.append('''[Google error](https://www.google.com?mock=mock_url_not_exist)''')
    error_id = "E301"
    assert_content_error_presence(mds, error_id)

def test_E301_not_triggered():
    mds = []
    mds.append('''[Google homepage](https://www.google.com?mock=mock_url_exist)''')
    error_id = "E301"
    assert_content_error_absence(mds, error_id)

def test_E302_trigger():
    mds = []
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/0000000000/credit-card-shared-on-twitter.jpg?mock=mock_url_not_exist)''')
    error_id = "E302"
    assert_content_error_presence(mds, error_id)

def test_E302_not_triggered():
    mds = []
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg?mock=mock_url_exist)''')
    error_id = "E302"
    assert_content_error_absence(mds, error_id)

def test_E303_trigger():
    mds = []
    mds.append('''[Good vid](https://www.youtube.com/watch?v=notfound&?mock=mock_url_not_exist)''')
    error_id = "E303"
    assert_content_error_presence(mds, error_id)

def test_E303_not_triggered():
    mds = []
    mds.append('''[Good vid](https://www.youtube.com/watch?v=nkV9kOsTyJU?mock=mock_url_exist)''')
    error_id = "E303"
    assert_content_error_absence(mds, error_id)

def test_W304_trigger():
    mds = []
    mds.append('''[Google error](https://www.google.com/?mock=mock_url_exist), [Google error](https://www.google.com/?mock=mock_url_exist)''')
    error_id = "W304"
    assert_content_error_presence(mds, error_id)

def test_W304_not_triggered():
    mds = []
    mds.append('''[Google homepage](https://www.google.com?mock=mock_url_exist), [Google calendar](https://www.google.com/calendar?mock=mock_url_exist)''')
    error_id = "W304"
    assert_content_error_absence(mds, error_id)


def test_E307_trigger():
    mds = []
    mds.append('''
    ---
    files:
        paper: https://cdn.elie.net/publications/nonexisting?mock=mock_url_not_exist
    ---
    ''')
    error_id = "E307"
    assert_content_error_presence(mds, error_id)

def test_E307_not_triggered():
    mds = []
    mds.append('''
    ---
    files:
        paper: https://cdn.elie.net/publications/i-am-a-legend-hacking-hearthstone-using-statistical-learning-methods.pdf?mock=mock_url_exist
    ---
    ''')
    error_id = "E307"
    assert_content_error_absence(mds, error_id)

def test_E308_trigger():
    mds = []
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/000000/i-am-a-legend-hacking-hearthstone-using-statistical-learning-methods.jpg?mock=mock_url_not_exist
    ---
    ''')
    error_id = "E308"
    assert_content_error_presence(mds, error_id)

def test_E308_not_triggered():
    mds = []
    mds.append('''
    ---
    banner: https://www.elie.net/image/public/1476002309/i-am-a-legend-hacking-hearthstone-using-statistical-learning-methods.jpg?mock=mock_url_exist
    ---
    ''')
    error_id = "E308"
    assert_content_error_absence(mds, error_id)