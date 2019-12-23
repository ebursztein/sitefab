from pathlib import Path
import pytest
from sitefab.SiteFab import SiteFab
from sitefab import __version__ as version
from sitefab import utils
# NOTE you don't need to import fixture explictly pytest do it for you. Avoid
# flake8 errors


TEST_ROOT_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def sitefab():
    "load a valid instance of sitefab"
    fname = TEST_ROOT_DIR / "data" / "config" / "valid_config.yaml"
    print('SiteFab version: %s' % version)
    return SiteFab(fname)


@pytest.fixture(scope="function")
def empty_post():
    "mock a post"
    post = utils.create_objdict()
    post.md = ""
    post.html = ""
    post.meta = utils.create_objdict()
    post.meta.statistics = utils.create_objdict()
    post.meta.toc = utils.create_objdict()
    post.elements = utils.create_objdict()
    return post
