# coding: utf-8
import logging
import re

import mistune
from mistune import Renderer
from SiteFab import utils

class FBRendererMixin(object):
    """Customized renderer for FB instant article"""

    def list_item(self, text):
        #print "fucking text:'%s'" % text
        text = text.replace("</p>\n<p>", " ") # Facebook want only one <p></p> ... 
        #print "rewrote:%s" % (text)
        rv = "<li>%s</li>\n" % (text)
        return rv

    def link(self, link, title, content):
        """Link and videos rewrite
        @note: not_embed=1 is used in the markdown to preven the conversion to a video embed.
        """

        if "no_embed=1" not in link and ("https://youtu.be/" in link or "https://www.youtube.com/" in link):
            if "embed" in link:  # Already correct link
                src = link
            else:
                if "https://youtu.be/" in link:
                    src = "https://www.youtube.com/embed/" + link.replace("https://youtu.be/", "")
                else:
                    d = re.search("v=([^&]+)", link)
                    if d:
                        vid = d.group(1)
                        src = "https://www.youtube.com/embed/" + vid
                    else:
                        print "error can't detect video id for link: %s" % link
                
            rv = '</p><figure class="op-interactive"><iframe width="560" height="315" src="%s"></iframe></figure><p>' % (src)
        else:
            link = link.replace("&no_embed=1", "")
            rv = '<a href="%s">%s</a>' % (link, content)
        return rv

    def image(self, src, title, alt_text):
        """Rewrite image"""
        rv = '</p><figure><img src="%s" /><figcaption>%s</figcaption></figure><p>' % (src, alt_text)
        return rv

    def header(self, text, level, raw=None):
        """Headers
        Facebook limit to h1 / h2 so h2 > h1 && H3,H4,H5 > H2
        """
        if level < 3:
            new_level = 1
        else:
            new_level = 2
        rv = '<h%d>%s</h%d>\n' % (new_level,text, new_level)
        return rv

class FBRenderer(FBRendererMixin, Renderer):
    """Combine our custom rendering code and mistune default one"""
    pass

def parse(md):
    """Parse MD to Facebook instant article format
    @param md: the post in md
    @return article in Facebook article format
    """
    renderer = FBRenderer()
    parser = mistune.Markdown(renderer=renderer)
    content = parser.render(md)

    #post rendering cleanup (Fuck facebook stupid rule: image not in a paragrah.)
    content = content.replace("<p></p>", "")
    return content