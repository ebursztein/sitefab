# encoding: utf-8
from .utils import get_linter_errors_list


def test_e104_triggered(sitefab, empty_post):
    empty_post.meta.mylist = ["test", "test"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E104" in error_list


def test_e104_not_triggered(sitefab, empty_post):
    empty_post.meta.mylist = ["test"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E104" not in error_list


def test_e105_triggered(sitefab, empty_post):
    empty_post.meta.tags = ["tag1", "category", "tag2"]
    empty_post.meta.category = "category"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E105" in error_list


def test_e105_not_triggered(sitefab, empty_post):
    empty_post.meta.tags = ["tag1", "tag4", "tag2"]
    empty_post.meta.category = "category"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E105" not in error_list


def test_e106_triggered(sitefab, empty_post):
    empty_post.meta.title = "title with   extra  space"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E106" in error_list


def test_e106_not_triggered(sitefab, empty_post):
    empty_post.meta.title = "title with no extra space"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E106" not in error_list


def test_e107_triggered(sitefab, empty_post):
    empty_post.meta.authors = "this is not a list"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E107" in error_list


def test_e107_not_triggered(sitefab, empty_post):
    empty_post.meta.authors = ['Elie, Bursztein', 'Celine, Bursztein']
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E107" not in error_list


def test_e108_triggered(sitefab, empty_post):
    empty_post.meta.authors = ['Elie, Bursztein', 'No Commas']
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E108" in error_list


def test_e108_not_triggered(sitefab, empty_post):
    empty_post.meta.authors = ['Elie, Bursztein',
                               'Celine, Bursztein', 'John, McBride']
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E108" not in error_list


def test_e109_triggered(sitefab, empty_post):
    empty_post.meta.authors = ['Elie, Bursztein', 'not, Capitalized']
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E109" in error_list


def test_e109_not_triggered(sitefab, empty_post):
    empty_post.meta.authors = ['Elie, Bursztein', 'Celine, Bursztein']
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E109" not in error_list


def test_e110_triggered(sitefab, empty_post):
    empty_post.meta.category = "not Lower"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E110" in error_list


def test_e110_not_triggered(sitefab, empty_post):
    empty_post.meta.category = "lower"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E110" not in error_list


def test_e112_triggered(sitefab, empty_post):
    empty_post.meta.files = "not Lower"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E112" in error_list


def test_e112_not_triggered(sitefab, empty_post):
    empty_post.meta.files = {"pdf": "/test/test.pdf"}
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E112" not in error_list


def test_e113_triggered(sitefab, empty_post):
    values = [53, ['bla'], {'bla': 'oups'}, None]
    for value in values:
        empty_post.meta.banner = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E113" in error_list


def test_e113_not_triggered(sitefab, empty_post):
    values = ["test", u"test", "", u""]
    for value in values:
        empty_post.meta.banner = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E113" not in error_list


def test_e114_triggered(sitefab, empty_post):
    test_values = [
        "http://",
        "https://"  # empty
        "hTTps://elie.net",  # caps
        "https://elie.net/ test.html"  # space
    ]
    for value in test_values:
        empty_post.meta.banner = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E114" in error_list


def test_e114_not_triggered(sitefab, empty_post):
    test_values = [
        "http://www.elie.net",
        "https://www.elie.net",
        "https://www.elie.net/test.html",
        "https://www.elie.net/test/test.html",
        "https://www.elie.net/test/test",
        "https://www.elie.net/test/test.pdf",
        "https://www.elie.net/test/test.pdf?a=42",
        "/cat/file",
        "cat/file",
        "/cat/file.pdf"
        "/cat/file.pdf?a=2"
    ]
    for value in test_values:
        empty_post.meta.banner = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E114" not in error_list


def test_e115_triggered(sitefab, empty_post):
    test_values = [
        "file .pdf",
    ]
    for value in test_values:
        empty_post.meta.banner = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E115" in error_list


def test_e115_not_triggered(sitefab, empty_post):
    test_values = [
        "file.pdf",
        "/file.pdf",
        "/files/file.pdf",
        "/file/file-test.pdf",
        "/file/file-test02.jpeg",

    ]
    for value in test_values:
        empty_post.meta.banner = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E115" not in error_list


def test_e116_triggered(sitefab, empty_post):
    empty_post.meta.title = None
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E116" in error_list


def test_e116_not_triggered(sitefab, empty_post):
    empty_post.meta.title = "this is my title"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E116" not in error_list


def test_e117_triggered(sitefab, empty_post):
    values = [53, ['bla'], {'bla': 'oups'}, None]
    for value in values:
        empty_post.meta.permanent_url = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E117" in error_list


def test_e117_not_triggered(sitefab, empty_post):
    values = ["test", u"test" u"", ""]
    for value in values:
        empty_post.meta.permanent_url = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E117" not in error_list


def test_e118_triggered(sitefab, empty_post):
    values = [
        "http://",
        "https://"  # empty
        "hTTps://elie.net",  # caps
        "https://elie.net/ test.html"  # space
    ]
    for value in values:
        empty_post.meta.permanent_url = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E118" in error_list


def test_e118_not_triggered(sitefab, empty_post):
    test_values = [
        "/cat/file",
        "/cat/file?a=5"
        "/cat/file.pdf",
        ""
    ]
    for value in test_values:
        empty_post.meta.permanent_url = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E118" not in error_list


def test_e119_triggered(sitefab, empty_post):
    values = ["notabsolute", "not/absolute/not"]
    for value in values:
        empty_post.meta.permanent_url = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E119" in error_list


def test_e119_not_triggered(sitefab, empty_post):
    values = ["/absolute", "/absolute/not"]
    for value in values:
        empty_post.meta.permanent_url = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E119" not in error_list


def test_e120_triggered(sitefab, empty_post):
    import pprint
    empty_post.meta.template = "blog_post"
    values = ["wrong", "wrong/again"]
    for value in values:
        empty_post.meta.permanent_url = value
        pprint.pprint(empty_post)
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E120" in error_list


def test_e120_not_triggered(sitefab, empty_post):
    empty_post.meta.template = "blog_post"
    values = ["/blog/ok", "/blog/ok/as", "/blog/ok/as.well"]
    for value in values:
        empty_post.meta.permanent_url = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E120" not in error_list


def test_e121_triggered(sitefab, empty_post):
    values = [{"not a valid type": "myslide"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E121" in error_list


def test_e121_not_triggered(sitefab, empty_post):
    values = [{"slides": "myslide"}, {
        "paper": "mypaper"}, {"video": "myvideo"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E121" not in error_list


def test_e122_triggered(sitefab, empty_post):
    values = [{"not a valid type": "not a valid file"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E122" in error_list


def test_e122_not_triggered(sitefab, empty_post):
    values = [{"slides": "/myslide.pdf"}, {"video": "/files/myvideo.mp4"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E122" not in error_list


def test_e123_triggered(sitefab, empty_post):
    values = [{"not a valid type": "/baprefix",
               "video": "files/almostcorrect"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E123" in error_list


def test_e123_not_triggered(sitefab, empty_post):
    values = [{"slides": "/files/myslide.pdf"},
              {"video": "/files/myvideo.mp4"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E123" not in error_list


def test_e124_triggered(sitefab, empty_post):
    values = [{"not a valid type": "/nosuffix.pdf",
               "video": "files/almostcorrect.pdf"},
              {"video": "htt://whateverr/files/myvideo.mp4"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E124" in error_list


def test_e124_not_triggered(sitefab, empty_post):
    values = [{"slides": "/files/myfiles-slides.pdf"},
              {"video": "https://whateverr/files/myvideo.mp4"}]
    for value in values:
        empty_post.meta.files = value
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list = get_linter_errors_list(results)
        assert "E124" not in error_list
