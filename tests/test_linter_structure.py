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

    ### 300 ###
    def test_e300_triggered(self, sitefab, empty_post):
        empty_post.meta.toc  = [["headline", 1, 0]]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E300" in error_list
    
    def test_e300_not_triggered(self, sitefab, empty_post):
        empty_post.meta.toc  = [["headline", 2, 0]]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E300" in error_list

    ### 301 ###
    def test_e301_triggered(self, sitefab, empty_post):
        empty_post.meta.toc  = [["headline", 2, 0]]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E301" in error_list
    
    def test_e301_not_triggered(self, sitefab, empty_post):
        empty_post.meta.toc  = [["headline", 2, 0], ["headline 2", 2, 1]]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E301" in error_list