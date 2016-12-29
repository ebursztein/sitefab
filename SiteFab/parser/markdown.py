# coding: utf-8
import logging
import re

import mistune
from mistune import Renderer
from SiteFab import utils


class HTMLRendererMixin(object):
    """Customized HTML renderer"""
    def link(self, link, title, content):
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

            rv = '<div class="video_wrapper"><iframe src="%s" frameborder="0" allowfullscreen></iframe></div>' % (src)
            self.info.videos.append(link)
        else:
            link = link.replace("&no_embed=1", "")
            rv = '<a href="%s">%s</a>' % (link, content)
            self.info.links.append(link)

        return rv

    def image(self, src, title, alt_text):
        m = re.search(r'(\d+)', src)
        try:
            ts = m.group(1)
            width = 0
            from model.Image import Image
            image = Image.getImageByTs(ts)
            if image:
                width = image.width
                logging.debug("found image %s, width: %s" % (ts, width))
        except Exception as e:
            width = 0
        rv = """<p> <noscript> <img style="display:block;" class="image_blog_nojs" src="%s"/> </noscript> <img class="image_blog" data-src="%s" data-addmodal="1" data-nocrop="1" data-container-width-id="post_body" data-width="%s"/> </p>
        """ % (src, src, width)
        self.info.images.append(src)
        return rv

    def header(self, text, level, raw=None):
        rv = '<h%d id="toc-%d">%s</h%d>\n' % (
            level, self.toc_count, text, level
        )
        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv

    def init(self):
        """Our own init function."""
        # reset toc
        self.toc_tree = []
        self.toc_count = 0

        # Various information collected during the parsing 
        self.info = metas = utils.create_objdict({
            "links": [],
            "images": [],
            "videos": [],
        })

        self.info.stats = utils.create_objdict({
            "num_links": 0,
            "num_images": 0,
            "num_videos": 0,
        })

    def get_info(self):
        info = self.info
        info['stats']['num_links'] = len(info['links'])
        info['stats']['num_videos'] = len(info['videos'])
        info['stats']['num_images'] = len(info['images'])
        return info

    ### TOC code ###

    def get_json_toc(self):
        """Render the TOC in JSON
        
        :param level: render toc up to the given level
        """
        first_level = None
        last_level = None
        lst = []
        for toc in self.toc_tree:
            index, text, l, raw = toc
            lst.append((text, l, index))
        return lst

    def get_html_toc(self, level=3):
        """Render TOC to HTML.

        :param level: render toc up to the given level
        """
        return ''.join(self._iter_html_toc(level))

    def _iter_html_toc(self, level):
        first_level = None
        last_level = None

        yield '<ul id="table-of-content">\n'

        for toc in self.toc_tree:
            index, text, l, raw = toc

            if l > level:
                # ignore this level
                continue

            if first_level is None:
                # based on first level
                first_level = l
                last_level = l
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l:
                yield '</li>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l - 1:
                last_level = l
                yield '<ul>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level > l:
                # close indention
                yield '</li>'
                while last_level > l:
                    yield '</ul>\n</li>\n'
                    last_level -= 1
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)

        # close tags
        yield '</li>\n'
        while last_level > first_level:
            yield '</ul>\n</li>\n'
            last_level -= 1

        yield '</ul>\n'


class HTMLRenderer(HTMLRendererMixin, Renderer):
    pass


def parse(text):
    """Parse MD to html
    @return html, toc: return the html generated and the toc
    """
    renderer = HTMLRenderer()
    md = mistune.Markdown(renderer=renderer)
    renderer.init()
    html = md.parse(text)
    info = renderer.get_info()
    info.toc = renderer.get_json_toc()
    return html, info
