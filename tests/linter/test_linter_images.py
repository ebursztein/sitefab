from .utils import get_linter_errors_list


def test_e201_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {}
    empty_post.elements.images = ["test.jpg"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E201" in error_list


def test_e201_not_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "test.jpg": {}
    }
    empty_post.elements.images = ["test.jpg"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E201" not in error_list


def test_e203_triggered(sitefab, empty_post):
    empty_post.elements.images = ["test.jpg", "test.jpg"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E203" in error_list


def test_e203_not_triggered(sitefab, empty_post):
    empty_post.elements.images = ["test.jpg"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E203" not in error_list


def test_e204_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "banner.jpg": {"width": 100, "height": 34}
    }
    empty_post.meta.banner = "banner.jpg"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E204" in error_list


def test_e204_not_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "banner.jpg": {"width": 1900, "height": 34}
    }
    empty_post.meta.banner = "banner.jpg"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E204" not in error_list


def test_e205_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "test.jpg": {"width": 50, "height": 34}
    }
    empty_post.elements.images = ["test.jpg"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E205" in error_list


def test_e205_not_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "test.jpg": {"width": 10000, "height": 34}
    }
    empty_post.elements.images = ["test.jpg"]
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E205" not in error_list


def test_e206_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "banner.jpg": {"width": 10000, "height": 34}
    }
    empty_post.meta.banner = "banner-typo.jpg"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E206" in error_list


def test_e206_not_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "banner.jpg": {"width": 10000, "height": 34}
    }
    empty_post.meta.banner = "banner.jpg"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E206" not in error_list


def test_e207_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "banner.jpg": {"width": 10000, "height": 34}
    }
    empty_post.meta.banner = "banner.jpg"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E207" in error_list


def test_e207_not_triggered(sitefab, empty_post):
    sitefab.plugin_data['image_info'] = {
        "banner.jpg": {"width": 1900, "height": 1080}
    }
    empty_post.meta.banner = "banner.jpg"
    results = sitefab.linter.lint(empty_post, "", sitefab)
    error_list = get_linter_errors_list(results)
    assert "E207" not in error_list
