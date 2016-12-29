import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
import makepost

def test_toc_generation():
    md = '''# H1 text\n## H2 text\n### H3 text
    '''
    
    post = makepost.parse(md)
    msg = "TOC should contains 3 elements. Got: %s\nhtml:%s" % (post.info.toc, post.html)
    assert len(post.info.toc) == 3, msg

    levels = []
    for elt in post.info.toc:
        txt, level, index = elt
        levels.append(level)
        
    msg = "TOC level are incorrect, expected 1,2,3 got:%s" % levels
    assert levels == [1,2,3], msg

def test_video_counting():
    md = "[link to embedded video](https://www.youtube.com/embed/ao3P5QCrF_M)"
    result = makepost.parse(md.strip())
    info = result.info

    msg = "Video counts in info.stats.num_videos incorrect:%s" % info.videos
    assert info.stats.num_videos == 1, msg

    msg = "Youtube link not found in info.videos:%s" % info.videos
    assert "https://www.youtube.com/embed/ao3P5QCrF_M" in info.videos, msg

def test_link_counting():
    md = "[link to embedded video](https://www.youtube.com/embed/ao3P5QCrF_M)"
    result = makepost.parse(md.strip())
    info = result.info

    msg = "Video counts in info.stats.num_videos incorrect:%s" % info.videos
    assert info.stats.num_videos == 1, msg

    msg = "Youtube link not found in info.videos:%s" % info.videos
    assert "https://www.youtube.com/embed/ao3P5QCrF_M" in info.videos, msg
