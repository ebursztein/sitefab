import os
from sitefab.docs.plugins import generate_plugins_readme
from ..conftest import TEMPLATE_DATA_PATH


def test_generate_readme(sitefab):
    fname = 'README_PLUGINS.md'
    tmp_dir = TEMPLATE_DATA_PATH / 'tmp'
    if not tmp_dir.exists():
        tmp_dir.mkdir()
    os.chdir(tmp_dir)
    generate_plugins_readme(sitefab, fname)
    rd_fname = tmp_dir / fname
    assert rd_fname.exists()
    content = open(rd_fname).read()
    assert 'SiteFab' in content
    assert 'Sitemap' in content
    assert 'RSS' in content
