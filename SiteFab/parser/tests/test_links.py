import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
import makepost

def test_youtube_embedded_link():
    md = "[link to embedded video](https://www.youtube.com/embed/ao3P5QCrF_M)"
    result = makepost.parse(md.strip())
    msg = "Youtube correct embedded URL not found. returned html:%s" % result.html
    assert "https://www.youtube.com/embed/ao3P5QCrF_M" in result.html, msg

    msg = "Youtube embedded iframe not found. returned html:%s" % result.html
    assert "<iframe" in result.html, msg

def test_youtube_short_link():
    md = "[link to embedded video](https://youtu.be/ao3P5QCrF_M)"
    result = makepost.parse(md)
    msg = "Youtube correct embedded URL not found. returned html:%s" % result.html
    assert "https://www.youtube.com/embed/ao3P5QCrF_M" in result.html, msg 

    msg = "Youtube embedded iframe not found returned html:%s" % result.html
    assert "<iframe" in result.html, msg


def test_youtube_no_embed():
    md = "[link to embedded video](https://www.youtube.com/watch?v=ao3P5QCrF_M&no_embed=1)"
    result = makepost.parse(md)
    #Note: we also test that the no_embed=1 is also removed
    msg = "Youtube link was changed to an embed link. returned html:%s" % result.html
    assert "https://www.youtube.com/watch?v=ao3P5QCrF_M" in result.html, msg 

    msg = "Youtube link was iframed not inlined:%s" % result.html
    assert '<a href="https://www.youtube.com/watch?v=ao3P5QCrF_M"' in result.html, msg

def test_youtube_regular_link():
    md = "[link to embedded video](https://www.youtube.com/watch?v=ao3P5QCrF_M)"
    result = makepost.parse(md)
    msg = "Youtube correct embedded URL not found. returned html:%s" % result.html
    assert "https://www.youtube.com/embed/ao3P5QCrF_M" in result.html, msg 

    msg = "Youtube embedded iframe not found returned html:%s" % result.html
    assert "<iframe" in result.html, msg

def test_regular_link():
    lnk = "https://www.elie.net"
    txt = "Elie's blog'"
    md = "[%s](%s)" % (txt, lnk)
    expected_html = '<a href="%s">%s</a>' % (lnk, txt)
    
    result = makepost.parse(md)
    generated_html = result.html

    msg = "Generated HTML does not contains expected link markup. returned html:%s" % generated_html
    assert expected_html in result.html, msg

def test_image_link():
    src = "https://www.elie.net/image/public/1420997372/elie.jpeg"
    txt = "Elie's blog'"
    md = "![%s](%s)" % (txt, src)

    # check dynamic image
    expected_html = '<img class="image_blog" data-src="%s" data-addmodal="1" data-nocrop="1" data-container-width-id="post_body" data-width="0"/>' % (src)
    result = makepost.parse(md)
    generated_html = result.html
    msg = "Generated HTML does not contains expected image markup. returned html:%s" % generated_html
    assert expected_html in result.html, msg

    #check <nocript> is here
    expected_html = 'p> <noscript> <img style="display:block;" class="image_blog_nojs" src="%s"/> </noscript>' % (src)
    result = makepost.parse(md)
    generated_html = result.html
    msg = "Generated HTML does not contains <noscript>. returned html:%s" % generated_html
    assert expected_html in result.html, msg



