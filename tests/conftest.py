from pathlib import Path

import pytest
import git
from termcolor import cprint

from sitefab import __version__ as version
from sitefab import utils
from sitefab import files
from sitefab.SiteFab import SiteFab

# NOTE you don't need to import fixture explictly pytest do it for you. Avoid
# flake8 errors

TEST_ROOT_DIR = Path(__file__).parent
TEMPLATE_DATA_PATH = TEST_ROOT_DIR / 'sitefab_template'
TEMPLATE_GIT_URL = 'https://github.com/ebursztein/sitefab-template'
TEMPLATE_DATA_CONFIG_FILE_PATH = TEMPLATE_DATA_PATH / 'config' / 'sitefab.yaml'
PLUGINS_DATA_PATH = TEMPLATE_DATA_PATH / 'plugins'
PLUGINS_GIT_URL = 'https://github.com/ebursztein/sitefab-plugins'


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

    cprint('[SiteFab Templates]', 'magenta')
    if TEMPLATE_DATA_PATH.exists():
        cprint('Pulling latest sitefab template', 'green')
        g = git.cmd.Git(TEMPLATE_DATA_PATH)
        g.pull()
    else:
        cprint('Cloning sitefab template', 'yellow')
        git.Repo().clone_from(TEMPLATE_GIT_URL, TEMPLATE_DATA_PATH)

    cprint('[SiteFab Plugins]', 'magenta')
    if PLUGINS_DATA_PATH.exists():
        cprint('Pulling latest sitefab plugins', 'green')
        g = git.cmd.Git(PLUGINS_DATA_PATH)
        g.pull()
    else:
        cprint('Cloning sitefab plugins', 'yellow')
        git.Repo().clone_from(PLUGINS_GIT_URL, PLUGINS_DATA_PATH)

    cprint('[Directory cleanup]', 'magenta')
    cache_dir = TEMPLATE_DATA_PATH / 'cache'
    cprint('|- cache dir cleanup: %s' % cache_dir, 'cyan')
    files.clean_dir(cache_dir)
