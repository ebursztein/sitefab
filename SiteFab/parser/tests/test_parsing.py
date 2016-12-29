import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
import makepost

def test_image():
    src = "https://www.google.net/logo.jpg"
    md = '''![Credit card on twitter](%s)''' % src
    
    post = makepost.parse(md)
    msg = "Image should be processed correctly but HTML don't contain it:%s'" % (post.html)
    assert src in post.html, msg

def test_bad_frontmatter():
    src = "https://www.google.net/logo.jpg"
    md = '''
    ---
    bad:frontmatter
    ---
    '''
    
    post = makepost.parse(md)
    msg = "Front matter should be none. Got:%s'" % (post.meta)
    assert post.meta == None, msg