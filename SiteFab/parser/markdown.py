# coding: utf-8
import logging
import re
import jinja2

# syntax coloring
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer


from mistune import Renderer, escape
from SiteFab import utils

youtube_matcher = re.compile("v=([^&]+)")

class HTMLRendererMixin(object):
    """Customized HTML renderer"""
    def link(self, link, title, content):
        
        embed = False

        # Youtube
        if "https://youtu.be/" in link or "https://www.youtube/" in link:
            embed = True

            if "embed" in link:  # Already correct link
                src = link
                template = self.jinja2.get_template('youtube')
            
            elif "&no_embed=1" not in link:
                #already embeded url or need to convert?
                if "https://youtu.be/" in link:
                    src = "https://www.youtube.com/embed/" + link.replace("https://youtu.be/", "")
                else:
                    d = youtube_matcher.search(link)
                    if d:
                        vid = d.group(1)
                        src = "https://www.youtube.com/embed/" + vid
                    else:
                        print "error can't detect video id for link: %s" % link
                template = self.jinja2.get_template('youtube')
                self.info.videos.append(link)
            
            else:
                # Youtube videos that are not embedded
                embed = False
                src = link.replace("&no_embed=1", "")
                template = self.jinja2.get_template('a')
                self.info.links.append(link)


        # Normal links
        else:
            src = link
            template = self.jinja2.get_template('a')
            self.info.links.append(link)

        rv = template.render(href=src, text=content, title=title, embed=embed)
        rv = rv.encode('utf-8')
        return rv

    def image(self, src, title, alt_text):
        
        self.info.images.append(src)
        
        template = self.jinja2.get_template('img')
        rv = template.render(src=src, alt=alt_text, title=title).encode('utf-8')
        return rv

    def header(self, text, level, raw=None):
        
        template = self.jinja2.get_template('h')
        rv = template.render(level=level, text=text, id=self.toc_count).encode('utf-8')

        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv


    def block_code(self, code, lang):
        "Block code highlighter and formater"
        css = ""

        try:
            if not lang:
                lexer = guess_lexer(code, stripall=True)
            else:
                lexer = get_lexer_by_name(lang, stripall=True)
            detected = True
            code = highlight(code, lexer, self.code_formatter)
            css = self.code_formatter.get_style_defs()
        except:
            code = escape(code)
            lang = None
       
        # template
        #fixing class name
        code = code.replace('class="highlight"', 'class="hll"')
        template = self.jinja2.get_template('code')
        rv = template.render(code=code, lang=lang, css=css)
        rv = rv.encode('utf-8')
        return rv

    def init(self, jinja2, code_formatter):
        """Init function called before each parsing.
        
        Note
            Used to ensure all the needed variables are reset between parsing execution        
        """
        # reset toc
        self.toc_tree = []
        self.toc_count = 0
        self.jinja2 = jinja2
        self.code_formatter = code_formatter
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