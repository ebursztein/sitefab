# encoding: utf-8
import pytest
from  test_linter import TestLinter

class TestLinterImages(TestLinter):

    ### 201 ###
    def test_e201_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {}
        empty_post.elements.images = ["test.jpg"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E201" in error_list
 
    def test_e201_not_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "test.jpg": {}
        }
        empty_post.elements.images = ["test.jpg"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E201" in error_list

    ### 203 ###
    def test_e203_triggered(self, sitefab, empty_post):
        empty_post.elements.images = ["test.jpg", "test.jpg"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E203" in error_list

    def test_e203_not_triggered(self, sitefab, empty_post):
        empty_post.elements.images = ["test.jpg"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E203" in error_list


   ### 204 ###
    def test_e204_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "banner.jpg": {"width": 100}
        }
        empty_post.meta.banner = "banner.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E204" in error_list

    def test_e204_not_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "banner.jpg": {"width": 1900}
        }
        empty_post.meta.banner = "banner.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E204" in error_list