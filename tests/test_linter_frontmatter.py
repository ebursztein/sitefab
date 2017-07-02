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

    ### 113 ###
    def test_e113_triggered(self, sitefab, empty_post):
        values = [53, ['bla'], {'bla': 'oups'}, None]
        for value in values:
            empty_post.meta.banner = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            error_list  = self.get_linter_errors_list(results)
            assert "E113" in error_list
    
    def test_e113_not_triggered(self, sitefab, empty_post):
        values = ["test", u"test", "", u""]
        for value in values:
            empty_post.meta.banner = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            print results
            error_list  = self.get_linter_errors_list(results)
            assert not "E113" in error_list

    ### 114 ###
    def test_e114_triggered(self, sitefab, empty_post):
        test_values = [
            "http://",
            "https://" # empty
            "hTTps://elie.net", # caps
            "https://elie.net/ test.html" #space
            ]
        for value in test_values:
            empty_post.meta.banner = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            error_list  = self.get_linter_errors_list(results)
            assert "E114" in error_list

    def test_e114_not_triggered(self, sitefab, empty_post):
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
            error_list  = self.get_linter_errors_list(results)
            assert not "E114" in error_list
    
    ### 115 ###
    def test_e115_triggered(self, sitefab, empty_post):
        test_values = [
            "file .pdf",
            ]
        for value in test_values:
            empty_post.meta.banner = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            error_list  = self.get_linter_errors_list(results)
            assert "E115" in error_list
    
    def test_e115_not_triggered(self, sitefab, empty_post):
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
            error_list  = self.get_linter_errors_list(results)
            assert not "E115" in error_list
    
    ### 116 ###
    def test_e116_triggered(self, sitefab, empty_post):
        empty_post.meta.title = None
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E116" in error_list
    
    def test_e116_not_triggered(self, sitefab, empty_post):
        tests = [
            u"this is my title",
            "title"
            "title again"
        ]
        for t in tests:
            empty_post.meta.title = "this is my title"
            results = sitefab.linter.lint(empty_post, "", sitefab)
            error_list  = self.get_linter_errors_list(results)
            assert not "E116" in error_list
    
    ### 117 ###
    def test_e117_triggered(self, sitefab, empty_post):
        values = [53, ['bla'], {'bla': 'oups'}, None]
        for value in values:
            empty_post.meta.permanent_url = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            error_list  = self.get_linter_errors_list(results)
            assert "E117" in error_list
    
    def test_e117_not_triggered(self, sitefab, empty_post):
        values = ["test", u"test" u"", ""]
        for value in values:
            empty_post.meta.permanent_url = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            print results
            error_list  = self.get_linter_errors_list(results)
            assert not "E117" in error_list

    ### 118 ###
    def test_e118_triggered(self, sitefab, empty_post):
        values = [
            "http://",
            "https://" # empty
            "hTTps://elie.net", # caps
            "https://elie.net/ test.html" #space
            ]
        for value in values:
            empty_post.meta.permanent_url = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            error_list  = self.get_linter_errors_list(results)
            assert "E118" in error_list

    def test_e118_not_triggered(self, sitefab, empty_post):
        test_values = [
            "/cat/file",
            "/cat/file?a=5"
            "/cat/file.pdf"
            ]
        for value in test_values:
            empty_post.meta.permanent_url = value
            results = sitefab.linter.lint(empty_post, "", sitefab)
            error_list  = self.get_linter_errors_list(results)
            assert not "E118" in error_list