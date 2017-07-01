# encoding: utf-8
import pytest
from  test_linter import TestLinter

from SiteFab import utils

class TestLinterStructure(TestLinter):

    def test_no_meta(self, sitefab, empty_post):
        empty_post.meta = None
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert isinstance(error_list, list)

    def test_meta_no_toc(self, sitefab, empty_post):
        empty_post.meta = utils.objdict()
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert isinstance(error_list, list)