from sitefab.files import read_file
from sitefab.parser import Parser
from ..conftest import TEST_ROOT_DIR


def test_parsing_real_md(sitefab):
    parser = Parser(sitefab.config.parser, sitefab)
    fn = sitefab.config.root_dir / 'content/posts/18-4-of-us-internet-users-got-at-least-one-of-their-account-compromised.md'  # noqa
    md = read_file(fn)
    post = parser.parse(md)
    assert 'internet' in post.html
    assert 'Elie' in post.meta.authors[0]
    assert post.meta.statistics.num_images == 2


def test_parsing_basic_md(sitefab):
    parser = Parser(sitefab.config.parser, sitefab)
    fn = TEST_ROOT_DIR / 'data/basic.md'
    md = read_file(fn)
    post = parser.parse(md)

    # frontmatter
    assert 'Elie, Bursztein' in post.meta.authors
    assert post.meta.title == 'Test'

    # html
    assert 'this is a test.' in post.html
    assert '<h1 id="toc-0">heading 1</h1>' in post.html
    assert '<h2 id="toc-1">heading 2</h2>' in post.html
    assert '<strong>bold test</strong>' in post.html

    # text
    assert 'this is a test' in post.text
    assert '<' not in post.text

    # toc
    # format: name, heading type: {1,2,3,4...}, id
    assert post.meta.toc[0] == ('heading 1', 1, 0)
    assert post.meta.toc[1] == ('heading 2', 2, 1)

    # statistics
    assert post.meta.statistics.num_videos == 1
    assert post.meta.statistics.num_images == 1
