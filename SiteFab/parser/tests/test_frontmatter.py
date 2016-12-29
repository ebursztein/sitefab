import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
import makepost

def test_creation_date_parsing():
    md = '''
    ---
        creation_date: 6 Jul 2016 08:15
    ---
    '''
    expected_ts = 1467818100 - (3600 *8) #PST time
    
    post = makepost.parse(md)
    r = post.meta.creation_date_ts
    msg = "Invalid date parsing. Got:%s, expected:%s" % (r, expected_ts)
    assert r == expected_ts, msg

def test_frontmatter_proper_removal():
    mds = []
    mds.append('''
---
title: this is a title
---
html content
''')

    mds.append('''

---
title: this is atitle
---

html content
''')

    for md in mds:
        post = makepost.parse(md)
        result = post.html.strip()
        expected = '<p>html content</p>'
        msg = "fontmatter improperly removed. Remaining HTML is:'%s'" % result
        assert result == expected, msg
        
    
