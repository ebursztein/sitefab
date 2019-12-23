from .utils import get_linter_errors_list
from sitefab.utils import objdict


def test_no_meta(sitefab, empty_post):
    empty_post.meta = None
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert isinstance(error_list, list)


def test_meta_no_toc(sitefab, empty_post):
    empty_post.meta = objdict()
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert isinstance(error_list, list)


def test_e300_triggered(sitefab, empty_post):
    empty_post.meta.toc = [["headline", 1, 0]]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E300" in error_list


def test_e300_not_triggered(sitefab, empty_post):
    empty_post.meta.toc = [["headline", 2, 0]]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E300" not in error_list


def test_e301_triggered(sitefab, empty_post):
    empty_post.meta.toc = [["headline", 2, 0]]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E301" in error_list


def test_e301_not_triggered(sitefab, empty_post):
    empty_post.meta.toc = [["headline", 2, 0], ["headline 2", 2, 1]]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E301" not in error_list
