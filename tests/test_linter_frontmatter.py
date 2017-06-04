# encoding: utf-8
import pytest
from  test_linter import TestLinter

class TestLinterFrontmatter(TestLinter):

    #FIXME check also for message content (the error num is i one of the message)

   
    ### 104 ###
    def test_e104_triggered(self, sitefab, empty_post):
        empty_post.meta.mylist = ["test", "test"]
        print "%s" % type(empty_post.meta.mylist)
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E104" in error_list

    def test_e104_not_triggered(self, sitefab, empty_post):
        empty_post.meta.mylist = ["test"]
        print "%s" % type(empty_post.meta.mylist)
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E104" in error_list