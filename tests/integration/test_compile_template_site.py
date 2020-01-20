import pytest
from sitefab.cmdline.cmdline import generate, version
from sitefab.files import get_files_list
from ..conftest import TEMPLATE_DATA_PATH


@pytest.mark.dependency(name="compile")
def test_compile_and_check_generated_content(sitefab):
    generate(sitefab.config_filename, version)


@pytest.mark.dependency(name="log", depends=["compile"])
def test_logs_presence():
    log_dir = TEMPLATE_DATA_PATH / 'logs'
    fnames = ['index.html', 'linter.html', 'stats.html']
    for fname in fnames:
        path = log_dir / fname
        assert path.exists()
        assert path.is_file()


@pytest.mark.dependency(name="content", depends=["compile"])
def test_content_presence():
    content_dir = TEMPLATE_DATA_PATH / 'generated'

    # root files
    fnames = ['index.html', 'rss.xml', 'sitemap.xml']
    for fname in fnames:
        path = content_dir / 'index.html'
        assert path.exists()
        assert path.is_file()

    # files in directories
    dirnames = ['blog', 'code', 'publications']
    for dirname in dirnames:
        path = content_dir / dirname / 'index.html'
        assert path.exists()
        assert path.is_file()