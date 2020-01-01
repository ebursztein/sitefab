# coding: utf-8
import re

# syntax coloring
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer


from mistune import Renderer, escape
from sitefab import utils

youtube_matcher = re.compile("v=([^&]+)")


class HTMLRendererMixin(object):
    """Customized HTML renderer"""
    def link(self, link, title, content):
        embed = False
        src = link

        # Youtube
        if (("https://youtu.be/" in link or "https://www.youtube.com/" in link)
                and ("&no_embed=1" not in link)):
            embed = True
            if "embed" in link:  # Already correct link
                src = link
                template = self.jinja2.get_template('youtube')
            else:
                # need to canonalize youtube url
                if "https://youtu.be/" in link:
                    src = "https://www.youtube.com/embed/"
                    src += link.replace("https://youtu.be/", "")
                else:
                    d = youtube_matcher.search(link)
                    if d:
                        vid = d.group(1)
                        src = "https://www.youtube.com/embed/" + vid
                    else:
                        print("error can't detect videoid for link: %s" % link)
                        print(self.meta.title)
                template = self.jinja2.get_template('youtube')
                self.info.videos.append(src)

        # Normal links or not embedded youtube videos
        else:
            src = link.replace("&no_embed=1", "")
            template = self.jinja2.get_template('a')
            self.info.links.append(src)

        rv = template.render(href=src, text=content, title=title, embed=embed,
                             site=self.site, meta=self.meta)
        # rv = rv.encode('utf-8')
        return rv

    def image(self, src, title, alt_text):

        self.info.images.append(src)
        template = self.jinja2.get_template('img')
        rv = template.render(src=src, alt=alt_text, title=title,
                             plugin_data=self.plugin_data, site=self.site,
                             meta=self.meta)
        # rv = rv.encode('utf-8')
        return rv

    def header(self, text, level, raw=None):

        template = self.jinja2.get_template('h')
        rv = template.render(level=level, text=text, id=self.toc_count,
                             site=self.site, meta=self.meta)
        # rv = rv.encode('utf-8')

        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv

    def block_quote(self, text):
        "Block quote highlighter"
        template = self.jinja2.get_template('blockquote')
        rv = template.render(text=text, site=self.site, meta=self.meta)
        # rv = rv.encode('utf-8')
        return rv

    def block_code(self, code, lang):
        "Block code highlighter and formater"
        try:
            if not lang:
                lexer = guess_lexer(code, stripall=True)
            else:
                lexer = get_lexer_by_name(lang, stripall=True)
            code = highlight(code, lexer, self.code_formatter)
        except:  # noqa
            code = escape(code)
            lang = None

        self.info.code.append(code)

        template = self.jinja2.get_template('code')
        rv = template.render(code=code, lang=lang, site=self.site,
                             meta=self.meta)
        # rv = rv.encode('utf-8')
        return rv

    def init(self, jinja2, code_formatter, site, meta):
        """Init function called before each parsing.

        Args:
            jinja2 (dict): jinja2 templates used for rendering
            code_formatter (dict): code syntax highlight configuration
            site (obj_dict): the full site context (SiteFab object)
            meta (obj_dict): the meta associated with the post
        Return:
            None
        Note:
            Used to ensure all the needed variables are reset between parsing
            executions.
        """
        # reset toc
        self.toc_tree = []
        self.toc_count = 0
        self.jinja2 = jinja2
        self.code_formatter = code_formatter
        self.plugin_data = site.plugin_data
        self.site = site
        self.meta = meta

        # Various information collected during the parsing
        self.info = utils.dict_to_objdict({
            "links": [],
            "images": [],
            "videos": [],
            "code": []
        })

        self.stats = utils.dict_to_objdict({
            "num_links": 0,
            "num_images": 0,
            "num_videos": 0,
            "num_code": 0,
        })

    def get_info(self):
        return self.info

    def get_stats(self):
        stats = self.stats
        stats['num_links'] = len(self.info['links'])
        stats['num_videos'] = len(self.info['videos'])
        stats['num_images'] = len(self.info['images'])
        return stats

    # [TOC code] #
    def get_json_toc(self):
        """Render the TOC in JSON.

        Returns:
            list: TOC as a list ready to be json.dumps().
        """
        lst = []
        for toc in self.toc_tree:
            index, text, l, raw = toc
            lst.append((text, l, index))
        return lst

    def get_html_toc(self, level=3):
        """Render TOC as HTML table.

        Args:
            level (int, optional): Max TOC level. Defaults to 3.

        Returns:
            str: HTML table containing the TOC.
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
