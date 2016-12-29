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

def assert_structure_error_presence(mds, error_id, debug=False):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, config_file="linter_config.yaml")
        msg = "Linting failed. %s not triggered. Got %s" % (error_id, lr.structure)
        if debug:
            print post.html
            print lr.structure
        assert error_is_reported(lr.structure, error_id) == True, msg

def assert_structure_error_absence(mds, error_id):
    for md in mds:
        post = makepost.parse(md)
        lr = makepost.lint(post, config_file="linter_config.yaml")
        msg = "Linting failed. %s triggered. Got %s" % (error_id, lr.structure)
        assert error_is_reported(lr.structure, error_id) == False, msg

def test_E201_triggered():
    mds = []
    mds.append('''
    No H1
    ''')
    error_id = "E201"
    assert_structure_error_absence(mds, error_id)

def test_E201_not_triggered():
    mds = []
    mds.append('''#H1 exist
    ''')
    error_id = "E201"
    assert_structure_error_presence(mds, error_id)

def test_E204_not_triggered():
    mds = []
    mds.append('''## Section 1''')
    error_id = "E204"
    assert_structure_error_absence(mds, error_id)

def test_E204_triggered():
    mds = []
    mds.append('''# not a h2''')
    error_id = "E204"
    assert_structure_error_presence(mds, error_id)

def test_E205_not_triggered():
    mds = []
    mds.append('''## h2 text\n## h2 text 2''')
    error_id = "E205"
    assert_structure_error_absence(mds, error_id)

def test_E205_triggered():
    mds = []
    mds.append('''## h2 text\n## h2 text''')
    # testing for upper case vs lowercase normalization
    mds.append('''## h2 text\n## H2 Text''') 
    error_id = "E205"
    assert_structure_error_presence(mds, error_id)

def test_E206_not_triggered():
    mds = []
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg)''')
    error_id = "E206"
    assert_structure_error_absence(mds, error_id)

def test_E206_triggered():
    mds = []
    # typo
    mds.append('''![Credit card on twitter](https://www.elie.snet/image/public/1468375524/credit-card-shared-on-twitter.jpg)''')
    # external
    mds.append('''![Credit card on twitter](https://www.google.net/logo.jpg)''')

    error_id = "E206"
    assert_structure_error_presence(mds, error_id)

def test_E207_not_triggered():
    mds = []
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg)''')
    error_id = "E207"
    assert_structure_error_absence(mds, error_id)

def test_E207_triggered():
    mds = []
    # ?
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg?param1=1)''')
    # encoded ? to %3F	
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg%3Fparam1=1)''')

    error_id = "E207"
    assert_structure_error_presence(mds, error_id)

def test_E208_not_triggered():
    mds = []
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on-twitter.jpg)''')
    error_id = "E208"
    assert_structure_error_absence(mds, error_id)

def test_E208_triggered():
    mds = []
    # space in the middle -> space in the middle are always triggered
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on twitter.jpg)''')
    # percent
    mds.append('''![Credit card on twitter](https://www.elie.net/image/public/1468375524/credit-card-shared-on%twitter.jpg)''')

    error_id = "E208"
    assert_structure_error_presence(mds, error_id)