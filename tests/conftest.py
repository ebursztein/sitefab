from pathlib import Path

import pytest
import git
from termcolor import cprint

from sitefab import __version__ as version
from sitefab import utils
from sitefab.SiteFab import SiteFab

# NOTE you don't need to import fixture explictly pytest do it for you. Avoid
# flake8 errors

TEST_ROOT_DIR = Path(__file__).parent
TEMPLATE_DATA_PATH = TEST_ROOT_DIR / 'sitefab_template'
TEMPLATE_GIT_URL = 'https://github.com/ebursztein/sitefab-template'


@pytest.fixture()
def myobjdict():
    d = {'a': 'test', 'b': {"c": '2nd'}}
    return utils.dict_to_objdict(d)


@pytest.fixture(scope="session")
def sitefab():
    "load a valid instance of sitefab"
    fname = TEMPLATE_DATA_PATH / "config" / "sitefab.yaml"
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


def pytest_configure(config):

    if TEMPLATE_DATA_PATH.exists():
        cprint('Pulling latest sitefab template', 'green')
        g = git.cmd.Git(TEMPLATE_DATA_PATH)
        g.pull()
    else:
        cprint('Cloning sitefab template', 'yellow')
        git.Repo().clone_from(TEMPLATE_GIT_URL, TEMPLATE_DATA_PATH)
