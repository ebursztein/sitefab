from sitefab.parser.html2text import html2text


def test_none():
    assert html2text(None) == ''


def test_empty():
    assert html2text('') == ''


def test_basic():
    assert html2text('<span>test</span>') == 'test'


def test_pre():
    snip = '''
        <pre>alert(1)</pre>
        <span>test</span>
    '''
    assert html2text(snip) == 'test'


def test_code():
    snip = '''
        <code>alert(1)</code>
        <span>test</span>
    '''
    assert html2text(snip) == 'test'


def test_upercase_code():
    snip = '''
        <code>alert(1)</CoDe>
        <span>test</span>
    '''
    assert html2text(snip) == 'test'


def test_dangling_tags():
    snip = '''
        <table><td>
            <span>test</span>
    '''
    assert html2text(snip) == 'test'


def test_broken_html():
    snip = '''
        </td>test</span>
    '''
    assert html2text(snip) == 'test'
