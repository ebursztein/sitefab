# encoding: utf-8
import pytest
from  test_linter import TestLinter

class TestLinterImages(TestLinter):

    #FIXME check also for message content (the error num is i one of the message)

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
            "banner.jpg": {"width": 100, "height": 34}
        }
        empty_post.meta.banner = "banner.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        print results
        error_list  = self.get_linter_errors_list(results)
        assert "E204" in error_list

    def test_e204_not_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "banner.jpg": {"width": 1900, "height": 34}
        }
        empty_post.meta.banner = "banner.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E204" in error_list
    
    ### 205 ###
    def test_e205_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "test.jpg": {"width": 50, "height": 34}
        }
        empty_post.elements.images = ["test.jpg"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E205" in error_list

    def test_e205_not_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "test.jpg": {"width": 10000, "height": 34}
        }
        empty_post.elements.images = ["test.jpg"]
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E205" in error_list

    ### 206 ###
    def test_e206_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "banner.jpg": {"width": 10000, "height": 34}
        }
        empty_post.meta.banner = "banner-typo.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E206" in error_list

    def test_e206_not_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "banner.jpg": {"width": 10000, "height": 34}
        }
        empty_post.meta.banner = "banner.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E206" in error_list
   
    ### 207 ###
    def test_e207_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "banner.jpg": {"width": 10000, "height": 34}
        }
        empty_post.meta.banner = "banner.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert "E207" in error_list

    def test_e207_not_triggered(self, sitefab, empty_post):
        sitefab.plugin_data['image_info'] = {
            "banner.jpg": {"width": 1900, "height": 1080}
        }
        empty_post.meta.banner = "banner.jpg"
        results = sitefab.linter.lint(empty_post, "", sitefab)
        error_list  = self.get_linter_errors_list(results)
        assert not "E207" in error_list