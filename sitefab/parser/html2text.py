import re
from html.parser import HTMLParser
from textacy import preprocessing


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def html2text(html):
    """HTML to text converter

    Args:
        html (str): html

    Returns:
        str: html page content in plaintext
    """
    if not html:
        return ''

    # remove code snippets
    html = re.sub(r'<pre>.*?</pre>', ' ', html,
                  flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)
    html = re.sub(r'<code>.*?</code>', ' ', html,
                  flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)

    # strip the rest
    s = MLStripper()
    s.feed(html)
    text = s.get_data()
    text = preprocessing.normalize_whitespace(text)
    return text
