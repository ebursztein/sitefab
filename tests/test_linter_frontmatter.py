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
    
    ### 107 ###
    def test_e107_triggered(self, sitefab, empty_post):
        empty_post.meta.authors = "this is not a list"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E107" in error_list
    
    def test_e107_not_triggered(self, sitefab, empty_post):
        empty_post.meta.authors = ['Elie, Bursztein', 'Celine, Bursztein']
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E107" in error_list
    
    ### 108 ###
    def test_e108_triggered(self, sitefab, empty_post):
        empty_post.meta.authors = ['Elie, Bursztein', 'No Commas']
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E108" in error_list
    
    def test_e108_not_triggered(self, sitefab, empty_post):
        empty_post.meta.authors = ['Elie, Bursztein', 'Celine, Bursztein']
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E108" in error_list

    ### 109 ###
    def test_e109_triggered(self, sitefab, empty_post):
        empty_post.meta.authors = ['Elie, Bursztein', 'not Capitalized']
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E109" in error_list
    
    def test_e109_not_triggered(self, sitefab, empty_post):
        empty_post.meta.authors = ['Elie, Bursztein', 'Celine, Bursztein']
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E109" in error_list

    ### 110 ###
    def test_e110_triggered(self, sitefab, empty_post):
        empty_post.meta.category = "not Lower"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E110" in error_list
    
    def test_e110_not_triggered(self, sitefab, empty_post):
        empty_post.meta.category = "lower"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E110" in error_list
    
    ### 112 ###
    def test_e112_triggered(self, sitefab, empty_post):
        empty_post.meta.files = "not Lower"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E112" in error_list
    
    def test_e112_not_triggered(self, sitefab, empty_post):
        empty_post.meta.files = {"pdf": "/test/test.pdf"}
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E112" in error_list