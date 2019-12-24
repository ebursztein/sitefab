import pytest
from pathlib import Path
from sitefab.SiteFab import SiteFab
from sitefab.files import get_files_list

TEST_ROOT_DIR = Path(__file__).parent


def test_empty_config():
    # is SiteFab raise the correct exception
    with pytest.raises(Exception) as excinfo:
        SiteFab(None)
        assert excinfo.value.message == 'Supply a configuration filename'


def test_non_existing_config():
    # is SiteFab raise the correct exception
    with pytest.raises(Exception) as excinfo:
        SiteFab(None)
        assert 'Configuration file not found:' in excinfo.value.message


def test_valid_config():
    # is SiteFab raise the correct exception
    fname = TEST_ROOT_DIR / "data" / "config" / "valid_config.yaml"
    site = SiteFab(fname)
    assert site.config
    # FIXME add more test for the correctness here.


def test_template_filters(sitefab):
    "ensure custom filters from plugins/template/filters are correctly loaded"
    assert 'str_to_list' in sitefab.jinja2.filters


def test_log_template_paths(sitefab):
    correct_path = Path('tests/data/config/generator_templates/logs')
    assert sitefab.config.logger.template_dir == correct_path


def test_get_config(sitefab):
    assert sitefab.get_config() == sitefab.config


def test_parser_templates_loaded(sitefab):
    print(sitefab.config.parser.templates_path)
    assert len(get_files_list(sitefab.config.parser.templates_path, "*.html"))
