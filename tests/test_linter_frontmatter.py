# encoding: utf-8
import pytest
from  test_linter import TestLinter

class TestLinterFrontmatter(TestLinter):

    #FIXME check also for message content (the error num is i one of the message)

   
    ### 104 ###
    def test_e104_triggered(self, sitefab, empty_post):
        empty_post.meta.mylist = ["test", "test"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E104" in error_list

    def test_e104_not_triggered(self, sitefab, empty_post):
        empty_post.meta.mylist = ["test"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E104" in error_list

    ### 105 ###
    def test_e105_triggered(self, sitefab, empty_post):
        empty_post.meta.tags = ["tag1", "category", "tag2"]
        empty_post.meta.category = "category"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E105" in error_list
    
    def test_e105_not_triggered(self, sitefab, empty_post):
        empty_post.meta.tags = ["tag1", "tag4", "tag2"]
        empty_post.meta.category = "category"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E105" in error_list

    ### 106 ###
    def test_e106_triggered(self, sitefab, empty_post):
        empty_post.meta.title = "title with   extra  space"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E106" in error_list
    
    def test_e106_not_triggered(self, sitefab, empty_post):
        empty_post.meta.title = "title with no extra space"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E106" in error_list