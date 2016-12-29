import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
import makepost

def test_list():
    "Facebook forbid multiple <p> in the list"
    md = '''
This is a list
 -  elt1

 - elt2.1

    elt 2.1

 - elt3
    '''

    expected = '''<p>This is a list</p>
<ul>
<li><p>elt1</p>
</li>
<li><p>elt2.1 elt 2.1</p>
</li>
<li><p>elt3</p>
</li>
</ul>
'''

    post = makepost.parse(md)
    msg = "Expected:\n'%s'\nGot:\n'%s'" % (expected, post.fb)
    assert expected == post.fb, msg

def test_order_list():
    "Facebook forbid multiple <p> in the list"
    md = '''
This is a list
 1.  elt1

 2. elt2.1

    elt 2.1

 3. elt3
    '''

    expected = '''<p>This is a list</p>
<ol>
<li><p>elt1</p>
</li>
<li><p>elt2.1 elt 2.1</p>
</li>
<li><p>elt3</p>
</li>
</ol>
'''

    post = makepost.parse(md)
    msg = "Expected:\n'%s'\nGot:\n'%s'" % (expected, post.fb)
    assert expected == post.fb, msg


def test_image():
    src = "https://www.google.net/logo.jpg"
    caption = "Credit card on twitter"
    
    md = '''![%s](%s)''' % (caption, src)
    expected = '<figure><img src="%s" /><figcaption>%s</figcaption></figure>\n' % (src, caption)

    post = makepost.parse(md)
    msg = "Expected:\n'%s'\nGot:\n'%s'" % (expected, post.fb)
    
    assert expected == post.fb, msg

def test_video():
    src = 'https://www.youtube.com/embed/ao3P5QCrF_M'
    
    md = "[link to embedded video](%s)" % src
    expected = '<figure class="op-interactive"><iframe width="560" height="315" src="%s"></iframe></figure>\n' % src
    
    post = makepost.parse(md)
    msg = "Expected:%s Got:%s'" % (expected, post.fb)
    
    assert expected == post.fb, msg

def test_h1():    
    md = '# test'
    expected = '<h1>test</h1>'

    post = makepost.parse(md)
    msg = "Expected:%s Got:%s'" % (expected, post.fb)
    
    assert expected in post.fb, msg

def test_h2():    
    md = '## test'
    expected = '<h1>test</h1>'

    post = makepost.parse(md)
    msg = "Expected:%s Got:%s'" % (expected, post.fb)
    
    assert expected in post.fb, msg

def test_h3():    
    md = '### test'
    expected = '<h2>test</h2>'

    post = makepost.parse(md)
    msg = "Expected:%s Got:%s'" % (expected, post.fb)
    
    assert expected in post.fb, msg

def test_h4():    
    md = '#### test'
    expected = '<h2>test</h2>'

    post = makepost.parse(md)
    msg = "Expected:%s Got:%s'" % (expected, post.fb)
    
    assert expected in post.fb, msg
